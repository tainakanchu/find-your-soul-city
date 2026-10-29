# National time-use / sleep-timing data: survey for a "night owl vs early bird" reference

Date: 2026-10-29. Research only. Follows `knowledge/decisions/external-access-policy.md`: only documented
routes were used (two Eurostat dissemination API calls, sequential, no errors). Web pages were read with a fetch tool.
Where a claim comes from a search snippet and not from the primary page, it is marked UNVERIFIED.

Our scope: 130 cities, **83 distinct countries** (not ~60): AE AO AR AT AU AZ BD BR CA CD CH CI CL CN CO CR CU CZ DE
DK DO DZ EC EG ES ET FI FR GB GE GH GR HU ID IE IL IN IR IS IT JO JP KE KH KR KZ LB LK MA MM MN MX MY MZ NG NL NO NP NZ
PA PE PH PK PL PT QA RW SA SE SG SN TH TN TR TW TZ UG US UY UZ VN ZA ZM.

## Verdict in one line

Only one source is openly licensed, documented-API, and measures timing: **Eurostat HETUS** (participation rate by
10-minute time of day). It covers **13 of 83 countries (19 of 130 cities)**, all European. Everything global is either
duration-only (OECD, UN), sample-biased (Walch 2016), or has no confirmed licence/access (Sleep Cycle, MTUS).
A worldwide-comparable "national chronotype" metric does **not** exist in open form. A Europe-only reference is defensible.

## 1. Eurostat HETUS (best candidate) - timing, open

- Tables (Eurobase, API): `tus_00startime` (2000 and 2010 waves) and `tus_20startime` (2020 wave).
  Title: "Participation rate in the main activity (wide groups) by sex and time of the day".
  - API (documented JSON-stat): `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tus_00startime?format=JSON&lang=EN`
    and same with `tus_20startime`. Both returned HTTP 200 on the first try (0.6 MB and 1.6 MB). DOIs: 10.2908/TUS_20STARTIME.
  - Dimensions: sex (T/M/F) x `startime` (144 ten-minute slots from 04:00, plus TOTAL) x activity group x geo x year.
    Activity groups include "Personal care except eating" (this contains sleep), eating, work/study, household, leisure, TV, commute.
    Unit: PTP_RT, percent of people doing that main activity in that slot on the diary day.
  - Variable type: genuine time-of-day timing, not durations. There is no explicit "bedtime" or "wake time"; sleep is only
    inside "personal care except eating". Proxy: share in personal care at 23:00 and at 06:00, or the clock time at which
    the share crosses 50% (a derived "sleep midpoint"-like measure). Dinner time can be read from the "Eating" curve.
    Work start can be read from "Employment and study".
- Years / countries (verified against API dimension lists; blank cells are missing, not zero):
  - 2000 wave (fieldwork 1998-2006): BE BG DE EE ES FR IT LV LT PL SI FI NO UK (EL, LU, HU, NL, RO, RS, TR are empty in 2000).
  - 2010 wave (2008-2015): BE DE EE EL ES FR IT LU HU NL PL RO FI NO UK RS TR (BG, LV, LT, SI empty in 2010).
  - 2020 wave (tus_20startime): BG DE EE HR HU NL AT PL FI NO RS.
  - Overlap with our list (13 countries, 19 cities): **AT (2020 only), DE, ES, FR, GB (Eurostat code UK), GR (Eurostat code EL),
    HU, IT, NL, NO, PL, FI, TR.** Not covered: CH, CZ, DK, IE, IS, PT, SE (absent from these startime tables), and all non-European countries.
  - Best-available year per country: 2020 for AT DE HU NL PL FI NO; 2010 for ES FR GB GR IT TR. Mixed vintages.
- Sample values (total sex, personal care except eating, % in that activity; shows the signal is real):

  | geo-year | 04:00 | 06:00 | 23:00 | 00:00 |
  |---|---|---|---|---|
  | ES 2010 | 97.5 | 96.0 | 32.1 | 68.6 |
  | EL 2010 | 99.2 | 94.9 | 35.5 | 71.1 |
  | NO 2010 | 97.4 | 91.2 | 46.9 | 77.2 |
  | NL 2020 | 98.8 | 94.4 | 59.6 | 82.9 |
  | DE 2020 | 97.7 | 86.0 | 68.2 | 88.4 |
  | PL 2020 | 98.1 | 83.7 | 81.4 | 94.3 |
  | HU 2020 | 95.2 | 74.5 | 79.6 | 92.3 |

  (Spain/Greece up late, Poland/Hungary asleep by 23:00. Large and plausible between-country spread.)
