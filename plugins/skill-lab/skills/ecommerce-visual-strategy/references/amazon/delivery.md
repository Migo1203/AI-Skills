# 交付与机械检查

这是Amazon交付v1专用格式，机械检查含保守主图和A+约定。国内/其他平台用[通用交付](../deliverables.md)，不强制转换成此格式。所有工具实际位于统一技能的`scripts/`，从技能根目录调用。

## 按范围交付

- **正文**：消费者可见的标题、要点、信息表；独立给关键词来源、宣称依据和缺口。
- **图片卡**：类型/用途、用户问题、布局及理由、线框、素材、短文案、提示词或PS步骤、平台核验状态、成图验收项。
- **A+**：页面地图及对应图片卡，记录模块/槽位和桌面、手机行为；未知尺寸留在稿外，不冒充后台配置。
- **改稿**：位置→原因→修改→验收，保留已采用方案。

完整制作按[可编辑制作流程](../editable-production.md)交付SVG母版、同版预览、原素材及制作说明，文案/形状/标注保持独立对象，照片仍为位图。用户审稿、用户改编、用户定稿和AI最终检查分别记录，AI不得替用户批准。JSON里的`status: draft`仅表示机械检查格式，不代表用户没有定稿；用户定稿与检查对象另记在制作说明中，不为通过脚本而更改真实状态。

需要机器检查或批量复用时使用下述JSON；普通对话可以直接交可读文字，无需每次输出JSON。

普通A+视觉审阅包沿用制作流程的简洁目录和一份使用说明，不因本参考列出JSON结构就生成整套机器文件。实际使用机械检查时，输入/报告集中到`04_过程记录/`；结构化队列文件保留在同一队列工作目录，不为归类而破坏续做依赖。交互HTML只在确有展示需要时生成。

## JSON交付结构 v1

可运行实例见项目根目录 `examples/demo-delivery.json`；对应合成资料在 `examples/demo-brief.md`。这些不是真实商品或官方规则。移植技能文件夹时不需要项目开发样例；可复用的品牌、本地化和实验表单位于技能自己的 `assets/`。

顶层字段：`schema_version: 1`、`status: draft`、`context`、`evidence`、`claims`。可选 `listing`、`images`、`rules`、`gaps`、`brand_style`。本版只审阅草案，不表达可发布状态。

- `context`：`sku`、`market`、`category`，均为明确字符串；本地化或批量任务还需`language`，可另记`brand_id`。
- `evidence[]`：唯一`id`、`kind`（document/supplier/visual/hypothesis）、`source`、`sku`、`verified`；供应商资料可补`cross_checked`。
- `claims[]`：唯一`id`、`text`、`evidence_ids[]`。每条商品事实须有当前SKU有效资料支持。
- `listing.title`、`listing.bullets[]`：`text`、`claim_ids[]`；`listing.attributes[]`：另有`name`。所有消费者可见事实文本必须关联事实，不把条件/来源放到正文外就认为语义已核验。
- `images[]`：唯一`id`、`kind`（main/secondary/a_plus/mobile_a_plus/concept）、`task`、`layout_id`（01–16），`main`可用`product_only`；`claim_ids[]`，可选`text`、`prompt`、`module_id`、`dimensions`。
- `prompt`：`mode`（background/product_concept）、`text`、`constraints[]`、`reference_ids[]`；background需`no_product: true`，含产品图需至少一个visual参照。每条应独立可复制，不能仅写“同上”。
- `dimensions`：`width`、`height`正整数，未知时省略。A+可关联`module_id`。
- `rules`：可选`source`、`verified_on`、`limits`和`modules`。`limits`仅支持`title_max_chars`、`bullet_max_chars`、`bullet_max_count`；字符数按Unicode码点含空格计算，是本工具计数约定。`modules`为`模块ID: {width, height}`。提供限制/模块时需来源和日期；脚本不联网验证它们。
- `gaps[]`：稿外缺口；不放消费者可见字段。`brand_style`记录色彩角色、字体层级、图标和对齐规则。

复用品牌时，将[品牌解析](../brand-profile.md)的`settings.style`映射到本次`brand_style`，另存完整解析结果和覆盖记录；文案遵守`settings.voice/glossary`。跨站点另存[本地化记录](../localization-and-audience.md)，多SKU按[批量工作流](batch-workflow.md)隔离目录，实验数据不混入商品事实证据。

脚本拒绝重复/悬空ID、错误SKU引用、未核实或只凭视觉/假设的宣称、明显占位符、未知图片类型、保守主图方案中的新增促销文字、缺产品参照、已输入限制超标及已知模块尺寸不匹配。缺规则/尺寸只列待核验警告，不补猜。

脚本不检查所有句子的语义、证据原件真实性、平台实时政策、布局合理性、实际图片或PSD；漏写宣称、错误翻译和误导暗示仍需审阅。通过结果只叫“机械检查通过”。

## 运行

在技能目录下，使用Python 3标准库：

```text
python scripts/audit_delivery.py ../../examples/demo-delivery.json
```

上面的相对路径从技能目录到项目examples；任意位置运行时可改成绝对路径。退出码0表示未发现已实现的机械错误；1表示交付内容有错误；2表示文件/JSON无法读取。输出JSON包含`errors`、`warnings`、`metrics`及检查范围。无网络、无API、无生图、无发布副作用。
