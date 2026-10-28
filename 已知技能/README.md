# 已知技能

更新：2026-10-28。集中保存本项目已经阅读、核验过的技能，方便学习、选择和以后创建自己的 Skill。

当前记录 **27 个技能**：7 个已安装或注册到项目，20 个为已知候选。候选资料的保存不会安装或运行这些技能，也不会使它们自动出现在当前云聊天的可用列表中。

按来源查找：[我的技能](../我的技能/README.md)收录3项个人维护技能，分别标为“个人·自建”“个人·融合改编”“个人·原有导出”；其余24项为第三方原版收录。用途分类与来源标记分别记录，个人入口不增加技能总数。

按用途查找：[国内电商视觉设计](分类/国内电商视觉设计.md)（产品分析与策略、详情页与信息图、商业生图服务和外部工作流）。

另见[商业美术指导与品牌视觉](分类/商业美术指导与品牌视觉.md)：产品创意表现、品牌视觉识别和参考图驱动的品牌概念。三项均为方法储备，未验证电商适配或实际提案质量。

## 怎么使用这个文件夹

| 内容 | 用来做什么 | 对后续工作的影响 |
| --- | --- | --- |
| 本页总清单 | 按任务找技能，查看来源、用途和安装状态 | 先从这里选，不需要一次安装所有候选 |
| `源文件/`中的固定版本 | 阅读完整技能目录、配套参考资料和脚本，比较写法或版本 | 可学习具体实现；实际使用仍需对应运行环境，不会自动获得浏览器等工具 |
| 各来源目录的`来源.md` | 查看固定提交、许可证、归档范围及依赖 | 更新时有依据，避免混淆不同版本 |

仓库原有的两份技能和新建融合技能在`plugins/skill-lab/skills/`中维护，本页直接链接，不复制出第二份维护源。其他上游技能按来源分目录归档，保留原文与配套资源；安装副本仍在各项目的`.agents/skills/`中。归档与安装独立，修改一份不代表另一份已同步。

## 已安装或已注册

| 技能与源文件 | 来源标记 | 适合做什么 | 当前项目与状态 |
| --- | --- | --- | --- |
| [study-skill](../plugins/skill-lab/skills/study-skill/SKILL.md) | **个人·自建** | 用中文解释技能的输入、步骤、输出，安排小练习 | AI-Skills：已通过符号链接注册；可直接读取后使用 |
| [plan-ecommerce-visuals](../plugins/skill-lab/skills/plan-ecommerce-visuals/SKILL.md) | **个人·原有导出** | 产品图与电商海报的信息规划、排版和审稿 | AIGC：已通过符号链接注册；保留原有云技能来源 |
| [find-skills](源文件/vercel-labs--skills/skills/find-skills/SKILL.md) | 第三方·原版 | 根据具体任务搜索、比较技能并给出安装选项 | AI-Skills：已安装；联网搜索已验证 |
| [skill-creator](源文件/openai--codex/codex-rs/skills/src/assets/samples/skill-creator/SKILL.md) | 第三方·原版 | 创建、修改和基础校验 Codex 技能 | AI-Skills：已安装；初始化和校验脚本已实测 |
| [frontend-design](源文件/anthropics--skills/skills/frontend-design/SKILL.md) | 第三方·原版 | 网站视觉方向、字体、配色、布局与页面实现 | AIGC：已安装；网站尚未开始实现 |
| [web-design-guidelines](源文件/vercel-labs--agent-skills/skills/web-design-guidelines/SKILL.md) | 第三方·原版 | 对照官方规则检查网页代码 | AIGC：已安装；规则可读取，代码审查待有网站后进行 |
| [ecommerce-visual-strategy](../plugins/skill-lab/skills/ecommerce-visual-strategy/SKILL.md) | **个人·融合改编** | 资料分析、视觉策略、文案、画面提示词与自主PS指导 | 新建v0.1.0，AI-Skills与AIGC项目均已注册；验证范围见[记录](../学习资料/电商视觉策略技能验证.md)，商业美术提案能力仍需改进和验证 |

