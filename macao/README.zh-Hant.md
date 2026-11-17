[English](README.md) · [繁體中文](README.zh-Hant.md) · [全部地區](../README.md)

# 🌙 澳門 — 農曆

複製下方連結，貼到日曆應用程式訂閱。

## 1. 透過連結訂閱

僅農曆節日

```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/lunar_mo_chinese_zh-Hant_festivals_latest.ics
```

貼到 Google Calendar、Apple Calendar 或 Outlook 的「透過 URL 訂閱」欄並儲存。下載後匯入 ICS 不會自動更新。

> 新連結在檔案發布到 main 分支後可用。

<details>
<summary>其他日曆：初一、十五／每日農曆</summary>

**節日＋初一、十五**

```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/lunar_mo_chinese_zh-Hant_observances_latest.ics
```

**每日農曆＋節日**

```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/lunar_mo_chinese_zh-Hant_daily_latest.ics
```

</details>

<details>
<summary>包含的農曆節日</summary>

| 農曆日/月 | 節日 |
| --- | --- |
| 1/1 | 農曆正月初一 |
| 2/1 | 農曆新年第二天 |
| 15/1 | 元宵節 |
| 23/3 | 媽祖誕 |
| 8/4 | 佛誕 |
| 5/5 | 端午節 |
| 18/5 | 哪吒誕 |
| 15/7 | 盂蘭節 |
| 15/8 | 中秋節 |
| 9/9 | 重陽節 |
| 農曆年最後一天 | 除夕 |

[來源與節日規則](../docs/FESTIVALS.md)

</details>

## 2. 使用 Python 自訂

請在專案根目錄執行指令: [lunar-calender](../README.md).

<details>
<summary>首次使用？設定 Python 3.11+ 環境</summary>

下載儲存庫，開啟包含 main.py 的根目錄並建立虛擬環境。啟用環境後安裝已鎖定的相依套件。

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
python main.py --config macao/calendar.config.json --language zh-Hant
```

<details>
<summary>修改設定檔</summary>

使用本目錄的 calendar.config.json。指令列參數優先於 JSON；需要英文時可將 language 改為 en。

訂閱前在 JSON 中設定 "feed_name": "family"。修改設定後 URL custom_family_latest.ics 維持不變；每個日曆使用獨立名稱。

```json
{
  "country": "MO",
  "tradition": "chinese",
  "language": "zh-Hant",
  "content": "festivals"
}
```

--year 或 --start/--end 選年份；--lunar-days all/none/1,15 選日期；--holiday-types lunar/solar/all/none 選類別；--split 產生分年檔及 ZIP；--output-dir 指定目錄。四個 --*-color 選項接受 #RRGGBB。

```powershell
python main.py --config macao/calendar.config.json --language zh-Hant --year 2027 --split --output-dir exports
python main.py --config macao/calendar.config.json --language zh-Hant --lunar-days 1,15
python main.py --countries VN,CN,KR --language en
```

[calendar.config.json](calendar.config.json)

</details>

<details>
<summary>在自己的 fork 自動更新</summary>

1. Fork 儲存庫並提交設定。
2. 啟用 Actions 並允許工作流程寫入儲存庫。
3. 將 CUSTOM_CONFIG 設為下方設定路徑。
4. 完成發布清單後，將 PUBLISH_LUNAR_FEEDS 設為 true，執行 Update Lunar Calendars；手動 custom_config 可覆寫該次路徑。
5. 用輸出的檔名建立自己 fork 的 raw main/output 連結。每年工作使用 CUSTOM_CONFIG。

預定每年1月1日00:00 UTC產生；修改程式或資料、手動執行皆可立即重建。公開GitHub儲存庫連續60天無活動可能停用排程，請維護及監控工作流程，或由外部排程器在需要時啟用工作流程，再呼叫 workflow_dispatch。

```text
macao/calendar.config.json
```

</details>

## 範圍與協助

傳統節日，不代表法定假日或補假安排。

滾動訂閱僅保留當年和下一年；更新年份後，舊年會從訂閱移除。以 --split --output-dir exports 儲存歷史快照；output/ 由程式管理，其中帶年份的匯出會在下次標準建置時清理。

支援 1901–2099 年。預設從當年開始連續涵蓋 2 年，不超出支援範圍。

曆法：chinese；參考時區：Asia/Macau。農曆十五並非天文滿月時刻；閏月不重複節日。

正式發布前，仍需母語審校及 Google/Apple/Outlook 實際訂閱測試。

<details>
<summary>FAQ</summary>

連結無法使用時，確認檔案位於正確儲存庫的 main 分支。更新頻率由應用程式決定。不支援的選項會報錯；色彩依應用程式而異。

</details>

**共用技術文件** · English

[Feeds](../docs/FEEDS.md) · [Development](../docs/DEVELOPMENT.md) · [Automation](../docs/AUTOMATION.md) · [Release](../docs/RELEASE.md) · [Sources](../tests/fixtures/README.md) · [index.json](../output/index.json)

[cmduyeen](https://github.com/cmduyeen) · [MIT](../LICENSE)
