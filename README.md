# 06 — Analisis Program Makan Bergizi Gratis (MBG): Jangkauan, Keracunan, Penutupan SPPG, dan Sentimen Publik

**Jenis data: 100% DATA ASLI.** Seluruh angka berasal dari publikasi yang dapat ditelusuri:
siaran pers dan paparan Badan Gizi Nasional (BGN), Kementerian Kesehatan, BPOM, Kementerian
Keuangan, lembaga survei (Indikator, LSI, Poltracking, Puspoll, Voxpol, IPO, Tempo Data
Science, Adidaya), pemantau independen (JPPI, KPAI), dan firma analitik (Drone Emprit, INDEF).
Setiap baris dataset memiliki kolom **sumber** dan **URL**. Tidak ada data simulasi di project ini.

Program Makan Bergizi Gratis diluncurkan 6 Januari 2025 dan dijalankan BGN. Project ini
menjawab empat pertanyaan yang paling sering diperdebatkan publik:

1. **Keberhasilan jangkauan** — seberapa besar program tumbuh?
2. **Keracunan** — berapa korban sebenarnya, dan kenapa tiap lembaga angkanya berbeda?
3. **SPPG yang ditutup** — berapa dapur yang ditindak BGN?
4. **Sentimen masyarakat** — bagaimana penilaian publik berubah dari 2025 ke 2026?

## Temuan utama (semua terverifikasi dari data di folder ini)

- **Tumbuh lebih dari 100 kali lipat:** SPPG 190 → 26.723 dapur terverifikasi; penerima
  570 ribu → 58 juta orang (6 Jan 2025 s.d. 29 Okt 2026). Capaian target akhir 82,9 juta:
  **70,0%**. Angka penerima sempat diklaim 63–65 juta, lalu dikoreksi Kepala BGN menjadi
  58 juta setelah ditemukan 6 juta data ganda.
- **Keracunan tidak punya satu angka resmi.** Total kumulatif terakhir: BGN 11.640 orang
  (12 Nov 2025, dan BGN tidak merilis total lagi sesudahnya), Kemenkes 50.059 orang / 560
  kejadian (2 Sep 2026), JPPI 43.838 orang (awal Sep 2026), KPAI 12.658 anak sepanjang 2025.
  Di rapat yang sama (12 Nov 2025) saja BGN dan Kemenkes berbeda: 11.640 vs 13.371.
- **Laju kasar lintas sumber** (bukan angka resmi): ±28 korban per 100 ribu penerima versi
  BGN (Nov 2025) vs ±87 per 100 ribu versi Kemenkes (Sep 2026); ±8,3 korban per 1 juta porsi.
- **Insiden terbesar:** Bandung Barat 1.333 orang (Sep 2025), Grobogan 803, Rembang 777,
  Sidoarjo 730, SMKN 6 Semarang 707. Hasil lab yang dipublikasikan berulang kali menemukan
  *E. coli*, *Bacillus cereus*, dan *Staphylococcus aureus*; BGN menyatakan 80–90% kasus
  yang ditelaah berkaitan dengan ketidakpatuhan SOP.
- **Penutupan SPPG:** 40 ditutup (Sep 2025) → 8.182 pernah di-suspend (Mei 2026) → 833
  suspend permanen (Jul 2026) → 1.288 ditutup (Okt 2026, setara 4,9% SPPG beroperasi), plus
  353 kepala SPPG diberhentikan dan Rp311,246 miliar kembali ke kas negara.
- **Publik berbalik terbelah.** Persetujuan awal sangat tinggi (LSI 89,6%; Indikator puas
  72,8% pada Jan 2026), tetapi survei Oktober 2026 mencatat Poltracking 47,4% puas vs 49,5%
  tidak puas dan IPO 36% puas vs 64% tidak puas. Di keluarga penerima (Tempo Data Science):
  48% puas vs 51% tidak puas.
- **Sentimen medsos:** Drone Emprit (Okt 2024–Okt 2025) 50% positif / 36% negatif / 14%
  netral; INDEF mencatat sentimen negatif X dan TikTok melonjak dari 85% menjadi 97% selama
  September 2025 dan 83% pada Oktober 2026.
- **Sampel Threads project ini** (50 postingan berinteraksi tertinggi tentang MBG, diambil
  29 Okt 2026): 33 postingan (66%) berlabel negatif atau sangat negatif, **nol** berlabel
  positif. Suara pro tetap ada, terutama di komentar postingan terbelah (mis. orang tua yang
  merasa terbantu secara ekonomi). Sampel ini condong ke periode krisis Oktober 2026 dan
  **bukan** sampel representatif; gunakan survei untuk gambaran publik umum.

## Struktur

```
06-analisis-program-mbg/
├── analisis.py                  # analisis + grafik + ringkasan (pandas, matplotlib)
├── data/
│   ├── perkembangan_program.csv         # 17 titik waktu SPPG & penerima, bersumber
│   ├── keracunan_kumulatif_per_lembaga.csv  # 13 total resmi per lembaga, apa adanya
│   ├── insiden_terbesar.csv             # 15 insiden terbesar + hasil lab + versi angka lain
│   ├── penutupan_sppg.csv               # 8 pernyataan resmi penindakan BGN
│   ├── survei_publik.csv                # 12 hasil survei 2025–2026
│   ├── sentimen_medsos_studi.csv        # Drone Emprit & INDEF
│   ├── sentimen_threads_sampel.csv      # ringkasan label 50 postingan Threads
│   └── sampel_postingan_threads.csv     # 50 postingan mentah (tanggal, penulis, URL, label)
└── output/
    ├── ringkasan_eksekutif.md
    ├── tabel_insiden_top10.csv
    ├── tabel_korban_terakhir_per_lembaga.csv
    └── grafik_1..5 (pertumbuhan, korban per lembaga, insiden, kepuasan, sentimen)
```

## Cara menjalankan

```bash
pip install pandas matplotlib
python analisis.py
```

## Keterbatasan (penting, jangan dilewati saat mengutip)

1. **Tidak ada dataset resmi terbuka per-insiden.** Daftar insiden disusun dari pemberitaan;
   angka per insiden adalah angka yang diberitakan, dan kolom `korban_versi_lain` mencatat
   versi berbeda yang juga beredar.
2. **Definisi korban berbeda antar-lembaga dan antar-tahap pendataan** (yang datang berobat
   vs yang masih diobservasi bisa berbeda belasan kali, contoh Dramaga 481 vs 13). Total
   antar-lembaga tidak boleh digabung atau dirata-rata.
3. **Penyebut anggaran 2026 ada lima versi** (Rp335 / 268 / 229 / 229,75 / 218,77 triliun);
   persentase realisasi hanya bermakna bersama penyebut dan tanggalnya.
4. **Angka 2026 adalah potret 29 Oktober 2026.** Program masih berjalan; angka akan berubah.
5. **Survei antar-lembaga tidak satu tren**: pertanyaan (puas vs setuju vs dukungan) dan basis
   responden (publik umum vs keluarga penerima) berbeda.
6. **Sampel Threads adalah sampel kemudahan berbasis interaksi** pada masa krisis, bukan
   sampel probabilitas; label sentimen adalah label platform pada saat pengambilan.
