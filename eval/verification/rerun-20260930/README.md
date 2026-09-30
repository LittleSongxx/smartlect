# 新版质量指标证据资产（2026-09-30 本地复跑与修复，新基线）

本目录是 2026-09-30 以**当前本地配置**（deepseek-flash + 百炼 qwen3.7-text-embedding/rerank，Qdrant 本地嵌入、SQLite、Redis/Langfuse 关闭）真实重跑项目全部既有质量指标、并完成异常修复后的完整证据集。口径与历史冻结证据（qwen3-max 系）不同，**新数值是新基线，不与历史对比**。全部文件 SHA256 指纹见 [evidence-manifest.sha256](evidence-manifest.sha256)（196 个文件，196MB）。

过程记录：[质量指标复跑](../../../docs/改动记录/2026-09-30/质量指标复跑.md)、[指标异常修复](../../../docs/改动记录/2026-09-30/指标异常修复.md)（含根因分析、失败版本与复测对照）。

## 终版指标 → 证据对照

| 指标 | 新基线数值 | 终版证据 | 说明 |
| --- | --- | --- | --- |
| 检索 v2 dev（16 查询） | 各档全 1.000 | [retrieval-dev/](retrieval-dev/) | 全 live 路径 |
| 检索 v2 holdout（54 查询） | hybrid+reranker **Recall@5 0.990 / MRR 1.000 / NDCG 0.992** | [retrieval-holdout-final/](retrieval-holdout-final/) | 召回池多样化改造后复跑，与改造前逐位一致（零回退） |
| 上下文治理（36 runs） | 36/36 通过；layered 相对 legacy input 降幅 **34.68%**（9.78M→6.38M tokens） | [context-holdout/](context-holdout/)（场景 a）+ [context-holdout-b/](context-holdout-b/) … [context-holdout-f/](context-holdout-f/)（场景 b–f，各 6 runs）；汇总 [context-summary.json](context-summary.json) | run 级 input_tokens 字段在本网关下为 None，数值由 [summarize_context.py](summarize_context.py) 从逐请求 usage 求和（可复算：`python3 summarize_context.py`） |
| 记忆提取（12 例） | **12/12 PASS** | [memory-extraction.json](memory-extraction.json) | deepseek-flash |
| Agent 门禁（release 30 用例） | **27/30 PASS，均分 0.950** | [agent-release-fixed/](agent-release-fixed/) | memory_multiturn 5/5 恢复；3 例失败均为 0.5 分表达类软失败 |
| 品类知识召回 | **Recall@3 1.000 / MRR 0.977 / NDCG 0.979，门禁 PASS** | [category-recall-fixed-k3-v2/](category-recall-fixed-k3-v2/)（@3 对齐旧口径）；[category-recall-fixed/](category-recall-fixed/)（@5：1.000/0.977/0.979，Precision 按标注集上限校准） | eval-* 快照分治后 |
| 商品召回正式门禁（扩充后 v1 release 225 条，K=3） | **PASS（修复后）：Recall@3 0.991 / MRR 1.000 / NDCG 0.981 / 负例 70/70 / 零降级**（composite 0.987 / semantic 0.982 / literal 1.000；K=8 0.994） | [product-recall-fixed-arch-k3-v2/](product-recall-fixed-arch-k3-v2/)（K=8：[fixed-arch-k8/](product-recall-fixed-arch-k8/)） | 主链路约束预过滤修复后；扩充集暴露盲区的过程证据 [expanded-k3/](product-recall-expanded-k3/)（0.742 BLOCK）保留 |
| 商品召回日常体检（67 条） | Recall@8 0.945 / MRR 0.899 / semantic 桶 0.931 | [product-recall-final/](product-recall-final/) | 门禁 BLOCK 属结构性（该集无负例桶，n/a；评测脚本已加显式警告） |
| 检索链路预检 | embedding + qwen3.7-text-rerank PASS | [preflight-retrieval.json](preflight-retrieval.json) | |
| 模型预检 | **6/6 PASS**（含强制 named tool_choice） | [preflight-model-after-fix/](preflight-model-after-fix/) | DeepSeek thinking 禁用适配后 |

## 过程证据（保留失败样本，按时间线）

复跑与修复的中间版本一律保留，是根因定位与"失败→修复→复测"链条的证据，不可删除：

