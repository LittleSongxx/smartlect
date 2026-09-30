#!/usr/bin/env python3
"""从评测证据 manifest 复算「首位命中率 R@1」。

用法（仓库根目录）：
    python3 eval/verification/readme-metrics-20261001/recompute_top1.py

为什么要单独复算：README「质量指标」表的严读数一列里，**只有 retrieval_v2.py 会直接输出
R@1/@3/@5 三档**；run_product_recall.py 与 run_category_recall.py 的报告只产出
Recall/Precision/MRR/NDCG@K，没有 @1 分档。因此那两行的 R@1 必须从逐题召回序离线复算，
本脚本给出可复跑、可核对的复算过程。

口径：R@1 =「返回结果的第 1 位命中任一金标」的题目数 / 非空正例题数（命中任一金标即计）。
`retrieved` / `canonical_retrieved` 已按相关性排序，取下标 0 即首位。
"""

from __future__ import annotations

import glob
import json
import pathlib
import sys

EVIDENCE = pathlib.Path("eval/verification/rerun-20260930")


def load_manifest(directory: str) -> dict | None:
    matches = sorted(glob.glob(str(EVIDENCE / directory / "*.manifest.json")))
    if not matches:
        print(f"  [跳过] 找不到 {directory} 的 manifest")
        return None
    return json.loads(pathlib.Path(matches[0]).read_text(encoding="utf-8"))


def top1(rows: list[dict], key: str) -> tuple[int, int]:
    """返回 (首位命中数, 非空正例题数)。"""
    positive = [row for row in rows if row.get("relevant")]
    hits = sum(
        1
        for row in positive
        if row.get(key) and row[key][0] in set(row["relevant"])
    )
    return hits, len(positive)


def recompute_product_recall(directory: str) -> None:
    manifest = load_manifest(directory)
    if manifest is None:
        return
    top_k = manifest["parameters"]["top_k"]
    observations = manifest["execution"]["observations"]
    print(f"{directory}  K={top_k}  selected={manifest['selection']['selected_count']}"
          f"  buckets={manifest['selection']['bucket_counts']}")
    for strategy, rows in observations.items():
        hits, total = top1(rows, "canonical_retrieved")
        print(f"  策略 {strategy}: R@1 = {hits}/{total} = {hits / total:.4f}")


def recompute_category_recall(directory: str) -> None:
    manifest = load_manifest(directory)
    if manifest is None:
        return
    rows = manifest["execution"]["observations"]
    hits, total = top1(rows, "retrieved")
    print(f"{directory}  K={manifest['execution']['metrics']['k']}  n={total}")
    print(f"  标准文档被排在第 1 位: R@1 = {hits}/{total} = {hits / total:.4f}")


def main() -> int:
    if not EVIDENCE.is_dir():
        print(f"请在仓库根目录运行；找不到 {EVIDENCE}", file=sys.stderr)
        return 1
    print("商品召回正式门禁（复算值，非报告字段）")
    recompute_product_recall("product-recall-fixed-arch-k3-v2")   # 当前 225 例门禁
    recompute_product_recall("product-recall-v1-release-k3-gate")  # 扩充前 45 例（37 正例）
    print()
    print("品类知识召回门禁（复算值，非报告字段）")
    recompute_category_recall("category-recall-fixed-k3-v2")
    print()
    print("对照：体检集 semantic 桶在 K=8 下的 MRR（README 旧稿曾把 0.811 误标成商品召回 R@1）")
    manifest = load_manifest("product-recall-final")
    if manifest is not None:
        per_query = manifest["execution"]["metrics"]["embedding_rerank"]["per_query"]
        semantic = [q for q in per_query if q.get("kind") == "semantic"]
        if semantic:
            mrr = sum(q["mrr"] for q in semantic) / len(semantic)
            print(f"  product-recall-final semantic 桶 n={len(semantic)} MRR={mrr:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