上表的“已安装”由项目文件与安装清单验证，不等于当前云聊天已自动加载全部技能。

## 已知候选，尚未安装

本节均为**第三方·原版**，用于学习与选择；保存源码不标为个人自建或融合改编。

| 技能与源文件 | 用途与使用时机 | 关键依赖或边界 |
| --- | --- | --- |
| [grill-me](源文件/mattpocock--skills/skills/productivity/grill-me/SKILL.md) | 通过分轮追问明确计划、需求与设计决定 | 入口依赖`grilling`；适合梳理作品集首版范围 |
| [grill-with-docs](源文件/mattpocock--skills/skills/engineering/grill-with-docs/SKILL.md) | 边讨论边维护术语和重要决定 | 依赖`grilling`、`domain-modeling`，会涉及文档写入 |
| [improve-codebase-architecture](源文件/mattpocock--skills/skills/engineering/improve-codebase-architecture/SKILL.md) | 调查现有代码，给出架构改进候选 | 需要已有代码及关联技能；用于结构分析 |
| [tdd](源文件/mattpocock--skills/skills/engineering/tdd/SKILL.md) | 先写行为测试，再实现对应功能 | 需要代码与测试环境；接口未明确时会使用`codebase-design` |
| [setup-matt-pocock-skills](源文件/mattpocock--skills/skills/engineering/setup-matt-pocock-skills/SKILL.md) | 配置任务跟踪、标签和文档约定 | 面向单个代码仓库，会涉及配置写入 |
| [handoff](源文件/mattpocock--skills/skills/productivity/handoff/SKILL.md) | 整理当前对话的进度、决定和文件，便于交接 | 交接文档需要在下一次会话中读取 |
| [triage](源文件/mattpocock--skills/skills/engineering/triage/SKILL.md) | 分类、复现和处理 Issue／按配置处理外部 PR | 需要任务跟踪约定和相应访问权限 |
| [agent-browser](源文件/vercel-labs--agent-browser/skills/agent-browser/SKILL.md) | 浏览器导航、点击、截图和网页测试 | 另需 CLI 和浏览器程序；保存资料不会安装它们 |
| [copywriting](源文件/coreyhaines31--marketingskills/skills/copywriting/SKILL.md) | 根据真实产品资料写标题、卖点和页面文案 | 按实际受众和用途提供资料，缺失事实需说明 |
| [copy-editing](源文件/coreyhaines31--marketingskills/skills/copy-editing/SKILL.md) | 修改已有营销文案，改善清晰度和语气 | 适合已有初稿或局部修改任务 |
| [canvas-design](源文件/anthropics--skills/skills/canvas-design/SKILL.md) | 概念海报、封面和静态视觉艺术 | 含配套字体及其许可；偏艺术表达，产品摄影另需图像工具 |
| [ecommerce-visual-copywriting](源文件/feichanggege--ecommerce-visual-copywriting-skill/SKILL.md) | 国内电商产品分析、购买理由、图组规划、文案与提示词 | 含配套参考与交付模板；当前规则仍需官方核验 |
| [taobao-detail-long-image](源文件/xianyu110--ecommerce-image-skills/skills/taobao-detail-long-image/SKILL.md) | 详情页分屏规划、逐屏提示词、长图拼接和切片 | 拼接需Python/Pillow；作者配置不是平台现行规范 |
| [baoyu-infographic](源文件/jimliu--baoyu-skills/skills/baoyu-infographic/SKILL.md) | 中文卖点信息图、参数对比、结构与流程可视化 | 通用信息图；生图工具和可选API分支需另行配置 |
| [linkpix-taobao-tmall-image](源文件/autoagc--linkpix-skills/skills/linkpix-taobao-tmall-image/SKILL.md) | 淘宝/天猫主图、详情页与活动图的服务工作流 | 依赖青虎账号、qhkit与积分；未接入服务 |
| [linkpix-jd-image](源文件/autoagc--linkpix-skills/skills/linkpix-jd-image/SKILL.md) | 京东主图、套图和活动图的服务工作流 | 依赖同上，未安装 |
| [ecommerce-image-workflow](源文件/nexu-io--open-design/skills/ecommerce-image-workflow/SKILL.md) | 真实产品参照下的主图、卖点图、场景图和素材清单 | 依赖OpenDesign调度与模型环境，未安装 |
| [art-direction](源文件/rampstackco--claude-skills/skills/art-direction/SKILL.md) | 已有品牌下的产品摄影、活动KV和具体交付物美术brief | 非电商专用；需要品牌与渠道输入，未覆盖商品卖点叙事、文案及国内平台规则；归档未安装 |
| [brand-identity](源文件/arnabbagxd--brand-building-skills/skills/brand-identity/SKILL.md) | 品牌识别提案：Logo方向、色彩、字体、摄影与图形语言 | 后续品牌作品集储备；输出brief，不是完整VI成品或电商方案；未安装 |
| [generate-reference-inspired-brand-worlds](源文件/mengto--skills/agent-skills/codex/generate-reference-inspired-brand-worlds/SKILL.md) | 拆解参考图视觉语言，探索品牌campaign概念 | 默认调用生图并生成词标；当前仅学习方法，原样运行不符合用户自主生图与PS分工；未安装 |

