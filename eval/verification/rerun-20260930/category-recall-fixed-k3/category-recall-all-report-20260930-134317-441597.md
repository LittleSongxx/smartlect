# 品类知识库召回评测报告（2026-09-30 13:43:22）

标注集 `eval/category_recall.jsonl`，正例 22 条。标注单位为知识文档名。

| 指标 | 值 | 阈值 |
|---|---|---|
| Recall@3 | 1.000 | ≥ 0.75（阻断） |
| Precision@3 | 0.364 | ≥ 0.45（阻断） |
| MRR | 0.977 | ≥ 0.65（阻断） |
| NDCG@3 | 0.979 | ≥ 0.7（阻断） |
| 不可回答准确率 | n/a | 未启用 |
| 政策拒答准确率 | n/a | 未启用 |

门禁结论：**BLOCK**

未达标项：
- Precision@3 0.3636 < 0.45

| query | Recall | Precision | MRR | NDCG | 召回文档 | 标注文档 |
|---|---|---|---|---|---|---|
| 旅行箱怎么选 铝框还是拉杆布箱 | 1.00 | 0.33 | 1.00 | 1.00 | travel-gear.md,outdoor-sports.md,home-living.md | travel-gear.md |
| 旅行装备的价格区间大概多少 | 1.00 | 0.33 | 1.00 | 1.00 | travel-gear.md,outdoor-sports.md,cross-border-guide.md | travel-gear.md |
| 买旅行三件套要注意什么坑 | 1.00 | 0.33 | 1.00 | 1.00 | travel-gear.md,outdoor-sports.md,digital-accessories.md | travel-gear.md |
| 登机箱尺寸有什么讲究 | 1.00 | 0.33 | 1.00 | 1.00 | travel-gear.md,cross-border-guide.md,outdoor-sports.md | travel-gear.md |
| 降噪耳机的降噪深度怎么看 | 1.00 | 0.33 | 1.00 | 1.00 | digital-accessories.md,cross-border-guide.md,travel-gear.md | digital-accessories.md |
| 氮化镓充电器功率怎么选 | 1.00 | 0.33 | 1.00 | 1.00 | digital-accessories.md,outdoor-sports.md,travel-gear.md | digital-accessories.md |
| 数码配件有哪些常见避坑点 | 1.00 | 0.33 | 1.00 | 1.00 | digital-accessories.md,cross-border-guide.md,outdoor-sports.md | digital-accessories.md |
| 移动电源能不能带上飞机 | 1.00 | 0.67 | 1.00 | 0.95 | digital-accessories.md,travel-gear.md,cross-border-guide.md | digital-accessories.md,cross-border-guide.md |
| 陶瓷杯和粗陶杯有什么区别 | 1.00 | 0.33 | 1.00 | 1.00 | home-living.md,cross-border-guide.md,outdoor-sports.md | home-living.md |
| 家居用品怎么判断是不是天然材质 | 1.00 | 0.67 | 1.00 | 0.95 | home-living.md,outdoor-sports.md,cross-border-guide.md | home-living.md,cross-border-guide.md |
| 家居生活类的价格区间参考 | 1.00 | 0.33 | 1.00 | 1.00 | home-living.md,travel-gear.md,cross-border-guide.md | home-living.md |
| 登山杖材质怎么选 铝合金还是碳纤维 | 1.00 | 0.33 | 1.00 | 1.00 | outdoor-sports.md,travel-gear.md,home-living.md | outdoor-sports.md |
| 睡袋的温标怎么理解 | 1.00 | 0.33 | 0.50 | 0.63 | travel-gear.md,outdoor-sports.md,home-living.md | outdoor-sports.md |
| 防潮垫的R值是什么意思 | 1.00 | 0.33 | 1.00 | 1.00 | outdoor-sports.md,digital-accessories.md,travel-gear.md | outdoor-sports.md |
| 户外装备常见的避坑点 | 1.00 | 0.33 | 1.00 | 1.00 | outdoor-sports.md,travel-gear.md,digital-accessories.md | outdoor-sports.md |
| 到手价是怎么算出来的 | 1.00 | 0.33 | 1.00 | 1.00 | cross-border-guide.md,travel-gear.md,digital-accessories.md | cross-border-guide.md |
| 免税额度 de minimis 怎么算 | 1.00 | 0.33 | 1.00 | 1.00 | cross-border-guide.md,digital-accessories.md,travel-gear.md | cross-border-guide.md |
| 跨境运费一般怎么收 | 1.00 | 0.33 | 1.00 | 1.00 | cross-border-guide.md,digital-accessories.md,outdoor-sports.md | cross-border-guide.md |
| 关税什么情况下要交 | 1.00 | 0.33 | 1.00 | 1.00 | cross-border-guide.md,digital-accessories.md,outdoor-sports.md | cross-border-guide.md |
| 推荐商品时话术上有什么原则 | 1.00 | 0.33 | 1.00 | 1.00 | cross-border-guide.md,outdoor-sports.md,home-living.md | cross-border-guide.md |
| 露营灯和营地灯选购要看什么 | 1.00 | 0.33 | 1.00 | 1.00 | outdoor-sports.md,travel-gear.md,digital-accessories.md | outdoor-sports.md |
| 旅行装备里哪些是当前热卖款 | 1.00 | 0.33 | 1.00 | 1.00 | travel-gear.md,outdoor-sports.md,digital-accessories.md | travel-gear.md |


## 执行证据

- 选集：`all`，22/22 条；完整选集：True。
- 选集内容 SHA-256：`2209e8dfb1709892752159c06e5a1013b825bd719a047ed475370e033e49c97f`。
- 工作区内容 SHA-256：`df6e77619b814aaaf7466ffc50b38d9d1135584b4ba6474d561e627264cc53f5`（包含未提交源文件；详细范围见同名 manifest）。
- 执行状态：**COMPLETED**；门禁：**BLOCK**；门禁范围：`diagnostic`。
- 实际策略：`["category_vector_document_scope_v1"]`。
- 模型、Prompt、数据文件、依赖版本及逐项 hash 均保存在同名 `.manifest.json`。
