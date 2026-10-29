# Agent guide

Read `README.md` for structure and commands. Knowledge (`knowledge/`) is the source of truth; `knowledge/cities/`
and `knowledge/reports/` are generated (`pnpm etl`, `pnpm validate`) — never edit them by hand.

## External services (mandatory — applies to every agent and subagent)

Rules from `knowledge/decisions/external-access-policy.md`. Read it before touching any remote service.

1. Get data only through routes the provider documents for data access: file downloads, documented APIs,
   public buckets, official releases. Never script a web UI (Shiny/websocket handlers, form posts, hidden
   endpoints, headless browsers against a provider's site) to extract data.
2. Read the provider's terms / rate limits first. Use `soulcity_etl.common.fetch()` (identifying User-Agent,
   retries with backoff) and send requests sequentially unless the docs allow more.
3. Stop at the first sign of distress: 429, 5xx, timeouts, "server too busy", or an error you caused (e.g. a
   crashed app session). Do not retry the same thing. Record what happened in the source's `etl/notes/` and
   report it to the user.
4. If the only remaining route is undocumented, stop and ask the user. Don't decide alone.
5. Delegating work to a subagent? Copy these rules into its brief (`etl/notes/BRIEF.md` already has them).

## Data rules

No hand-typed numbers, no placeholder values, missing stays missing with a reason. Details: `etl/notes/BRIEF.md`.
