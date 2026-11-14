[English](README.md) · [한국어](README.ko.md) · [모든 지역](../../README.md)

# 🌙 미국 — 대한민국 — 음력 달력

아래 URL을 복사해 달력 앱에 붙여 넣고 구독하세요.

## 1. URL로 구독

음력 명절만

```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/lunar_us_korean_ko_festivals_latest.ics
```

Google Calendar, Apple Calendar 또는 Outlook의 URL로 구독 입력란에 붙여 넣고 저장하세요. 다운로드한 ICS 파일 가져오기는 자동 갱신되지 않습니다.

> 새 링크는 파일이 main 브랜치에 게시된 뒤 사용할 수 있습니다.

미국 내 공동체를 위한 달력입니다. 명절 날짜는 원래 역법을 따르며 미국 법정 공휴일이 아닙니다. 종일 일정의 날짜는 시간대에 따라 이동하지 않습니다.

<details>
<summary>다른 달력: 초하루·보름 / 매일의 음력</summary>

**명절 + 초하루·보름**

```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/lunar_us_korean_ko_observances_latest.ics
```

**매일의 음력 + 명절**

```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/lunar_us_korean_ko_daily_latest.ics
```

</details>

<details>
<summary>포함된 음력 명절</summary>

| 음력 일/월 | 명절 |
| --- | --- |
| 1/1 | 설날 |
| 2/1 | 설날 다음 날 |
| 15/1 | 정월대보름 |
| 8/4 | 부처님오신날 |
| 5/5 | 단오 |
| 14/8 | 추석 전날 |
| 15/8 | 추석 |
| 16/8 | 추석 다음 날 |
| 음력 한 해의 마지막 날 | 설날 전날 |

[출처 및 명절 규칙](../../docs/FESTIVALS.md)

</details>

## 2. Python으로 맞춤 설정

프로젝트 루트 폴더에서 명령을 실행하세요: [lunar-calender](../../README.md).

<details>
<summary>처음 사용하시나요? Python 3.11+ 환경 설정</summary>

저장소를 다운로드하고 main.py가 있는 루트 폴더에서 가상 환경을 만드세요. 환경을 활성화한 뒤 고정된 의존성을 설치하세요.

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
python main.py --config united-states/korean/calendar.config.json --language ko
```

<details>
<summary>설정 파일 수정</summary>

이 폴더의 calendar.config.json을 사용하세요. 명령줄 옵션이 JSON보다 우선하며 영어는 language를 en으로 설정하세요.

구독 전에 JSON에 "feed_name": "family"를 설정하세요. 설정을 바꿔도 custom_family_latest.ics URL은 유지됩니다. 달력마다 고유한 이름을 사용하세요.

```json
{
  "country": "US",
  "tradition": "korean",
  "language": "ko",
  "content": "festivals"
}
```

--year 또는 --start/--end로 연도, --lunar-days all/none/1,15로 날짜, --holiday-types lunar/solar/all/none으로 분류를 선택합니다. --split은 연도별 파일과 ZIP, --output-dir은 출력 폴더입니다. 네 가지 --*-color 옵션은 #RRGGBB 형식입니다.

```powershell
python main.py --config united-states/korean/calendar.config.json --language ko --year 2027 --split --output-dir exports
python main.py --config united-states/korean/calendar.config.json --language ko --lunar-days 1,15
python main.py --countries VN,CN,KR --language en
```

[calendar.config.json](calendar.config.json)

</details>

<details>
<summary>내 fork에서 자동 갱신</summary>

1. 저장소를 fork하고 설정 파일을 커밋하세요.
2. Actions를 활성화하고 저장소 쓰기 권한을 주세요.
3. CUSTOM_CONFIG를 아래 설정 경로로 지정하세요.
4. 출시 점검표 완료 후 PUBLISH_LUNAR_FEEDS를 true로 설정하고 Update Lunar Calendars를 실행하세요. 수동 custom_config는 해당 실행에만 적용됩니다.
5. 출력 파일명으로 본인 fork의 raw main/output URL을 만드세요. 연간 작업은 CUSTOM_CONFIG를 사용합니다.

매년 1월1일 00:00 UTC에 생성하도록 예약되며 코드·데이터 변경이나 수동 실행으로 즉시 재생성할 수 있습니다. 공개 GitHub 저장소가 60일간 비활성 상태이면 예약이 해제될 수 있습니다. 워크플로를 유지·모니터링하거나 외부 스케줄러에서 필요 시 워크플로를 활성화한 후 workflow_dispatch를 호출하세요.

```text
united-states/korean/calendar.config.json
```

</details>

## 범위와 도움말

전통 기념일이며 법정 공휴일이나 대체공휴일 일정이 아닙니다.

구독에는 올해와 내년만 유지하며 범위 갱신 시 이전 연도는 제거됩니다. --split --output-dir exports로 과거 스냅샷을 보관하세요. output/의 연도별 내보내기는 다음 표준 빌드에서 정리됩니다.

지원 범위: 1901–2050년. 기본 범위는 올해부터 연속 2년이며 지원 한도를 넘지 않습니다.

역법: korean; 기준 시간대: Asia/Seoul. 음력 보름은 천문학적 보름달 시각과 다릅니다. 윤달에 명절을 반복하지 않습니다.

공식 배포 전 원어민 검토와 Google/Apple/Outlook 실제 구독 검사가 필요합니다.

<details>
<summary>FAQ</summary>

링크가 없으면 올바른 저장소의 main 브랜치를 확인하세요. 갱신 간격과 색상은 앱에 따라 다릅니다. 지원하지 않는 옵션은 오류로 알립니다.

</details>

**공유 기술 문서** · English

[Feeds](../../docs/FEEDS.md) · [Development](../../docs/DEVELOPMENT.md) · [Automation](../../docs/AUTOMATION.md) · [Release](../../docs/RELEASE.md) · [Sources](../../tests/fixtures/README.md) · [index.json](../../output/index.json)

[cmduyeen](https://github.com/cmduyeen) · [MIT](../../LICENSE)