- Licence: the metadata page (tus_00_esms) states no licence. Eurostat copyright notice
  (`https://ec.europa.eu/eurostat/help/copyright-notice`): search results say Eurostat editorial content is CC BY 4.0 and
  reuse policy is Commission Decision 2011/833/EU (reuse allowed with source acknowledgement), with an exception for data
  "identified as belonging to sources other than Eurostat" (non-commercial only) - UNVERIFIED on the primary page, re-read before shipping.
  Per-dataset flags in the JSON-stat extension were not licence-bearing. Verdict: **reusable with attribution (CC BY 4.0 / Decision 2011/833/EU)**;
  needs an attribution string "Source: Eurostat (tus_00startime / tus_20startime)".
- Comparability issues (from the Eurostat ESMS): "largely comparable" by harmonised guidelines but sampling design/size differ;
  weights differ by country; Austria used 15-min slots (2020); Germany quota sampling; fieldwork spans 2008-2015 in the 2010 wave,
  so years and DST/season differ; 10-minute diaries of people aged 20-74 (tables); diary day mixes weekday/weekend; slots are local clock time
  (not solar time). Estimates with <25 observations are flagged. Cross-wave comparability is weak.
  The "personal care" group is not only sleep (it also holds washing, dressing, resting), so levels at 23:00 overstate
  sleep but the cross-country ranking is expected to hold.

## 2. OECD Time Use Database - durations only

- URL: `https://www.oecd.org/en/data/datasets/time-use-database.html` (WebFetch returned 403; facts below are from search snippets, UNVERIFIED).
- Variables: minutes per day by activity (sleep, paid work, leisure, ...) for ages 15-64 in most countries. No time-of-day. About 30 OECD countries (+ some partners); includes the 2024 additions AT JP US. Normalised to 1440 minutes.
- Licence: OECD terms changed 1 July 2024 so that OECD data and publications are in principle CC BY 4.0 (NDL record), with third-party exceptions. UNVERIFIED on primary page.
- Verdict: **not usable for night owl vs early bird** (no timing). Sleep duration only.

## 3. MTUS (Multinational Time Use Study, Oxford/UCL)

- `https://www.timeuse.org/mtus`: 30 countries, 55 years, more than 1 million diary days, 100+ surveys. Free account/registration required to download; a "Restricted Level" is mentioned. No licence text on the page. Harmonised diary episodes do include clock times in the underlying data, but the page does not say so.
- Verdict: **access gated by registration; terms (redistribution) not confirmed** - treat as not open. Would require asking the user and reading its user agreement; no scripted download.

## 4. US ATUS (BLS)

- `https://www.bls.gov/tus/`; 2025 data; US only. Public data files and tables; hourly "percent engaged in sleeping" exists in the microdata (not confirmed on the tables page). BLS site is US-government content (public domain by default - UNVERIFIED on the BLS copyright page). Covers US only (13 of our 130 cities).
- Useful only as a per-country add-on, not cross-national.

## 5. Japan Social Life Basic Survey (社会生活基本調査, e-Stat)

- Source: Statistics Bureau of Japan, e-Stat (documented API exists; app ID registration needed). Survey every 5 years (2021 latest). Sleep is a defined activity; time-slot activity rates (15-minute slots) and weekday bedtime/wake times are published (FAQ 23E-Q01; e-Stat dbview tables such as 0003066851/66853 for 2011).
- Licence: 政府標準利用規約 (compatible with CC BY 4.0); I found no confirmation in search results - UNVERIFIED, read the e-Stat terms before use.
- Japan only (4 of our cities). Different survey design from HETUS (different age range, slots), so not harmonised with it.
- Similar single-country sources (Korea KOSTAT, ABS Australia, ONS UK, Statistics Canada GSS, China, India NSO Time Use Survey 2019, etc.) exist but are not harmonised and were not checked.

## 6. UN Statistics Division / Global Gender Statistics / ILO

