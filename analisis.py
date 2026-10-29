# -*- coding: utf-8 -*-
"""
Project 06 — Analisis Program Makan Bergizi Gratis (MBG), 2025–2026
Semua data DATA ASLI dari publikasi resmi/media yang dapat ditelusuri
(setiap baris CSV memiliki kolom sumber dan URL). Tidak ada data simulasi.

Menjawab empat pertanyaan:
1. Seberapa besar dan seberapa cepat program ini tumbuh? (keberhasilan jangkauan)
2. Berapa korban keracunan menurut tiap lembaga, dan kenapa angkanya berbeda?
3. Berapa SPPG yang ditutup/dibekukan BGN?
4. Bagaimana penilaian publik (survei) dan sentimen media sosial berubah?

Jalankan:  python analisis.py
Keluaran:  output/ringkasan_eksekutif.md, 2 tabel CSV, 5 grafik PNG
"""
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
OUT = os.path.join(BASE, "output")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({"font.size": 10, "axes.titlesize": 12, "axes.grid": True,
                     "grid.alpha": 0.3, "figure.dpi": 130})

perk = pd.read_csv(os.path.join(DATA, "perkembangan_program.csv"), parse_dates=["tanggal"])
korb = pd.read_csv(os.path.join(DATA, "keracunan_kumulatif_per_lembaga.csv"), parse_dates=["tanggal_cutoff"])
insd = pd.read_csv(os.path.join(DATA, "insiden_terbesar.csv"))
tutup = pd.read_csv(os.path.join(DATA, "penutupan_sppg.csv"), parse_dates=["tanggal"])
surv = pd.read_csv(os.path.join(DATA, "survei_publik.csv"))
meds = pd.read_csv(os.path.join(DATA, "sentimen_medsos_studi.csv"))
thr = pd.read_csv(os.path.join(DATA, "sentimen_threads_sampel.csv"))

# ============ 1. Pertumbuhan ============
awal, akhir = perk.iloc[0], perk.iloc[-1]
kali_sppg = akhir["sppg"] / awal["sppg"]
kali_penerima = akhir["penerima_manfaat"] / awal["penerima_manfaat"]
TARGET = 82_900_000
capaian_target = akhir["penerima_manfaat"] / TARGET * 100

# ============ 2. Keracunan: laju per penerima (lintas sumber, diberi label hati-hati) ============
# BGN 12 Nov 2025 (11.640) terhadap penerima 11 Nov 2025 (41,6 jt)
laju_bgn = 11_640 / 41_600_000 * 100_000
# Kemenkes 2 Sep 2026 (50.059) terhadap penerima terdekat 9 Okt 2026 (57.491.334)
laju_kemenkes = 50_059 / 57_491_334 * 100_000
# Per juta porsi: 11.640 korban (12 Nov 2025) terhadap 1,41 miliar porsi (20 Okt 2025)
per_juta_porsi = 11_640 / 1_410_000_000 * 1_000_000
terakhir_per_lembaga = (korb.sort_values("tanggal_cutoff")
                        .groupby("lembaga").tail(1)
                        .sort_values("total_korban", ascending=False))

# ============ 3. Penutupan ============
baris_tutup_terakhir = tutup[tutup["kategori"].str.startswith("Ditutup (melanggar")].iloc[0]
sppg_okt2026 = perk.loc[perk["tanggal"] == "2026-10-09", "sppg"].iloc[0]
persen_ditutup = baris_tutup_terakhir["jumlah"] / sppg_okt2026 * 100

# ============ 4. Survei & sentimen ============
puas = surv[surv["jenis_indikator"] == "Kepuasan"].copy()
puas["label"] = puas["lembaga"].str.replace(" (Indonesia Political Opinion)", "", regex=False) + " " + puas["periode_survei"]
okt2026 = surv[surv["periode_survei"] == "2026-10"]
thr_neg = thr.loc[thr["label_indonesia"].isin(["Sangat Negatif", "Negatif"]), "jumlah_postingan"].sum()
thr_total = thr["jumlah_postingan"].sum()

# ============ Grafik 1: pertumbuhan ============
fig, ax1 = plt.subplots(figsize=(9.5, 4.6))
p = perk.dropna(subset=["penerima_manfaat"])
ax1.bar(p["tanggal"], p["penerima_manfaat"] / 1e6, width=22, color="#9db8dd",
        label="Penerima manfaat (juta)")
