# Mochi Cards API Reference

Source: <https://mochi.cards/docs/api/> (fetched 2026-06-08). Distilled for skill-building. Where the live docs contain errors, this doc gives the corrected version and flags it under **Known doc errors**.

---

## Overview

- **Base URL:** `https://app.mochi.cards/api/`
- **Style:** REST, JSON in / JSON out. Also supports `transit+json` (Clojure encoding) — **avoid it for a skill**; use plain JSON.
- **Auth:** HTTP Basic. API key as the **username**, empty password.
- **Gating:** The API is a **Mochi Pro** feature. Unauthorized/free accounts get `403 {"errors": ["Please upgrade to use this feature."]}`.
- **Secret handling:** Treat the API key as a secret (read from env, e.g. `MOCHI_API_KEY`; never hardcode).

```bash
curl https://app.mochi.cards/api/decks -u $MOCHI_API_KEY:
# trailing colon stops curl prompting for a password
```

---

## Critical gotchas

These are the things that silently break a naive client:

1. **Keys are kebab-case, booleans/predicates end in `?`.** `deck-id`, `template-id`, `parent-id`, `archived?`, `review-reverse?`, `show-sides?`, `sort-by-direction`, `new?`, `trashed?`. (Backend is Clojure; these are EDN keywords.)
2. **In JSON, "keyword" params are sent as plain strings.** The docs type many fields as `keyword` (e.g. `deck-id`, `template-id`, enum values). In JSON you just send the string: `"deck-id": "btmZUXWM"`. The `~:`-prefixed forms in the docs are the *transit* encoding — ignore them unless you opt into transit.
3. **One concurrent request per account.** The concurrency limiter rejects parallel calls; bursts return `429`. **Serialize everything** and add retry/backoff. No parallelism in a skill.
4. **Two-sided cards split on `---`.** A plain card's front/back are separated by a markdown horizontal rule. The built-in "Simple flashcard" template is literally `# << Front >>\n---\n<< Back >>`.
5. **Attachments are a two-step, name-matched dance.** Reference `![](@media/<filename>)` in the card `content`, then upload the bytes to `POST /cards/:id/attachments/<filename>` as multipart. The filename in the URL must match the `@media/` reference.
6. **`update` is `POST`, not `PUT`/`PATCH`.** All mutations except delete are POST.
7. **Pagination is cursor-based and lossy-looking.** Responses give `docs` + `bookmark`; a returned bookmark does **not** guarantee more pages. Stop when `docs` is short/empty.

---

## Conventions

### Encoding
Send `Content-Type: application/json` and `Accept: application/json`. (Transit: `application/transit+json`, with `~:key`, `~#set`, `~#dt`, `~t<ms>` tagged values — not recommended.)

### Pagination
List endpoints return:
```json
{ "bookmark": "g1AAAAB...", "docs": [ { ... }, ... ] }
```
Pass `?bookmark=<value>` to get the next page. Loop until empty/short `docs`.

### Errors
- `2xx` success, `4xx` client error, `5xx` server error (rare).
- Validation errors return a per-field map:
```json
422 { "errors": { "content": ":content field cannot be nil." } }
```
- General errors return an array: `500 { "errors": ["Something went wrong!"] }`.
- `403` → not authorized / not Pro.

### Rate limits
- `429` on bursts.
- **Concurrency limiter: 1 active request per account.** Wait for each response before the next request.

---

## Cards

```
GET    /cards       List cards (paginated)
POST   /cards       Create a card
GET    /cards/:id   Retrieve a card
POST   /cards/:id   Update a card
DELETE /cards/:id   Delete a card (permanent, incl. attachments)
POST   /cards/:id/attachments/:filename     Add attachment (multipart)
DELETE /cards/:id/attachments/:filename     Delete attachment
```

### Create / update params
| Field | Type | Req | Notes |
|---|---|---|---|
| `content` | string | ✓ (create) | Markdown. Front/back split on `---`. Can be blank if `fields` is set. |
| `deck-id` | string | ✓ (create) | Target deck. |
| `template-id` | string | – | Template to render the card. |
| `archived?` | boolean | – | Archived cards aren't "new" or due. |
| `review-reverse?` | boolean | – | Also review bottom-to-top. |
| `pos` | string | – | Lexicographic sort position (e.g. insert `"6V"` between `"6"` and `"7"`). |
| `manual-tags` | array of strings | – | Tags without leading `#`. **Overwrites** existing on update. |
| `fields` | map | – | `field-id → {"id": <same id>, "value": <string>}`. For template cards. |
| `trashed?` | ISO 8601 timestamp | – | **Update only.** Soft-delete (set to current time). |

