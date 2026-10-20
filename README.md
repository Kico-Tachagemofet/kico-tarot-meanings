# Kico 大阿卡纳牌意 DLC v1.0.0

22 张大阿卡纳的中文牌意正文与对应标签，由 Kico 审订。
作为可选资料包，供 [Symbol Anchor Check](https://github.com/Kico-Tachagemofet/symbol-anchor-check)
和[量化塔罗](https://github.com/Kico-Tachagemofet/statistical-tarot-elemental-reading)读取。

正文保留各牌的动作、条件和不同表达；加载后参与牌意理解、场域称重与候选检验。
本包不提供抽取功能，不改动抽到的牌、不决定统计显著度，也不替代解释者的判断。

## 安装与开关

下载完整仓库或固定版本的 release，保留 `manifest.json` 与 `cards/` 的位置。
两套消费者均支持 `--meanings-pack <本包目录>` 与 `--no-meanings`。
公开安装默认关闭；启用但文件缺失、身份不完整或校验不符时明确失败。

牌意正文由本包独立维护；消费者只内置读取器，不捆绑 22 张正文。
更新本包不会自动覆盖已保存报告。复核旧报告时使用其记录的版本。

## 包内容与身份

- `cards/`：22 张牌的完整正文及标签。无私有讨论、审核日志、历史版本链接或案例。
- `manifest.json`：整包版本、单牌版本、固定身份、文件校验值、作者及许可。
- `card_meanings.py`：标准库读取器，供 Python 接入；两套消费者内置同版本副本。
- `HANDOFF.md`：给网站维护者的接入约定与验收方法。

固定身份使用 Book T ID。力量是 `atu_11_fortitude`，正义是 `atu_08_justice`。
正文标题中的罗马数字按原稿保留，不能用标题编号代替身份匹配。

每次只向模型传入相关牌意：Anchor Check 加载主牌和补牌中的大牌，并按身份去重；
量化塔罗加载进入解读的突出大牌（包括偏多和偏少）。
补牌的原有父位作用不变；读取牌意不会把补牌提升为全场主位。

## Token

`manifest.json` 每张牌的 `tokens` 是对该 Markdown 文件的本地实测，
提供 `o200k_base` 与 `cl100k_base` 两种口径。整包分别为 **8,668 / 12,603** token。
没有启用时不传正文；使用几张就按去重后的实际文本计数。

这些数字不包含包信息、提示词、其他符号或输出，不能直接当作 Claude 的 token。
网页可先显示本包文本增量，再用所选模型的官方计数接口核对完整请求。
多次模型调用应分别计数，不把一次资料载入当成整条工作流的总费用。

## 许可与署名

`cards/`、`manifest.json` 中的牌意与对应资料，以及本包说明文档：
**Copyright © 2026 Kico — CC BY-NC-SA 4.0**。
请署名 Kico、链接本仓库与许可、标明改动；改作采用同一许可。
商业使用需另行获得权利人授权。见 [LICENSE-CONTENT](LICENSE-CONTENT)。

读取器 `card_meanings.py` 及测试代码采用 MIT，见 [LICENSE-CODE](LICENSE-CODE)。
读取器的 MIT 许可不改变牌意正文的 CC BY-NC-SA 4.0 许可。

推荐署名：**Kico 大阿卡纳牌意 v1.0.0 · Kico · CC BY-NC-SA 4.0**。
