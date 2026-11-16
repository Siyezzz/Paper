# 独立文献与新颖性审计 — 2026-11-16

## 范围与证据等级

本轮先读取 `docs/NOVELTY_AUDIT_2026-11-15.md` 了解旧边界，再分别调用 WebFetch 访问下列四项原始 arXiv abs 页面和对应版本 HTML。四项 abs 与四项 HTML 均成功返回；本文件中的元数据与方法判断来自本轮返回内容，不是将旧结论改日期。工具对 HTML 提供的是提取/归纳结果，且四项正文均报告截断；没有下载或通读完整 PDF，没有审阅任何实现仓库，没有复现实验。因此，下文“未见/未核实”仅限返回范围，不能改写成论文或代码绝对不存在相应机制。版本日期按 arXiv UTC 记录；核验日为 2026-11-16。

运行状态补注：文献代理最近一次调用被系统报告为上游网关空响应，该次调用没有可用输出，不能作为成功核验。磁盘上的本审计记录先前抓取；主代理随后重新请求四个版本 HTML，独立核对了 replay、RRSI 式 (17)、因子替换以及 SkillsBench 附录 C/第 6 节等关键边界。此补核仍是提取后的截断文本，不是完整 PDF 或源码审查。Dream-RSI D.2 元数据接口在此次返回中依赖附带编码载荷，不属于截断前直接可见行；不将该接口细节当作直接展示文本的独立确认。本轮可见范围与旧审计不同：RRSI 已返回 D.3 式 (17)，SkillsBench 的附录 C metadata 约束已可见，必须据此更新措辞。未覆盖的旧结论不自动获得重新验证资格。

## 1. Dream-RSI

### 元数据与实际访问 URL

- abs：https://arxiv.org/abs/2609.14858
- HTML：https://arxiv.org/html/2609.14858v2
- 标题：**Dream-RSI: Recursive Self-Improvement through Evolving Worlds**。
- 作者（按 abs 顺序）：Tong Zheng; Xidong Wu; Zheng Zhang; Zhankui He; Chaoyi Zhang; Benjamin Coleman; Ruoqiao Wei; Di Bai; Haolin Liu; Rui Liu; Xue Wang; Yue Zhuan; Wang-Cheng Kang; Renkai Xiang; Heng Huang; Xinwu Cheng; Yunsong Guo。
- 版本：v1 = 2026-09-14 00:10:47 UTC；v2 = 2026-10-06 09:37:58 UTC。此次 abs 指向 v2。

### 本轮可见的方法与限制

摘要描述：保持基础 agent 不变，通过轻量编排层显式编程探索策略，将已积累的 discovery history 作为 replay simulator，在历史树内获得低成本 off-policy 反馈，再部署改进策略进行在线发现。

§3 Offline evaluation 原文：

> “The recorded tree T_i never changes; only the observed portion grows.”
> “Unlike online execution, offline replay returns recorded children of the selected nodes deterministically rather than generating new candidates.”
> “no outcome outside T_i is produced.”

回放只能揭示历史树既有子节点，不能证明对未探索动作的预测能力。§3 形式化描述中，从根揭示创建时间最早且尚未揭示的子节点，非根节点揭示唯一已记录后继；策略改变推进、分组和停止，不能跳过祖先获取深层结果。

§3 明确 `pi_t^0 = pi_t`，附录 B.2 配置为 incumbent 加三个新策略版本，M=4。§3 Policy improvement and selection 在固定历史池 H_t 上对各树 replay 分数取均值并选最大者，因此所选策略的同池平均 replay 分数不低于 incumbent。公式 (1) 将质量—调用预算曲线的归一化 hypervolume 与并行惩罚合成；它不保证每棵树、每个预算、独立质量分量、下一轮在线发现或新世界泛化逐项改善，也不保证跨变化历史池的数值单调性。§4 的 discovery cost 是 discovery-agent 调用数，不能等同端到端 token、费用或实际耗时。

本轮新增边界：D.2 提示词可见 `question.meta(cell_id) -> CellMeta` 及 branch/attempt/parent_id/seq/tags，存在网格宽度和深度范围检查；这是 metadata 接口及局部结构校验，不是已验证的金融语义/时间有效性 validator。§3 单根依次揭示与 D.2 多个 `legal_roots()` 的接口描述存在口径差异，本轮未审代码，不能消解。

### 与本项目的比较

历史回放、候选保留 incumbent、策略迭代均不能单独构成本项目的新颖性。可见范围未建立金融口径和源版本的适用性判定、持久技能运行前撤销或重新准入的完整机制，也未见与普通 metadata validator 的该类对照。但这只是待比较的研究空间，不是独占优先权证明。固定池选择性质不能充当本项目在线金融任务改善或统计显著性的证据。

