"""Shared ETL plumbing: paths, cached downloads with a hash manifest, interim output contract.

Rules every source module follows:
- Raw inputs are fetched by URL into `.cache/raw/` (gitignored). The URL, byte size, sha256 and
  retrieval time are recorded in `data/provenance/downloads.json` (committed), so a rerun can
  tell whether upstream changed.
- No value is typed in by hand. Every number in `data/interim/<source_id>.json` is computed from
  a recorded input by code in this package.
- A value that cannot be computed is reported under `missing` with a reason, never filled in.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import math
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import requests

REPO = Path(__file__).resolve().parents[2]
CACHE = REPO / ".cache" / "raw"
DATA = REPO / "data"
INTERIM = DATA / "interim"
PROVENANCE = DATA / "provenance"
REFERENCE = DATA / "reference"
DOWNLOADS = PROVENANCE / "downloads.json"

QUALITIES = {"observed", "estimated", "imputed", "missing"}
# Identify ourselves to data providers (knowledge/decisions/external-access-policy.md).
USER_AGENT = "soul-city-etl/0.1 (+https://github.com/tainakanchu/find-your-soul-city)"


def now_iso() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_manifest() -> dict[str, Any]:
    return json.loads(DOWNLOADS.read_text()) if DOWNLOADS.exists() else {}


def _save_manifest(m: dict[str, Any]) -> None:
    DOWNLOADS.parent.mkdir(parents=True, exist_ok=True)
    DOWNLOADS.write_text(json.dumps(dict(sorted(m.items())), indent=2, ensure_ascii=False) + "\n")


def fetch(url: str, dest: Path, *, refresh: bool = False, record: bool = True, retries: int = 4,
          timeout: float = 120, **kwargs: Any) -> Path:
    """Download `url` to `dest` (under CACHE) unless already cached; record it in the manifest.

    `record=False` is for bulk chunk reads (e.g. thousands of zarr chunks) where the module records
    one manifest entry for the dataset itself instead.
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    if refresh or not dest.exists():
        tmp = dest.with_suffix(dest.suffix + ".part")
        headers = {"User-Agent": USER_AGENT, **kwargs.pop("headers", {})}
        for attempt in range(retries + 1):
            try:
                with requests.get(url, stream=True, timeout=timeout, headers=headers, **kwargs) as r:
                    r.raise_for_status()
                    with tmp.open("wb") as f:
                        for chunk in r.iter_content(1 << 20):
                            f.write(chunk)
                os.replace(tmp, dest)
                break
            except requests.HTTPError as e:
                # Rate limiting / server distress: stop instead of hammering the provider.
                if e.response is not None and e.response.status_code in (429, 503):
                    raise
                if attempt == retries:
                    raise
                time.sleep(2 ** (attempt + 1))
                continue
            except (requests.RequestException, OSError):
                if attempt == retries:
                    raise
                time.sleep(2 ** (attempt + 1))
        fresh = True
    else:
        fresh = False
    if record:
        m = _load_manifest()
        key = url
        digest = sha256_file(dest)
        prev = m.get(key)
        if fresh or prev is None or prev.get("sha256") != digest:
            m[key] = {
                "path": str(dest.relative_to(REPO)),
                "bytes": dest.stat().st_size,
                "sha256": digest,
                "retrieved_at": now_iso(),
                **({"previous_sha256": prev["sha256"]} if prev and prev.get("sha256") != digest else {}),
            }
            _save_manifest(m)
    return dest


def record_dataset(key: str, **info: Any) -> None:
    """Manifest entry for an input that is not a single file (e.g. a remote zarr store or an API)."""
    m = _load_manifest()
    m[key] = {**info, "retrieved_at": now_iso()}
    _save_manifest(m)


@dataclass
class Interim:
    """Per-source output. One file per source: data/interim/<source_id>.json.

    values[metric_key][city_id] = {"value": float, "quality": "observed"|"estimated"|"imputed",
                                   "year": int | "YYYY-YYYY", "detail": {...optional diagnostics}}
    missing[metric_key][city_id] = "reason the value could not be computed"
    """

    source_id: str
    inputs: list[str] = field(default_factory=list)  # keys into downloads.json
    values: dict[str, dict[str, dict[str, Any]]] = field(default_factory=dict)
    missing: dict[str, dict[str, str]] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)

    def put(self, metric: str, city_id: str, value: float, *, quality: str, year: int | str,
            detail: dict[str, Any] | None = None) -> None:
        if quality not in QUALITIES - {"missing"}:
            raise ValueError(f"bad quality {quality}")
        if value is None or math.isnan(value):  # None / NaN must go through miss()
            raise ValueError(f"{metric}/{city_id}: use miss() for absent values")
        entry: dict[str, Any] = {"value": float(value), "quality": quality, "year": year}
        if detail:
            entry["detail"] = detail
        self.values.setdefault(metric, {})[city_id] = entry

    def miss(self, metric: str, city_id: str, reason: str) -> None:
        self.missing.setdefault(metric, {})[city_id] = reason

    def write(self) -> Path:
        INTERIM.mkdir(parents=True, exist_ok=True)
        path = INTERIM / f"{self.source_id}.json"
        body = {
            "source_id": self.source_id,
            "generated_at": now_iso(),
            "inputs": self.inputs,
            "notes": self.notes,
            "values": {k: dict(sorted(v.items())) for k, v in sorted(self.values.items())},
            "missing": {k: dict(sorted(v.items())) for k, v in sorted(self.missing.items())},
        }
        path.write_text(json.dumps(body, indent=2, ensure_ascii=False) + "\n")
        return path
