"""
Vehicle Inspection Quality & Pricing Analysis
Author: Mohd Aaseen
Dataset: 10,000+ Used Car Listings (India)
Tools: Python (Pandas, Matplotlib, Seaborn)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ── Config ──────────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="Blues_d")
plt.rcParams.update({'font.family': 'DejaVu Sans', 'figure.dpi': 150})
BLUE = "#1a56a0"
COLORS = ["#1a56a0", "#2e86de", "#54a0ff", "#a29bfe", "#fd79a8", "#00b894", "#fdcb6e", "#e17055", "#6c5ce7", "#00cec9"]

df = pd.read_csv("data/car_inspection_data.csv")

print("=" * 55)
print("  VEHICLE INSPECTION QUALITY & PRICING ANALYSIS")
print("=" * 55)
print(f"\n📦 Dataset Shape   : {df.shape[0]:,} rows × {df.shape[1]} columns")
print(f"🚗 Brands Covered  : {df['brand'].nunique()} OEM brands")
print(f"📅 Year Range      : {df['year'].min()} – {df['year'].max()}")
print(f"💰 Price Range     : ₹{df['selling_price'].min():,.0f} – ₹{df['selling_price'].max():,.0f}")
print(f"🔍 Inspection Grades: {sorted(df['inspection_grade'].unique())}")

# ── EDA ─────────────────────────────────────────────────
print("\n── Missing Values ──")
print(df.isnull().sum())

print("\n── Statistical Summary ──")
print(df[['age', 'km_driven', 'selling_price']].describe().round(0))

# ── Key Insights ────────────────────────────────────────
print("\n" + "=" * 55)
print("  KEY BUSINESS INSIGHTS")
print("=" * 55)

# 1. Brand avg price
brand_avg = df.groupby('brand')['selling_price'].mean().sort_values(ascending=False)
print("\n1. Average Resale Price by Brand (Top 5):")
for b, p in brand_avg.head(5).items():
    print(f"   {b:<15} ₹{p:>10,.0f}")

# 2. Inspection grade impact
grade_avg = df.groupby('inspection_grade')['selling_price'].mean().sort_values(ascending=False)
grade_a = grade_avg['A']
grade_d = grade_avg['D']
premium = ((grade_a - grade_d) / grade_d) * 100
print(f"\n2. Inspection Grade Impact:")
for g, p in grade_avg.items():
    print(f"   Grade {g}: ₹{p:>10,.0f}")
print(f"   → Grade A commands {premium:.1f}% premium over Grade D")

# 3. Fuel type
fuel_avg = df.groupby('fuel_type')['selling_price'].mean().sort_values(ascending=False)
petrol = fuel_avg['Petrol']
diesel = fuel_avg['Diesel']
diesel_premium = ((diesel - petrol) / petrol) * 100
print(f"\n3. Fuel Type Pricing:")
for f, p in fuel_avg.items():
    print(f"   {f:<10} ₹{p:>10,.0f}")
print(f"   → Diesel commands {diesel_premium:.1f}% premium over Petrol")

# 4. Transmission
trans_avg = df.groupby('transmission')['selling_price'].mean()
auto = trans_avg['Automatic']
manual = trans_avg['Manual']
auto_premium = ((auto - manual) / manual) * 100
print(f"\n4. Transmission Premium:")
print(f"   Automatic : ₹{auto:>10,.0f}")
print(f"   Manual    : ₹{manual:>10,.0f}")
print(f"   → Automatic commands {auto_premium:.1f}% premium")

# 5. KM impact
km_bins = [0, 30000, 60000, 100000, 150000, 300000]
km_labels = ['0–30K', '30–60K', '60–100K', '100–150K', '150K+']
df['km_bucket'] = pd.cut(df['km_driven'], bins=km_bins, labels=km_labels)
km_avg = df.groupby('km_bucket')['selling_price'].mean()
print(f"\n5. Price by KM Driven:")
for k, p in km_avg.items():
    print(f"   {k:<12} ₹{p:>10,.0f}")

# ── Visualizations ───────────────────────────────────────
fig = plt.figure(figsize=(20, 24))
fig.patch.set_facecolor('#f8f9fa')
gs = gridspec.GridSpec(3, 2, figure=fig, hspace=0.45, wspace=0.35)

# Plot 1: Brand avg price
ax1 = fig.add_subplot(gs[0, 0])
bars = ax1.barh(brand_avg.index, brand_avg.values / 1e5, color=COLORS[:len(brand_avg)])
ax1.set_xlabel("Avg Selling Price (₹ Lakhs)", fontsize=11)
ax1.set_title("Average Resale Price by Brand", fontsize=13, fontweight='bold', color=BLUE)
for bar, val in zip(bars, brand_avg.values):
    ax1.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
             f'₹{val/1e5:.1f}L', va='center', fontsize=9)
ax1.set_facecolor('#ffffff')

# Plot 2: Inspection grade vs price
ax2 = fig.add_subplot(gs[0, 1])
grade_order = ['A', 'B', 'C', 'D']
grade_data = df.groupby('inspection_grade')['selling_price'].mean().reindex(grade_order)
bar_colors = ["#1a56a0", "#2e86de", "#fdcb6e", "#e17055"]
bars2 = ax2.bar(grade_data.index, grade_data.values / 1e5, color=bar_colors, edgecolor='white', linewidth=1.5)
ax2.set_xlabel("Inspection Grade", fontsize=11)
ax2.set_ylabel("Avg Selling Price (₹ Lakhs)", fontsize=11)
ax2.set_title("Inspection Grade Impact on Resale Price", fontsize=13, fontweight='bold', color=BLUE)
for bar, val in zip(bars2, grade_data.values):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
             f'₹{val/1e5:.1f}L', ha='center', fontsize=10, fontweight='bold')
ax2.set_facecolor('#ffffff')

# Plot 3: Price depreciation by age
ax3 = fig.add_subplot(gs[1, 0])
age_avg = df.groupby('age')['selling_price'].mean()
ax3.plot(age_avg.index, age_avg.values / 1e5, color=BLUE, linewidth=2.5, marker='o', markersize=5)
ax3.fill_between(age_avg.index, age_avg.values / 1e5, alpha=0.15, color=BLUE)
ax3.set_xlabel("Vehicle Age (Years)", fontsize=11)
ax3.set_ylabel("Avg Selling Price (₹ Lakhs)", fontsize=11)
ax3.set_title("Price Depreciation Over Vehicle Age", fontsize=13, fontweight='bold', color=BLUE)
ax3.set_facecolor('#ffffff')

# Plot 4: Fuel type price comparison
ax4 = fig.add_subplot(gs[1, 1])
fuel_order = fuel_avg.sort_values(ascending=False)
fuel_colors = ["#e17055", "#1a56a0", "#00b894", "#a29bfe"]
bars4 = ax4.bar(fuel_order.index, fuel_order.values / 1e5, color=fuel_colors, edgecolor='white', linewidth=1.5)
ax4.set_xlabel("Fuel Type", fontsize=11)
ax4.set_ylabel("Avg Selling Price (₹ Lakhs)", fontsize=11)
ax4.set_title("Resale Price by Fuel Type", fontsize=13, fontweight='bold', color=BLUE)
for bar, val in zip(bars4, fuel_order.values):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
             f'₹{val/1e5:.1f}L', ha='center', fontsize=10, fontweight='bold')
ax4.set_facecolor('#ffffff')

# Plot 5: KM bucket vs price
ax5 = fig.add_subplot(gs[2, 0])
km_plot = df.groupby('km_bucket', observed=True)['selling_price'].mean()
bars5 = ax5.bar(km_plot.index, km_plot.values / 1e5, color=COLORS[:5], edgecolor='white', linewidth=1.5)
ax5.set_xlabel("KM Driven Range", fontsize=11)
ax5.set_ylabel("Avg Selling Price (₹ Lakhs)", fontsize=11)
ax5.set_title("Resale Price by Mileage Range", fontsize=13, fontweight='bold', color=BLUE)
for bar, val in zip(bars5, km_plot.values):
    ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
             f'₹{val/1e5:.1f}L', ha='center', fontsize=9, fontweight='bold')
ax5.set_facecolor('#ffffff')

# Plot 6: Heatmap brand x grade
ax6 = fig.add_subplot(gs[2, 1])
heatmap_data = df.groupby(['brand', 'inspection_grade'])['selling_price'].mean().unstack() / 1e5
heatmap_data = heatmap_data[['A', 'B', 'C', 'D']]
sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap='Blues', ax=ax6,
            linewidths=0.5, linecolor='white', cbar_kws={'label': '₹ Lakhs'})
ax6.set_title("Brand × Inspection Grade Price Matrix (₹ Lakhs)", fontsize=13, fontweight='bold', color=BLUE)
ax6.set_xlabel("Inspection Grade", fontsize=11)
ax6.set_ylabel("Brand", fontsize=11)

fig.suptitle("Vehicle Inspection Quality & Pricing Analysis\nIndia Used Car Market — 10,000+ Listings",
             fontsize=16, fontweight='bold', color=BLUE, y=0.98)

plt.savefig("images/analysis_dashboard.png", bbox_inches='tight', facecolor='#f8f9fa')
plt.close()
print("\n✅ Dashboard saved: images/analysis_dashboard.png")
print("\n✅ Analysis Complete!")