抓取限制：返回报告在 D.2 带行号代码第 30 行 `question.reset()` 附近截断；B.3 仅见标题，E.1/E.2 被引用但实际程序未见，图的完整曲线数据未核。未验证正式多重比较校正或聚类推断，不能断言完整论文没有。

## 2. RRSI

### 元数据与实际访问 URL

- abs：https://arxiv.org/abs/2609.24972
- HTML：https://arxiv.org/html/2609.24972v3
- 标题：**RRSI: Regularized Recursive Self-Improvement of Agent Harnesses**。
- 作者（按 abs 顺序，保留网页拼写）：Peng Xia; Rujun Han; Zifeng Wang; Yanfei Chen; Yufan Zhuang; Yoonho Lee; Chengsong Huang; Han Yu; Zhongying CuiZhu; Yifei Ming; Huaxiu Yao; Burak Gokturk; Tomas Pfister; Chen-Yu Lee。
- 版本：v1 = 2026-09-21 17:54:49 UTC；v2 = 2026-09-23 22:10:39 UTC；v3 = 2026-10-04 02:18:13 UTC。

### 本轮可见的方法与限制

摘要与 §3 描述对冻结 backbone 周围的 prompts/control flow/tooling/memory/context management 进行演化；proposer 使用随轮次退火的编辑预算并鼓励未探索路径，selector 使用 critic 和 pruner。

§3.3 Leakage Screening 原文：

> “Before full evaluation, a critic reads each candidate diff and rejects edits that explicitly encode task names, entity names, task-specific values, answers, or other logic specific to the evolve benchmark, as well as edits that add inert machinery.”

D.1 Algorithm 1 强调 critic 读取 diff，不是 proposal。§3.3 与 D.2 的 pruning 将近期没有严格正实测增益的组件报告给 proposer，作为 subsequent proposals 的 deletion targets。多编辑候选共享候选级 ΔS、ΔC 和结果，并非每组件独立因果消融。后续删除候选仍需评测和通过 gates；不能称为立即运行时撤销。

Algorithm 2 的硬条件包括历史分数 floor `S_hat' >= S* - delta`、成本/收益条件以及 `DomainGuard(H_t,H')`。delta 由重复评测不变 base harness 得到经验噪声带，DomainGuard 仅见 “per-domain specific checks”，具体规则未见。

本轮实际见到 D.3 式 (17)，更新旧审计的截断边界：若 `ΔS > delta`，使用 `ΔC <= beta_0 + beta_1 ΔS`；否则使用 `w_s ΔS - w_c ΔC + w_n nu_t(H') > 0`，并仍需通过历史 floor。nu_t 对此前未出现在获胜编辑中的 client_tool/skill/memory/subagent 类型计数。它不是金融语义或有效期校验。Algorithm 2 的 “no credit for score” 注释与式 (17) 仍含 w_sΔS 的关系需保留；权重未核，不能自行解释为分数项恒为零。

另一个未消解口径：§3.3 称 S* 为 “best evolve-set score observed so far”，Algorithm 2 第 19 行仅用获选下一 incumbent 更新 S*。未通过成本/DomainGuard 的高分候选是否计入最高分，不能由本轮算法文字统一。

### 与本项目的比较

通用候选准入、泄漏筛查、删减无收益组件、成本 gates、跨模型/基准评估已是明显相邻工作，本项目不能以这些抽象概念申报贡献。可见 pruning 不等于因金融口径、数据源时点或适用范围变化触发的运行前撤销，也未见金融专用技能迁移再认证或普通 metadata validator 对照。应将这些列为需通过任务和代码证实的差异，不应宣称 RRSI 不具备所有撤销能力。经验噪声带不等同正式序贯/多重比较校正。

抓取限制：本轮返回在 D.3 式 (17) 后标记截断，未核完整 DomainGuard、权重与所有后续超参数；abs 虽给代码链接，未访问或审阅仓库。

## 3. FactorMiner

### 元数据与实际访问 URL

- abs：https://arxiv.org/abs/2602.14670
- HTML：https://arxiv.org/html/2602.14670v2
- 标题：**FactorMiner: A Self-Evolving Agent with Skills and Experience Memory for Financial Alpha Discovery**。
- 作者：Yanlong Wang; Jian Xu; Hongkang Zhang; Shao-Lun Huang; Danny Dongning Sun; Xiao-Ping Zhang。
- 版本：v1 = 2026-02-16 11:48:52 UTC；v2 = 2026-08-19 04:16:20 UTC。

### 本轮可见的方法与限制

§3.2 的 Modular Skill Architecture 将系统金融评估封装为执行工具，包含金融算子、确定性 IC/ICIR 计算和验证。§3.3 的 Experience Memory 将成功模式与失败约束蒸馏为紧凑自然语言模板及典型例子，根据因子库诊断和近期拒绝原因检索，作为生成提示约束。§4.1 明言不更新 LLM 权重，自演化来自 retrieval-conditioned generation、deterministic skill execution、library admission 和 memory distillation。

