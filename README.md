# AI-Skills

Migo 的 Skill 学习与实践仓库：收集有明确来源的技能，学习如何使用，把稳定的工作方法做成自己的 Skill。

AIGC 作品与音箱项目仍在[现有作品仓库](https://github.com/Migo1203/Fun)管理，该仓库计划改名为 AIGC。这里专门管理技能源文件、学习笔记和练习。

## 从这里开始

1. 看[入门与官方参考](学习资料/入门与官方参考.md)，分清“保存源文件”“安装到环境”和“实际调用”。
2. 打开[技能清单](技能清单.md)，查看两份起步技能及其来源。
3. 从[读懂一个 Skill](plugins/skill-lab/skills/study-skill/SKILL.md)开始练习，再阅读自己的[电商视觉规划技能](plugins/skill-lab/skills/plan-ecommerce-visuals/SKILL.md)。
4. 要创建新技能时，使用[SKILL.md 模板](模板/SKILL.md.template)，写一个具体、能重复使用的任务。

## 当前内容

| 内容 | 位置 |
| --- | --- |
| 两份 Skill 的源文件 | [plugins/skill-lab/skills](plugins/skill-lab/skills) |
| Codex 技能插件声明 | [plugin.json](plugins/skill-lab/.codex-plugin/plugin.json) |
| 本仓库的插件目录 | [marketplace.json](.agents/plugins/marketplace.json) |
| 来源、状态与练习记录 | [技能清单](技能清单.md) |

技能采用当前官方示例中的插件结构：`plugins/<插件名>/skills/<技能名>/SKILL.md`。插件清单放在 `.agents/plugins/marketplace.json`，指向本仓库的 `./plugins/skill-lab`。标准目录与英文 slug 保留规范名称，学习资料使用中文。

**文件保存到 GitHub，不代表当前 Codex 聊天已经安装或启用了这些技能。** 在支持工作区插件的 Codex 环境中打开本仓库，再按该环境的插件入口发现、安装或启用；以界面和实际可用技能列表为准。具体操作见[入门说明](学习资料/入门与官方参考.md)。

以后安装新技能，请提供来源链接和准备解决的任务；登记来源与版本，再验证一次实际调用。这个起步仓库没有安装未指定的第三方技能。