## 一起归档的关联技能

以下3项是上述候选引用的关联技能，未计入27项主清单，也没有安装：

- [grilling](源文件/mattpocock--skills/skills/productivity/grilling/SKILL.md)：需求与设计追问。
- [domain-modeling](源文件/mattpocock--skills/skills/engineering/domain-modeling/SKILL.md)：术语和设计决定记录。
- [codebase-design](源文件/mattpocock--skills/skills/engineering/codebase-design/SKILL.md)：代码接口与结构设计。

## 来源和版本

- [Anthropic Skills](源文件/anthropics--skills/来源.md)：`frontend-design`、`canvas-design`。
- [Vercel Skills CLI](源文件/vercel-labs--skills/来源.md)：`find-skills`。
- [Vercel Agent Skills](源文件/vercel-labs--agent-skills/来源.md)：`web-design-guidelines`。
- [OpenAI Codex](源文件/openai--codex/来源.md)：当前 Codex 源码中的`skill-creator`。
- [Matt Pocock Skills](源文件/mattpocock--skills/来源.md)：截图中的7项及3项关联技能。
- [Marketing Skills](源文件/coreyhaines31--marketingskills/来源.md)：`copywriting`、`copy-editing`。
- [Vercel Agent Browser](源文件/vercel-labs--agent-browser/来源.md)：`agent-browser`及配套流程资料。
- [电商视觉策划](源文件/feichanggege--ecommerce-visual-copywriting-skill/来源.md)：`ecommerce-visual-copywriting`。
- [电商详情长图](源文件/xianyu110--ecommerce-image-skills/来源.md)：`taobao-detail-long-image`。
- [Baoyu Skills](源文件/jimliu--baoyu-skills/来源.md)：`baoyu-infographic`。
- [Linkpix Skills](源文件/autoagc--linkpix-skills/来源.md)：淘宝/天猫与京东图像工作流。
- [OpenDesign](源文件/nexu-io--open-design/来源.md)：`ecommerce-image-workflow`。
- [Rampstack美术指导](源文件/rampstackco--claude-skills/来源.md)：`art-direction`。
- [品牌识别提案](源文件/arnabbagxd--brand-building-skills/来源.md)：`brand-identity`。
- [Mengto品牌概念探索](源文件/mengto--skills/来源.md)：`generate-reference-inspired-brand-worlds`。
- 仓库原有两份技能的来源见[技能清单](../技能清单.md)。

后续新增时，记录用途、源仓库和原路径、固定版本、许可、实际依赖，以及“只收录／已安装／已实际验证”的状态。仅有来源链接或文件，不记录为已经成功调用。

[返回仓库首页](../README.md) · [查看技能清单](../技能清单.md)
