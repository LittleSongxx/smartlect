# README 质量指标口径修正的复算与回归证据（2026-10-01）

本目录是 2026-10-01 修正 [README.md](../../../README.md)「质量指标」表与「技术栈」表商品检索一行时，为所引数值补的可复跑证据。**不修改、不移动 `eval/verification/rerun-20260930/` 下的任何既有证据**。

## 文件

| 文件 | 内容 |
| --- | --- |
| [recompute_top1.py](recompute_top1.py) | 从评测 evidence manifest 复算「首位命中率 R@1」；仓库根目录下 `python3 eval/verification/readme-metrics-20261001/recompute_top1.py` 即可复跑 |
| [top1-recompute.txt](top1-recompute.txt) | 上述脚本 2026-10-01 在本机的输出原文 |
| [full-tests.log](full-tests.log) | 后端全量回归（本机 apt 的 Redis 6.0.16）：`12 failed, 1455 passed, 1 skipped in 372.59s`，`EXIT=1` |
| [full-tests-redis74.log](full-tests-redis74.log) | 冻结树（含本轮全部改动）+ Redis 7.4.11：`2 failed, 1465 passed, 1 skipped in 321.16s`，`EXIT=1` |

## 为什么要单独复算 R@1

README 原表把「严读数（首位命中）」当作既有字段，但实际只有 [retrieval_v2.py](../../../scripts/eval/retrieval_v2.py) 一次运行直接产出 @1/@3/@5 三档；[run_product_recall.py](../../../scripts/eval/run_product_recall.py) 与 `run_category_recall.py` 的报告只写 `Recall@K / Precision@K / MRR / NDCG@K`，**没有 @1 分档**。因此这两行的 R@1 只能从逐题召回序离线复算。

复算结果（口径：返回结果第 1 位命中任一金标即计，分母为非空正例题数）：

| 集合 | 证据目录 | R@1 |
| --- | --- | --- |
| 商品召回正式门禁 v1 release 225 例（K=3） | `rerun-20260930/product-recall-fixed-arch-k3-v2/` | **155/155 = 1.0000** |
| 商品召回扩充前 45 例（37 正例，K=3） | `rerun-20260930/product-recall-v1-release-k3-gate/` | 35/37 = 0.9459 |
| 品类知识召回 22 例（K=3） | `rerun-20260930/category-recall-fixed-k3-v2/` | **21/22 = 0.9545** |
| 对照：67 条体检集 semantic 桶 MRR（K=8） | `rerun-20260930/product-recall-final/` | 0.8111 |

最后一行说明原表的错误来源：**0.811 是 67 条体检集 semantic 桶的 MRR**，不是任何商品召回集的 R@1。项目 README、[证据目录 README](../rerun-20260930/README.md) 与 [改动记录 2026-09-30 指标异常修复](../../../docs/改动记录/2026-09-30/指标异常修复.md) 三处都曾把它标成「商品召回 R@1」，三处已于 2026-10-01 一并更正，以本目录的复算为准。

## 后端回归：两轮复跑与失败归因

| 轮次 | Redis | 结果 |
| --- | --- | --- |
| 第一次 | 本机 apt 的 **6.0.16** | `12 failed, 1455 passed, 1 skipped`（372.59s） |
| 第二次 | **7.4.11**（`redis:7.4-bookworm` 镜像里取出的可移植二进制） | `3 failed, 1464 passed, 1 skipped`（340.06s） |
| 第三次（冻结树复跑） | **7.4.11** | `2 failed, 1465 passed, 1 skipped`（321.16s，即 [full-tests-redis74.log](full-tests-redis74.log)） |

**12 → 2 的差异全部来自 Redis 版本 + 一项已知偶发。** 队列测试自己拉起隔离的 Redis 进程（`tests/test_queue_reliability.py` 读 `SMARTLECT_REDIS_SERVER_BIN`，否则用 `PATH` 里的 `redis-server`），Redis 6.0 没有 `XAUTOCLAIM`（6.2+ 才有），日志里满是 `unknown command XAUTOCLAIM`。取一份 ≥6.2 的二进制即可，不需要改系统 Redis：

```bash
docker create --name redis74tmp redis:7.4-bookworm
mkdir -p ~/.local/bin
docker cp redis74tmp:/usr/local/bin/redis-server ~/.local/bin/redis-server-7.4
docker rm -f redis74tmp && chmod +x ~/.local/bin/redis-server-7.4
SMARTLECT_REDIS_SERVER_BIN=$HOME/.local/bin/redis-server-7.4 .venv/bin/python -m pytest tests/ -q
```

### 剩下的失败项

| 失败项 | 现状与判断 |
| --- | --- |
| `tests/test_langfuse_verification.py::test_derived_config_uses_real_otlp_sanitizer_and_v4_http` | 断言收到的 OTLP 请求带 `x-langfuse-ingestion-version: 4`。**待排查**：把同一段测试体原样搬到 pytest 之外运行可以通过（`_export_settings` 与应用侧导出器都实测会同时发出 `Authorization` 与 `x-langfuse-ingestion-version`），只在 pytest 进程内失败；两次捕获到的请求头形状也不同（pytest 下缺 `Accept-Encoding`/`Connection`、`Content-Length` 位置前移），指向测试进程内的 HTTP 栈差异，与本次文档改动无关 |
| `tests/test_tracing.py::test_otlp_real_http_path_auth_and_native_agentscope_parent_chain` | 同上，同一断言 |
| `tests/test_queue_reliability.py::test_api_session_lease_and_worker_share_exclusion` | **已知偶发**：该文件单独复跑 5 次为 4 失败 1 通过（日志为「执行租约失效…Redis 租约未能在剩余时间内完成续期」+ `TimeoutError`），三次全量里出现在第二次而不在第一、三次。与 [改动记录 2026-09-30](../../../docs/改动记录/2026-09-30/指标异常修复.md) 记的「queue 租约测试在满载下的偶发」一致，未根治 |

已排除的干扰项：`__pycache__` 里残留改写前目录名（`globex-agent`）的 `.pyc` 会让 traceback 指向不存在的路径，已清理；清理不改变以上结论。

## 复现

```bash
cd <仓库根目录>
.venv/bin/python -m pytest tests/ -q -p no:cacheprovider     # Redis 6.0：12 failed / 1455 passed / 1 skipped
SMARTLECT_REDIS_SERVER_BIN=$HOME/.local/bin/redis-server-7.4 \
  .venv/bin/python -m pytest tests/ -q -p no:cacheprovider  # Redis 7.4：2~3 failed / 1464~1465 passed / 1 skipped
.venv/bin/python eval/verification/readme-metrics-20261001/recompute_top1.py
```
