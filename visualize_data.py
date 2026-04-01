import pandas as pd
import matplotlib.pyplot as plt

# ── Veri yükleme ──────────────────────────────────────────────
df = pd.read_csv("data.csv", encoding="utf-8")

col_names = {
    "Batarya_Döngü_Sayısı":    "Batarya Döngü Sayısı",
    "Günlük_Şarj_Tüketimi_%":  "Günlük Şarj Tüketimi (%)",
    "Batarya_Sağlığı_%":        "Batarya Sağlığı (%)",
    "Ortalama_Sıcaklık_°C":    "Ort. Sıcaklık (°C)"
}
cols = list(df.columns)          # orijinal sütun adları
labels = list(col_names.values())

COLORS = ["#4C72B0", "#DD8452", "#55A868", "#C44E52"]

# ══════════════════════════════════════════════════════════════
# 1. Histogram – Her değişkenin dağılımı
# ══════════════════════════════════════════════════════════════
fig1, axes = plt.subplots(2, 2, figsize=(12, 8))
fig1.suptitle("Değişken Dağılımları (Histogram)", fontsize=15, fontweight="bold")

for ax, col, label, color in zip(axes.flat, cols, labels, COLORS):
    ax.hist(df[col], bins=20, color=color, edgecolor="white", linewidth=0.6)
    ax.set_title(label, fontsize=11)
    ax.set_xlabel("Değer")
    ax.set_ylabel("Frekans")
    ax.grid(axis="y", alpha=0.4)

plt.tight_layout()
plt.savefig("grafik_1_histogram.png", dpi=150)
print("Kaydedildi: grafik_1_histogram.png")

# ══════════════════════════════════════════════════════════════
# 2. Boxplot – Aykırı değerler ve yayılım
# ══════════════════════════════════════════════════════════════
fig2, ax = plt.subplots(figsize=(10, 6))
fig2.suptitle("Değişken Yayılımı (Boxplot)", fontsize=15, fontweight="bold")

bp = ax.boxplot(
    [df[c] for c in cols],
    patch_artist=True,
    tick_labels=labels,
    medianprops=dict(color="black", linewidth=2)
)
for patch, color in zip(bp["boxes"], COLORS):
    patch.set_facecolor(color)
    patch.set_alpha(0.75)

ax.set_ylabel("Değer")
ax.grid(axis="y", alpha=0.4)
plt.xticks(fontsize=9)
plt.tight_layout()
plt.savefig("grafik_2_boxplot.png", dpi=150)
print("Kaydedildi: grafik_2_boxplot.png")

# ══════════════════════════════════════════════════════════════
# 3. Scatter – Batarya Sağlığı vs Sıcaklık
#              Şarj Tüketimi vs Döngü Sayısı
# ══════════════════════════════════════════════════════════════
fig3, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
fig3.suptitle("Değişkenler Arası İlişki (Scatter)", fontsize=15, fontweight="bold")

ax1.scatter(df[cols[2]], df[cols[3]], alpha=0.45, color=COLORS[2], edgecolors="white", linewidth=0.3)
ax1.set_xlabel("Batarya Sağlığı (%)")
ax1.set_ylabel("Ort. Sıcaklık (°C)")
ax1.set_title("Batarya Sağlığı – Sıcaklık")
ax1.grid(alpha=0.3)

ax2.scatter(df[cols[0]], df[cols[1]], alpha=0.45, color=COLORS[1], edgecolors="white", linewidth=0.3)
ax2.set_xlabel("Batarya Döngü Sayısı")
ax2.set_ylabel("Günlük Şarj Tüketimi (%)")
ax2.set_title("Döngü Sayısı – Günlük Tüketim")
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.savefig("grafik_3_scatter.png", dpi=150)
print("Kaydedildi: grafik_3_scatter.png")

# ══════════════════════════════════════════════════════════════
# 4. Korelasyon Matrisi (Matplotlib heatmap)
# ══════════════════════════════════════════════════════════════
corr = df.corr(numeric_only=True).values

fig4, ax = plt.subplots(figsize=(7, 6))
fig4.suptitle("Korelasyon Matrisi", fontsize=15, fontweight="bold")

im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
plt.colorbar(im, ax=ax)

ax.set_xticks(range(len(labels)))
ax.set_yticks(range(len(labels)))
ax.set_xticklabels(labels, rotation=20, ha="right", fontsize=8)
ax.set_yticklabels(labels, fontsize=8)

for i in range(len(labels)):
    for j in range(len(labels)):
        ax.text(j, i, f"{corr[i, j]:.2f}", ha="center", va="center",
                fontsize=9, color="black" if abs(corr[i, j]) < 0.6 else "white")

plt.tight_layout()
plt.savefig("grafik_4_korelasyon.png", dpi=150)
print("Kaydedildi: grafik_4_korelasyon.png")

# ══════════════════════════════════════════════════════════════
# 5. Döngü Sayısına göre Ortalama Tüketim (Bar Chart)
# ══════════════════════════════════════════════════════════════
avg_by_cycle = df.groupby(cols[0])[cols[1]].mean()

fig5, ax = plt.subplots(figsize=(8, 5))
fig5.suptitle("Döngü Sayısına Göre Ortalama Günlük Şarj Tüketimi", fontsize=13, fontweight="bold")

bars = ax.bar(avg_by_cycle.index.astype(str), avg_by_cycle.values,
              color=COLORS[0], edgecolor="white", linewidth=0.8)

for bar, val in zip(bars, avg_by_cycle.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f"{val:.1f}%", ha="center", va="bottom", fontsize=9)

ax.set_xlabel("Günlük Döngü Sayısı")
ax.set_ylabel("Ort. Şarj Tüketimi (%)")
ax.grid(axis="y", alpha=0.4)
plt.tight_layout()
plt.savefig("grafik_5_bar.png", dpi=150)
print("Kaydedildi: grafik_5_bar.png")

plt.show()
print("\nTüm grafikler olusturuldu ve PNG olarak kaydedildi.")
