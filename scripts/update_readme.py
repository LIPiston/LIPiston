#!/usr/bin/env python3
"""Update the marked RSS section of readme.md."""

from dataclasses import dataclass
from datetime import timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
import sys
from tempfile import NamedTemporaryFile
from typing import Final
from urllib.error import URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ElementTree


RSS_URL: Final[str] = "https://lipiston.top/feed"
START_MARKER: Final[str] = "<!-- BLOG-POST-LIST:START -->"
END_MARKER: Final[str] = "<!-- BLOG-POST-LIST:END -->"
README_PATH: Final[Path] = Path("readme.md")
ENTRY_LIMIT: Final[int] = 5


@dataclass(frozen=True, slots=True)
class FeedEntry:
    """A validated RSS entry ready for Markdown rendering."""

    title: str
    link: str
    date: str


class RssUpdateError(Exception):
    """A recoverable RSS or README update failure."""

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)

    def __str__(self) -> str:
        return self.detail


def _child_text(item: ElementTree.Element, name: str) -> str:
    for child in item:
        if child.tag.rsplit("}", 1)[-1] == name:
            return (child.text or "").strip()
    return ""


def parse_feed(feed_bytes: bytes) -> list[FeedEntry]:
    """Parse the first five complete RSS items in feed order."""
    try:
        root = ElementTree.fromstring(feed_bytes)
    except ElementTree.ParseError as error:
        raise RssUpdateError(f"RSS XML is malformed: {error}") from error

    items = [element for element in root.iter() if element.tag.rsplit("}", 1)[-1] == "item"]
    if len(items) < ENTRY_LIMIT:
        raise RssUpdateError(f"RSS feed contains {len(items)} items; exactly five are required")

    entries: list[FeedEntry] = []
    for position, item in enumerate(items[:ENTRY_LIMIT], start=1):
        title = _child_text(item, "title")
        link = _child_text(item, "link")
        pub_date = _child_text(item, "pubDate")
        if not title or not link or not pub_date:
            raise RssUpdateError(f"RSS item {position} has an empty title, link, or pubDate")
        parsed_link = urlsplit(link)
        if (
            parsed_link.scheme != "https"
            or not parsed_link.netloc
            or any(character.isspace() or character in "()[]<>\\" for character in link)
        ):
            raise RssUpdateError(f"RSS item {position} has a non-HTTPS link")
        try:
            parsed_date = parsedate_to_datetime(pub_date)
        except (TypeError, ValueError) as error:
            raise RssUpdateError(f"RSS item {position} has an invalid pubDate") from error
        if parsed_date is None or parsed_date.tzinfo is None:
            raise RssUpdateError(f"RSS item {position} has an invalid pubDate timezone")
        entries.append(FeedEntry(title, link, parsed_date.astimezone(timezone.utc).strftime("%Y-%m-%d")))
    return entries


def render_markdown(entries: list[FeedEntry]) -> str:
    """Render validated feed entries as the required Markdown list."""
    return "\n".join(
        f"- [{escape_markdown_title(entry.title)}]({entry.link}) - {entry.date}"
        for entry in entries
    )


def escape_markdown_title(title: str) -> str:
    """Make an RSS title a single escaped Markdown link-label line."""
    return (
        title.replace("\\", "\\\\")
        .replace("\r", " ")
        .replace("\n", " ")
        .replace("[", "\\[")
        .replace("]", "\\]")
        .replace("<", "\\<")
        .replace(">", "\\>")
    )


def update_text(readme_text: str, markdown: str) -> str:
    """Replace only the content between the README markers."""
    if readme_text.count(START_MARKER) != 1 or readme_text.count(END_MARKER) != 1:
        raise RssUpdateError("README must contain exactly one RSS start and end marker")
    start = readme_text.find(START_MARKER)
    end = readme_text.find(END_MARKER)
    if start < 0 or end < 0:
        raise RssUpdateError("README is missing RSS section markers")
    if end < start:
        raise RssUpdateError("README RSS section markers are reversed")
    content_start = start + len(START_MARKER)
    return readme_text[:content_start] + "\n" + markdown + "\n" + readme_text[end:]


def update_file(readme_path: Path, markdown: str) -> bool:
    """Update a README file and return whether its contents changed."""
    original = readme_path.read_text(encoding="utf-8")
    updated = update_text(original, markdown)
    if updated == original:
        return False
    temporary_path: Path | None = None
    try:
        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=readme_path.parent,
            prefix=f".{readme_path.name}.",
            delete=False,
        ) as temporary_file:
            temporary_file.write(updated)
            temporary_path = Path(temporary_file.name)
        temporary_path.replace(readme_path)
    except OSError as error:
        raise RssUpdateError(f"Unable to replace README atomically: {error}") from error
    finally:
        if temporary_path is not None:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError:
                pass
    return True


def fetch_feed() -> bytes:
    """Fetch the configured RSS feed using the standard library."""
    request = Request(RSS_URL, headers={"User-Agent": "LIPiston-RSS-Updater/1.0"})
    try:
        with urlopen(request, timeout=30) as response:
            return response.read()
    except URLError as error:
        raise RssUpdateError(f"Unable to fetch RSS feed: {error.reason}") from error


def run(readme_path: Path = README_PATH) -> bool:
    """Fetch RSS data and update the README only after complete validation."""
    markdown = render_markdown(parse_feed(fetch_feed()))
    return update_file(readme_path, markdown)


def main() -> int:  # noqa: BROAD_EXCEPT_OK
    """Run the updater CLI and report actionable failures."""
    try:
        changed = run()
    except RssUpdateError as error:
        print(f"RSS README update failed: {error}", file=sys.stderr)
        return 1
    print("README updated" if changed else "README already current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
