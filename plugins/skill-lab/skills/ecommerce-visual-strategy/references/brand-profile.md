# 品牌档案与继承

适用：创建品牌规范、沿用现有品牌、多SKU/系列保持一致。先找本次用户已有档案，不把合成模板当作用户的真实品牌，也不把本次临时探索永久设成规范。

## 保存与范围

复制[品牌表单](../assets/brand-profile.template.json)到用户指定的项目资料目录。默认仅为当前任务读取与解析；用户要求沉淀品牌时才将确认内容写回档案。记录`brand_id`、`revision`、`status`（confirmed/hypothesis），修改确认状态和版本应有实际依据。

可继承部分：

| 部分 | 记录内容 |
| --- | --- |
| style | palette_roles、typography、icons、spacing、photography、avoid |
| voice | tone、avoid |
| glossary | source、target、language、status（approved/proposed） |
| assets | path、license、source；可另记用途和许可范围 |

色彩用角色解释（背景、正文、强调），字体说明层级及可用替代。移动端先保证文字和对比，不把某一种构图变成所有产品的强制模板。素材的license字段是用户记录，不是工具核验授权；无法确定时标记unknown并使用可替代方案。

商品尺寸、材质、承重、功效、配件、认证、保修、目标站点规则、受众结论与实验结果不属于品牌默认值，保存在各自SKU资料。文字中含性能暗示仍需事实审核，放进voice不使它成为有效宣称。

## 解析与覆盖

顺序为：**defaults → 选定series → 当前任务overrides**。站点调整放在当前任务override里，不能改完全局品牌后让其他市场无意继承。

```text
python scripts/resolve_brand.py brand.json --series desk --overrides task-style.json
```

标准输出为解析JSON，可由调用方保存到新文件。字典递归合并；字符串和数组整体替换，不拼接数组；空字典不删除已有值，不支持用null删除设置。要换一整份术语表应提供完整目标数组。省略series表示只用品牌默认，写错series会报错。

结果含`settings`和逐字段`origins`，可核对究竟来自品牌版本、系列还是本次任务。工具拒绝未定义的可继承大类，不能识别所有藏在自然语言中的商品宣称。

## 使用与验收

通用视觉稿将解析结果用于本次SVG和制作说明；Amazon交付v1还可将`settings.style`映射到`brand_style`。写文案时读取voice和对应语言术语。每张图片仍按信息任务选[布局](layout-library.md)，不为统一而强制同版。

交付保留：采用的品牌版本、系列、覆盖项及原因、解析结果文件、仍是假设的设置。检查两款SKU：共同样式能追溯；单款强调色变化不污染另一款；产品事实不会因为继承出现。后续品牌更新后重新解析和审阅，不静默修改已采用的旧稿。
