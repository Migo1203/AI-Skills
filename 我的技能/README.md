# 我的技能

更新：2026-11-07。这里收录由 Migo 创建、融合改编或维护的技能；具体来源以各项标记为准。

目前共 **3 项个人维护技能**：1项自建、1项融合改编、1项用户原有云技能导出。它们已经计入全仓库的29项清单，本页不重复计数。第三方原版技能见[已知技能](../已知技能/README.md)。

## 个人技能档案

| 技能与源文件 | 来源标记 | 用途分类 | 版本与验证状态 | 来源说明 |
| --- | --- | --- | --- | --- |
| [ecommerce-visual-strategy](../plugins/skill-lab/skills/ecommerce-visual-strategy/SKILL.md) | **个人·融合改编** | 国内电商＋Amazon全案／文案、16类布局、素材与SVG、用户改稿及定稿检查 | v0.4.1；融合本地Amazon项目，含品牌、本地化、批量与实验模块；38项工具测试及结构校验通过，见[记录](../plugins/skill-lab/迁移与验证.md)；真实成图、编辑兼容与商业效果待验证 | [来源与许可](../plugins/skill-lab/skills/ecommerce-visual-strategy/来源.md) |
| [study-skill](../plugins/skill-lab/skills/study-skill/SKILL.md) | **个人·自建** | 学习辅助／读懂和试用Skill | 未单独设版本；已有直接读取后使用的[练习记录](../学习资料/第一次练习.md) | [创建记录](../plugins/skill-lab/skills/study-skill/来源.md) |
| [plan-ecommerce-visuals](../plugins/skill-lab/skills/plan-ecommerce-visuals/SKILL.md) | **个人·原有导出** | 电商视觉／信息规划、排版与审稿 | 未单独设版本；保留云端原文及原有使用记录 | [导出来源](../plugins/skill-lab/skills/plan-ecommerce-visuals/来源.md) |

“个人·自建”表示根据 Migo 需求由 Codex 辅助编写；“个人·融合改编”保留引用的上游来源与许可；“个人·原有导出”仅说明来自用户原有云技能，不据此推定其为本仓库原创。

## 源文件与维护位置

本文件夹是个人技能的归档和查找入口。三份技能的维护源仍在`plugins/skill-lab/skills/`，点击上表即可查看完整目录中的入口与配套文件；不另外复制或移动，以继续使用现有调用路径、插件声明和项目链接。

`ecommerce-visual-strategy`的两份来源继续保留。新收录的`art-direction`、`brand-identity`和`generate-reference-inspired-brand-worlds`仍归[第三方方法储备](../已知技能/分类/商业美术指导与品牌视觉.md)，没有加入融合版。商业提案的后续验证在[AIGC独立任务](https://github.com/Migo1203/AIGC/tree/main/任务/商业视觉提案验证)推进。

历史v0.2.0新增[电商布局参考库](../plugins/skill-lab/skills/ecommerce-visual-strategy/references/layout-library.md)，把单图/整页布局选择、系列样式与PS衔接接入现有流程。学习amazon-image-skill的布局选择思路后重新编写，原档继续保留，未把无明确许可的模板原文复制进个人技能。

## 当前版本使用

2026-11-07同步v0.4.1，统一调用`$ecommerce-visual-strategy`，不再单独安装amazon-listing-studio。六类旧布局去重合并到16类库，保留原线框和整页方法；Amazon规则在专用模块读取，国内稿不套Amazon校验。完整示例见[使用说明](../plugins/skill-lab/使用说明.md)。v0.4.1将交付整理为四类目录及一份使用说明，JSON/HTML按需生成。默认制作到用户审阅包，用户确认最终版后AI只检查指定文件。

## 归档标记约定

- 来源性质与用途分开记录：自建、融合改编、原有导出、第三方原版分别标明，再填写学习辅助、电商视觉等用途。
- 每项链接到唯一维护源及来源说明；融合改编保留上游版本、署名与许可，第三方原版不标成个人原创。
- 版本与验证范围按实际记录填写；“已归档”“已安装或注册”“已验证效果”分别记录。没有单独版本号时以Git提交追踪，不补造版本。

本轮更新ecommerce-visual-strategy及配套说明、模板、脚本、样例和测试，保留其技能名称与其他个人技能；插件元数据随新范围更新。GitHub源文件同步不代表已在其他环境安装。

[返回仓库首页](../README.md) · [三份技能维护清单](../技能清单.md) · [全部已知技能](../已知技能/README.md)
