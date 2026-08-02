import unittest

from discordrpc import button
from discordrpc.exceptions import InvalidURL
from discordrpc.utils import required_url, valid_url


class ValidUrlTests(unittest.TestCase):
    def test_accepts_http_and_https(self):
        self.assertEqual(valid_url("http://example.com"), "http://example.com")
        self.assertEqual(valid_url("https://example.com/path"), "https://example.com/path")

    def test_accepts_query_and_fragment(self):
        self.assertEqual(valid_url("https://example.com?a=1#frag"), "https://example.com?a=1#frag")

    def test_none_is_optional(self):
        self.assertIsNone(valid_url(None))

    def test_rejects_unsupported_schemes(self):
        for url in ("ftp://example.com", "javascript:alert(1)", "file:///tmp/x"):
            with self.assertRaises(InvalidURL):
                valid_url(url)

    def test_rejects_bare_scheme_without_host(self):
        for url in ("http://", "https://", "http://?", "https://#frag"):
            with self.assertRaises(InvalidURL):
                valid_url(url)

    def test_rejects_empty_string(self):
        with self.assertRaises(InvalidURL):
            valid_url("")

    def test_rejects_non_string(self):
        with self.assertRaises(InvalidURL):
            valid_url(12345)


class RequiredUrlTests(unittest.TestCase):
    def test_none_rejected_when_required(self):
        with self.assertRaises(InvalidURL):
            required_url(None)

    def test_empty_rejected_when_required(self):
        with self.assertRaises(InvalidURL):
            required_url("")


class ButtonTests(unittest.TestCase):
    def test_valid_button(self):
        self.assertEqual(
            button("Repository", "https://github.com/Senophyx/discord-rpc"),
            {"label": "Repository", "url": "https://github.com/Senophyx/discord-rpc"},
        )

    def test_none_url_rejected(self):
        with self.assertRaises(InvalidURL):
            button("Repository", None)

    def test_empty_url_rejected(self):
        with self.assertRaises(InvalidURL):
            button("Repository", "")

    def test_unsupported_scheme_rejected(self):
        with self.assertRaises(InvalidURL):
            button("Repository", "ftp://example.com")


if __name__ == "__main__":
    unittest.main(verbosity=2)
