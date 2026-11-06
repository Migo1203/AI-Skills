# 本地工具的适用范围

所有工具只用Python 3标准库，不联网、不生图、不修改已有设计文件、不上架。命令从技能目录运行；示例资料在维护项目的`examples/`，独立搬走技能目录后可用自己的输入文件替换。

| 工具 | 可用任务 | 明确边界 |
| --- | --- | --- |
| `scripts/resolve_brand.py` | 任意平台品牌→系列→任务样式解析 | 记录逐字段来源；不验证字体/素材许可或品牌真实性 |
| `scripts/analyze_experiment.py` | 符合输入定义的二项A/B计划与数据 | 只支持预指定独立用户二项指标、固定样本；不支持平台所有实验报表 |
| `scripts/audit_delivery.py` | Amazon交付v1单SKUJSON | 带有Amazon保守主图/A+字段约定，不用于国内稿件判定；不看SVG或实际图像 |
| `scripts/audit_localization.py` | Amazon交付v1的源/目标JSON及本地化表单 | 方法可共享，脚本仍依赖上述格式；不检查翻译语义或所有未记录数值 |
| `scripts/batch_workflow.py` | Amazon交付v1多项prepare/audit | 只准备任务和汇总机械检查；没有自动文案生成、支付调用或通用平台适配 |

```text
python scripts/resolve_brand.py brand.json --series desk
python scripts/analyze_experiment.py experiment-plan.json
python scripts/analyze_experiment.py experiment-plan.json --data experiment-data.json
python scripts/audit_delivery.py amazon-delivery.json
python scripts/audit_localization.py source.json target.json localization.json
python scripts/batch_workflow.py prepare amazon-manifest.json --output batch-run
python scripts/batch_workflow.py audit amazon-manifest.json --output batch-run
```

相关格式见[品牌](brand-profile.md)、[实验](experiments.md)、[本地化](localization-and-audience.md)、[Amazon交付](amazon/delivery.md)、[Amazon批量](amazon/batch-workflow.md)。现有测试验证这些工具的行为，不能证明模型自动读取、成图质量、SVG编辑器兼容、真实营销效果或商业许可。