| 目录/文件 | 阶段 | 结果与保留原因 |
| --- | --- | --- |
| [preflight-model/](preflight-model/) | 复跑预检 | passed=false：echo_probe（按名强制工具）被 DeepSeek 网关拒绝——异常 #4 的发现证据 |
| [agent-release/](agent-release/) | Agent 门禁第 1 轮 | 30/30 ERROR：judge 直连 `os.environ['LLM_BASE_URL']` 而脚本 import 链不加载 .env——运行方式坑的证据 |
| [agent-release-r2/](agent-release-r2/) | Agent 门禁第 2 轮 | 24/30：memory_multiturn 5 例因评测无法决议审批全挂——审批确认缺口（后修复为 API 通道）的发现证据 |
| [category-recall/](category-recall/)、[category-recall-k3/](category-recall-k3/) | 品类召回修复前 | BLOCK：eval-* 快照污染知识库（Precision 0.173），@3 对照 |
| [category-recall-fixed-k3/](category-recall-fixed-k3/) | 污染修复后 | Recall 1.000 但 Precision 0.364=数学上限仍 BLOCK——暴露门禁阈值与单正例标注集结构性不匹配，随后做上限校准 |
| [product-recall/](product-recall/) | 复跑首轮 | 0.842 BLOCK（同款重复率 0.433） |
| [product-recall-fixed/](product-recall-fixed/) | 同款去重后 | 0.898 / 重复率 0（误用 67 条体检集配正式门禁） |
| [product-recall-v1-release/](product-recall-v1-release/) | 首次正确数据集 | 负例 7/8（0.875）：发现负例被 catalog-v3 击穿 |
| [product-recall-negcheck/](product-recall-negcheck/) | 负例校验首跑 | 前置校验抓出 3 条击穿并 SystemExit——防护机制生效的证据 |
| [product-recall-v1-release-final/](product-recall-v1-release-final/)、[-final2/](product-recall-v1-release-final2/)、[-final3/](product-recall-v1-release-final3/) | 校准与修正迭代 | 依次：校准后又抓 1 条（9.99 USD 仍可满足）→ 截断 bug 被既有测试拦下后修复 → 退出码统一 |
| [product-recall-diversified/](product-recall-diversified/) | 召回池多样化后（体检集） | 0.945：semantic 桶 0.736→0.931 的对照点 |
| [retrieval-holdout/](retrieval-holdout/) | 复跑首轮 holdout | 0.990/0.965→(新口径) 0.990/1.000：新 embedding 基线 |
| [retrieval-holdout-diversified/](retrieval-holdout-diversified/) | 多样化改造中间验证 | 核心指标不变的中间确认 |
| [product-recall-negcheck/](product-recall-negcheck/) | 负例校验首跑（前轮） | 抓出 3 条被 v3 击穿的旧负例并 SystemExit——防护机制生效 |
| [product-recall-expanded-k3/](product-recall-expanded-k3/)、[expanded-k8/](product-recall-expanded-k8/) | **评测集扩充后首测** | R@3 **0.742 BLOCK**（composite 0.455）：扩充集如实暴露"紧价格约束 × 语义召回"架构盲区——本轮修复的起点证据 |
| [product-recall-fixed-arch-k3/](product-recall-fixed-arch-k3/) | 预过滤修复首测 | 指标 0.991 但 70 条负例被误标 keyword_2gram 降级触发防降级门禁——空匹配标记修复的发现证据 |
| [product-recall-fixed-arch-k3-v2/](product-recall-fixed-arch-k3-v2/)、[fixed-arch-k8/](product-recall-fixed-arch-k8/) | **修复后终版** | K=3 门禁 **PASS**（0.991/1.000/0.981，零降级）；K=8 0.994 |
| [retrieval-holdout-archcheck/](retrieval-holdout-archcheck/) | 检索改动回归 | v2 三档与基线逐位一致——无硬约束链路零波及的证明 |

## 数值适用边界（必读）

**全指标严口径审计（2026-09-30）**：对每项指标给出规模、严读数（R@1 = 首位命中）与已知局限，避免只看标称值：

