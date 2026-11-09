import pytest
import requests

from lotto_lab.fetcher import fetch_html


def test_fetch_html_success(monkeypatch):

    class FakeResponse:
        text = "<html><body>Test</body></html>"

        def raise_for_status(self):
            pass

    def fake_get(url, timeout):
        return FakeResponse()

    monkeypatch.setattr(
        "lotto_lab.fetcher.requests.get",
        fake_get
    )

    result = fetch_html("https://example.com")

    assert result == "<html><body>Test</body></html>"


def test_fetch_html_http_error(monkeypatch):

    class FakeResponse:
        def raise_for_status(self):
            raise requests.exceptions.HTTPError("404 Not Found")

    def fake_get(url, timeout):
        return FakeResponse()

    monkeypatch.setattr(
        "lotto_lab.fetcher.requests.get",
        fake_get
    )

    with pytest.raises(requests.exceptions.HTTPError):
        fetch_html("https://example.com/missing")


def test_fetch_html_timeout(monkeypatch):

    def fake_get(url, timeout):
        raise requests.exceptions.Timeout("Request timed out")

    monkeypatch.setattr(
        "lotto_lab.fetcher.requests.get",
        fake_get
    )

    with pytest.raises(requests.exceptions.Timeout):
        fetch_html("https://example.com")