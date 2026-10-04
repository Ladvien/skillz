"""Minimal streamable-HTTP JSON-RPC client for the home-still MCP server.

Shared by the research-synthesis scripts. Import with `import hs_mcp` (uv puts
the script's directory on sys.path). Requires `httpx` (declare it in the
calling script's PEP 723 header).

Why not use the harness's MCP tools for batch work: the harness client has a
~30 s default request timeout, and for `scribe_convert` a client-side timeout
CANCELS the server-side conversion. This client uses long per-call timeouts and
one MCP session per in-flight unit of work.

URL resolution order: explicit `url` arg > $HS_MCP_URL > ~/.omp/agent/mcp.json
> ~/.claude.json / ./.mcp.json (server named "home-still"); with none of these it exits (no built-in default).
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import httpx

PROTOCOL_VERSION = "2024-11-05"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}

# Per-tool default timeouts (seconds). scribe_convert on a long PDF can run
# many minutes; the harness's 30 s default is what kills it.
TIMEOUTS = {"scribe_convert": 1800, "paper_download": 300, "distill_index": 600, "distill_reindex": 600}
DEFAULT_TIMEOUT = 120


class McpError(RuntimeError):
    """Protocol-level error (JSON-RPC error object or transport failure)."""


class ToolError(McpError):
    """Tool ran but reported isError=true. `.text` holds the tool's message."""

    def __init__(self, tool: str, text: str):
        super().__init__(f"{tool}: {text[:500]}")
        self.tool, self.text = tool, text


def resolve_url(url: str | None = None) -> str:
    if url:
        return url
    if os.environ.get("HS_MCP_URL"):
        return os.environ["HS_MCP_URL"]
    candidates = [Path.home() / ".omp/agent/mcp.json", Path.home() / ".claude.json", Path(".mcp.json")]
    for p in candidates:
        try:
            data = json.loads(p.read_text())
        except Exception:
            continue
        servers = data.get("mcpServers") or data.get("servers") or data
        if isinstance(servers, dict):
            for name, cfg in servers.items():
                if isinstance(cfg, dict) and re.search(r"home[-_]?still", name) and cfg.get("url"):
                    return cfg["url"]
    sys.exit("no home-still MCP URL: pass --url or set $HS_MCP_URL (e.g. http://<host>:<port>/mcp), or add a home-still entry with a `url` to ~/.claude.json or ./.mcp.json")


def _parse_sse_or_json(text: str, want_id: int | None) -> dict | None:
    """Return the JSON-RPC message with id == want_id (or the last one)."""
    text = text.strip()
    if not text:
        return None
    if text.startswith("{"):
        return json.loads(text)
    last = None
    for line in text.splitlines():
        if line.startswith("data:"):
            payload = line[5:].strip()
            if not payload:  # server sends empty priming `data:` events
                continue
            try:
                msg = json.loads(payload)
            except json.JSONDecodeError:
                continue
            last = msg
            if want_id is not None and msg.get("id") == want_id:
                return msg
    return last


class Session:
    """One MCP session. Open lazily; use as a context manager."""

    def __init__(self, url: str | None = None, client: httpx.Client | None = None):
        self.url = resolve_url(url)
        self._own_client = client is None
        self.client = client or httpx.Client(timeout=DEFAULT_TIMEOUT)
        self.sid: str | None = None
        self._id = 0

    # -- lifecycle ---------------------------------------------------------
    def open(self) -> "Session":
        r = self.client.post(
            self.url,
            headers=HEADERS,
            json={
                "jsonrpc": "2.0",
                "id": 0,
                "method": "initialize",
                "params": {
                    "protocolVersion": PROTOCOL_VERSION,
                    "capabilities": {},
                    "clientInfo": {"name": "research-synthesis", "version": "1"},
                },
            },
        )
        r.raise_for_status()
        self.sid = r.headers.get("mcp-session-id")
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized"}, expect_reply=False)
        return self

    def close(self) -> None:
        if self.sid:
            try:
                self.client.delete(self.url, headers={**HEADERS, "mcp-session-id": self.sid}, timeout=10)
            except Exception:
                pass
            self.sid = None
        if self._own_client:
            self.client.close()

    def __enter__(self) -> "Session":
        return self.open()

    def __exit__(self, *exc) -> None:
        self.close()

    # -- transport ---------------------------------------------------------
    def _post(self, body: dict, expect_reply: bool = True, timeout: float | None = None) -> dict | None:
        headers = dict(HEADERS)
        if self.sid:
            headers["mcp-session-id"] = self.sid
        r = self.client.post(self.url, headers=headers, json=body, timeout=timeout or DEFAULT_TIMEOUT)
        if r.status_code >= 400:
            raise McpError(f"HTTP {r.status_code} from {self.url}: {r.text[:300]}")
        if not expect_reply:
            return None
        msg = _parse_sse_or_json(r.text, body.get("id"))
        if msg is None:
            raise McpError("empty response")
        if "error" in msg:
            raise McpError(f"JSON-RPC error: {msg['error']}")
        return msg

    def request(self, method: str, params: dict | None = None, timeout: float | None = None) -> dict:
        self._id += 1
        msg = self._post({"jsonrpc": "2.0", "id": self._id, "method": method, "params": params or {}}, timeout=timeout)
        return msg["result"]  # type: ignore[index]

    # -- tools -------------------------------------------------------------
    def call_text(self, tool: str, args: dict | None = None, timeout: float | None = None) -> str:
        """Call a tool; return concatenated text content. Raises ToolError on isError."""
        args = {k: v for k, v in (args or {}).items() if v is not None}
        res = self.request(
            "tools/call", {"name": tool, "arguments": args}, timeout=timeout or TIMEOUTS.get(tool, DEFAULT_TIMEOUT)
        )
        text = "\n".join(c.get("text", "") for c in res.get("content", []) if c.get("type") == "text")
        if res.get("isError"):
            raise ToolError(tool, text)
        return text

    def call(self, tool: str, args: dict | None = None, timeout: float | None = None) -> Any:
        """Call a tool; parse the text as JSON when possible, else return the str."""
        text = self.call_text(tool, args, timeout)
        try:
            return json.loads(text)
        except (json.JSONDecodeError, ValueError):
            return text

    def list_tools(self) -> list[dict]:
        return self.request("tools/list")["tools"]