| 指标 | 规模 | 标称值 | 严读数 R@1 | 已知局限 |
| --- | --- | --- | --- | --- |
| 检索 v2 hard | 54 条（48 正例，平均 7.4 金标） | R@5 0.995 | **0.649** | 查询与描述同源模板；R@5 含标注洞保守扣分 |
| 商品召回 v1 正式集 | **225 条（155 正例+70 负例）** | **R@3 0.991 门禁 PASS**（修复后；暴露期 0.742 BLOCK 证据保留） | 0.811（扩充前 45 条口径） | 统计稳健（CI 半宽 ±0.072、负例排除 >4.3% 泄漏）；0.742→0.991 的修复链 = 主链路约束预过滤 + 金标完备性回补 |
| 品类知识召回 | 22 题 | R@3 1.000 | **0.955**（21/22） | **候选池仅 5 篇文档**——任务窄是线上库的真实状态，非评测缺陷 |
| Agent 门禁 | release 30 例 | 27/30（0.950） | — | **judge 与被测同为 deepseek-flash（自评偏宽风险）**；P0 为程序断言不受影响；3 例失败均 0.5 分软失败 |
| 记忆提取 | **50 例**（原 12 + 38 扩充） | **50/50** | — | 扩充含 2 例 case 设计缺陷修正与 2 个真发现（例外拆分行为不稳定、场景限定冲突判定不一致），见改动记录 |
| 上下文治理 | 6 场景×2 策略×3 次 | 36/36，降幅 34.68% | — | 36/36 为确定性事实保留断言非模糊评分；本轮未算 bootstrap CI（工具依赖单目录网格，已注明） |
| 后端回归 / 模型预检 | 1467 测试 / 6 用例 | 全绿 / 6/6 | — | 工程门禁与协议检查，非质量指标 |

检索 v2 的 0.990/1.000/0.992 是**受控易题上的管线对照值**，不等于真实用户查询的召回率：

- **规模**：holdout 54 条（48 正例 + 6 负例），正例对 353 个（平均每条 7.4 个正确答案）；0.990 即 353 对中漏约 4 对。dev 18 条。目录 1,000 件。
- **题目构成**：目录 500/1000 件是 Roamix 单品牌的功能×规格矩阵，holdout 48 条正例查询**全部带"在 Roamix 系列中"品牌前缀**；金标是命中系列的全 SKU 集合（多正例），Top5 命中系列内任意变体即计分。
- **两侧同源**：查询模板与商品描述由同一生成器按同一意图规则产出（生成脚本有反泄漏声明：不用商品标题做查询、不按排序结果改金标），语义对齐天然高于真实查询。
- **区分度参照**：同数据上 keyword 0.660（查询非字面拷贝）、旧 BGE dense 0.948（存在难度梯度），新 embedding 做到 1.000 说明该题难度上限即在此。
- 更接近真实难度的参照：v1 正式集（单正例、无品牌提示、含负例约束）release Recall@8 0.973；v1 多语言跨语言词项召回仅 0.171。v2 的定位始终是"五档召回管线的受控对照实验"，非真实效果验收。

## v2-hard（去品牌提示视角，2026-09-30 追加）

由冻结 v2 集派生（[生成脚本](../../../scripts/generate_retrieval_v2_hard.py)：仅剥掉"在 Roamix 系列中"品牌前缀，金标/split/kind 原样继承、不按新结果重标），用于检验"数值适用边界"中指出的品牌送分项。运行口径与 v2 完全一致，证据：[retrieval-holdout-hard/](retrieval-holdout-hard/)。

| 档位 | v2 holdout（带品牌提示） | **v2-hard（无提示）** |
| --- | --- | --- |
| keyword | 0.660 / 0.813 / 0.702 | 0.870 / 0.786 / 0.814 |
| bm25 | 0.898 / 0.767 / 0.803 | 0.887 / 0.732 / 0.783 |
| dense | 1.000 / 0.976 / 0.981 | 0.990 / 0.951 / 0.961 |
| hybrid | 0.972 / 0.931 / 0.930 | 0.950 / 0.884 / 0.895 |
| hybrid+reranker | 0.990 / 1.000 / 0.992 | 0.995 / 0.979 / 0.985 |

**Recall@K 阶梯（2026-09-30 二次加严）**：[retrieval_v2.py](../../../scripts/eval/retrieval_v2.py) 升级为一次运行产出 @1/@3/@5 多口径（检索统一取 8 条，评分层按 K 切；R@1 即"第一名必须命中"的严口径）。v2-hard 证据：[retrieval-holdout-hard-k/](retrieval-holdout-hard-k/)；v2 原集对照：[retrieval-holdout-k/](retrieval-holdout-k/)。

