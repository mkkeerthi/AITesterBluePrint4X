"""Settings come from .env; sources come from sources.yaml."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")


def _env(key: str, default: str) -> str:
    return os.getenv(key, default).strip()


def _int(key: str, default: int) -> int:
    try:
        return int(_env(key, str(default)))
    except ValueError:
        return default


def _bool(key: str, default: bool) -> bool:
    return _env(key, "true" if default else "false").lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Source:
    id: str
    label: str
    path: Path
    kind: str
    description: str = ""
    phase: int = 1

    @property
    def rel_path(self) -> str:
        return self.path.relative_to(ROOT).as_posix()


@dataclass(frozen=True)
class Settings:
    qdrant_url: str = field(default_factory=lambda: _env("QDRANT_URL", "http://localhost:6333"))
    qdrant_api_key: str = field(default_factory=lambda: _env("QDRANT_API_KEY", ""))
    collection: str = field(default_factory=lambda: _env("QDRANT_COLLECTION", "qabuddy"))

    ollama_url: str = field(default_factory=lambda: _env("OLLAMA_URL", "http://localhost:11434"))
    embed_model: str = field(default_factory=lambda: _env("EMBED_MODEL", "qwen3-embedding:0.6b"))
    embed_dim: int = field(default_factory=lambda: _int("EMBED_DIM", 1024))

    rerank_enabled: bool = field(default_factory=lambda: _bool("RERANK_ENABLED", True))
    rerank_model: str = field(default_factory=lambda: _env("RERANK_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2"))

    llm_provider: str = field(default_factory=lambda: _env("LLM_PROVIDER", "groq"))
    llm_model: str = field(default_factory=lambda: _env("LLM_MODEL", "openai/gpt-oss-120b"))
    groq_api_key: str = field(default_factory=lambda: _env("GROQ_API_KEY", ""))
    openai_api_key: str = field(default_factory=lambda: _env("OPENAI_API_KEY", ""))
    openai_base_url: str = field(default_factory=lambda: _env("OPENAI_BASE_URL", "https://api.openai.com/v1"))

    prefetch_k: int = field(default_factory=lambda: _int("PREFETCH_K", 40))
    rerank_candidates: int = field(default_factory=lambda: _int("RERANK_CANDIDATES", 24))
    final_k: int = field(default_factory=lambda: _int("FINAL_K", 6))
    context_tokens: int = field(default_factory=lambda: _int("CONTEXT_TOKENS", 3500))

    jira_base_url: str = field(default_factory=lambda: _env("JIRA_BASE_URL", "").rstrip("/"))
    jira_email: str = field(default_factory=lambda: _env("JIRA_EMAIL", ""))
    jira_api_token: str = field(default_factory=lambda: _env("JIRA_API_TOKEN", ""))
    jira_jql: str = field(default_factory=lambda: _env("JIRA_JQL", ""))

    port: int = field(default_factory=lambda: _int("PORT", 8300))

    index_dir: Path = ROOT / ".index"

    @property
    def jira_configured(self) -> bool:
        placeholder = "your-site" in self.jira_base_url
        return bool(self.jira_base_url and self.jira_email and self.jira_api_token and not placeholder)


@lru_cache
def settings() -> Settings:
    return Settings()


@lru_cache
def sources() -> tuple[Source, ...]:
    raw = yaml.safe_load((ROOT / "sources.yaml").read_text())
    out = []
    for s in raw["sources"]:
        out.append(
            Source(
                id=s["id"],
                label=s["label"],
                path=(ROOT / s["path"]).resolve(),
                kind=s["kind"],
                description=s.get("description", ""),
                phase=int(s.get("phase", 1)),
            )
        )
    return tuple(out)


def source_by_id(source_id: str) -> Source | None:
    return next((s for s in sources() if s.id == source_id), None)


@lru_cache
def glossary() -> dict[str, list[str]]:
    path = ROOT / "glossary.yaml"
    if not path.exists():
        return {}
    raw = yaml.safe_load(path.read_text()) or {}
    return {k.lower(): [v.lower() for v in vals] for k, vals in (raw.get("expansions") or {}).items()}
