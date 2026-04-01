import csv
import random

# ── Normal dağılım yardımcısı ──────────────────────────────────
def gauss_clamp(mu, sigma, lo, hi, as_int=False):
    """Normal dağılımdan örnek üretir; [lo, hi] aralığına kırpar."""
    value = random.gauss(mu, sigma)
    value = max(lo, min(hi, value))
    return round(value) if as_int else round(float(value), 1)

# ── Veri seti parametreleri ────────────────────────────────────
NUM_ROWS    = 500
OUTPUT_FILE = "data.csv"

# Değişken 1: Batarya Döngü Sayısı  (0 – 4)
#   Çoğu kullanıcı günde 1-2 kez şarj eder → mu=1.5
CYCLE_MU,  CYCLE_SIGMA,  CYCLE_LO,  CYCLE_HI  = 1.5, 0.8,  0,    4

# Değişken 2: Günlük Şarj Tüketimi (%)  (50 – 130)
#   Ortalama iPhone kullanıcısı ~85% harcar → mu=85
CONS_MU,   CONS_SIGMA,   CONS_LO,   CONS_HI   = 85,  15,   50,   130

# Değişken 3: Batarya Sağlığı (%)  (79 – 100)
#   Kullanıcıların büyük çoğunluğu %88-92 aralığında → mu=90
HEALTH_MU, HEALTH_SIGMA, HEALTH_LO, HEALTH_HI = 90,  4,    79,   100

# Değişken 4: Ortalama Sıcaklık (°C)  (20 – 45)
#   Normal kullanımda ~30°C civarı → mu=30
TEMP_MU,   TEMP_SIGMA,   TEMP_LO,   TEMP_HI   = 30,  5,    20.0, 45.0

# ── CSV başlık satırı ──────────────────────────────────────────
HEADERS = [
    "Batarya_Döngü_Sayısı",
    "Günlük_Şarj_Tüketimi_%",
    "Batarya_Sağlığı_%",
    "Ortalama_Sıcaklık_°C"
]

def generate_row():
    """Normal dağılım (çan eğrisi) ile gerçekçi bir veri satırı üretir."""
    cycle_count = gauss_clamp(CYCLE_MU,  CYCLE_SIGMA,  CYCLE_LO,  CYCLE_HI,  as_int=True)
    consumption = gauss_clamp(CONS_MU,   CONS_SIGMA,   CONS_LO,   CONS_HI,   as_int=True)
    health      = gauss_clamp(HEALTH_MU, HEALTH_SIGMA, HEALTH_LO, HEALTH_HI, as_int=True)
    temperature = gauss_clamp(TEMP_MU,   TEMP_SIGMA,   TEMP_LO,   TEMP_HI,   as_int=False)
    return [cycle_count, consumption, health, temperature]

def main():
    rows = [generate_row() for _ in range(NUM_ROWS)]

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(HEADERS)
        writer.writerows(rows)

    print(f"'{OUTPUT_FILE}' olusturuldu — {NUM_ROWS} satir, normal dagilim (can egrisi).")
    print()
    print("Dagilim Parametreleri (mu / sigma / min / max):")
    print(f"  Batarya Dongu Sayisi     : {CYCLE_MU} / {CYCLE_SIGMA} / {CYCLE_LO} / {CYCLE_HI}")
    print(f"  Gunluk Sarj Tuketimi (%) : {CONS_MU} / {CONS_SIGMA} / {CONS_LO} / {CONS_HI}")
    print(f"  Batarya Sagligi (%)      : {HEALTH_MU} / {HEALTH_SIGMA} / {HEALTH_LO} / {HEALTH_HI}")
    print(f"  Ortalama Sicaklik (C)    : {TEMP_MU} / {TEMP_SIGMA} / {TEMP_LO} / {TEMP_HI}")

if __name__ == "__main__":
    main()
