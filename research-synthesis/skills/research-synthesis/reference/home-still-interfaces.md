# home-still interface reference (observed 2026-10-02)

Everything below was observed live unless tagged [INFERENCE]. Server: `serverInfo {name: "rmcp", version: "1.3.0"}`, protocol `2024-11-05`.
Pipeline: search → download → convert (scribe) → embed (distill/Qdrant, bge-m3) → semantic search.

## 1. MCP server config

| Where | Entry |
|---|---|
| `~/.omp/agent/mcp.json` → `mcpServers.home-still` | `{"type":"http","url":"http://<host>:<port>/mcp","timeout":900000}` (timeout ms = 15 min; no auth header) |
| `~/.claude.json` → `mcpServers.home-still` | either the same http form, or stdio: `node <path>/home-still-bridge.mjs` (stdio↔HTTPS bridge to a cloud gateway given by `~/.home-still/config.yaml` `cloud.gateway_url`; bearer token from `~/.home-still/cloud-token` — secret, not recorded) |
| `.mcp.json` in repo | no home-still entry |

- Transport (omp): streamable HTTP; responses may be SSE (`data: {...}`) or plain JSON. Server reachable at time of observation.
- omp's *default* MCP timeout is 30 s; the 900000 ms override above is read at session start.
- Raw JSON-RPC recipe (works, tested):
```python
H={"Content-Type":"application/json","Accept":"application/json, text/event-stream"}
r=c.post(U,headers=H,json={"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"x","version":"1"}}})
H["mcp-session-id"]=r.headers["mcp-session-id"]
c.post(U,headers=H,json={"jsonrpc":"2.0","method":"notifications/initialized"})
c.post(U,headers=H,json={"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"distill_search","arguments":{"query":"..","limit":5}}})
# result.content[0].text is a JSON string (parse it); result.isError bool
```

## 2. Tools (34 total). `*` = required arg. `?` = optional (nullable).

### Read-only / safe
| Tool | Args | Purpose |
|---|---|---|
| `paper_search` | `query*` str; `provider?` str (all, arxiv, openalex, semantic_scholar/s2, europmc/pmc, crossref, core; default all; unknown → error); `search_type?` (keywords, title, author, doi, subject; default keywords); `date?` str (`>=2023`, `2020-2024`); `max_results?` int (default 10); `offset?` int; `min_citations?` int (arXiv ignores); `sort?` (relevance, citations, date) | Search 6 providers (live external APIs, slow ~10 s) |
| `paper_get` | `doi*` | Full metadata for one DOI |
| `paper_references` | `doi*` | Reference list (Semantic Scholar) |
| `paper_citations` | `doi*`; `limit?` (def 100, max 1000); `year_from?` int; `sort?` (year default, citations) | Forward citations |
| `distill_search` | `query*`; `limit?` (def 10); `year?` str (`>2020`, `2023`, `>=2021`); `include_text?` bool (def true; false = metadata only) | Semantic search over chunk collection `academic_papers` |
| `abstract_search` | same as distill_search | Semantic search over per-paper abstracts (`paper_abstracts` collection) |
| `distill_status` | none | Qdrant/embedder status |
| `distill_exists` | `doc_id*` | Is doc indexed? → `{"doc_id","indexed":bool}` |
| `system_status` | `include_repaired?` bool | Whole pipeline counts + server health + recent history |
| `scribe_health` | none | Scribe server health |
| `catalog_read` | `stem*` | Full catalog entry (YAML-ish JSON) |
| `catalog_list` | `limit?`, `offset?`, `embedded?` bool | List catalog papers |
| `catalog_recent` | `limit?` (def 30), `include_repaired?` | Recent download/convert/embed events |
| `markdown_read` | `stem*`; `page?` uint (1-based) | Converted markdown, whole or one page |
| `markdown_list` | `limit?`, `offset?` (schema also shows a copy-pasted `embedded?`) | List markdown docs w/ size, pages |
| `openalex_search` | `query*`; `max_results?` (def 10, max 200); `min_citations?`; `sort?` (relevance, citations, year); `year_from?`; `year_to?` | BM25 over LOCAL OpenAlex DuckDB (no external call) |
| `openalex_get` | `id_or_doi*` | Work + authors + topics |
| `openalex_references` | `openalex_id*`; `limit?` (def 100, max 1000) | Outbound refs (local) |
| `openalex_citations` | `openalex_id*`; `limit?`; `sort?` (citations, year); `year_from?` | Citing works (local) |
| `openalex_authors_by_topic` | `topic_id*` (e.g. T13975); `limit?` (def 25, max 200) | Top authors for topic |
| `personal_list/read/search` | `category?`, `limit?`, `stem*` / `query*` | PRIVATE medical/financial records — research skill must NOT use |
| Dry-run reports | `catalog_repair`, `catalog_backfill_title`, `dedupe_url_encoded`, `distill_reconcile`, `distill_scan_repetitions`, `distill_backfill` (`dry_run` default true; `limit?`) | Maintenance; `catalog_backfill_title`/`catalog_repair`/`distill_backfill` WRITE if `dry_run=false` |

