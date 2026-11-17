[English](README.md) · [Bahasa Melayu](README.ms.md) · [Semua negara](../README.md)

# 🌙 Malaysia — Kalendar lunar

Salin URL di bawah dan tampal dalam aplikasi kalendar untuk melanggan.

## 1. Langgan melalui URL

Perayaan lunar sahaja

```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/lunar_my_chinese_ms_festivals_latest.ics
```

Tampal dalam Subscribe from web atau From URL di Google Calendar, Apple Calendar atau Outlook, kemudian simpan. Import fail ICS tidak menerima kemas kini automatik.

> Pautan baharu tersedia selepas fail diterbitkan ke cabang main.

Perayaan tradisional; bukan jadual cuti umum rasmi atau cuti gantian.

<details>
<summary>Kalendar lain: hari pertama dan ke-15 / setiap tarikh lunar</summary>

**Perayaan + hari pertama dan ke-15**

```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/lunar_my_chinese_ms_observances_latest.ics
```

**Setiap tarikh lunar + perayaan**

```text
https://raw.githubusercontent.com/cmduyeen/lich-am-viet-nam/main/output/lunar_my_chinese_ms_daily_latest.ics
```

</details>

<details>
<summary>Perayaan lunar yang disertakan</summary>

| Tarikh lunar (hari/bulan) | Perayaan |
| --- | --- |
| 1/1 | Tahun Baharu Cina |
| 2/1 | Tết — Hari Kedua |
| 15/1 | Chap Goh Mei |
| 5/5 | Perayaan Perahu Naga |
| 15/7 | Perayaan Hantu Lapar |
| 15/8 | Perayaan Pertengahan Musim Luruh |
| Hari terakhir tahun lunar | Malam Tahun Baharu Cina |

[Sumber dan peraturan perayaan](../docs/FESTIVALS.md)

</details>

## 2. Sesuaikan dengan Python

Jalankan arahan dari folder akar projek: [lunar-calender](../README.md).

<details>
<summary>Kali pertama? Sediakan Python 3.11+</summary>

Muat turun repositori dan buka folder akar yang mengandungi main.py. Cipta serta aktifkan persekitaran maya sebelum memasang kebergantungan terkunci.

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
python main.py --config malaysia/calendar.config.json --language ms
```

<details>
<summary>Sunting konfigurasi</summary>

Gunakan calendar.config.json dalam folder ini. Pilihan CLI mengatasi JSON; tukar language kepada en untuk bahasa Inggeris.

Tetapkan "feed_name": "family" dalam JSON sebelum melanggan. URL custom_family_latest.ics kekal apabila tetapan berubah; gunakan nama unik bagi setiap kalendar.

```json
{
  "country": "MY",
  "tradition": "chinese",
  "language": "ms",
  "content": "festivals"
}
```

Gunakan --year atau --start/--end untuk tahun, --lunar-days all/none/1,15 untuk tarikh, --holiday-types lunar/solar/all/none untuk kategori, --split untuk fail tahunan dan ZIP, serta --output-dir untuk folder. Empat pilihan --*-color menerima #RRGGBB.

```powershell
python main.py --config malaysia/calendar.config.json --language ms --year 2027 --split --output-dir exports
python main.py --config malaysia/calendar.config.json --language ms --lunar-days 1,15
python main.py --countries VN,CN,KR --language en
```

[calendar.config.json](calendar.config.json)

</details>

<details>
<summary>Kemas kini automatik pada fork anda</summary>

1. Fork repositori dan komit konfigurasi.
2. Aktifkan Actions dan kebenaran menulis repositori.
3. Tetapkan CUSTOM_CONFIG kepada laluan konfigurasi di bawah.
4. Selepas senarai semak keluaran selesai, tetapkan PUBLISH_LUNAR_FEEDS kepada true dan jalankan Update Lunar Calendars. Input manual custom_config mengatasi laluan untuk larian itu sahaja.
5. Gunakan nama fail output pada URL raw main/output fork anda. Jadual tahunan menggunakan CUSTOM_CONFIG.

Penjanaan dijadualkan setiap 1 Januari 00:00 UTC; perubahan kod/data atau larian manual boleh menjana semula serta-merta. Jadual repositori GitHub awam boleh dilumpuhkan selepas 60 hari tidak aktif. Selenggara dan pantau aliran kerja atau gunakan penjadual luar untuk mengaktifkan aliran kerja apabila perlu dan memanggil workflow_dispatch.

```text
malaysia/calendar.config.json
```

</details>

## Liputan dan bantuan

Perayaan tradisional; bukan jadual cuti umum rasmi atau cuti gantian.

Langganan hanya menyimpan tahun semasa dan tahun berikutnya; tahun lama dikeluarkan apabila julat bergerak. Simpan sejarah dengan --split --output-dir exports. Fail bertarikh dalam output/ diurus dan dibersihkan oleh binaan standard berikutnya.

Julat sokongan: 1901–2099. Lalai meliputi 2 tahun berturut-turut bermula tahun semasa dalam had ini.

Kalendar: chinese; zon waktu rujukan: Asia/Kuala_Lumpur. Hari ke-15 lunar bukan waktu bulan purnama astronomi yang tepat. Perayaan tidak diulang pada bulan lompat.

Semakan penutur asli dan ujian langganan sebenar Google/Apple/Outlook masih diperlukan sebelum penerbitan rasmi.

<details>
<summary>FAQ</summary>

Jika URL tiada, semak cabang main repositori yang betul. Sela muat semula dan warna bergantung pada aplikasi. Pilihan yang tidak disokong menghasilkan ralat.

</details>

**Dokumentasi teknikal bersama** · English

[Feeds](../docs/FEEDS.md) · [Development](../docs/DEVELOPMENT.md) · [Automation](../docs/AUTOMATION.md) · [Release](../docs/RELEASE.md) · [Sources](../tests/fixtures/README.md) · [index.json](../output/index.json)

[cmduyeen](https://github.com/cmduyeen) · [MIT](../LICENSE)
