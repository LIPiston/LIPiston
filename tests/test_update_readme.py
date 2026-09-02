import sys
import tempfile
import unittest
from pathlib import Path
from urllib.error import URLError
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1]))

from scripts import update_readme


START = "<!-- BLOG-POST-LIST:START -->"
END = "<!-- BLOG-POST-LIST:END -->"


def rss_item(title: str = "Title", link: str = "https://example.com", pub_date: str = "Wed, 02 Sep 2026 03:00:00 +0000") -> str:
    return f"<item><title>{title}</title><link>{link}</link><pubDate>{pub_date}</pubDate></item>"


def rss_feed(*items: str) -> bytes:
    return ("<rss><channel>" + "".join(items) + "</channel></rss>").encode()


class UpdateReadmeTests(unittest.TestCase):
    def test_parse_feed_keeps_first_five_in_feed_order(self) -> None:
        feed = rss_feed(*(rss_item(f"Post {index}", f"https://example.com/{index}") for index in range(7)))

        entries = update_readme.parse_feed(feed)

        self.assertEqual([entry.title for entry in entries], [f"Post {index}" for index in range(5)])

    def test_parse_feed_converts_dates_to_utc(self) -> None:
        feed = rss_feed(*(rss_item(pub_date="Wed, 02 Sep 2026 03:00:00 -0500") if index == 0 else rss_item() for index in range(5)))

        entries = update_readme.parse_feed(feed)

        self.assertEqual(entries[0].date, "2026-09-02")

    def test_render_markdown_uses_exact_format(self) -> None:
        feed = rss_feed(*(rss_item("A title", "https://example.com/a", "Wed, 02 Sep 2026 03:00:00 +0000") if index == 0 else rss_item() for index in range(5)))

        markdown = update_readme.render_markdown(update_readme.parse_feed(feed))

        expected = "\n".join(["- [A title](https://example.com/a) - 2026-09-02", *["- [Title](https://example.com) - 2026-09-02"] * 4])
        self.assertEqual(markdown, expected)

    def test_update_text_preserves_manual_text_outside_markers(self) -> None:
        original = f"before\n{START}\nold\n{END}\nafter"
        expected = f"before\n{START}\n" + "\n".join(["- [Title](https://example.com) - 2026-09-02"] * 5) + f"\n{END}\nafter"

        feed = rss_feed(*(rss_item() for _ in range(5)))
        updated = update_readme.update_text(original, update_readme.render_markdown(update_readme.parse_feed(feed)))

        self.assertEqual(updated, expected)

    def test_update_text_is_idempotent(self) -> None:
        original = f"before\n{START}\nold\n{END}\nafter"
        markdown = "- [Title](https://example.com) - 2026-09-02"
        updated = update_readme.update_text(original, markdown)

        self.assertEqual(update_readme.update_text(updated, markdown), updated)

    def test_parse_feed_rejects_malformed_xml(self) -> None:
        with self.assertRaises(update_readme.RssUpdateError):
            update_readme.parse_feed(b"<rss>")

    def test_parse_feed_rejects_fewer_than_five_items(self) -> None:
        with self.assertRaises(update_readme.RssUpdateError):
            update_readme.parse_feed(rss_feed(rss_item("Only one")))

    def test_parse_feed_rejects_empty_required_fields(self) -> None:
        for item in (rss_item("", "https://example.com"), rss_item("Title", ""), rss_item("Title", "https://example.com", "")):
            with self.subTest(item=item), self.assertRaises(update_readme.RssUpdateError):
                update_readme.parse_feed(rss_feed(item, rss_item(), rss_item(), rss_item(), rss_item()))

    def test_parse_feed_rejects_invalid_pub_date(self) -> None:
        feed = rss_feed(*(rss_item(pub_date="not a date") if index == 0 else rss_item() for index in range(5)))

        with self.assertRaises(update_readme.RssUpdateError):
            update_readme.parse_feed(feed)

    def test_parse_feed_rejects_non_https_links(self) -> None:
        for link in ("javascript:alert(1)", "http://example.com"):
            with self.subTest(link=link):
                feed = rss_feed(*(rss_item(link=link) if index == 0 else rss_item() for index in range(5)))
                with self.assertRaises(update_readme.RssUpdateError):
                    update_readme.parse_feed(feed)

    def test_parse_feed_rejects_https_links_with_markdown_delimiters(self) -> None:
        link = "https://example.com/a) [injected](https://evil.example"
        feed = rss_feed(*(rss_item(link=link) if index == 0 else rss_item() for index in range(5)))

        with self.assertRaises(update_readme.RssUpdateError):
            update_readme.parse_feed(feed)

    def test_parse_feed_accepts_standard_https_link(self) -> None:
        feed = rss_feed(*(rss_item(link="https://example.com/articles/1") if index == 0 else rss_item() for index in range(5)))

        entries = update_readme.parse_feed(feed)

        self.assertEqual(entries[0].link, "https://example.com/articles/1")

    def test_escape_markdown_title_flattens_and_escapes_control_characters(self) -> None:
        title = r"bad ](https://evil.example)\n- injected <tag> [label] \path"

        escaped = update_readme.escape_markdown_title(title)

        self.assertEqual(escaped, r"bad \](https://evil.example)\\n- injected \<tag\> \[label\] \\path")

    def test_escape_markdown_title_replaces_actual_line_breaks(self) -> None:
        escaped = update_readme.escape_markdown_title("first\r\nsecond")

        self.assertEqual(escaped, "first  second")

    def test_render_markdown_keeps_control_character_title_in_one_safe_line(self) -> None:
        title = "bad ](https://evil.example)\n- injected"
        feed = rss_feed(*(rss_item(title=title) if index == 0 else rss_item() for index in range(5)))

        markdown = update_readme.render_markdown(update_readme.parse_feed(feed))

        self.assertEqual(markdown.splitlines()[0], r"- [bad \](https://evil.example) - injected](https://example.com) - 2026-09-02")
        self.assertEqual(len(markdown.splitlines()), 5)

    def test_update_text_rejects_missing_markers(self) -> None:
        with self.assertRaises(update_readme.RssUpdateError):
            update_readme.update_text("no markers", "content")

    def test_update_text_rejects_reversed_markers(self) -> None:
        with self.assertRaises(update_readme.RssUpdateError):
            update_readme.update_text(f"{END}\n{START}", "content")

    def test_update_text_rejects_duplicate_start_marker(self) -> None:
        with self.assertRaises(update_readme.RssUpdateError):
            update_readme.update_text(f"{START}\n{START}\n{END}", "content")

    def test_update_text_rejects_duplicate_end_marker(self) -> None:
        with self.assertRaises(update_readme.RssUpdateError):
            update_readme.update_text(f"{START}\n{END}\n{END}", "content")

    def test_fetch_feed_wraps_url_error(self) -> None:
        with patch("scripts.update_readme.urlopen", side_effect=URLError("offline")):
            with self.assertRaises(update_readme.RssUpdateError):
                update_readme.fetch_feed()

    def test_update_file_replaces_atomically_after_writing_temp_file(self) -> None:
        original = f"before\n{START}\nold\n{END}\nafter"
        markdown = "new content"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "readme.md"
            path.write_text(original, encoding="utf-8")
            with patch("scripts.update_readme.NamedTemporaryFile", wraps=update_readme.NamedTemporaryFile) as temporary_file:
                changed = update_readme.update_file(path, markdown)

            self.assertTrue(changed)
            self.assertEqual(path.read_text(encoding="utf-8"), f"before\n{START}\n{markdown}\n{END}\nafter")
            temporary_file.assert_called_once()

    def test_update_file_preserves_original_when_replacement_fails(self) -> None:
        original = f"before\n{START}\nold\n{END}\nafter"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "readme.md"
            path.write_text(original, encoding="utf-8")
            with patch.object(Path, "replace", side_effect=OSError("replacement failed")):
                with self.assertRaises(update_readme.RssUpdateError):
                    update_readme.update_file(path, "new content")

            self.assertEqual(path.read_text(encoding="utf-8"), original)

    def test_update_file_does_not_write_when_text_is_identical(self) -> None:
        original = f"{START}\ncontent\n{END}"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "readme.md"
            path.write_text(original, encoding="utf-8")
            changed = update_readme.update_file(path, "content")
            self.assertFalse(changed)
            self.assertEqual(path.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