§3.2 原文流程：

> “check_ic → check_correlation → admit”

§3.4 Algorithm 1 可见快速 |IC| 筛选、对既有因子库的绝对相关性过滤、replacement check、批内去重、全量验证、因子入库与记忆更新。replacement 的对象是因子：新因子 alpha 与一个既有 g* 冲突、与其余均不冲突且质量提升达门槛时，替换 g*。附录 A 更具体写单个 correlated factor 替换；不能改写为持久 skill 的撤销或替换。

§3.1 式 (3) 的 rho 是逐时点横截面 Spearman 相关的时间平均，本身有符号；主要约束使用 |rho|。主算法 Stage 2/2.5 和附录 A 式 (10) 使用绝对值，但 A 式 (11) 的替换集合使用 `rho(alpha,g) > theta`，Stage 3 的批内 rho 也未显式取绝对值。主算法初筛使用 |IC|，附录入库/替换直接写 IC。需要审实现才能统一方向处理；Table 1 的绝对均值 `|E[IC_t]|` 不等于 `E[|IC_t|]`。

时间实验口径：§4.1 写训练期 2024-Q1 至 Q4、held-out 2025。§4.2.1 与 Table 1 明确 Top-40 在 CSI500 (2024) 选一次并冻结，2025 跨数据集评估；组合权重/方向由 2024 确定。§4.2.4 Table 4 是完整 110 因子库直至 2026-Q1 的另一实验，不能与冻结 Top-40 实验混称。

### 与本项目的比较

金融执行工具、因子准入与替换、经验记忆、数据集迁移均不能作为本项目孤立新颖点。FactorMiner 已经是金融领域直接相关工作。因子有效性与金融文档概念/单位/主体/源版本的正确性是不同测试对象；配置市场上下文与冻结样本外测试，不自动等于技能生命周期中按源时点、口径变化作准入/撤销/迁移再验证。可见文本未给这类技能治理或普通 metadata validator 对照，但不得外推至未读代码。相关性去冗余不等于 familywise/FDR 校正；未验证正式多重比较或聚类统计方法。

抓取限制：本轮正文返回到附录 D 因子 014 附近截断；论文声称 110 因子，不代表本轮核对了全部公式。未读完整 PDF、未审执行代码、未复现 IC 或收益。

## 4. SkillsBench

### 元数据与实际访问 URL

- abs：https://arxiv.org/abs/2602.12670
- HTML：https://arxiv.org/html/2602.12670v4
- 标题：**SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks**。
- 作者（按 abs 顺序）：Xiangyi Li; Yimin Liu; Wenbo Chen; Bingran You; Zonglin Di; Yifeng He; Shenghan Zheng; Kyoung Whan Choe; Jiankai Sun; Shuyi Wang; Chujun Tao; Binxu Li; Xuandong Zhao; Hejia Geng; Xiaojun Wu; Junwei Zhou; Xiaokun Chen; Hanwen Xing; Yubo Li; Qunhong Zeng; Di Wang; Yuanli Wang; Roey Ben Chaim; Penghao Jiang; Haotian Shen; Luyang Kong; Xinyi Liu; Runhui Wang; Xuanqing Liu; Jiachen Li; Xin Lan; Yueqian Lin; Wengao Ye; Junwei He; Songlin Li; Yue Zhang; Yipeng Gao; Yijiang Li; Ze Ma; Liqiang Jing; Tianyu Wang; Kaixin Li; Yiqi Xue; Haoran Lyu; Yizhuo He; Yuchen Tian; Shutong Wu; Bowei Wang; Yixuan Gao; Bo Chen; Litong Liu; Sikai Cheng; Jiajun Bao; Shuaicheng Tong; Shuwen Xu; Terry Yue Zhuo; Tinghan Ye; Qi Qi; Miao Li; Longtai Liao; Zelin Tan; Chang Shi; Xilin Tang; Srinath Tankasala; Boqin Yuan; Yaoyao Qian; Jianhong Tu; Chenguang Wang; Yizhou Sun; Wei Wang; Aaron Taylor; Ziyue Yang; Changkun Guan; Zhikang Dong; Xinyu Zhang; Steven Dillmann; Han-chung Lee; Dawn Song。
- 版本：v1 = 2026-02-13 07:06:06 UTC；v2 = 2026-03-07 00:51:15 UTC；v3 = 2026-03-13 07:33:01 UTC；v4 = 2026-06-14 21:21:07 UTC。

### 本轮可见的方法与限制

