# AI-Skills

Migo 的 Skill 学习与实践仓库：收集有明确来源的技能，学习如何使用，把稳定的工作方法做成自己的 Skill。

AIGC 作品与音箱项目在 [AIGC 仓库](https://github.com/Migo1203/AIGC)管理。这里专门管理技能源文件、学习笔记和练习。

## 从这里开始

1. 看[入门与官方参考](学习资料/入门与官方参考.md)，分清“保存源文件”“安装到环境”和“实际调用”。
2. 打开[我的技能](我的技能/README.md)，按“个人·自建／融合改编／原有导出”找到三份个人维护技能；维护状态见[技能清单](技能清单.md)，第三方技能与源码见[已知技能](已知技能/README.md)。
3. 从[第一次练习](学习资料/第一次练习.md)了解已完成的使用示例，再阅读[学习技能](plugins/skill-lab/skills/study-skill/SKILL.md)和自己的[电商视觉规划技能](plugins/skill-lab/skills/plan-ecommerce-visuals/SKILL.md)。
4. 做国内电商或Amazon文案、主图、详情页和A+时，使用[个人电商全案与可编辑制作 v0.4.1](plugins/skill-lab/skills/ecommerce-visual-strategy/SKILL.md)。统一流程为AI策划→按规划制作素材与SVG→用户审稿调整→用户定稿→AI检查；[完整使用说明](plugins/skill-lab/使用说明.md)包含调用示例与工具边界。生图取决于环境实际能力，上传仓库不等于已启用。
5. 要创建新技能时，使用[SKILL.md 模板](模板/SKILL.md.template)，写一个具体、能重复使用的任务。

## 三项设计技能：范围与入口

更新：2026-11-15。完整适用范围与NED项目用法分别记录，源码已收录，不等于自动安装或全部场景已实测。

| 技能 | 完整定位与适用对象 | 入口 |
| --- | --- | --- |
| taste-skill | 前端网页视觉设计与实现：品牌官网、产品／服务网站、店铺与作品集等 | [来源与源码](已知技能/源文件/Leonxlnx--taste-skill/来源.md) |
| Impeccable | 跨平台界面与体验设计：网页、产品UI、组件、后台，以及原生iOS／Android界面 | [来源与源码](已知技能/源文件/pbakaus--impeccable/来源.md) |
| diagram-design | 多载体信息图解：架构、流程、图表、用户旅程等，服务于PPT、报告、文章、社媒与文档 | [来源与源码](已知技能/源文件/cathrynlavery--diagram-design/来源.md) |

[完整适用范围、官方依据与使用示例](已知技能/分类/界面设计与信息图解技能.md)。taste-skill旧合集的迁移关系也在该页说明，不能把其他仓库的功能算作当前已收录。

## 当前内容

| 内容 | 位置 |
| --- | --- |
| 我的技能：自建、融合改编与原有导出 | [个人归档入口](我的技能/README.md) |
| 三份 Skill 的源文件 | [plugins/skill-lab/skills](plugins/skill-lab/skills) |
| 统一技能使用说明 | [v0.4.1使用说明](plugins/skill-lab/使用说明.md) |
| 最新融合迁移与验证 | [融合迁移与交付组织验证](plugins/skill-lab/迁移与验证.md) |
| 历史融合技能的验证范围与结果 | [电商视觉策略技能验证](学习资料/电商视觉策略技能验证.md) |
| Codex 技能插件声明 | [plugin.json](plugins/skill-lab/.codex-plugin/plugin.json) |
| 本仓库的插件目录 | [marketplace.json](.agents/plugins/marketplace.json) |
| 来源、状态与练习记录 | [技能清单](技能清单.md) |
| 前端视觉、跨平台UI／UX与信息图解三项技能 | [完整范围与用法](已知技能/分类/界面设计与信息图解技能.md) |
| 已知技能、固定版本源码与来源说明 | [已知技能](已知技能/README.md) |
| 品牌基础、视觉识别、角色IP与网站系统候选 | [品牌设计与角色IP](已知技能/分类/品牌设计与角色IP.md) |
| 2026-11-09品牌归档与文件核验 | [本轮归档记录](学习资料/品牌技能归档-2026-11-09/README.md) |
| 商业美术、品牌视觉候选与电商适用范围 | [商业美术指导与品牌视觉](已知技能/分类/商业美术指导与品牌视觉.md) |

技能采用当前官方示例中的插件结构：`plugins/<插件名>/skills/<技能名>/SKILL.md`。插件清单放在 `.agents/plugins/marketplace.json`，指向本仓库的 `./plugins/skill-lab`。标准目录与英文 slug 保留规范名称，学习资料使用中文。

**文件保存到 GitHub，不代表当前 Codex 聊天已经安装或启用了这些技能。** 在支持工作区插件的 Codex 环境中打开本仓库，再按该环境的插件入口发现、安装或启用；以界面和实际可用技能列表为准。具体操作见[入门说明](学习资料/入门与官方参考.md)。

以后安装新技能，先明确准备解决的任务，核验来源、版本和依赖，再验证实际调用。两个项目目前的项目级安装状态见[已知技能](已知技能/README.md)；归档候选源码不会安装或自动启用这些候选。
