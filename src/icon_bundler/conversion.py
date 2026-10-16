from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps
import PIL.IcnsImagePlugin  # registers ICNS save support

ICO_SIZES = [(16, 16), (32, 32), (48, 48), (256, 256)]
ICNS_SIZES = [(16, 16), (32, 32), (64, 64), (128, 128), (256, 256), (512, 512), (1024, 1024)]
OUTPUT_FORMATS = {
    "ICO": {"suffix": ".ico", "sizes": ICO_SIZES},
    "ICNS": {"suffix": ".icns", "sizes": ICNS_SIZES},
}
SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg"}
LANG_ENV = "ICON_BUNDLER_LANGUAGE"
SOURCE_ENV = "ICON_BUNDLER_SOURCE"

try:
    RESAMPLE_LANCZOS = Image.Resampling.LANCZOS
except AttributeError:  # Pillow < 9
    RESAMPLE_LANCZOS = Image.LANCZOS


class IconConversionError(Exception):
    """Base error for expected icon conversion failures."""


class MissingSourceError(IconConversionError):
    """Raised when the source image path does not exist."""

    def __init__(self, source_path: Path) -> None:
        super().__init__(str(source_path))
        self.source_path = source_path


class UnsupportedSourceError(IconConversionError):
    """Raised when the source image is not a supported file type."""


class UnsupportedOutputFormatError(IconConversionError):
    """Raised when an output format or suffix is not supported."""


def validate_source_path(source_path: Path) -> None:
    """Validate that the source path points to a supported image file."""
    if source_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise UnsupportedSourceError("PNG, JPG, JPEG files only.")
    if not source_path.is_file():
        raise MissingSourceError(source_path)


def get_output_config(output_suffix: str, format_name: str) -> dict[str, object]:
    """Return output settings after validating a format/suffix pair."""
    output_config = OUTPUT_FORMATS.get(format_name)
    if output_config is None or output_config["suffix"] != output_suffix:
        raise UnsupportedOutputFormatError(f"Unsupported output format: {format_name} ({output_suffix})")
    return output_config


def build_icon_source(image: Image.Image, canvas_size: int) -> Image.Image:
    """Resize the source image into a square RGBA canvas for icon export."""
    prepared = ImageOps.exif_transpose(image).convert("RGBA")
    # Keep the original aspect ratio and pad with transparency instead of stretching.
    contained = ImageOps.contain(
        prepared,
        (canvas_size, canvas_size),
        method=RESAMPLE_LANCZOS,
    )

    canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    offset_x = (canvas_size - contained.width) // 2
    offset_y = (canvas_size - contained.height) // 2
    canvas.alpha_composite(contained, (offset_x, offset_y))
    return canvas


def build_icon_sizes(original_size: tuple[int, int], available_sizes: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Keep sizes in ascending order and stop before the first upscale."""
    max_dimension = min(original_size)
    selected_sizes = [size for size in available_sizes if size[0] <= max_dimension and size[1] <= max_dimension]
    if not selected_sizes:
        selected_sizes = [available_sizes[0]]
    return selected_sizes


def convert_image(source_path: Path, output_suffix: str, format_name: str) -> Path:
    """Convert a PNG/JPG image into a multi-size icon file."""
    validate_source_path(source_path)
    output_config = get_output_config(output_suffix, format_name)

    output_path = source_path.with_suffix(output_suffix)

    with Image.open(source_path) as image:
        icon_sizes = build_icon_sizes(image.size, output_config["sizes"])
        canvas_size = icon_sizes[-1][0]
        icon_base = build_icon_source(image, canvas_size)
        icon_base.save(output_path, format=format_name, sizes=icon_sizes)

    return output_path