| 档位 | R@1 | R@3 | R@5 |
| --- | --- | --- | --- |
| keyword | 0.543 | 0.734 | 0.870 |
| bm25 | 0.450 | 0.720 | 0.887 |
| dense | 0.618 | 0.873 | 0.990 |
| hybrid | 0.543 | 0.835 | 0.950 |
| **hybrid+reranker** | **0.649** | **0.906** | 0.995 |

（v2 带品牌对照：hybrid+reranker R@1 0.665 / R@3 0.906 / R@5 0.990。）严口径下档位差异显著（bm25 0.450 vs rerank 0.649），rerank 的增益从 R@5 的不可见变为 R@1/R@3 的明确优势；R@5 口径仍含前述标注洞的保守扣分，R@1/R@3 不受其影响（命中任一金标即计）。

读法（两档并列，互不替代）：

- 干扰生效但幅度有限：dense 的 Recall/MRR/NDCG 均回落（500 件同品类非 Roamix 商品开始竞争），hybrid+reranker 的 **MRR 1.000→0.979**（第一名不再必然是金标）。剩余高分的根源仍是数据集固有属性（多正例平均 7.4 个、查询与描述同源模板），刻意再加深（单正例化、口语改写）会走向另一种人为设计，故未做——更严口径请直接看 v1 正式集（0.973）。
- **去品牌后 rerank 的品牌偏置消失**：hybrid+reranker Recall 反而 0.990→0.995——"Roamix"一词此前让同品牌一切变体在精排中互相抬分。
- 扣分条目抽查分两类，**不可混读**：①标注洞（约 5-6 条）：Nordic 中性色陶瓷杯、CompressCube 压缩收纳袋、LinenFold 衣物收纳套等非 Roamix 商品同样满足查询意图，但冻结金标只含 Roamix 系列——这部分是继承标注的保守扣分，压低而非抬高分数，未回改金标（防按结果改标注）；②真实错误（如"办公室不想按键吵"检索回"仅 2.4G **有声按键**"鼠标）——规格级混淆，v2（带品牌提示）下被品牌词掩盖、v2-hard 才暴露，是本视角的主要价值。

## 证据完整性事件记录（2026-09-30 18:04 发现）

16:47:50 有**外部批量操作**（非本证据会话所为，同纳秒时间戳）改写了 25 个报告 md 与 18 个 run 级 sessions.db：md 的改动经抽查确认为品牌名替换（Globex→Smartlect，并行会话的全局重命名波及），**全部指标数字与结论零变化**（如 agent-release-fixed 的 27/30、0.950 原值保留）；sessions.db 为 SQLite 被工具打开的元数据变化。处置：抽查 3 个目录 md 与 manifest 数字一致后，指纹清单按现状全量重算（222 条全部通过）。该事件说明证据目录对工作区级批量操作无防护——若需强保护，后续可将关键结论性文件（report.json/manifest）单独锁定。

## 大文件说明

`retrieval-*/vectors.json`（约 22MB/份）与 `retrieval-*/index/`（本地 Qdrant 库，约 10MB/份）是评测运行时生成的向量与索引快照，属原始证据的一部分（可再生：重跑对应命令），指纹已入清单。核心结论性文件是各目录的 `report.json` / `*.md` / `manifest.json`。

## 评测集与生成器资产（git 内，本轮新增/变更）

- `eval/v1/product_retrieval.jsonl`（SHA256 `2ed6a225…`）：750 条（原 150 冻结 + 600 扩充），由 [scripts/expand_eval_v1.py](../../../scripts/expand_eval_v1.py)（`cb173340…`）确定性生成（catalog-v3 反向枚举金标 + 16 条旧 case 完备性回补）。
- `eval/memory/cases.json`（SHA256 `9025e6c7…`）：50 例（原 12 + 38 对抗模式变体，期望先行设计）。
- `scripts/eval/run_product_recall.py`：online-main 正式门禁 K=3 业务口径 + 负例可满足性前置校验。
- `scripts/eval/retrieval_v2.py`：`--dataset` 参数 + 一次运行产出 R@1/@3/@5 阶梯。

## 复算与复跑

- 上下文治理汇总：`python3 eval/verification/rerun-20260930/summarize_context.py`（从各 run 的逐请求 usage 重算 token 降幅）
- 各评测复跑命令与运行注意（judge 需 `set -a; source .env; set +a`、`run_context` 逐场景独立目录等）见两份改动记录的"运行方式备注"节
- 指纹校验：`cd eval/verification/rerun-20260930 && sha256sum -c evidence-manifest.sha256`
