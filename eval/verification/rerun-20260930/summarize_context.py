# -*- coding: utf-8 -*-
"""汇总 rerun-20260930 上下文治理成对评测：从各场景 run 目录的 result.json 直接求和 usage。

run_context 写的 run 级 input_tokens 汇总字段在本次口径下为 None（usage 明细完整），
本脚本从逐请求 usage 求和，不经 report_context 的 grid 校验，输出 JSON 与终端摘要。
"""
import json
import glob
import collections
from pathlib import Path

BASE = Path(__file__).parent

rows = []
for result_file in sorted(glob.glob(str(BASE / "context-holdout*" / "v3-*" / "result.json"))):
    r = json.loads(Path(result_file).read_text())
    usage = r.get("usage") or []
    rows.append({
        "case_id": r["case_id"], "strategy": r["strategy"], "repetition": r["repetition"],
        "passed": bool(r.get("passed")), "error": r.get("error"),
        "input_tokens": sum(u.get("input_tokens") or 0 for u in usage),
        "output_tokens": sum(u.get("output_tokens") or 0 for u in usage),
        "model_calls": r.get("model_calls"), "elapsed_ms": r.get("elapsed_ms"),
    })

agg = collections.defaultdict(lambda: {"runs": 0, "passed": 0, "input_tokens": 0, "output_tokens": 0, "model_calls": 0})
for r in rows:
    a = agg[r["strategy"]]
    a["runs"] += 1
    a["passed"] += 1 if r["passed"] else 0
    a["input_tokens"] += r["input_tokens"]
    a["output_tokens"] += r["output_tokens"]
    a["model_calls"] += r["model_calls"] or 0

summary = {k: {**v, "success_rate": v["passed"] / v["runs"] if v["runs"] else 0} for k, v in agg.items()}
if "legacy" in summary and "layered" in summary and summary["legacy"]["input_tokens"]:
    li, la = summary["legacy"]["input_tokens"], summary["layered"]["input_tokens"]
    summary["layered_vs_legacy_input_reduction"] = (li - la) / li

report = {"runs_total": len(rows), "summary": summary, "rows": rows,
          "notes": "input_tokens 从逐请求 usage 求和；延迟为共享网关环境。"}
out = BASE / "context-summary.json"
out.write_text(json.dumps(report, ensure_ascii=False, indent=2))
print(json.dumps({"runs_total": len(rows), "summary": summary}, ensure_ascii=False, indent=2))
print("written:", out)