### Write / mutating — do not call casually
| Tool | Args | Purpose |
|---|---|---|
| `paper_download` | `doi*` | Download PDF to papers dir; creates catalog entry; returns path/size/sha256 |
| `scribe_convert` | `stem*` | Convert PDF/HTML → markdown (minutes for PDFs; see hazards) |
| `distill_index` | `stem*` | Index markdown into Qdrant |
| `distill_reindex` | `stem*` | Purge + re-index |
| `personal_add` / `personal_reindex` | `filename*` (+`category?`,`title?`,`force?`) / `stem*` | Personal store ingest |

### Resources / templates / prompts
- `resources/list` returns one `catalog:///{stem}` per catalog entry (huge; includes odd stems like `0003122412445802 -- 4c29… -- Anna’s Archive`).
- Templates: `catalog:///{stem}` (application/yaml), `markdown:///{stem}` (text/markdown), `markdown:///{stem}/page/{page}`.
- Prompts (all `prompts/get` bodies, verbatim, `{x}` = arg):

| Prompt | Args | Body |
|---|---|---|
| `research_paper` | `topic*` | `Research the topic: "{topic}"` + steps: 1 paper_search; 2 catalog_read (check collection); 3 markdown_read full text of converted papers; 4 distill_search across indexed corpus; 5 synthesize comprehensive summary with citations |
| `summarize_document` | `stem*` | `Read and summarize the paper with stem "{stem}".` 1 catalog_read metadata; 2 markdown_read full text; 3 structured summary: objective, methods, key findings, limitations, relevance |
| `compare_papers` | `stem_a*`, `stem_b*` | `Compare these two papers: Paper A "{stem_a}", Paper B "{stem_b}"`: catalog_read both; markdown_read both; compare research questions, methodology, findings, conclusions; note agreements, contradictions, complementary insights |

## 3. Example responses (trimmed; each `content[0].text` is JSON)

### system_status
```json
{"pipeline":{"documents":10941,"pdfs":9467,"htmls":1474,"epubs":0,"markdown":10795,"catalog_entries":10933,
  "embedded_documents":10850,"embedded_chunks":331917,"embedding_skipped":420,"corrupted_pdfs":138,
  "inbox_pending":0,"in_flight_conversions":0,"pipeline_drift":98,"pipeline_drift_threshold":3},
 "scribe_instances":[{"url":"http://<scribe-host>:7433","healthy":true,"version":"0.0.1-rc.355","activity":"idle","in_flight":0,"slots_total":6,"slots_available":6},
                     {"url":"http://<gpu-host>:7435","healthy":false,"activity":"backend unavailable","slots_total":12,"slots_available":0}],
 "distill_instances":[{"url":"http://<gpu-host>:7434","healthy":true,"compute_device":"Cuda","embed_model":"bge-m3","collection":"academic_papers"}],
 "qdrant":{"collection":"academic_papers","qdrant_url":"http://localhost:6334","qdrant_version":"1.19.1"},
 "history":[{"activity":"Embed|Convert","stem":"10.1038_tp.2016.161","name":"<title>","detail":"28 chunks|9pg 180.9s","at":"ISO8601","chunks":28,"pages":9,"duration_secs":180.9}]}
```
Note: observed `pipeline_drift` 98 > threshold 3, one scribe instance unhealthy.

### distill_status
```json
{"health":{"collection":"academic_papers","compute_device":"Cuda","embed_model":"bge-m3","qdrant_url":"http://localhost:6334","qdrant_version":"1.19.1","status":"ok","version":"0.0.1-rc.358"},
 "status":{"collection":"academic_papers","documents_count":10850,"points_count":331917,"embed_model":"bge-m3","compute_device":"Cuda"}}
```