- Time-use collections are durations (paid work, unpaid care) and not timing. Not useful. Not individually checked.

## 7. Walch, Cochran & Forger 2016 (Science Advances 2:e1501705, ENTRAIN app)

- Open access, **CC BY-NC** (PMC4928979 page, quoted: "Creative Commons Attribution-NonCommercial license"). Data availability: "in the paper and/or Supplementary Materials; additional data may be requested from the authors".
- Content: self-reported typical bedtime and wake time (rounded to the hour) from 8,070 users (5,450 after cleaning). Country values appear only in figures (Fig 1E, Fig 3) for the **top 20 countries**; supplementary tables S1-S8 are regression outputs, not country tables. US 45%, Australia 9%, Canada 5%.
- Verdict: **not usable**. Non-commercial licence, no numeric table, self-selected app users, ~20 countries, hour rounding, heavy US weighting. Extracting values from a figure would also be a hand-typed number.

## 8. Wearable / app companies

- **Sleep Cycle** "open dataset API" at `https://sandman.sleepcycle.com/data` (cited in arXiv 2509.03358): country average Sleep Quality, Sleep Duration, Wakeup Time, Bedtime for 61 countries. This is the only global country-level bedtime/wake-time table I found. **I could not reach the host**: the session proxy returned 502 and DNS did not resolve (host not in the allowed network list). I did not retry or work around it. No licence text found; the arXiv paper only says "publicly available". Triage Method's atlas says underlying Sleep Cycle data is subject to Sleep Cycle's own licence. Verdict: **licence unknown; needs the host allowed in the session network settings and the terms read; user decision**. Also biased: smartphone-app users who place the phone in bed, self-selected, different by country.
- Oura chronotype blog (shares only, no dataset), Triage Method "Global Sleep Atlas" (CC BY 4.0 on the compilation, JSON download, but its sleep data are durations from OECD and Sleep Cycle; underlying licences still apply), Bloc Blinds/Dreams press pieces: secondary, not suitable as sources.
- UBC Shi & Heine chronotype survey: 20 countries, N=5,128, licence CC BY-NC-ND 4.0 (search snippet) - not usable.
- Sci Rep 2023 s41598-023-36762-5 (wearable-based paper): paywalled/redirect from this session, not read.

## Recommendation

1. If we want this dimension, derive it from **Eurostat HETUS** and label it clearly "national time-use reference, Europe only",
   applied to AT DE ES FR GB GR HU IT NL NO PL FI TR (19 cities). All other cities: missing, reason "no open cross-national timing data
   for this country". Do not fill the gaps with modelled or app data.
2. Suggested definition (derived, no typed numbers): per country, from the latest wave available, take the "Personal care except eating"
   participation rate, total sex, at the 23:00-23:09 slot (share still not "in personal care" is not a clean measure; better to report the
   share in personal care at 23:00 as "asleep-ish at 23:00" and at 06:00 for early wake), plus the time at which "Eating" peaks in the evening as
   dinner time. Document the mixed vintages (2010 vs 2020) and that Austria uses 15-minute slots.
3. Honest caveat for the quiz: values describe adult national behaviour in local clock time, not individual chronotype; they mostly reflect
   culture and work schedules (e.g. Spain, Greece up late) and are not a preference.
4. Optional later additions, each needing a user decision: Sleep Cycle (licence + network allowlist), MTUS (registration/terms),
   single-country official data for JP (e-Stat) and US (ATUS) once terms are read. These would break the "one harmonised source" property,
   so they should be shown as separate, labelled fields or not at all.
5. If the dimension must be global, a defensible national-reference metric does **not** exist from open sources; drop it or use a
   city-level proxy that we already hold (for example the daylight/latitude features in `etl/soulcity_etl/daylight.py`).
   A user-facing quiz question (own preference) is a cleaner source than national data.

## Process log

- 2 Eurostat API calls (tus_20startime, tus_00startime), sequential, 3 s apart, custom User-Agent, both HTTP 200. Raw JSON kept only in the scratchpad, not in the repo.
- sandman.sleepcycle.com: connection rejected by proxy (502) / ENOTFOUND. Stopped, not retried.
- science.org, oecd.org, triagemethod.com, nature.com returned 403/530/redirect to login; no workaround attempted.
