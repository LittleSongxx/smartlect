# 品类知识库召回评测报告（2026-09-30 13:10:21）

标注集 `eval/category_recall.jsonl`，正例 22 条。标注单位为知识文档名。

| 指标 | 值 | 阈值 |
|---|---|---|
| Recall@3 | 0.818 | ≥ 0.75（阻断） |
| Precision@3 | 0.288 | ≥ 0.45（阻断） |
| MRR | 0.795 | ≥ 0.65（阻断） |
| NDCG@3 | 0.800 | ≥ 0.7（阻断） |
| 不可回答准确率 | n/a | 未启用 |
| 政策拒答准确率 | n/a | 未启用 |

门禁结论：**BLOCK**

未达标项：
- Precision@3 0.2879 < 0.45

| query | Recall | Precision | MRR | NDCG | 召回文档 | 标注文档 |
|---|---|---|---|---|---|---|
| 旅行箱怎么选 铝框还是拉杆布箱 | 1.00 | 0.33 | 1.00 | 1.00 | travel-gear.md,eval-travel-gear-参数判断.md,eval-travel-gear-价格与预算.md | travel-gear.md |
| 旅行装备的价格区间大概多少 | 1.00 | 0.33 | 1.00 | 1.00 | travel-gear.md,eval-travel-gear-价格与预算.md,eval-beauty-care-价格与预算.md | travel-gear.md |
| 买旅行三件套要注意什么坑 | 1.00 | 0.33 | 1.00 | 1.00 | travel-gear.md,eval-travel-gear-避坑与合规.md,eval-travel-gear-价格与预算.md | travel-gear.md |
| 登机箱尺寸有什么讲究 | 1.00 | 0.33 | 1.00 | 1.00 | travel-gear.md,eval-travel-gear-避坑与合规.md,eval-travel-gear-参数判断.md | travel-gear.md |
| 降噪耳机的降噪深度怎么看 | 1.00 | 0.33 | 1.00 | 1.00 | digital-accessories.md,eval-digital-accessories-参数判断.md,eval-digital-accessories-概览.md | digital-accessories.md |
| 氮化镓充电器功率怎么选 | 1.00 | 0.33 | 1.00 | 1.00 | digital-accessories.md,eval-digital-accessories-参数判断.md,eval-digital-accessories-概览.md | digital-accessories.md |
| 数码配件有哪些常见避坑点 | 1.00 | 0.33 | 1.00 | 1.00 | digital-accessories.md,eval-digital-accessories-避坑与合规.md,eval-digital-accessories-概览.md | digital-accessories.md |
| 移动电源能不能带上飞机 | 0.50 | 0.33 | 0.50 | 0.48 | eval-policy-battery.md,digital-accessories.md,eval-digital-accessories-避坑与合规.md | digital-accessories.md,cross-border-guide.md |
| 陶瓷杯和粗陶杯有什么区别 | 1.00 | 0.33 | 1.00 | 1.00 | home-living.md,eval-home-living-参数判断.md,eval-home-living-避坑与合规.md | home-living.md |
| 家居用品怎么判断是不是天然材质 | 0.50 | 0.33 | 0.50 | 0.48 | eval-home-living-避坑与合规.md,home-living.md,eval-home-living-价格与预算.md | home-living.md,cross-border-guide.md |
| 家居生活类的价格区间参考 | 1.00 | 0.33 | 1.00 | 1.00 | home-living.md,eval-home-living-价格与预算.md,eval-home-living-概览.md | home-living.md |
| 登山杖材质怎么选 铝合金还是碳纤维 | 1.00 | 0.33 | 1.00 | 1.00 | outdoor-sports.md,eval-outdoor-sports-价格与预算.md,travel-gear.md | outdoor-sports.md |
| 睡袋的温标怎么理解 | 0.00 | 0.00 | 0.00 | 0.00 | travel-gear.md,eval-outdoor-sports-参数判断.md,eval-travel-gear-参数判断.md | outdoor-sports.md |
| 防潮垫的R值是什么意思 | 0.00 | 0.00 | 0.00 | 0.00 | eval-outdoor-sports-参数判断.md,eval-outdoor-sports-价格与预算.md,eval-outdoor-sports-概览.md | outdoor-sports.md |
| 户外装备常见的避坑点 | 1.00 | 0.33 | 0.50 | 0.63 | eval-outdoor-sports-避坑与合规.md,outdoor-sports.md,eval-outdoor-sports-概览.md | outdoor-sports.md |
| 到手价是怎么算出来的 | 1.00 | 0.33 | 1.00 | 1.00 | cross-border-guide.md,eval-home-living-价格与预算.md,eval-kitchen-dining-价格与预算.md | cross-border-guide.md |
| 免税额度 de minimis 怎么算 | 1.00 | 0.33 | 1.00 | 1.00 | cross-border-guide.md,digital-accessories.md,eval-policy-us.md | cross-border-guide.md |
| 跨境运费一般怎么收 | 1.00 | 0.33 | 1.00 | 1.00 | cross-border-guide.md,eval-policy-global-shipping.md,eval-policy-cn.md | cross-border-guide.md |
| 关税什么情况下要交 | 1.00 | 0.33 | 1.00 | 1.00 | cross-border-guide.md,digital-accessories.md,eval-policy-us.md | cross-border-guide.md |
| 推荐商品时话术上有什么原则 | 0.00 | 0.00 | 0.00 | 0.00 | eval-policy-global-shipping.md,eval-policy-us.md,eval-policy-jp.md | cross-border-guide.md |
| 露营灯和营地灯选购要看什么 | 1.00 | 0.33 | 1.00 | 1.00 | outdoor-sports.md,eval-outdoor-sports-价格与预算.md,eval-office-study-概览.md | outdoor-sports.md |
| 旅行装备里哪些是当前热卖款 | 1.00 | 0.33 | 1.00 | 1.00 | travel-gear.md,eval-travel-gear-价格与预算.md,eval-travel-gear-概览.md | travel-gear.md |


## 执行证据

- 选集：`all`，22/22 条；完整选集：True。
- 选集内容 SHA-256：`2209e8dfb1709892752159c06e5a1013b825bd719a047ed475370e033e49c97f`。
- 工作区内容 SHA-256：`2a8bc54d255769c8db8f406960a276e0bb6225f7059f0f25a404464306117de8`（包含未提交源文件；详细范围见同名 manifest）。
- 执行状态：**COMPLETED**；门禁：**BLOCK**；门禁范围：`diagnostic`。
- 实际策略：`["category_vector_document_scope_v1"]`。
- 模型、Prompt、数据文件、依赖版本及逐项 hash 均保存在同名 `.manifest.json`。
