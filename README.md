# AI-Skills

Migo 的 Skill 学习与实践仓库：收集有明确来源的技能，学习如何使用，把稳定的工作方法做成自己的 Skill。

AIGC 作品与音箱项目在 [AIGC 仓库](https://github.com/Migo1203/AIGC)管理。这里专门管理技能源文件、学习笔记和练习。

## 从这里开始

1. 看[入门与官方参考](学习资料/入门与官方参考.md)，分清“保存源文件”“安装到环境”和“实际调用”。
2. 打开[技能清单](技能清单.md)，查看本仓库维护的三份技能及其来源；更多已核验技能与源码见[已知技能](已知技能/README.md)。
3. 从[第一次练习](学习资料/第一次练习.md)了解已完成的使用示例，再阅读[学习技能](plugins/skill-lab/skills/study-skill/SKILL.md)和自己的[电商视觉规划技能](plugins/skill-lab/skills/plan-ecommerce-visuals/SKILL.md)。
4. 做产品分析、视觉策略、背景/概念图提示词与自主PS排版时，使用新建的[电商视觉策略与PS指导](plugins/skill-lab/skills/ecommerce-visual-strategy/SKILL.md)。它结合两份来源技能，保留原版，默认只交付文字方案。
5. 要创建新技能时，使用[SKILL.md 模板](模板/SKILL.md.template)，写一个具体、能重复使用的任务。

## 当前内容

| 内容 | 位置 |
| --- | --- |
| 三份 Skill 的源文件 | [plugins/skill-lab/skills](plugins/skill-lab/skills) |
| 融合技能的验证范围与结果 | [电商视觉策略技能验证](学习资料/电商视觉策略技能验证.md) |
| Codex 技能插件声明 | [plugin.json](plugins/skill-lab/.codex-plugin/plugin.json) |
| 本仓库的插件目录 | [marketplace.json](.agents/plugins/marketplace.json) |
| 来源、状态与练习记录 | [技能清单](技能清单.md) |
| 已知技能、固定版本源码与来源说明 | [已知技能](已知技能/README.md) |

技能采用当前官方示例中的插件结构：`plugins/<插件名>/skills/<技能名>/SKILL.md`。插件清单放在 `.agents/plugins/marketplace.json`，指向本仓库的 `./plugins/skill-lab`。标准目录与英文 slug 保留规范名称，学习资料使用中文。

**文件保存到 GitHub，不代表当前 Codex 聊天已经安装或启用了这些技能。** 在支持工作区插件的 Codex 环境中打开本仓库，再按该环境的插件入口发现、安装或启用；以界面和实际可用技能列表为准。具体操作见[入门说明](学习资料/入门与官方参考.md)。

以后安装新技能，先明确准备解决的任务，核验来源、版本和依赖，再验证实际调用。两个项目目前的项目级安装状态见[已知技能](已知技能/README.md)；归档候选源码不会安装或自动启用这些候选。
