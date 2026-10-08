"""CLI: python -m qabuddy <command>

    ingest [--full] [--source ID ...]   build or update the index
    ask "question" [--mode rca]          answer with citations
    search "question"                    retrieval only, with the trace
    sync-jira [--jql "..."]              pull tickets matching a JQL
    eval                                 retrieval hit-rate on eval/golden.yaml
    export-demo                          write ui/public/demo.json for the hosted demo
    serve                                start the API + UI on $PORT
"""

from __future__ import annotations

import argparse
import json
import sys


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="qabuddy")
    sub = p.add_subparsers(dest="cmd", required=True)
    pi = sub.add_parser("ingest")
    pi.add_argument("--full", action="store_true")
    pi.add_argument("--source", action="append")
    pi.add_argument("--force", action="store_true", help="re-chunk and re-embed even unchanged files")
    pa = sub.add_parser("ask")
    pa.add_argument("question")
    pa.add_argument("--mode", default="ask")
    ps = sub.add_parser("search")
    ps.add_argument("question")
    ps.add_argument("--source", action="append")
    pj = sub.add_parser("sync-jira")
    pj.add_argument("--jql")
    sub.add_parser("eval")
    pe = sub.add_parser("export-demo")
    pe.add_argument("--only", action="append", help="re-record only questions containing this text")
    sub.add_parser("serve")
    a = p.parse_args(argv)

    if a.cmd == "ingest":
        from .ingest import ingest

        last = {"stage": None}

        def progress(stage, done, total):
            if stage != last["stage"] or done == total or done % 50 == 0:
                print(f"  {stage:10s} {done}/{total}", flush=True)
                last["stage"] = stage

        print(json.dumps(ingest(a.source, a.full, progress, a.force), indent=1))
    elif a.cmd == "ask":
        from .answer import answer

        out = answer(a.question, a.mode)
        print(out["answer"])
        print("\nSources:")
        for s in out["retrieval"]["sources"]:
            print(f"  [{s['n']}] {s['title']}  ({s['file_path']} · {s['locator']})")
        print("\ncitations:", out.get("citations"), "| usage:", out.get("usage"), "| timings:", out.get("timings"))
    elif a.cmd == "search":
        from .retrieve import retrieve

        r = retrieve(a.question, source_ids=a.source)
        for s in r.public()["sources"]:
            sc = s["scores"]
            print(f"  [{s['n']}] {s['source_id']:13s} rerank={sc['rerank']} dense#{sc['dense_rank']} bm25#{sc['bm25_rank']} exact={sc['exact']}  {s['title'][:70]}")
        print("timings:", r.timings, "| low_confidence:", r.low_confidence)
    elif a.cmd == "sync-jira":
        from .jira_sync import sync

        print(json.dumps(sync(a.jql), indent=1))
    elif a.cmd == "eval":
        from .evaluate import run

        return run()
    elif a.cmd == "export-demo":
        from .demo_export import export

        export(a.only)
    elif a.cmd == "serve":
        import uvicorn

        from .config import settings

        uvicorn.run("qabuddy.api:app", host="0.0.0.0", port=settings().port, log_level="info")
    return 0


if __name__ == "__main__":
    sys.exit(main())
