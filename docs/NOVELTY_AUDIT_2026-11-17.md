# 独立文献与新颖性审计 — 2026-11-17（Iteration 16）

## 0. 证据范围、来源时点与继承边界

本轮核验日：2026-11-17。先读取 `docs/NOVELTY_AUDIT_2026-11-16.md` 与 `docs/ITERATION15_PRIMARY_RECHECK.md`，再直接访问四个 arXiv abs 页面与其当前版本 HTML；并尝试保存原始 HTML。四个指定 ID 与 abs 返回的标题、版本链接一致：

| ID | abs 当前版本 | 标题 | 本轮来源状态 |
|---|---|---|---|
| `2609.14858` | v2（2026-10-06） | Dream-RSI: Recursive Self-Improvement through Evolving Worlds | abs 的 urllib 请求 SSL EOF；v2 HTML HTTP 200，2,801,764 bytes，SHA-256 见 `raw_fetch_receipts.json` |
| `2609.24972` | v3（2026-10-04） | RRSI: Regularized Recursive Self-Improvement of Agent Harnesses | abs 的 urllib 请求 SSL EOF；v3 HTML HTTP 200，404,674 bytes，SHA-256 见 receipt |
| `2602.14670` | v2（2026-08-19） | FactorMiner: A Self-Evolving Agent with Skills and Experience Memory for Financial Alpha Discovery | abs 与 v2 HTML 均 HTTP 200；HTML 452,804 bytes |
| `2602.12670` | v4（2026-06-14） | SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks | abs 与 v4 HTML 均 HTTP 200；HTML 738,092 bytes |

**本地原始 HTML 补核。**本轮以 Python 标准库直接解析四份已保存文件，四份 `<title>` 均与上表一致，文件均含闭合 `</html>`；直接定位到 SkillsBench `unknown keys are rejected at parse time` 与 `We propose extending the SKILL.md frontmatter`、FactorMiner `check_ic → check_correlation → admit`、Dream-RSI 固定 recorded tree 与 `legal_roots`、RRSI Algorithm 2 `DomainGuard`。这超出了截断 WebFetch 的少量可见内容，但不等于逐行通读全部正文。下文各篇的“截断末尾”专指 WebFetch 提取结果，不代表本地原始 HTML 在该处终止。Dream-RSI 的 `legal_roots` 在本地 HTML 已直接定位，但未完整审计该 API 的字段语义与实现，不能借此确认金融适用性机制。原始响应可能含附加编码数据，本轮不解码。

原始归档尝试与响应头/哈希在 `experiments/artifacts/iteration16/literature/raw_fetch_receipts.json`；保存的四个版本 HTML 也在同目录。`fetch_primary.py` 是归档脚本，不是论文实现复现。abs 页面正文只含元数据与摘要，不把摘要当正文证据。HTML 原始文件可解析，但本审计仍只把明确可读章节/引文作为主张依据；未解码页面中的编码载荷，未下载 PDF/TeX，未审阅外部实现仓库，未复现实验。

本文件将“本轮新检查”与“继承自 2026-11-16/Iteration 15”分开。此前报告中的细节若未在本轮再次直接看到，仅作继承背景，不升级为本轮新证据。

## 1. 本轮新检查：四项指定主文献

### 1.1 Dream-RSI（`2609.14858v2`）

**本轮直接核对。** abs 标题、作者页、摘要与版本历史匹配；HTML 第 3 节明确：`The recorded tree T_i never changes; only the observed portion grows.` 离线 replay 返回已记录子节点而非生成新候选，且 `no outcome outside T_i is produced`。第 3 节的选择是在历史回放池上的平均 replay score 中选择下一在线策略；当前策略包含在候选中，只支持“当前历史池平均回放分数不低于 incumbent”，不支持在线发现、未记录结果或金融适用性单调改善保证。

本轮可读范围还明确看到节点资格/rollout 停止等搜索规则，以及第 4.3 节把 Lasso regularization path 作为跨领域（含 finance）的计算任务；这不是金融业务概念、主体、单位、来源版本或有效时间 validator。未在可读范围建立持久技能的金融准入、运行前撤销、迁移再认证机制。`question.meta` 的完整字段语义未本轮核实；`legal_roots` 名称后来在本地 HTML 被直接定位，但这不确认其完整规则。此前审计中的 API 字段/范围检查结论只能标作继承且受限。HTML 可见末尾报告到附录 D.2 Listing 2、`question.reset()` 附近；未解码附加内容。

**与项目边界。**固定历史树 replay、候选策略选择和重新部署是相邻先例，不能单独申报新颖性。能说的是“本轮明确检查的可读部分未建立等价的金融源时点生命周期机制”；不能说完整论文/代码绝不存在。

### 1.2 RRSI（`2609.24972v3`）

**本轮直接核对。** abs 标题和 v3 版本历史匹配。§3.3 原文明确 critic 在完整评测前读取 candidate diff，并拒绝显式编码任务名、实体名、任务特定值、答案或基准特定逻辑的编辑。pruning 路径是：近期无严格正实测收益的组件成为 deletion targets，交给 proposer 在后续 proposal 中删除，再经过筛选、评测与选择；不是发现后立即运行时撤销。

