---
name: convodump
description: Transcribe audio or video files with speaker diarization, time codes and word timestamps, and extract media metadata, through the ConvoDump server. Use whenever asked to transcribe, diarize, caption, time-code or pull metadata from a media file (m4a, mp3, wav, mp4, mov, …).
---

# ConvoDump: media file → metadata + diarized, time-coded transcript

ConvoDump turns one media file into one JSON document. A server does the work; this host only
uploads the file with the `convodump` client. Never run a speech model yourself.

Always call the client by its absolute path: `~/.local/bin/convodump`.

## Procedure

1. Check the server: `~/.local/bin/convodump server status`
   (prints `server <url> ok`, the engine, the models and `busy <bool>`).
2. Transcribe: `~/.local/bin/convodump media run <file> --out-dir <dir>`
   * `<dir>` is the directory the user names; if they name none, the file's own directory.
   * It writes `<dir>/<file stem>.convodump.json` and prints that path. Several files may be
     given at once. An existing output is refused unless `--force`.
   * `--language <code>` only when the user states the language; the default is auto-detect.
   * A long file takes minutes (roughly one tenth of its duration); the call blocks until done.
3. Read the JSON with `jq` (recipes below) and answer from it. Do not paste the whole file into
   the conversation: quote the parts the user asked for.

Without `--out-dir`, `convodump media run <file>` prints readable lines
(`[00:00:05.000 → 00:00:05.900] S2: text`); `--output json` prints the document on one line.

## Output schema (`schema_version` 2)

* `source`: `file_name` (basename only), `size_bytes`, `sha256`.
* `media`: ffprobe metadata: `format_name`, `format_long_name`, `duration_s`, `size_bytes`,
  `bit_rate`, `tags` (title, artist, creation time, … as the file carries them), `streams[]`
  and `chapters[]` (raw ffprobe), `transcribed_stream_index` (the audio stream that was used).
* `engine`: `name`, `version`, `asr_model`, `diarization_model`, `diarization_preset`,
  `recognition_mode` (`offline-chunked` when a long file was split for full-attention
  recognition, `offline` when one pass covered it), `language_requested`.
* `transcript`:
  * `text`, `languages[]`, `duration_s`, `confidence`, `unattributed_word_count`
  * `speakers[]`: `id` (`S1`, `S2`, …), `word_count`, `segment_count`, `talk_time_s`, `first_start_s`
  * `segments[]`: `index`, `speaker` (null if unattributed), `start_s`, `end_s`, `start_tc`,
    `end_tc` (`HH:MM:SS.mmm`), `text`, `first_word`, `last_word`
  * `words[]`: `index`, `text`, `start_s`, `end_s`, `confidence`, `speaker`
* `timing`: `probe_ms`, `decode_ms`, `diarize_ms` (the separate diarization pass), `engine_ms`,
  `total_ms`.

A segment is one diarizer turn; each word carries the speaker of the turn it overlaps longest.
When the diarizer finds nothing, segments fall back to grouping words by speaker change or a pause
over 2 s, and `unattributed_word_count` shows how much went unlabelled.

## jq recipes

```sh
# speaker turns
jq -r '.transcript.segments[]|"[\(.start_tc)] \(.speaker): \(.text)"' out.convodump.json
# who talked how much
jq '.transcript.speakers' out.convodump.json
# media metadata
jq '.media|{format_name,duration_s,tags}' out.convodump.json
# words in a time window (seconds)
jq '[.transcript.words[]|select(.start_s>=60 and .end_s<=120)|.text]|join(" ")' out.convodump.json
```

## Exit codes and errors

| Exit | Meaning | What to do |
| --- | --- | --- |
| 0 | success | read the output |
| 1 | the server rejected the file, or a local file problem | read `error.code` in the message: `no_audio_stream`, `unreadable_media`, `engine_failed`, `too_large`, or `already exists` (use `--force` only if the user wants it overwritten) |
| 2 | this host's convodump config or token is missing or wrong | report it to the user; do not edit the token yourself |
| 3 | the server is unreachable | report it to the user. Do not switch servers, edit the config, or run the model locally |
| 4 | some files succeeded and some failed | report which failed and why |

## Rules

* Speaker ids `S1…` are anonymous labels. Never attach a name to them from what is said in the
  content; a name comes from the user.
* The recordings and their outputs are private. Never write them into a git repository, and
  never paste a transcript into an issue, a commit message or a log.
* The server keeps nothing after the job; the output file you write is the only copy.
