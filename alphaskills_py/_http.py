"""Shared HTTP client with polite defaults + SEC-compliant User-Agent."""

from __future__ import annotations
import os
import time
import urllib.request
import urllib.parse
import urllib.error
import json as _json
from typing import Any, Optional

# SEC EDGAR requires User-Agent in the form "Name email@domain.com" —
# they return HTTP 403 without it. Set ALPHASKILLS_USER_AGENT env var
# to your own contact string for production use.
DEFAULT_UA = os.environ.get(
    "ALPHASKILLS_USER_AGENT",
    "AlphaSkills Research mohye24k@users.noreply.github.com",
)

_last_request_at: dict[str, float] = {}


def _throttle(host: str, min_interval_s: float = 0.11) -> None:
    """Crude per-host rate limiter. SEC asks ≤10 req/sec; we use 0.11s = ~9/s."""
    last = _last_request_at.get(host, 0.0)
    elapsed = time.time() - last
    if elapsed < min_interval_s:
        time.sleep(min_interval_s - elapsed)
    _last_request_at[host] = time.time()


def request(
    url: str,
    *,
    method: str = "GET",
    headers: Optional[dict[str, str]] = None,
    params: Optional[dict[str, Any]] = None,
    data: Optional[Any] = None,
    json_body: Optional[Any] = None,
    timeout: float = 30.0,
    host_throttle: bool = True,
) -> tuple[int, dict[str, str], bytes]:
    """Low-level HTTP request returning (status, headers, raw_body)."""
    if params:
        url = url + ("&" if "?" in url else "?") + urllib.parse.urlencode(params, doseq=True)

    parsed = urllib.parse.urlparse(url)
    if host_throttle:
        _throttle(parsed.netloc)

    merged_headers = {"User-Agent": DEFAULT_UA, "Accept-Encoding": "gzip, deflate"}
    if headers:
        merged_headers.update(headers)

    body: Optional[bytes] = None
    if json_body is not None:
        body = _json.dumps(json_body).encode()
        merged_headers.setdefault("Content-Type", "application/json")
    elif data is not None:
        if isinstance(data, (dict, list)):
            body = urllib.parse.urlencode(data).encode()
            merged_headers.setdefault("Content-Type", "application/x-www-form-urlencoded")
        elif isinstance(data, str):
            body = data.encode()
        else:
            body = data  # assume bytes

    req = urllib.request.Request(url, data=body, method=method, headers=merged_headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            # auto-decompress gzip
            if resp.headers.get("Content-Encoding") == "gzip":
                import gzip
                raw = gzip.decompress(raw)
            return resp.status, dict(resp.headers), raw
    except urllib.error.HTTPError as e:
        raw = e.read()
        if (e.headers or {}).get("Content-Encoding") == "gzip":
            import gzip
            try:
                raw = gzip.decompress(raw)
            except Exception:
                pass
        return e.code, dict(e.headers or {}), raw


def get_json(url: str, **kwargs: Any) -> Any:
    """GET and parse JSON."""
    status, _, raw = request(url, **kwargs)
    if status != 200:
        snippet = raw[:300].decode("ascii", errors="replace") if isinstance(raw, bytes) else str(raw)[:300]
        raise RuntimeError(f"HTTP {status} from {url}: {snippet}")
    return _json.loads(raw)


def get_text(url: str, **kwargs: Any) -> str:
    """GET and return text."""
    status, _, raw = request(url, **kwargs)
    if status != 200:
        raise RuntimeError(f"HTTP {status} from {url}")
    return raw.decode("utf-8", errors="replace")


def post_json(url: str, json_body: Any, **kwargs: Any) -> Any:
    """POST JSON body, expect JSON response."""
    kwargs.setdefault("method", "POST")
    status, _, raw = request(url, json_body=json_body, **kwargs)
    if status != 200:
        raise RuntimeError(f"HTTP {status} from {url}: {raw[:300].decode(errors='replace')}")
    return _json.loads(raw)
