# 给舒望：Kico 大阿卡纳牌意 DLC 接入交接

版本：2026-10-20 · 数据包 v1.0.0 · Anchor Check v4.3 · 量化塔罗 v3.3

两套解读已提供同一份牌意包的读取入口。本交接提供数据和调用约定；
网站的界面、请求协议、模型接入和部署由网站侧实现。

## 需要接上的行为

公开网站默认不启用。用户勾选「使用 Kico 大阿卡纳牌意」后，按本次解读
实际需要传入完整正文；取消勾选时移除正文。切换只重新解读现有结果，
不能触发重新抽牌，也不能修改已有随机记录。

建议网站请求保存以下语义，字段名称可自行调整：

```json
{
  "meaning_pack": {
    "enabled": true,
    "pack_id": "kico-major-arcana",
    "version": "1.0.0"
  }
}
```

这不是已经实现的 HTTP 接口。后端将允许的 pack_id/version 映射到已安装的
包目录；浏览器不应提交服务器文件路径。固定版本部署，不在每次解读时追踪 main。
资料包无模型密钥要求，读取器本身不联网、不调用模型。

## 下载与许可

- [牌意包](https://github.com/Kico-Tachagemofet/kico-tarot-meanings)：安装 v1.0.0。
- [Anchor Check](https://github.com/Kico-Tachagemofet/symbol-anchor-check)：使用 v4.3 或之后兼容版本。
- [量化塔罗](https://github.com/Kico-Tachagemofet/statistical-tarot-elemental-reading)：使用 v3.3 或之后兼容版本。

牌意正文和标签采用 **CC BY-NC-SA 4.0**，作者 **Kico**；
软件读取器采用 MIT。保留作者、包来源、许可链接和修改说明。
建议界面署名为「Kico 大阿卡纳牌意 v1.0.0 · CC BY-NC-SA 4.0」。
许可全文见仓库的 LICENSE-CONTENT，软件许可不替代正文许可。

## Anchor Check

对已经保存的牌阵运行：

```bash
python phase3_unfold.py saved-spread.json --meanings-pack /installed/kico-tarot-meanings
python phase3_unfold.py saved-spread.json --no-meanings
```

也可以调用 `unfold_spread(saved_spread, meanings_pack=pack_directory)`；
显式关闭传 `meanings_pack=False`。省略参数才使用安装级配置，公开包默认关闭。

输出增加三个部分：

| 字段 | 用途 |
|---|---|
| `meaning_pack` | 是否启用、包名、版本、manifest 校验值、实际加载牌名、单牌版本和文本 token |
| `author_meanings[card_id]` | 去重后的完整 `text`、单牌版本、校验值和作者元素标签 |
| `per_card[].author_meaning_ref` | 本位指向哪个正文条目 |

所有主牌和补牌中的大阿卡纳都覆盖。同一张牌出现多次只传一份正文，各位置
仍保留自己的职责；补牌只澄清其父位。`raw_correspondences` 和
`spread_synthesis` 保持原有 Book T 数据，不用作者正文重写。

向模型发送时，必须包括 `author_meanings` 的完整正文，不能只传 `per_card`
或 `meaning_pack` 回执。继续执行更新版 SKILL.md 和
`references/meaning-pack.md`：先读取正文，再进入 Phase 3.5/4，
保留逐牌 `meaning_use` 的正文短引与推理用途。
脚本输出并不是最终解读；勾选框也不能只改前端展示。

## 量化塔罗

新抽取在用户已明确要求抽取时，可为原有命令加入
`--meanings-pack /installed/kico-tarot-meanings` 或 `--no-meanings`。
包校验在随机抽取前完成。

用户已有统计结果而只切换开关时，使用专门入口：

```bash
python scripts/enrich_meanings.py \
  --statistics saved/statistics.json \
  --out reports/with-kico \
  --meanings-pack /installed/kico-tarot-meanings

python scripts/enrich_meanings.py \
  --statistics saved/statistics.json \
  --out reports/without-kico \
  --no-meanings
```

输出目录必须是新的报告目录。此入口只更新资料，保留旧文件；
不调用随机源、不复制或伪造新的 raw.ndjson。
`protocol` 和 `receipt` 保留抽取时原值，`enrichment_source.statistics_sha256`
记录源统计文档。当前 DLC 状态看顶层 `meaning_pack`，不要把
`protocol.meaning_pack_at_draw` 当作当前解释选择。

输出中的 `piles[key=major].highlights[].major_meaning.text` 和生成的
`positions/major.md` 含完整正文。只加载突出大牌，包括偏多与偏少；
不能将整副牌里未被强调的牌全塞进当前解释。
大牌分读模型必须收到该数据卡完整内容，执行更新后的 position-brief。
主模型合并时保留正文中的限制与条件，不能仅保留元素标签。

频数、正逆、z、p、分段和突出项不因开关改变。
解释性元素标仍遵守「Book T 有归属则优先，否则作者标签补足」。
开启或关闭可能改变这部分标签及最终解释，属于预期行为。

## 不用 Python 时

读取 `manifest.json`，核对 schema_version=1 和 22 个固定身份；对本次需要的
`cards[card_id].file` 读取 UTF-8 正文并核对 SHA-256。文件必须位于包目录内。
完整对应列表在 manifest，不从数字猜牌：

- 力量：`atu_11_fortitude`；正文显示 VIII。
- 正义：`atu_08_justice`；正文显示 XI。
- 命运之轮：`atu_10_wheel_of_fate`。
- 高塔：`atu_16_blasted_tower`。
- 审判：`atu_20_judgment`。
- 世界：`atu_21_universe`。

新包只按稳定身份匹配。旧的自定 Markdown 目录是兼容入口，
不应拿来加载这个新包；公共旧目录默认 Book T 编号，
RWS 旧目录才加 `--meanings-numbering rws`。

启用时缺包、缺卡、校验不符都应明确报错，不能静默退回基础解释。
包安装后改过文件需要更新单牌版本、校验值、token 与整包版本。
SHA-256 用于完整性与复核，不是对任意来源包的身份认证。

## Token 与显示

`meaning_pack.text_tokens` 是已选正文按分词器求和，重复牌去重。
`o200k_base` 和 `cl100k_base` 不是模型名称；这些值不是 Claude 计数。
全部 22 张为 **8,668 / 12,603 token**。通常只加载其中几张。

可以分两层显示：

1. 抽牌前：「按需加载大阿卡纳完整牌意」。
2. 抽牌后：「本次载入 N 张，正文约增加 X 输入 token（分词口径：…）」。

包回执、提示词、其余符号、输出和推理量不包含在这个正文数里。
若需要费用预估，用目标模型的计数接口计算最终请求；
模型调用完成后以实际 usage 为准。分读、合并等多个请求分别累计。

## 联调验收

| 打开什么、做什么 | 应看到 | 不应看到 |
|---|---|---|
| 同一已保存牌阵，开关各跑一次 | 原牌、位置、正逆及 Book T 汇总一致；开启后多出正文与版本 | 新的随机结果 |
| 力量与正义同在一盘 | 各自正确正文与固定 ID | 两张牌因 8/11 对调 |
| 同一大牌主位和补位出现 | 一份正文、各自位置引用；补位仍局部参与 | 重复正文费用、补位变主位 |
| 纯小牌阵开启 DLC | enabled=true，加载列表为空 | 无关大牌正文 |
| 已存量化结果切换 | 数值、原协议和回执不变，新报告只改解释资料 | 再调用抽取脚本 |
| 人为指定不存在的包 | 清楚报错，尚未抽取时无随机消耗 | 悄悄关闭 DLC |
| 检查模型实际输入与分析 | 正文完整到达；meaning_use 有精确正文短引及用途 | 只有“已加载”的状态标记 |

仓库里的自动测试验证资料传递与数值不变，不证明任意模型都会正确理解。
网站接入目标模型后，还需按最后一行检查实际请求和输出。
