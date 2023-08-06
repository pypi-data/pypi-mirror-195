from pathlib import Path

import daiquiri
import typer
import yaml  # type: ignore
from pptx import Presentation as _open_presentation
from pptx.presentation import Presentation
from typer import FileBinaryRead

from dbnomics_pptx_tools.cli.slide_expr import parse_slide_expr, parse_slides_expr, slide_to_number
from dbnomics_pptx_tools.metadata import PresentationMetadata

logger = daiquiri.getLogger(__name__)


def load_presentation_metadata(metadata_file: Path | None, *, pptx_file: Path) -> PresentationMetadata:
    if metadata_file is None:
        metadata_file = Path(pptx_file.name).with_suffix(".yaml")
        logger.debug(
            "Metadata file not passed as an option, using file named after the presentation, with '.yaml' suffix"
        )
    logger.debug("Loading presentation metadata from %r...", str(metadata_file))
    presentation_metadata_data = yaml.safe_load(metadata_file.read_text())
    return PresentationMetadata.parse_obj(presentation_metadata_data)


def open_presentation(input_pptx_file: FileBinaryRead) -> Presentation:
    logger.debug("Loading presentation from %r...", str(input_pptx_file.name))
    prs: Presentation = _open_presentation(input_pptx_file)
    return prs


def parse_slide_option(expr: str, *, slide_ids: list[str]) -> int:
    try:
        slide = parse_slide_expr(expr)
    except Exception:
        raise typer.BadParameter(f"Could not parse {expr!r}")

    try:
        return slide_to_number(slide, slide_ids=slide_ids)
    except ValueError as exc:
        raise typer.BadParameter(f"Invalid slide expression {expr!r}: {exc}") from exc


def parse_slides_option(expr: str, *, slide_ids: list[str]) -> list[int]:
    try:
        slides = list(parse_slides_expr(expr))
    except Exception:
        raise typer.BadParameter(f"Could not parse {expr!r}")

    return [slide_to_number(slide, slide_ids=slide_ids) for slide in slides]