ax2 = ax1.twinx()
s = perk.dropna(subset=["sppg"])
ax2.plot(s["tanggal"], s["sppg"], color="#c0501f", marker="o", lw=2, label="SPPG beroperasi")
ax1.set_ylabel("Penerima manfaat (juta)")
ax2.set_ylabel("Jumlah SPPG")
ax1.set_title("Pertumbuhan MBG: 190 SPPG / 0,57 juta penerima menjadi 26.723 SPPG / 58 juta penerima")
ax1.axhline(82.9, color="grey", ls="--", lw=1)
ax1.text(p["tanggal"].iloc[1], 84.5, "Target akhir 82,9 juta", color="grey", fontsize=9)
h1, l1 = ax1.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=9)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "grafik_1_pertumbuhan.png")); plt.close(fig)

# ============ Grafik 2: kumulatif korban per lembaga ============
fig, ax = plt.subplots(figsize=(9.5, 4.6))
warna = {"BGN": "#1f6fb2", "Kemenkes": "#c0501f", "Kemenkes (SKDR)": "#e08a4c",
         "BPOM": "#7a7a7a", "JPPI": "#2e8b57", "KPAI": "#9467bd"}
for lem, g in korb.groupby("lembaga"):
    g = g.sort_values("tanggal_cutoff")
    ax.plot(g["tanggal_cutoff"], g["total_korban"], marker="o", lw=1.8,
            color=warna.get(lem, None), label=f"{lem} (terakhir {g['total_korban'].iloc[-1]:,.0f})")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.set_ylabel("Total korban kumulatif (orang)")
ax.set_title("Satu program, banyak angka: total korban keracunan menurut tiap lembaga")
ax.legend(fontsize=9, ncol=2)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "grafik_2_korban_per_lembaga.png")); plt.close(fig)

# ============ Grafik 3: insiden terbesar ============
top = insd.sort_values("korban_utama", ascending=True).tail(12)
fig, ax = plt.subplots(figsize=(9.5, 5.2))
ax.barh([f"{r.lokasi} — {r.sekolah_atau_sppg}"[:62] for r in top.itertuples()],
        top["korban_utama"], color="#c0501f")
for i, v in enumerate(top["korban_utama"]):
    ax.text(v + 18, i, f"{v:,}", va="center", fontsize=9)
ax.set_xlim(0, top["korban_utama"].max() * 1.18)
ax.set_xlabel("Korban (orang, angka utama yang diberitakan)")
ax.set_title("12 insiden keracunan MBG terbesar yang diberitakan")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "grafik_3_insiden_terbesar.png")); plt.close(fig)

# ============ Grafik 4: kepuasan survei ============
puas = puas.sort_values("periode_survei")
fig, ax = plt.subplots(figsize=(9.5, 4.4))
ax.bar(range(len(puas)), puas["persen_positif"], color="#1f6fb2")
ax.bar(range(len(puas)), puas["persen_negatif"], bottom=puas["persen_positif"], color="#d9d9d9")
ax.set_xticks(range(len(puas)))
ax.set_xticklabels([f"{r.lembaga.split()[0]}\n{r.periode_survei}" for r in puas.itertuples()], fontsize=8.5)
for i, r in enumerate(puas.itertuples()):
    ax.text(i, r.persen_positif + 1.5, f"{r.persen_positif:.1f}%", ha="center", fontsize=9, fontweight="bold")
ax.set_ylim(0, 108); ax.set_ylabel("% responden")
ax.set_title("Kepuasan publik terhadap MBG (biru = puas; abu = tidak puas, bila dilaporkan)")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "grafik_4_kepuasan_survei.png")); plt.close(fig)

# ============ Grafik 5: sentimen ============
fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
de = meds[(meds["analis"] == "Drone Emprit")].iloc[0]
axes[0].barh(["Drone Emprit\nOkt 2024–Okt 2025"], [de["persen_positif"]], color="#2e8b57", label="Positif 50%")
axes[0].barh(["Drone Emprit\nOkt 2024–Okt 2025"], [de["persen_netral"]], left=[de["persen_positif"]], color="#c9c9c9", label="Netral 14%")
axes[0].barh(["Drone Emprit\nOkt 2024–Okt 2025"], [de["persen_negatif"]],
             left=[de["persen_positif"] + de["persen_netral"]], color="#c0501f", label="Negatif 36%")