### paper_search ("<query>", max_results 1) → JSON array
```json
[{"id":"W2034220807","title":"Acetylcholine Elevation Relieves Cognitive Rigidity and Social Deficiency in a Mouse Model of Autism",
  "authors":[{"name":"Golan Karvat","affiliations":["Weizmann Institute of Science"]}, {"name":"Tali Kimchi","affiliations":[]}],
  "abstract_text":null,"publication_date":"2013-10-07","doi":"10.1038/npp.2013.274",
  "download_urls":["https://www.nature.com/articles/npp2013274.pdf"],"cited_by_count":215,"source":"openalex"}]
```
`source` = `+`-joined providers (e.g. `crossref+openalex`). `abstract_text` is often null in search (provider=all) but filled in `paper_get`. Author lists may contain duplicates in "Last, First" form. No `year` field → derive from `publication_date`. `id` is an OpenAlex ID (usable with `openalex_*` tools).

### distill_search ("<query>", limit 2) → JSON array of chunk hits
```json
[{"doc_id":"10.1038_s41583-021-00428-w","title":"Cognitive and behavioural flexibility: neural mechanisms and clinical considerations.",
  "authors":["Lucina Q. Uddin","Uddin, Lucina Q"],"year":2021,"doi":"10.1038/s41583-021-00428-w",
  "chunk_text":"…(markdown chunk; this one was a reference-list chunk)…","score":0.754,
  "pdf_path":"papers/10/10.1038_s41583-021-00428-w.pdf","line_start":757,"line_end":904,"page":1,"category":null}]
```
- **`doc_id` == `stem`** (DOI with `/` → `_`, e.g. `10.1016_j.tics.2008.11.006`) — pass as `stem` to catalog_read/markdown_read and as `doc_id` to distill_exists.
- Hits are chunks: the same doc can appear multiple times; chunks can be bibliography fragments (check text). `line_start/line_end` index lines of the markdown file. `page` was 1 for both hits (single-page HTML-derived docs; for PDFs [INFERENCE] it is the PDF page). `pdf_path` ext may disagree with catalog (`.pdf` in hit vs `.html` in catalog for the same stem).
- DOI may be reconstructed from `doc_id` only heuristically (`_`→`/` is ambiguous) — prefer the `doi` field. `authors`/`year`/`title` may be null/dirty [INFERENCE for null; duplicates observed].

### catalog_read (stem = doc_id)
```json
{"title":"…","authors":[{"name":"Lucina Q. Uddin"},{"name":"Uddin, Lucina Q"}],"doi":"10.1038/s41583-021-00428-w",
 "publication_date":"2021-02-03","abstract_text":"…full abstract…","cited_by_count":734,"source":"core+crossref+europe_pmc+openalex",
 "download_urls":["https://www.nature.com/articles/…pdf"],"pdf_path":"papers/10/<stem>.html","markdown_path":"markdown/10/<stem>.md",
 "downloaded_at":"ISO","file_size_bytes":581594,"sha256":"…",
 "conversion":{"server":"html-parser","duration_secs":0.01,"total_pages":1,"converted_at":"ISO","pages":[{"page":1,"char_start":0,"char_end":39372}],"converted_by":"glm_ocr"},
 "embedding":{"server":"event-watch","chunks_indexed":13,"compute_device":"Cuda","embedded_at":"ISO"}}
```
Citation source = `title`, `authors[].name`, `publication_date` (year), `doi`. Absent `conversion`/`embedding` blocks = not converted/embedded [INFERENCE]; failures may appear as `conversion_failed` stamps (named in `hs scribe reconvert` help).

### markdown_read
- `{stem}` → full markdown as plain text (starts `## Abstract\n\n…`). Large; always prefer `page`.
- `{stem, page:N}` → page text; out of range → plain text `Page 2 not found. Document has 1 pages.` (not JSON, not necessarily isError).
- Page boundaries = `catalog_read.conversion.pages[].char_start/char_end`.

### From a search hit to a citation
`distill_search` hit → (`title`,`authors`,`year`,`doi` in hit; verify with `catalog_read(doc_id)`) → full text `markdown_read(doc_id[, page])`. Unindexed candidates: `paper_search` result `doi` → `paper_get` → (write path) `paper_download` → `scribe_convert` → `distill_index` (stem = DOI with `/`→`_`, [INFERENCE] from observed stems).