附录 D.1 Algorithm 2 明确先 `Evaluate`，再执行 `g ← DomainGuard(H_t,H') // per-domain specific checks`，并与历史分数 floor、成本/准入条件共同决定候选准入；因此不能把可见 DomainGuard 顺序写成评测前金融 validator。D.3 可见式（17）为 `w_s ΔS - w_c ΔC + w_n ν_t(H') > 0`，属于稳定性下限和噪声容忍度场景的候选准入规则；没有可见的金融来源版本、有效时间、撤销状态或迁移认证变量。HTML 可见末尾在 D.3 式（17）之后；完整 DomainGuard、权重、后文和仓库未核。

**与项目边界。**RRSI 已有通用泄漏筛查、pruning、成本/分数 gate、DomainGuard 接口和结构新颖性项。项目不能以这些抽象概念单独主张贡献。可见文本未建立项目所称的金融源时点驱动准入、运行前阻止旧技能、撤销传播和迁移再认证组合，但不能外推到未读材料。

### 1.3 FactorMiner（`2602.14670v2`）

**本轮直接核对。** abs 与 HTML 元数据匹配。§3.2 把因子挖掘封装为可复用 Agent Skill，验证流程明确为 `check_ic → check_correlation → admit`；IC/ICIR 由确定性代码计算。§3.3 的 experience memory 保存成功模式与因高相关而拒绝的方向，并作为 prompt-level constraint；这不是技能权限撤销名单。§3.4 与附录 A 的 admission/replacement 对象明确是金融因子及因子库成员：候选因子进入库，或由高质量候选替换一个相关的既有因子，不是持久 skill 的撤销/迁移。

本轮也核对了跨市场配置与时间实验文字：配置切换支持不同市场；2024-Q1 至 Q4 为训练/选择、2025 为 held-out 测试，Top-40 在 CSI500（2024）选择后冻结。可见材料未建立金融文档概念/主体/单位/源版本适用性，也未建立持久 skill 撤销、迁移映射或迁移后再认证。相关性去冗余不等于 FWER/FDR 或聚类推断。HTML 可见至附录 D 因子 014 后截断；未核因子 015–110、实现与数值复现。

**与项目边界。**FactorMiner 是直接金融相邻先例，必须在论文中承认其金融执行工具、因子验证、准入/替换、经验记忆和跨市场评估；不能把这些写成项目独有。只能把不同的、需实验证明的组合限定为金融源版本/有效时点驱动的技能生命周期治理，并与普通 validator 做直接对照。

### 1.4 SkillsBench（`2602.12670v4`）

**本轮直接核对。** abs 标题、v4 历史和 HTML 匹配。§2 定义 Skill 必须含 `SKILL.md`，可带脚本/模板/参考资料；Skill 本身不是模型权重或可执行工具，而由兼容 harness 注入并暴露资源。Appendix C 针对的是 `task.md`：

- C.1：顶层未知键解析时拒绝，但 free-form `metadata` 内部开放；
- C.2：category、task_type、modality、interface、skill_type、difficulty 属受控层，且“closed tier is enforced at review time rather than at parse time”，无 load-time enumeration check；
- C.3：`network_mode` 为枚举，`allowlist` 必须含非空 `allowed_hosts`，否则解析错误。

这些是普通结构和字段联动 validator 的直接先例；不能把普通 baseline 弱化为“仅 JSON 可解析”。但本轮未审开源 harness/test，规则的代码行为仍是论文作者声明。

§6 原文是 `We propose extending the SKILL.md frontmatter with an explicit complexity contract`，涉及预计 tool/token cost、applicability boundaries 和 lightweight fallback。它是提议，不是当前已实现/强制的 parser requirement；不能把 `task.md` Appendix C 规则偷换成 `SKILL.md` 生命周期治理。可见范围含 Finance & Economics 分类/任务线索，但未建立金融源发布时间、数据版本或时点触发的持久技能准入、撤销、迁移认证。HTML 可见末尾到 Appendix D.6 标题后截断；M.9、N 等仅被引用的附录不能视为已读。

**与项目边界。**SkillsBench 已有配对评测、任务 schema、普通 metadata/网络字段约束；这些不是孤立新颖点。项目须至少对比必填字段、类型/枚举、字段联动、源 ID/日期/有效期规则，以及确定性金融边界规则。

## 2. 本轮新增的近邻核验：不能忽略 FINSKILLOPS 与 ESCROW

### 2.1 FINSKILLOPS（`2609.19680v1`）——重大新颖性风险

本轮直接访问 abs，ID 与标题精确匹配：**FINSKILLOPS: A Self-Evolving Multi-Agent System for SEC Filing QA**，v1，提交 2026-09-17 04:25:17 UTC。摘要直接声称：将重复失败转为 scoped skill patches；用 typed、evidence-grounded failure diagnoses；以 targeted validation、protected-case regression checks、negative controls，以及 versioned replacement or retirement 治理技能；并报告其 SEC filing QA 的 skill registry、promote/reject 与 retirement 方向。