@contextmanager
def session(url: str | None = None):
    s = Session(url)
    try:
        yield s.open()
    finally:
        s.close()


def call_retry(s: Session, tool: str, args: dict, tries: int = 3, backoff: float = 2.0, timeout: float | None = None):
    """Retry transient transport errors (not ToolError) with exponential backoff."""
    for i in range(tries):
        try:
            return s.call(tool, args, timeout)
        except ToolError:
            raise
        except (McpError, httpx.HTTPError) as e:
            if i == tries - 1:
                raise
            time.sleep(backoff * (2**i))
            print(f"[retry {i + 1}/{tries}] {tool}: {e}", file=sys.stderr)


# -- helpers shared by scripts ---------------------------------------------
def norm_doi(doi: str | None) -> str:
    if not doi:
        return ""
    d = doi.strip().lower()
    d = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:)", "", d)
    return d.rstrip(".,;)")


def doi_to_stem_candidates(doi: str) -> list[str]:
    """Plausible catalog stems for a DOI; the real stem MUST be confirmed via catalog_read."""
    d = norm_doi(doi)
    return [d.replace("/", "_"), d.replace("/", "%2F"), d.replace("/", "-")]


def add_common_args(ap) -> None:
    ap.add_argument("--url", help="MCP endpoint (default: $HS_MCP_URL, then a home-still entry with a url in ~/.omp/agent/mcp.json, ~/.claude.json or ./.mcp.json)")


def resolve_meta(s: Session, stem: str) -> dict:
    """Best-effort bibliographic metadata for a corpus stem.

    Many corpus stems (OpenAlex W-ids, PubMed ids, hash names) have EMPTY title/doi in catalog_read.
    Order: catalog_read -> openalex_get (W-id, DOI, or DOI-shaped stem) -> first heading of markdown page 1.
    `source` says which one answered; 'markdown_head' is an UNVERIFIED guess and must be treated as such.
    """
    m = {"stem": stem, "title": "", "doi": "", "year": "", "authors": [], "source": "", "in_catalog": False,
         "converted": False, "embedded": False}
    try:
        c = s.call("catalog_read", {"stem": stem})
    except ToolError:
        c = None
    if isinstance(c, dict):
        m.update(in_catalog=True, converted=bool(c.get("conversion")), embedded=bool(c.get("embedding")),
                 title=(c.get("title") or "").strip(), doi=norm_doi(c.get("doi")),
                 year=str(c.get("publication_date") or "")[:4],
                 authors=[a.get("name", "") for a in (c.get("authors") or []) if isinstance(a, dict)][:8])
        if m["title"]:
            m["source"] = "catalog"
    if not m["title"]:
        key = stem if re.fullmatch(r"W\d+", stem) else (m["doi"] or (stem.replace("_", "/", 1) if stem.startswith("10.") else ""))
        if key:
            try:
                g = s.call("openalex_get", {"id_or_doi": key})
                if isinstance(g, dict) and g.get("title"):
                    m.update(title=g["title"].strip(), doi=m["doi"] or norm_doi(g.get("doi")),
                             year=m["year"] or str(g.get("publication_year") or ""),
                             authors=m["authors"] or [a.get("display_name", "") for a in (g.get("authors") or [])][:8],
                             source="openalex")
            except (ToolError, McpError):
                pass
    if not m["title"] and m["in_catalog"]:
        try:
            md = s.call_text("markdown_read", {"stem": stem, "page": 1}, timeout=120)
            boiler = re.compile(r"(research|original|review|brief|short|case)\s+(article|report|paper|communication)|repository|"
                                r"link to published|citation of|https?:|doi|copyright|peer-reviewed|journal of|accepted|"
                                r"available online|abstract|keywords?|downloaded|^\W*page\b|all rights|license", re.I)
            for line in md[:6000].splitlines():
                t = line.strip().lstrip("#").strip().strip("*_ \"'")
                if len(t) >= 30 and len(t.split()) >= 5 and not boiler.search(t):
                    m.update(title=t[:200], source="markdown_head")
                    break
        except (ToolError, McpError, httpx.HTTPError):
            pass
    return m