§4 与 D.1–D.2 描述 87 tasks × 18 configurations × 2 conditions × 3 trials = 9,396-slot frame，并报告 9,396 selected public result files；这不证明 9,396 个独立观测。两条件为 no Skills 与 curated Skills，self-generated 条件另报。§4 先在每任务三试验平均，再跨固定任务平均；配对差值定义于 `(configuration, task)`，不是未配对 pool，未核三次 trial 的随机种子是否一一配对。

§2 说明 Skill 包必须有 SKILL.md，可含 scripts/templates/reference/examples：

> “a Skill is neither model weights nor an executable tool by itself; it becomes actionable through a compatible harness that injects its instructions and exposes its resources.”

所以不能将所有 Skill 等同执行工具，也不能说所有 Skill 都只有文字。§6 使用 “We propose extending the SKILL.md frontmatter with an explicit complexity contract”，包括 expected tool/token cost、applicability boundaries 与 lightweight fallback；本轮未见该提议已实现并被强制校验的证据。

### 本轮新增的普通 metadata validator 证据

附录 C.1–C.3 实际可见，不能再笼统写“未见 metadata validator”：

| 可见规则 | 实际约束范围 |
|---|---|
| C.1 “unknown keys are rejected at parse time” | 顶层 schema 在解析时拒绝未知键 |
| C.1 “values within the free-form metadata block are open by design” | metadata 内部是开放映射，顶层严格不代表所有内部语义严格 |
| C.2 “The closed tier is enforced at review time rather than at parse time”；“no load-time enumeration check” | 受控 metadata 词表在审核阶段约束，没有加载时枚举校验 |
| C.3 allowlist 要求非空 allowed_hosts，否则解析错误 | 网络配置具有明确字段联动约束 |

这些是普通结构/字段约束的直接相关证据，而非与本项目机制的实证对照实验。Finance & Economics 在 §5.1.2 Table 3 有 9 个任务，但领域定义指向不可见的 Appendix M.9/Table 19，不能补写具体金融任务定义。基准收录有质量评分、泛化要求及泄漏审查；它们不同于生产技能随金融源版本变化的运行前再准入。

### 统计与治理边界

图注可见 95% CIs；Appendix N 被引用但未返回其正文，因此 CI 构造、bootstrap 是否配对、聚类单位、multiplicity 均未核。§7 的 paired bootstrap CIs 短语描述相关工作，不能移植为本论文方法。本轮未见金融技能有效期、失效撤销、版本迁移再认证的完整协议；这不是不存在断言。配对评估本身已是已有原则，本项目不能仅以“paired evaluation”主张新颖。

抓取限制：正文在 Appendix D.6 标题后截断；N 与 M.9 未见。未检查公开结果文件、validator 源码或每个任务。

## 5. 新颖性边界与必须完成的对照

以上证据只支持收窄贡献边界，不能确立“首个”或优先权。应删除/避免将通用 skill 演化、执行工具、记忆、candidate admission、pruning、cost gate、迁移、固定历史池单调选择、配对评估或 schema 验证单独作为核心贡献。

可检验的研究主张应具体到：金融源文档及其发布时间/数据版本确定概念、主体、单位和计算口径；技能有显式适用范围；新增证据或口径变化会影响持久技能的准入、运行前阻止使用、撤销和迁移后再验证；该机制对真实模型生成并持久保存的技能提供超出普通 validator 的增量。这里描述的是待证实贡献，不代表本轮验证本仓库已经实现这些行为。

最低限度对照应保持同一基座模型、任务、候选来源、工具权限、搜索与评价预算：

1. 普通 metadata validator：必填字段、类型/枚举、schema 及字段联动、直接可比较的日期/有效期/源ID规则。不得故意弱化为只检查 JSON 是否能解析；SkillsBench C 已证明结构校验与字段联动并非新概念。
2. 更强确定性规则基线：为已知金融口径/日期边界写普通规则，评估学习技能是否真正超出规则可解决范围；同一规则若只是换包装，不构成新增能力。
3. 增加模型生成并持久化技能的完整生命周期机制，并消融准入、撤销、迁移再验证，分别报告错误使用/漏撤销/过度撤销、任务正确率与成本。
4. 任务按真实来源版本与可用时点构造；训练、技能生成与选择不得读取未来文档/目标答案。以独立文档或实体/事件族作为留出及推断单位，不能将同源重写或多次 trial 当独立样本。
5. 锁定测试集与选择流程后做等预算配对比较，说明聚类/重采样与多重选择的处理。固定池最大化、噪声带、因子相关性过滤都不能代替这类统计论证。

当前四项返回范围都不足以证明对方没有上述完整组合；本轮也未验证本项目真实金融任务效果。最稳妥表述是：在本轮明确检查的章节中，未建立与本项目所拟金融口径/时间适用性生命周期机制等价的实现与普通 validator 对照；需要继续阅读剩余附录/代码并完成项目实验，才能升级新颖性与有效性结论。
