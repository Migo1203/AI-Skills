# 个人电商全案与可编辑制作

当前版本0.4.1（2026-11-07；v0.4.0于2026-11-06融合），统一技能名`ecommerce-visual-strategy`。合并个人通用电商视觉v0.3.0与Amazon Listing Studio v0.3.0；国内与Amazon任务不再分别维护两套技能。此补丁简化默认交付：四类目录和一份使用说明，过程记录集中存放，不默认为每次检查生成JSON或HTML。

- [使用说明](使用说明.md)：调用、输入、制作、审稿、定稿检查与常用示例。
- [技能入口](skills/ecommerce-visual-strategy/SKILL.md)：按平台/任务读取参考。
- [统一16类布局库](skills/ecommerce-visual-strategy/references/layout-library.md)：含原个人库六类线框与整页编排。
- [SVG制作流程](skills/ecommerce-visual-strategy/references/editable-production.md)：位图/矢量、交付和用户确认阶段。
- [工具索引](skills/ecommerce-visual-strategy/references/tools.md)：通用工具与Amazon专用检查的边界。
- [来源与许可记录](skills/ecommerce-visual-strategy/来源.md)、[迁移与验证](迁移与验证.md)。

GitHub维护目录为本目录下`skills/ecommerce-visual-strategy`，完整使用说明、开发样例与测试放在本目录。Migo的本地AIGC工作区已将统一入口连接到其本地维护源，并停用旧Amazon入口；仓库上传不会创建其他环境的链接或自动安装技能。GitHub版与本地副本需显式同步。

生图使用宿主实际可用的工具；本项目不包含生图引擎、后台生成服务或平台连接。SVG中照片仍是位图，文案/图形保持独立对象。用户审阅与定稿需要真实反馈，工具通过不等于平台过审。

维护项目包含`examples/`合成输入和`tests/`标准库工具测试；技能文件夹可独立移植，不依赖旧项目路径。从本项目根目录运行：

```text
python -B -m unittest discover -s tests -v
python skills/ecommerce-visual-strategy/scripts/audit_delivery.py examples/demo-delivery.json
python skills/ecommerce-visual-strategy/scripts/resolve_brand.py examples/demo-brand.json --series desk
python skills/ecommerce-visual-strategy/scripts/audit_localization.py examples/demo-delivery.json examples/demo-delivery-de.json examples/demo-localization.json
python skills/ecommerce-visual-strategy/scripts/analyze_experiment.py skills/ecommerce-visual-strategy/assets/experiment-plan.template.json --data examples/demo-experiment-data.json
```

这里的Amazon、品牌、翻译和实验数据全部是合成开发样例，不是真实商品、用户研究或营销结果。样例不能作为正式商品的性能证据。