### Returned card shape
```json
{
  "id": "QQJ8ssvL",
  "content": "New card from API.",
  "name": null,
  "deck-id": "btmZUXWM",
  "template-id": null,
  "pos": "00F",
  "tags": [],
  "references": [],
  "reviews": [],
  "archived?": true,
  "new?": false,
  "created-at": { "date": "2021-09-10T01:29:49.879Z" },
  "updated-at": { "date": "2021-09-11T14:23:53.250Z" }
}
```
Note timestamps come back wrapped as `{ "date": "<ISO>" }`.

### List cards
- `deck-id` *optional* — filter to one deck.
- `limit` *optional* — 1–100, **default 10**.
- `bookmark` *optional* — pagination cursor.

### Attachment upload (multipart)
```bash
curl -X POST \
  https://app.mochi.cards/api/cards/<card-id>/attachments/<filename> \
  -u $MOCHI_API_KEY: \
  -H "Content-Type: multipart/form-data" \
  -F file="@/path/to/<filename>"
```

---

## Decks

```
GET    /decks       List decks (paginated)
POST   /decks       Create a deck
GET    /decks/:id   Retrieve a deck
POST   /decks/:id   Update a deck
DELETE /decks/:id   Delete a deck (permanent)
```

### Create / update params
| Field | Type | Req | Notes |
|---|---|---|---|
| `name` | string | ✓ (create) | Deck name. |
| `parent-id` | string | – | Nest under another deck. |
| `sort` | integer | – | Numeric sort among decks. |
| `archived?` | boolean | – | Archived → cards not new/due. |
| `trashed?` | ISO 8601 timestamp | – | Soft-delete; cascades to children. |
| `sort-by` | string | – | One of `none`, `lexicographically`, `created-at`, `updated-at`, `retention-rate-asc`, `interval-length`. |
| `cards-view` | string | – | One of `list`, `grid`, `note`, `column`. |
| `show-sides?` | boolean | – | Show all sides on deck page. |
| `sort-by-direction` | boolean | – | Reverse sort order. |
| `review-reverse?` | boolean | – | Reveal sides bottom-to-top too. |

List decks takes only `bookmark` (no documented `limit`).

---

## Templates

```
GET  /templates       List templates (paginated)
POST /templates       Create a template
GET  /templates/:id   Retrieve a template
```
No documented update/delete for templates.

### Create params
| Field | Type | Req | Notes |
|---|---|---|---|
| `name` | string | ✓ | 1–64 chars. |
| `content` | string | ✓ | Markdown with `<< Field name >>` placeholders. |
| `pos` | string | – | Lexicographic sort. |
| `fields` | map | ✓ | `field-id → field def` (below). |
| `style` | map | – | `text-alignment`: `left`/`center`/`right`. |
| `options` | map | – | `show-sides-separately?`: boolean. |

**Field definition:** `id` (req, = key), `name`, `type`, `pos`, `content` (default/instructions), `options` (e.g. `multi-line?`, `hide-term`, `ai-task`).

**Field `type` values:** `text`, `boolean`, `number`, `draw`, `ai`, `speech`, `image`, `translate`, `transcription`, `dictionary`, `pinyin`, `furigana`.

To populate a template card, set the card's `fields` map keyed by these field IDs.

---

## Due

```
GET /due           Cards due on a date (default: today)
GET /due/:deck-id   Same, scoped to a deck
```
- `date` *optional* — ISO 8601 timestamp; omitted = today.
- Response is `{ "cards": [ ... ] }` (a plain `cards` array — **not** the `docs`/`bookmark` shape). Each card includes its `reviews` history (`date`, `due`, `remembered?`).

---

## Known doc errors (in the live docs as of 2026-06-08)

- **Deck create/update examples** show `http://localhost:8090/api/decks/` and `https://app.mochi.card/api/decks/` (leaked dev URL / missing `s`). Real base is `https://app.mochi.cards/api/`.
- **"Get all due cards"** section body is copy-pasted from Templates (says `POST /templates`, describes templates). The real endpoint is `GET /due` / `GET /due/:deck-id` with the `date` param and a `{"cards": [...]}` response.
- **`sort-by` enum** lists both `:lexigraphically` (typo) and `:lexicographically`. Use `lexicographically`.
- **Python sample** has typos (`imoprt requests`, missing `HTTPBasicAuth` import); **fetch sample** has `body formData` (missing colon). Don't copy these verbatim.
- **Delete a deck** notes "TODO: Cards and decks in the deleted deck are not deleted" — cascade behavior on hard delete is ambiguous; prefer soft-delete via `trashed?`.

---

## Minimal "create a basic flashcard" recipe (JSON)

```bash
curl -X POST https://app.mochi.cards/api/cards/ \
  -u $MOCHI_API_KEY: \
  -H "Content-Type: application/json" \
  -d '{
    "content": "What is the capital of France?\n---\nParis",
    "deck-id": "btmZUXWM"
  }'
```
