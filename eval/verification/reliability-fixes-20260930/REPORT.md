# 可靠性修复批次交付报告

日期：2026-09-30（Asia/Shanghai）。分支 main，起点 commit `f10ed0e`。本地修改，未提交推送。
范围：上轮深度审查确认的 B1–B8 全部基线修复 + 用户选定的 D2/D3/D4/D5/D6/D7；D1（多语言理解层）按用户决策本轮不做，仅登记。

## 交付内容

| 批次 | 项 | 关键源码 |
|---|---|---|
| 1 | B1 语义缓存多语言写意图过滤 + 归一化保留词边界 | app/infrastructure/cache/semantic_cache.py |
| 1 | B2 熔断半开单探测（本地 probe_deadline / 共享 SET NX 探测锁 / 取消释放名额） | app/infrastructure/resilience.py, shared_breaker.py |
| 1 | B3 流式输出守卫（StreamingMasker 动态扣留，token.delta 与 TEXT_MESSAGE_CONTENT 双路径） | app/infrastructure/security/output_guard.py, orchestrator.py, ag_ui_adapter.py |
| 2 | B4 会话锁修剪 + `_injected_preferences` 死状态删除 + SessionRegistry LRU | orchestrator.py, main_agent.py |
| 2 | B5 事件订阅队列有界 + 溢出丢最旧 token.delta + journal 写队列高水位告警 | eventbus.py, ag_ui_runtime.py |
| 2 | B7 心跳存储抖动有界重试（renew=False 仍立即失效）+ reserve 后重算 deadline | ag_ui_runtime.py, redis_stream_queue.py |
| 3 | B6 journal 读路径只读探测、命中才写事务恢复 | ag_ui_journal.py |
| 3 | B8 on_model_call 单次 deepcopy/单次 count_tokens + 已读块跳过全文哈希 | context_governance.py |
| 3 | D5 重 CPU 定点卸载（deepcopy/打分/投影合并 → to_thread） | context_governance.py, ag_ui_journal.py, catalog_search.py |
| 4 | D2 AG-UI 主路径启用语义缓存（命中经 finish() 合成完整事件流） | ag_ui_runtime.py, ag_ui.py |
| 4 | D3 journal 事件保留策略（非 last_run 归档至 runs.db.archive，默认关） | ag_ui_journal.py |
| 4 | D4 BM25 预计算索引 + 目录指纹缓存（parity 与 bm25_rank 逐分数一致） | app/infrastructure/retrieval/bm25.py |
| 4 | D6 运行级 deadline（RUN_MAX_SECONDS，默认 0=关，DEADLINE_EXCEEDED 收口） | ag_ui_runtime.py |
| 4 | D7 编排重试 SDK 契约测试（inputs=[] 重入不丢/不重复用户消息） | tests/test_orchestrator_retry_contract.py |

新增配置（默认即新行为或关闭）：`TOOL_PROBE_TIMEOUT_SECONDS=300`、`SESSION_AGENT_CACHE_LIMIT=128`、`EVENT_QUEUE_MAXSIZE=4096`、`JOURNAL_RETENTION_DAYS=0`（关）、`RUN_MAX_SECONDS=0`（关）。

## 验证方式与证据

全部为本地假模型/假 Redis/内存 SQLite 测试，不依赖真实模型凭据与外部服务。

- 分批全量回归：[batch1](batch1-full-tests.log) 1425 passed / 16 failed → [batch2](batch2-full-tests.log) 1437 / 16 → [batch3](batch3-full-tests.log) 1442 / 19（含 3 个 D3 预写测试当时未实现）→ [final](final-full-tests.log) **1450 passed, 1 skipped, 16 failed**。
- **16 个失败与本轮改动前的原代码基线完全一致**（git stash 对照验证，见 [原代码对照记录](baseline-check.txt)）：test_queue_reliability×10 + test_queue_redis_restart×1 + test_reranker_client×2 + test_retrieval×2（+1 计数差为集合内分布）均为环境性既有失败（隔离 Redis/外部检索依赖在当前 WSL2 不可用），非本轮回归。
- 新增测试 25 个，分布在 test_streaming_guard / test_runtime_lease / test_session_state_hygiene / test_journal_read_path / test_journal_retention / test_run_deadline / test_bm25_index / test_orchestrator_retry_contract 及既有文件的追加用例。

## 阶段失败与修正（保留过程）

1. B3 首版固定 128 字符扣留 → 短流式文本延迟到 END 输出，与"等首个 TEXT 增量再断连"的既有 TCP 测试死锁（批次 1 首次全量中断）；改为字面触发串动态扣留后恢复即时流式，死锁消失。
2. 事件总线 `asyncio.Queue(max=…)` 参数名错误（应为 maxsize）导致订阅全线崩溃，当轮 16 failed；修正后通过。
3. test_abandoned_run 0.04s 租约在本机稳定失败——stash 对照原代码同样失败（环境性），放宽至 0.5s/0.7s，语义不变。
4. 心跳重试测试初版断言时机早于重试间隔、且未区分"运行先完成（心跳被正常取消）"与"重试未发生"，重写场景后通过。

## 启用与回滚

- 代码级：全部改动 revert 即可，无破坏性数据迁移（agui_runs 新增带默认值的 events_archived 列，旧库 ALTER 兼容，回滚代码后旧库多一列无影响）。
- 配置级：`JOURNAL_RETENTION_DAYS=0`、`RUN_MAX_SECONDS=0` 默认即旧行为；语义缓存主路径回滚需同时还原 ag_ui_runtime.py 与 ag_ui.py 的 `use_semantic_cache=True`。

## 未完成项

- D1 多语言理解层（类目/约束抽取/材质黑名单中文硬编码）：用户决策本轮不做，缺口已登记。
- B8/D5 的量化收益未做基准（本轮消除明确的重复计算）；token 级基线随质量指标复跑另行进行。
- 归档库（runs.db.archive）自身无二次清理；worker 路径无端到端 deadline。
- 当日 README 既有的 [质量指标复跑](../../改动记录/2026-09-30/README.md) 链接指向的文件缺失，系本轮之前遗留，未代为补写。