因此，任何“首个金融技能生命周期治理”“首次金融技能准入/撤销/替换”这类宽泛表述在本轮后均不成立或至少未获支持。当前仅核实 abs/摘要；对 `https://arxiv.org/html/2609.19680v1` 的 WebFetch 失败，未获得 HTML 逐节引文，也未归档该文 HTML，不得把摘要扩写为已验证的具体 source-time 机制。应将 FINSKILLOPS 作为必须补全文本/代码核验的直接金融先例，并将项目贡献收窄到明确超出其 SEC QA 范围、且有实验支持的差异。

### 2.2 `2608.01772`——实际是 ESCROW，不是 FRAMES

本轮 abs 直接核验：最新是 v2（2026-10-01 04:00:59 UTC），标题为 **ESCROW: Guarded and Dual-Objective Continual Maintenance for Agents in Policy-Governed Enterprise Workflows**，不是“FRAMES”。其摘要明确：LLM 提议候选修订但只有 empirical evaluated version 才部署；有 per-category non-regression guard、cross-cycle anti-regression、accuracy-cost Pareto search、versioned auditable diff；摘要还提到内部 financial document-auditing system 与公开 τ-bench transfer probe。

可读 HTML 提取进一步核实：来源条款回链、技能版本化/可读 diff/审计轨迹、分类别非退化门槛、历史案例回归抽样和金融文档审计均是已有相邻机制。可读部分未定义不可变源政策版本、有效/失效日期、撤销传播或正式迁移再认证；HTML 在附录 D.7 开头截断，不能据此断言全文不存在。该文必须作为金融文档技能维护与迁移评估的近邻先例，不得再写成 FRAMES。

### 2.3 不可采信的未来/错引 ID

域研究摘要中的 `2808.17684` 是按年份 2028 的未来 ID；相对于本审计日期 2026-11-17 不可作为已发表/可用先例。没有把它写入已验证文献，也没有使用域研究摘要中的自相矛盾指标。

## 3. 继承结论与本轮必须收窄的主张

以下来自 2026-11-16/Iteration 15，且与本轮一致：不能将 generic skill evolution、replay、memory、candidate admission、pruning、cost gate、factor validation/replacement、paired evaluation、schema validation 或普通迁移评测单独申报核心新颖性；未读完整附录/代码时不能把“未见”改写为“不存在”；未复现论文报告的指标，不能把作者结果当独立实验。

本轮新增的决定性收窄是：FINSKILLOPS 摘要已经覆盖 SEC Filing QA 中 scoped patch、保护案例回归、negative controls、versioned replacement/retirement；ESCROW 摘要/可见正文覆盖金融文档审计中的受保护更新边界、分类别回归与可审计版本化。项目若仍主张金融技能生命周期新颖性，必须明确、可证地超出这些邻近工作，例如：

1. 金融源文档的发布时间/数据版本/有效期直接决定概念、主体、单位与计算口径；
2. 这些时点与适用范围变化触发持久技能运行前阻止、撤销传播和迁移再认证；
3. 在相同模型、任务、工具权限、候选、搜索/评估预算下，与 SkillsBench 强普通 validator、确定性金融规则、FINSKILLOPS/ESCROW 可比生命周期基线做消融；
4. 报告错误使用、漏撤销、过度撤销、迁移后正确性、成本及统计聚类/多重选择处理。

这些是待证明的研究假设，不是本审计替项目确认的既有实现或优先权。

## 4. 明确未被本轮证明的事项

- 未证明四项指定论文或 FINSKILLOPS/ESCROW 的完整代码不存在更强金融 source-time 机制；
- 未证明项目自身已经实现上述 lifecycle 组合，也未验证真实金融任务效果；
- 未核对 FINSKILLOPS HTML/PDF/源码；
- 未将 ESCROW 的可读 HTML 截断后附录当作已读；
- 未解码任何 `data:text/plain;base64,...` 或其他编码附件；
- abs 两次 urllib SSL EOF（Dream-RSI、RRSI）意味着本地未保存其 abs 原始响应，但本轮 WebFetch 已直接返回对应 abs 元数据；HTML 原始文件已保存并有哈希；
- 原始 HTML 保存成功不等于论文正文语义已被完整独立验证，解析器/工具输出可能截断。

## 5. 来源文件

- `experiments/artifacts/iteration16/literature/raw_fetch_receipts.json`：四项固定版本 HTML/abs 归档尝试、HTTP 响应、字节数、SHA-256 与 SSL 失败记录。
- `experiments/artifacts/iteration16/literature/2609.14858v2_html.html`
- `experiments/artifacts/iteration16/literature/2609.24972v3_html.html`
- `experiments/artifacts/iteration16/literature/2602.14670_abs.html`
- `experiments/artifacts/iteration16/literature/2602.14670v2_html.html`
- `experiments/artifacts/iteration16/literature/2602.12670_abs.html`
- `experiments/artifacts/iteration16/literature/2602.12670v4_html.html`
- `experiments/artifacts/iteration16/literature/fetch_primary.py`

本轮未修改 MAIN README、ledger 或其他既有审计文件，未提交 git commit。