## 4. `hs` CLI (`hs` on PATH)
Global flags (all subcommands): `--output text|json|ndjson` (default text), `--color auto|always|never`, `--quiet`, `--verbose`, `--config-dir <DIR>`, `-y/--yes`.
Top-level commands: `scribe paper personal distill status restart upgrade serve server cloud mcp config migrate pipeline openalex`.

| Command | Flags |
|---|---|
| `hs paper search <QUERY>` | `-t/--type keywords\|title\|author\|doi\|subject`; `-a/--abstract`; `-d/--date ">=2025"`, `">2023 <2025"`, `">=2024-06"`; `-n/--max-results` (10); `--offset`; `-p/--provider all\|arxiv\|openalex\|semanticscholar\|europepmc\|crossref\|core`; `-s/--sort relevance\|date\|citations`; `--min-citations` |
| `hs paper get --doi <DOI>` | single paper |
| `hs paper download [QUERY]` | `--doi`; `-d/--date`; `-n` (10); `-c/--concurrency` (4); `-t/--type`; `-p/--provider` |
| `hs scribe` | subcommands `convert`, `watch-events`, `inbox`, `catalog-backfill`, `reconvert` (clear failure stamps, republish `papers.ingested`) |
| `hs distill` | subcommands `init index search status watch-events diagnose reconcile purge abstracts` |
| `hs distill search <QUERY>` | `-l/--limit` (10); `--year ">2020"`; `--topic`; `--server <URL>` |
| `hs openalex` | local OpenAlex DuckDB (bulk-load, query, FTS) |
Note CLI provider names differ from MCP (`semanticscholar`/`europepmc` vs `semantic_scholar`/`europmc`). CLI has `--topic` filter; MCP `distill_search` does not.

## 5. Storage / catalog locations (observed)
- Client config: `~/.home-still/config.yaml`; `home.project_dir: <local mount point>` (in the observed setup an NFS mount of S3-backed storage, bucket `home-still`, with NATS for events).
- Mount contents: `catalog/ corrupted/ markdown/ papers/ research/` plus `eth_ingest_*.jsonl`. Sharded by first 2 chars of stem: `papers/10/<stem>.pdf|.html`, `markdown/10/<stem>.md` (shard dirs `00,01,02,…`).
- Catalog paths in entries are relative (`markdown/10/<stem>.md`). Research outputs go under `<mount>/research/<topic>/`.
- Services (ports as observed): MCP `<host>:7445`; distill `<gpu-host>:7434`; scribe `<scribe-host>:7433` (healthy) and `<gpu-host>:7435` (unhealthy at time of check); Qdrant `localhost:6334` (on server side), collection `academic_papers` (+ `paper_abstracts`), embed model bge-m3.

## 6. Known operational hazards
Source: the `home-still-bulk-ingest` skill, if installed (read it before any bulk work).
- **30 s MCP timeout cancels `scribe_convert`** server-side (HTML ok, PDFs ~20%). Fix: per-server `timeout` in mcp.json (set to 900000 here, applies next session) or raw JSON-RPC (§1) with ~1800 s httpx timeout; open each session inside the concurrency semaphore.
- **Verify via catalog, not NFS**: the mount gives stale negative lookups. Use `catalog_read` (`conversion`/`embedding` blocks), `distill_exists`, `distill_search`. A "failed" client-side convert may have succeeded.
- **Right-size convert concurrency** to the VLM backend's real slots (`slots_total` can overstate); oversubscription → 502s, stalled conversions. No cancel RPC: killed clients leave orphan conversions; don't restart batches repeatedly.
- Server deadline `convert_deadline_secs` default 900 s (PDF failing at ~900 s with "Stream read error").
- `scribe_convert` bypasses the FIFO and writes catalog + publishes `scribe.completed`; `hs scribe convert --out` does neither (invisible to search).
- **Paywalled vs transient** download failures: `No open-access PDF found…` = paywalled (don't retry); timeouts/5xx/rate limits = transient. `"skipped": true` = already in storage. Detect anti-bot gate pages (Cloudflare, "Checking your browser", "Article Locator Bypass", OSF SPA shells) in first ~20 KB → unconvertible, not a convert failure.
- Don't leave services down; don't add a second scribe worker on a single-model GPU host.

## 7. Gotchas seen while probing
- `markdown_list` schema's `embedded` description says "catalog_list only".
- Duplicate author spellings in hits/catalog; `year` missing from `paper_search`.
- `paper_search` ~10–20 s per call; `distill_search` ~10–20 s on first call [observed total run times 20–40 s for 5 calls].
- `personal_*` tools expose private records; keep out of research workflows.