axes[0].set_xlim(0, 100); axes[0].legend(fontsize=8); axes[0].set_title("Sentimen percakapan MBG (studi)")
thr_o = thr.sort_values("jumlah_postingan")
axes[1].barh(thr_o["label_indonesia"], thr_o["jumlah_postingan"],
             color=["#8f2d12" if x == "Sangat Negatif" else "#c0501f" if x == "Negatif" else "#bdbdbd" for x in thr_o["label_indonesia"]])
axes[1].set_title("Sampel 50 postingan Threads berinteraksi tertinggi\n(29 Okt 2026; BUKAN sampel representatif)")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "grafik_5_sentimen.png")); plt.close(fig)

# ============ Tabel keluaran ============
insd.sort_values("korban_utama", ascending=False).head(10).to_csv(
    os.path.join(OUT, "tabel_insiden_top10.csv"), index=False)
terakhir_per_lembaga.to_csv(os.path.join(OUT, "tabel_korban_terakhir_per_lembaga.csv"), index=False)

# ============ Ringkasan eksekutif ============
baris_lembaga = "\n".join(
    f"- **{r.lembaga}**: {r.total_korban:,.0f} orang (per {r.tanggal_cutoff.date()})"
    for r in terakhir_per_lembaga.itertuples())
md = f"""# Ringkasan Eksekutif — Analisis Program Makan Bergizi Gratis (MBG)

**Sifat data: 100% DATA ASLI.** Semua angka diambil dari publikasi BGN, Kemenkes, BPOM,
Kemenkeu, lembaga survei, dan pemantau independen yang dapat ditelusuri. Setiap baris dataset
memuat kolom sumber dan URL. MBG diluncurkan 6 Januari 2025 oleh Badan Gizi Nasional (BGN).

## 1. Keberhasilan jangkauan: tumbuh lebih dari 100 kali lipat

- SPPG beroperasi: **190 → 26.723 dapur terverifikasi** (naik **{kali_sppg:.0f} kali**) dari
  6 Jan 2025 ke 29 Okt 2026.
- Penerima manfaat: **570 ribu → 58 juta orang** (naik **{kali_penerima:.0f} kali**).
- Capaian terhadap target akhir 82,9 juta: **{capaian_target:.1f}%**. Target belum tercapai
  menurut angka terakhir BGN sendiri.
- Realisasi anggaran 2025: Rp51,5 triliun dari pagu Rp71 triliun (72,5%). Anggaran 2026 yang
  terpakai s.d. 29 Okt 2026: Rp165 triliun (penyebut pagu 2026 beredar dalam lima versi:
  Rp335 / 268 / 229 / 229,75 / 218,77 triliun).
- Dampak ekonomi yang dinyatakan BGN (Okt 2026): 1.027.998 tenaga aktif dan 63.608 pemasok
  terlibat, 82,83% di antaranya UMKM. Kajian DEN–BPS (Susenas): penerima MBG lebih jarang
  absen; 95% siswa yang menilai menu sangat baik merasa semangat belajarnya meningkat.

## 2. Keracunan: tidak ada satu angka resmi yang disepakati

Total kumulatif terakhir menurut tiap lembaga:

{baris_lembaga}

- Pada rapat yang sama (12 Nov 2025), BGN menyebut 11.640 korban sedangkan Kemenkes 13.371.
- BGN tidak ditemukan merilis total kumulatif lagi setelah November 2025; angka 2026 berasal
  dari Kemenkes dan JPPI.
- Laju kasar lintas sumber (bukan angka resmi; tanggal numerator dan denominator berbeda):
  versi BGN Nov 2025 ≈ **{laju_bgn:.0f} korban per 100 ribu penerima**; versi Kemenkes Sep 2026
  ≈ **{laju_kemenkes:.0f} per 100 ribu penerima**; terhadap porsi tersalurkan ≈
  **{per_juta_porsi:.1f} korban per 1 juta porsi**.
- Insiden terbesar: klaster Bandung Barat (1.333 orang, Sep 2025), Grobogan (803), Rembang
  (777), Sidoarjo (730), SMKN 6 Semarang (707). Hasil lab yang dipublikasikan menunjukkan
  kontaminasi bakteri berulang: *E. coli* (31% temuan lab dalam paparan BGN Okt 2026),
  *Bacillus cereus* (15%), *Staphylococcus aureus* (11%); BGN menyatakan 80–90% kasus yang
  ditelaah berkaitan dengan ketidakpatuhan SOP.
- Definisi korban tidak seragam: di Dramaga (Okt 2026), 481 siswa datang berobat, tetapi BGN
  menyatakan hanya 13 yang masih diobservasi. Angka awal dan angka akhir sering diberitakan
  bergantian.

## 3. SPPG yang ditutup: penindakan nyata, kategorinya tumpang tindih

- 40 dapur ditutup (26 Sep 2025) → 106 dihentikan (20 Okt 2025) → 8.182 pernah di-suspend
  s.d. 29 Mei 2026 → 833 di-suspend permanen (27 Jul 2026) → **1.288 ditutup** dalam paparan
  BGN Oktober 2026, plus 353 kepala SPPG diberhentikan dan Rp311,246 miliar dikembalikan ke
  kas negara dari 414 SPPG.
- 1.288 dapur ditutup setara **{persen_ditutup:.1f}%** dari 26.385 SPPG beroperasi (9 Okt 2026).
- Kategori pernah-suspend, permanen, dan ditutup **tumpang tindih dan tidak boleh dijumlahkan**.

## 4. Penilaian publik: dari sangat positif menjadi terbelah

- Awal program sangat diterima: persetujuan LSI 89,6% (2025); kepuasan Indikator 64,6%
  (Jan 2025) dan memuncak 72,8% (Jan 2026).
- Oktober 2026 terbelah dan cenderung negatif pada pertanyaan kepuasan pelaksanaan:
  Poltracking 47,4% puas vs 49,5% tidak puas; IPO 36% puas vs 64% tidak puas. Di antara
  keluarga penerima (Tempo Data Science, Agt 2026): 48% puas vs 51% tidak puas. Lembaga dengan
  pertanyaan persetujuan/manfaat (Voxpol 61,1%; Adidaya 69,9%) tetap lebih positif, jadi angka
  antar-lembaga tidak bisa dirata-rata.
- Sentimen media sosial: Drone Emprit (Okt 2024–Okt 2025) mencatat 50% positif / 36% negatif /
  14% netral untuk percakapan MBG; INDEF mencatat negatif X dan TikTok melonjak 85% menjadi
  97% selama September 2025 dan 83% pada analisis Oktober 2026.
- Sampel Threads project ini (50 postingan berinteraksi tertinggi, diambil 29 Okt 2026,
  mayoritas Oktober 2026): **{thr_neg} dari {thr_total} postingan ({thr_neg/thr_total*100:.0f}%)
  berlabel negatif atau sangat negatif, dan tidak ada satu pun berlabel positif**. Suara pro
  muncul di kolom komentar postingan terbelah, misalnya orang tua yang merasa terbantu.
  Sampel ini bias ke masa krisis dan tidak mewakili publik umum; bandingkan dengan survei.

## Keterbatasan (dibaca sebelum mengutip)

1. Tidak ada dataset resmi terbuka per-insiden; daftar insiden disusun dari pemberitaan.
2. Total korban antar-lembaga memakai definisi dan cut-off berbeda; jangan digabung.
3. Penyebut anggaran 2026 ada lima versi; persentase realisasi hanya sah bersama tanggalnya.
4. Angka penerima 2026 sempat terkoreksi dari 63 juta menjadi 58 juta karena 6 juta data
   ganda; angka bulan-bulan sebelumnya (65 juta, Feb 2026) sudah tidak berlaku.
5. Survei antar-lembaga berbeda pertanyaan dan basis responden; bukan satu tren tunggal.
6. Sampel Threads adalah sampel kemudahan berbasis interaksi, bukan sampel probabilitas.
"""
with open(os.path.join(OUT, "ringkasan_eksekutif.md"), "w", encoding="utf-8") as f:
    f.write(md)

print("kali_sppg", round(kali_sppg, 1), "| kali_penerima", round(kali_penerima, 1),
      "| capaian target %", round(capaian_target, 1))
print("laju per 100rb: BGN", round(laju_bgn, 1), "| Kemenkes", round(laju_kemenkes, 1),
      "| per juta porsi", round(per_juta_porsi, 2))
print("persen ditutup", round(persen_ditutup, 2), "| threads negatif", thr_neg, "dari", thr_total)
print("Output:", sorted(os.listdir(OUT)))
