[English](README.md) · [简体中文](README.zh-Hans.md) · [全部地区](../README.md)

# 🌙 新加坡 — 农历

复制下方链接，粘贴到日历应用中订阅。

## 1. 通过链接订阅

仅农历节日

```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/lunar_sg_chinese_zh-Hans_festivals_latest.ics
```

粘贴到 Google Calendar、Apple Calendar 或 Outlook 的“通过 URL 订阅”栏并保存。下载后导入 ICS 不会自动更新。

> 新链接在文件发布到 main 分支后可用。

传统节日，不代表法定假日或调休安排。

<details>
<summary>其他日历：初一、十五／每日农历</summary>

**节日＋初一、十五**

```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/lunar_sg_chinese_zh-Hans_observances_latest.ics
```

**每日农历＋节日**

```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/lunar_sg_chinese_zh-Hans_daily_latest.ics
```

</details>

<details>
<summary>包含的农历节日</summary>

| 农历日/月 | 节日 |
| --- | --- |
| 1/1 | 春节 |
| 2/1 | 春节（正月初二） |
| 15/1 | 元宵节 |
| 5/5 | 端午节 |
| 15/7 | 中元节 |
| 15/8 | 中秋节 |
| 农历年最后一天 | 除夕 |

[来源与节日规则](../docs/FESTIVALS.md)

</details>

## 2. 使用 Python 自定义

请在项目根目录运行命令: [lunar-calender](../README.md).

<details>
<summary>首次使用？设置 Python 3.11+ 环境</summary>

下载仓库，打开包含 main.py 的根目录并创建虚拟环境。激活环境后安装已锁定的依赖。

```powershell
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install --require-hashes -r requirements.txt
```

macOS / Linux:

```bash
source .venv/bin/activate
python -m pip install --require-hashes -r requirements.txt
```

</details>

```powershell
python main.py --config singapore/calendar.config.json --language zh-Hans
```

<details>
<summary>修改配置文件</summary>

使用本目录的 calendar.config.json。命令行参数优先于 JSON；需要英文时可将 language 改为 en。

订阅前在 JSON 中设置 "feed_name": "family"。修改设置后 URL custom_family_latest.ics 保持不变；每个日历使用独立名称。

```json
{
  "country": "SG",
  "tradition": "chinese",
  "language": "zh-Hans",
  "content": "festivals"
}
```

--year 或 --start/--end 选择年份；--lunar-days all/none/1,15 选择日期；--holiday-types lunar/solar/all/none 选择类别；--split 生成分年文件与 ZIP；--output-dir 指定目录。四个 --*-color 选项接受 #RRGGBB。

```powershell
python main.py --config singapore/calendar.config.json --language zh-Hans --year 2027 --split --output-dir exports
python main.py --config singapore/calendar.config.json --language zh-Hans --lunar-days 1,15
python main.py --countries VN,CN,KR --language en
```

[calendar.config.json](calendar.config.json)

</details>

<details>
<summary>在自己的 fork 中自动更新</summary>

1. Fork 仓库并提交配置。
2. 启用 Actions 并允许工作流写入仓库。
3. 将 CUSTOM_CONFIG 设为下方配置路径。
4. 完成发布清单后将 PUBLISH_LUNAR_FEEDS 设为 true，运行 Update Lunar Calendars；手动 custom_config 可覆盖本次路径。
5. 用输出文件名创建自己 fork 的 raw main/output 链接。每年任务使用 CUSTOM_CONFIG。

计划每年1月1日00:00 UTC生成；修改代码或数据、手动运行均可立即重建。公开GitHub仓库连续60天无活动可能停用计划任务，请维护和监控工作流，或由外部调度器在需要时启用工作流，再调用 workflow_dispatch。

```text
singapore/calendar.config.json
```

</details>

## 范围与帮助

传统节日，不代表法定假日或调休安排。

滚动订阅仅保留当年和下一年；更新年份后，旧年会从订阅中移除。用 --split --output-dir exports 保存历史快照；output/ 由程序管理，其中带年份的导出会在下次标准构建时清理。

支持 1901–2099 年。默认从当年开始连续覆盖 2 年，不超出支持范围。

历法：chinese；参考时区：Asia/Singapore。农历十五并非天文满月时刻；闰月不重复节日。

正式发布前，仍需母语审校及 Google/Apple/Outlook 实际订阅测试。

<details>
<summary>FAQ</summary>

链接不可用时确认文件位于正确仓库的 main 分支。刷新间隔由应用决定。不支持的选项会报错；颜色支持因应用而异。

</details>

**共享技术文档** · English

[Feeds](../docs/FEEDS.md) · [Development](../docs/DEVELOPMENT.md) · [Automation](../docs/AUTOMATION.md) · [Release](../docs/RELEASE.md) · [Sources](../tests/fixtures/README.md) · [index.json](../output/index.json)

[cmduyeen](https://github.com/cmduyeen) · [MIT](../LICENSE)
