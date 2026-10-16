#!/bin/bash
set -euo pipefail
umask 077

MODE="${1:-}"
APP_PATH="${APP_PATH:?APP_PATH is required}"
APPLE_API_KEY_P8="${APPLE_API_KEY_P8:?APPLE_API_KEY_P8 is required}"
APPLE_API_KEY_ID="${APPLE_API_KEY_ID:?APPLE_API_KEY_ID is required}"
APPLE_API_ISSUER="${APPLE_API_ISSUER:?APPLE_API_ISSUER is required}"

API_KEY_PATH="$RUNNER_TEMP/AuthKey_${APPLE_API_KEY_ID}.p8"
NOTARY_ZIP="$RUNNER_TEMP/IconBundler-notarize.zip"
SUBMIT_RESPONSE="$RUNNER_TEMP/notary-submit.json"
INFO_RESPONSE="$RUNNER_TEMP/notary-info.json"
NOTARY_ERROR="$RUNNER_TEMP/notary-error.log"
NOTARY_LOG="$RUNNER_TEMP/notary-log.json"

write_api_key() {
  printf '%s' "$APPLE_API_KEY_P8" > "$API_KEY_PATH"
}

notary_auth_args=(--key "$API_KEY_PATH" --key-id "$APPLE_API_KEY_ID" --issuer "$APPLE_API_ISSUER")

case "$MODE" in
  submit)
    codesign --verify --deep --strict --verbose=2 "$APP_PATH"
    ditto -c -k --sequesterRsrc --keepParent "$APP_PATH" "$NOTARY_ZIP"
    write_api_key

    if ! xcrun notarytool submit "$NOTARY_ZIP" "${notary_auth_args[@]}" \
      --no-wait --output-format json > "$SUBMIT_RESPONSE" 2> "$NOTARY_ERROR"; then
      cat "$NOTARY_ERROR" >&2
      echo "Notarization submission did not return successfully; no retry was attempted to avoid duplicate submissions." >&2
      exit 1
    fi

    SUBMISSION_ID="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8")).get("id", ""))' "$SUBMIT_RESPONSE")"
    if [[ -z "$SUBMISSION_ID" ]]; then
      cat "$SUBMIT_RESPONSE" >&2
      echo "Could not read the Apple notarization submission ID." >&2
      exit 1
    fi

    echo "Apple notarization submission ID: $SUBMISSION_ID"
    echo "APPLE_NOTARY_SUBMISSION_ID=$SUBMISSION_ID" >> "$GITHUB_ENV"
    echo "submission_id=$SUBMISSION_ID" >> "$GITHUB_OUTPUT"
    {
      echo "### Apple notarization"
      echo "- Submission ID: \`$SUBMISSION_ID\`"
      echo "- Status lookup reuses this ID and retries temporary network errors."
    } >> "$GITHUB_STEP_SUMMARY"
    ;;

  wait)
    SUBMISSION_ID="${APPLE_NOTARY_SUBMISSION_ID:?APPLE_NOTARY_SUBMISSION_ID is required}"
    write_api_key
    echo "Checking Apple notarization submission $SUBMISSION_ID"

    network_failures=0
    network_delays=(5 15 30 60 120 300 300 300)
    max_polls=240
    poll_interval=60

    for ((poll=1; poll<=max_polls; poll++)); do
      if xcrun notarytool info "$SUBMISSION_ID" "${notary_auth_args[@]}" \
        --output-format json > "$INFO_RESPONSE" 2> "$NOTARY_ERROR"; then
        network_failures=0
        STATUS="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8")).get("status", ""))' "$INFO_RESPONSE")"
        echo "Apple notarization status ($poll/$max_polls): $STATUS"

        case "$STATUS" in
          Accepted)
            {
              echo "- Final status: **Accepted**"
            } >> "$GITHUB_STEP_SUMMARY"
            exit 0
            ;;
          Invalid|Rejected)
            echo "Apple rejected notarization submission $SUBMISSION_ID." >&2
            if xcrun notarytool log "$SUBMISSION_ID" "${notary_auth_args[@]}" "$NOTARY_LOG"; then
              cat "$NOTARY_LOG" >&2
            else
              echo "Could not retrieve the notary log; submission ID: $SUBMISSION_ID" >&2
            fi
            {
              echo "- Final status: **$STATUS**"
              echo "- Review the Notarize macOS app log for Apple's rejection details."
            } >> "$GITHUB_STEP_SUMMARY"
            exit 1
            ;;
          "In Progress")
            ;;
          *)
            echo "Unexpected Apple notarization status '$STATUS' for submission $SUBMISSION_ID." >&2
            cat "$INFO_RESPONSE" >&2
            exit 1
            ;;
        esac
      else
        error_text="$(cat "$NOTARY_ERROR")"
        if printf '%s' "$error_text" | grep -Eiq 'NSURLErrorDomain Code=(-1001|-1003|-1004|-1005|-1006|-1008|-1009)|network connection.*(lost|offline|unavailable)|internet connection.*offline|connection (was )?lost|could not resolve|failed to connect|timed out|temporarily unavailable|HTTP[^0-9]*(408|425|429|5[0-9]{2})'; then
          if (( network_failures >= ${#network_delays[@]} )); then
            echo "$error_text" >&2
            echo "Apple status lookup exhausted network retries. Keep submission ID $SUBMISSION_ID and retry the lookup later." >&2
            {
              echo "- Last lookup: network error after $network_failures retries"
              echo "- Resume with submission ID: \`$SUBMISSION_ID\`"
            } >> "$GITHUB_STEP_SUMMARY"
            exit 1
          fi
          delay="${network_delays[$network_failures]}"
          network_failures=$((network_failures + 1))
          echo "Temporary network error while checking submission $SUBMISSION_ID; retry $network_failures/${#network_delays[@]} in ${delay}s." >&2
          cat "$NOTARY_ERROR" >&2
          sleep "$delay"
          continue
        fi
        cat "$NOTARY_ERROR" >&2
        echo "Apple status lookup failed for a non-network reason; submission ID: $SUBMISSION_ID" >&2
        exit 1
      fi

      sleep "$poll_interval"
    done

    echo "Apple notarization did not finish after $((max_polls * poll_interval / 60)) minutes. Submission ID: $SUBMISSION_ID" >&2
    {
      echo "- Status lookup timed out; the Apple request may still be processing."
      echo "- Resume with submission ID: \`$SUBMISSION_ID\`"
    } >> "$GITHUB_STEP_SUMMARY"
    exit 1
    ;;

  *)
    echo "Usage: $0 {submit|wait}" >&2
    exit 2
    ;;
esac
