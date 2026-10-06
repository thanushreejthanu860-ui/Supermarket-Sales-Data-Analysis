# ============================================================
#   Supermarket Sales Data Analysis
#   Beginner-Level Python Project
#   Libraries: pandas, matplotlib
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ── Helper: print a section heading ─────────────────────────
def section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

# ============================================================
# SECTION 1 — Load the dataset
# ============================================================
section("1. Loading the Dataset")

# Read the CSV file into a pandas DataFrame
# encoding='utf-8-sig' handles the hidden BOM character at the
# start of the file so the first column name is read correctly
df = pd.read_csv("SuperMarket Analysis.csv", encoding="utf-8-sig")

# Convert the Date column to a proper datetime type so we can
# extract month names later
df["Date"] = pd.to_datetime(df["Date"])

# Extract a readable month name (e.g. "January") from the date
df["Month"] = df["Date"].dt.strftime("%B")

# Fix column name casing for easier access
df.rename(columns={"Sales": "Sales", "gross income": "Gross Income"}, inplace=True)

print(f"File loaded successfully!")
print(f"  Rows    : {df.shape[0]}")
print(f"  Columns : {df.shape[1]}")

# ============================================================
# SECTION 2 — Basic Dataset Overview
# ============================================================
section("2. Dataset Overview")

print("\nColumn names and data types:")
print(df.dtypes.to_string())

# ============================================================
# SECTION 3 — Check for Missing Values
# ============================================================
section("3. Missing Values Check")

missing = df.isnull().sum()
total_missing = missing.sum()

if total_missing == 0:
    print("[OK] No missing values found. The dataset is complete!")
else:
    print("[!] Missing values detected:")
    print(missing[missing > 0])

# ============================================================
# SECTION 4 — Check for Duplicate Records
# ============================================================
section("4. Duplicate Records Check")

duplicates = df.duplicated().sum()

if duplicates == 0:
    print("[OK] No duplicate records found.")
else:
    print(f"[!] {duplicates} duplicate rows found.")

# ============================================================
# SECTION 5 — Core Sales Metrics
# ============================================================
section("5. Core Sales Metrics")

total_sales        = df["Sales"].sum()
total_quantity     = df["Quantity"].sum()
total_gross_income = df["Gross Income"].sum()
avg_rating         = df["Rating"].mean()
total_transactions = len(df)
avg_sale_per_txn   = df["Sales"].mean()

print(f"  Total Sales Revenue   : ${total_sales:,.2f}")
print(f"  Total Quantity Sold   : {total_quantity:,} units")
print(f"  Total Gross Income    : ${total_gross_income:,.2f}")
print(f"  Total Transactions    : {total_transactions:,}")
print(f"  Average Sale (per txn): ${avg_sale_per_txn:,.2f}")
print(f"  Average Customer Rating: {avg_rating:.2f} / 10")

# ============================================================
# SECTION 6 — Sales by Product Line
# ============================================================
section("6. Sales by Product Line")

product_sales = (
    df.groupby("Product line")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print(product_sales.apply(lambda x: f"${x:,.2f}").to_string())

# ============================================================
# SECTION 7 — Sales by Branch
# ============================================================
section("7. Sales by Branch")

branch_sales = (
    df.groupby("Branch")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print(branch_sales.apply(lambda x: f"${x:,.2f}").to_string())

# ============================================================
# SECTION 8 — Sales by Payment Method
# ============================================================
section("8. Sales by Payment Method")

payment_sales = (
    df.groupby("Payment")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print(payment_sales.apply(lambda x: f"${x:,.2f}").to_string())

# ============================================================
# SECTION 9 — Member vs Normal Customers
# ============================================================
section("9. Member vs Normal Customers")

customer_stats = df.groupby("Customer type").agg(
    Total_Sales    = ("Sales", "sum"),
    Avg_Sale       = ("Sales", "mean"),
    Transactions   = ("Sales", "count")
)

print(customer_stats.to_string())

# ============================================================
# SECTION 10 — Male vs Female Sales
# ============================================================
section("10. Male vs Female Sales")

gender_stats = df.groupby("Gender").agg(
    Total_Sales  = ("Sales", "sum"),
    Avg_Sale     = ("Sales", "mean"),
    Transactions = ("Sales", "count")
)

print(gender_stats.to_string())

# ============================================================
# SECTION 11 — Monthly Sales
# ============================================================
section("11. Monthly Sales")

# Keep months in calendar order
month_order = ["January", "February", "March"]
monthly_sales = (
    df.groupby("Month")["Sales"]
    .sum()
    .reindex(month_order)
)

print(monthly_sales.apply(lambda x: f"${x:,.2f}").to_string())

# ============================================================
# SECTION 12 — Top-Selling Product Categories (by Quantity)
# ============================================================
section("12. Top-Selling Categories by Quantity Sold")

product_qty = (
    df.groupby("Product line")["Quantity"]
    .sum()
    .sort_values(ascending=False)
)

print(product_qty.to_string())

# ============================================================
# SECTION 13 — LANDSCAPE DASHBOARD  (FIXED: GridSpec only)
# ============================================================
# KEY DESIGN DECISION:
# All axes — header, KPI cards, and chart panels — are created
# via GridSpec / GridSpecFromSubplotSpec.  Card styling is done
# on the axes themselves (set_facecolor, spine colours) so that
# NO figure-level patch can ever obscure chart content.
# ============================================================
section("13. Building Dashboard...")

import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches

# ── Colour palette (navy / teal / blue family) ──────────────
C_NAVY   = "#0B2B4E"   # deep navy    – header bg, primary bars
C_TEAL   = "#0E6B6B"   # dark teal    – accent strip, line chart
C_BLUE   = "#1A6FB5"   # medium blue  – secondary bars
C_LTEAL  = "#2AABB0"   # light teal   – line fill, pie slice
C_SKY    = "#74BCD4"   # sky blue     – lighter bar fill
C_ICE    = "#B8DDE8"   # ice blue     – histogram fill, area
C_BG     = "#F0F4F8"   # very light blue-grey – figure bg
C_CARD   = "#FFFFFF"   # white – KPI & chart card face
C_BORDER = "#D0DCE8"   # soft border colour
C_TEXT   = "#0B2B4E"   # navy text
C_MUTED  = "#4A6070"   # muted axis labels / subtitles
C_GRID   = "#E0EAF2"   # faint grid lines
C_ACCENT = "#D95E2B"   # amber – mean-rating line only

# 6-step bar palette for product-line chart (navy→sky)
C_CAT6 = [C_NAVY, C_TEAL, C_BLUE, C_LTEAL, C_SKY, "#9BBDD4"]

# ── Global rcParams ──────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor":  C_BG,
    "axes.facecolor":    C_CARD,
    "axes.edgecolor":    C_BORDER,
    "axes.linewidth":    0.5,
    "axes.titlesize":    8.5,
    "axes.titleweight":  "bold",
    "axes.titlecolor":   C_TEXT,
    "axes.titlepad":     7,
    "axes.labelsize":    7,
    "axes.labelcolor":   C_MUTED,
    "xtick.labelsize":   6.5,
    "ytick.labelsize":   6.5,
    "xtick.color":       C_MUTED,
    "ytick.color":       C_MUTED,
    "xtick.major.size":  0,
    "ytick.major.size":  0,
    "grid.color":        C_GRID,
    "grid.linewidth":    0.5,
    "font.family":       "DejaVu Sans",
    "legend.frameon":    False,
    "legend.fontsize":   6.5,
})

# ── Axes styling helper ──────────────────────────────────────
def style_ax(ax, grid="y"):
    """Remove decorative spines; add a subtle one-axis grid."""
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_facecolor(C_CARD)
    if grid == "y":
        ax.yaxis.grid(True, linestyle="--", linewidth=0.45, color=C_GRID)
        ax.xaxis.grid(False)
        ax.set_axisbelow(True)
    elif grid == "x":
        ax.xaxis.grid(True, linestyle="--", linewidth=0.45, color=C_GRID)
        ax.yaxis.grid(False)
        ax.set_axisbelow(True)
    else:
        ax.yaxis.grid(False)
        ax.xaxis.grid(False)

# ════════════════════════════════════════════════════════════
# FIGURE  —  20 × 11 landscape
#
# Outer GridSpec: 3 rows
#   row 0  height 9.5%  →  header banner
#   row 1  height 9.0%  →  KPI card row
#   row 2  height 81.5% →  chart area (2 rows × 4 cols)
#
# Using GridSpec rows for ALL zones means every Axes is a
# proper subplot child — patches drawn on the axes background
# (ax.set_facecolor / ax.patch) stay behind the chart content
# automatically, with no z-order conflict.
# ════════════════════════════════════════════════════════════
fig = plt.figure(figsize=(20, 11), facecolor=C_BG)

gs_outer = gridspec.GridSpec(
    3, 1,
    figure=fig,
    height_ratios=[0.095, 0.090, 0.815],
    hspace=0.065,          # increased gap → clear space between KPI and charts
    left=0.0, right=1.0,
    top=1.0, bottom=0.0,
)

# ── ZONE A: Header row ───────────────────────────────────────
ax_hdr = fig.add_subplot(gs_outer[0, 0])
ax_hdr.set_facecolor(C_NAVY)
for sp in ax_hdr.spines.values():
    sp.set_visible(False)
ax_hdr.set_xticks([])
ax_hdr.set_yticks([])

# Teal left-edge accent strip painted inside the header axes
ax_hdr.add_patch(mpatches.Rectangle(
    (0, 0), 0.006, 1,
    transform=ax_hdr.transAxes,
    facecolor=C_LTEAL, linewidth=0, zorder=3,
))

# Two-line title (left-aligned)
ax_hdr.text(0.013, 0.70, "SUPERMARKET SALES",
            transform=ax_hdr.transAxes,
            ha="left", va="center",
            fontsize=16, fontweight="bold", color="#FFFFFF")
ax_hdr.text(0.013, 0.22, "ANALYSIS DASHBOARD",
            transform=ax_hdr.transAxes,
            ha="left", va="center",
            fontsize=11, fontweight="bold", color=C_ICE)

# Right-aligned italic subtitle
ax_hdr.text(0.99, 0.50,
            "Sales Performance   |   Customer Insights   |   Product Analysis",
            transform=ax_hdr.transAxes,
            ha="right", va="center",
            fontsize=8, color=C_ICE, fontstyle="italic")

# ── ZONE B: KPI cards (5 equal columns) ─────────────────────
gs_kpi = gridspec.GridSpecFromSubplotSpec(
    1, 5,
    subplot_spec=gs_outer[1, 0],
    wspace=0.022,
)

kpi_rows = [
    ("TOTAL SALES",    f"${total_sales:,.0f}",          C_TEAL),
    ("TOTAL QUANTITY", f"{total_quantity:,} units",      C_BLUE),
    ("GROSS INCOME",   f"${total_gross_income:,.0f}",    C_LTEAL),
    ("AVG RATING",     f"{avg_rating:.2f} / 10",         C_SKY),
    ("TRANSACTIONS",   f"{total_transactions:,}",        C_NAVY),
]

for i, (lbl, val, accent) in enumerate(kpi_rows):
    ax_k = fig.add_subplot(gs_kpi[0, i])
    ax_k.set_facecolor(C_CARD)
    for sp in ax_k.spines.values():
        sp.set_color(C_BORDER)
        sp.set_linewidth(0.6)
    ax_k.set_xticks([])
    ax_k.set_yticks([])

    # Left accent colour strip inside the card axes
    ax_k.add_patch(mpatches.Rectangle(
        (0, 0), 0.045, 1,
        transform=ax_k.transAxes,
        facecolor=accent, linewidth=0, zorder=3,
    ))

    # KPI label  (small, uppercase, muted)
    ax_k.text(0.10, 0.74, lbl,
              transform=ax_k.transAxes,
              ha="left", va="center",
              fontsize=6.5, color=C_MUTED)

    # KPI value  (large, bold, navy)
    ax_k.text(0.10, 0.34, val,
              transform=ax_k.transAxes,
              ha="left", va="center",
              fontsize=12.5, color=C_TEXT, fontweight="bold")

# ── ZONE C: Chart area ──────────────────────────────────────
# 2 rows × 4 columns, unequal column widths to give the
# product-line chart and the units chart more horizontal space.
gs_charts = gridspec.GridSpecFromSubplotSpec(
    2, 4,
    subplot_spec=gs_outer[2, 0],
    width_ratios=[2.1, 1.55, 1.0, 1.0],
    height_ratios=[1, 1],
    hspace=0.50,
    wspace=0.30,
)

# Helper: create a subplot with white card background
def card_ax(spec):
    ax = fig.add_subplot(spec)
    ax.set_facecolor(C_CARD)
    for sp in ax.spines.values():
        sp.set_color(C_BORDER)
        sp.set_linewidth(0.5)
    return ax

# ── CHART 1 — Total Sales by Product Line ───────────────────
ax1 = card_ax(gs_charts[0, 0])
bars1 = ax1.bar(
    product_sales.index, product_sales.values,
    color=C_CAT6, width=0.58,
    edgecolor="white", linewidth=0.4, zorder=3,
)
ax1.set_title("Total Sales by Product Line")
ax1.set_xticks(range(len(product_sales)))
ax1.set_xticklabels(product_sales.index,
                    rotation=22, ha="right", fontsize=6.5)
ax1.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"${x/1000:.0f}K"))
ax1.bar_label(bars1,
              labels=[f"${v/1000:.0f}K" for v in product_sales.values],
              padding=3, fontsize=6.5, color=C_TEXT, fontweight="bold")
ax1.set_ylim(0, product_sales.max() * 1.22)
style_ax(ax1)

# ── CHART 2 — Monthly Sales Trend ───────────────────────────
ax2 = card_ax(gs_charts[0, 1])
ax2.fill_between(monthly_sales.index, monthly_sales.values,
                 color=C_LTEAL, alpha=0.18, zorder=1)
ax2.plot(monthly_sales.index, monthly_sales.values,
         marker="o", linewidth=2.5, markersize=8,
         color=C_TEAL, markerfacecolor="white",
         markeredgewidth=2, markeredgecolor=C_TEAL, zorder=3)
for month, val in monthly_sales.items():
    ax2.annotate(
        f"${val/1000:.1f}K", (month, val),
        textcoords="offset points", xytext=(0, 10),
        ha="center", fontsize=7, fontweight="bold", color=C_TEAL,
    )
ax2.set_title("Monthly Sales Trend  (Jan \u2013 Mar 2019)")
ax2.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"${x/1000:.0f}K"))
ax2.set_ylim(0, monthly_sales.max() * 1.30)
style_ax(ax2)

# ── CHART 3 — Sales by Branch ────────────────────────────────
ax3 = card_ax(gs_charts[0, 2])
bars3 = ax3.bar(
    branch_sales.index, branch_sales.values,
    color=[C_NAVY, C_TEAL, C_SKY], width=0.50,
    edgecolor="white", linewidth=0.4, zorder=3,
)
ax3.set_title("Sales by Branch")
ax3.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"${x/1000:.0f}K"))
ax3.bar_label(bars3,
              labels=[f"${v/1000:.0f}K" for v in branch_sales.values],
              padding=3, fontsize=7, color=C_TEXT, fontweight="bold")
ax3.set_ylim(0, branch_sales.max() * 1.22)
style_ax(ax3)

# ── CHART 4 — Payment Method Pie ─────────────────────────────
ax4 = card_ax(gs_charts[0, 3])
ax4.set_facecolor(C_CARD)
wedges, texts, autotexts = ax4.pie(
    payment_sales.values,
    labels=payment_sales.index,
    autopct="%1.0f%%",
    colors=[C_NAVY, C_TEAL, C_SKY],
    startangle=90,
    wedgeprops={"edgecolor": "white", "linewidth": 1.8},
    textprops={"fontsize": 7, "color": C_TEXT},
    pctdistance=0.68,
    radius=0.88,
)
for at in autotexts:
    at.set_fontsize(7.5)
    at.set_fontweight("bold")
    at.set_color("white")
ax4.set_title("Payment Method")
style_ax(ax4, grid="none")

# ── CHART 5 — Units Sold by Category ─────────────────────────
ax5 = card_ax(gs_charts[1, 0])
bars5 = ax5.barh(
    product_qty.index, product_qty.values,
    color=C_TEAL, edgecolor="white", linewidth=0.4,
    height=0.52, zorder=3,
)
ax5.set_title("Units Sold by Product Category")
ax5.bar_label(bars5,
              labels=[f"{int(v):,}" for v in product_qty.values],
              padding=4, fontsize=7, color=C_TEXT, fontweight="bold")
ax5.set_xlim(0, product_qty.max() * 1.18)
ax5.tick_params(axis="y", labelsize=6.8)
ax5.invert_yaxis()
style_ax(ax5, grid="x")

# ── CHART 6 — Avg Sale: Member vs Normal ─────────────────────
ax6 = card_ax(gs_charts[1, 1])
cust_avg = customer_stats["Avg_Sale"]
bars6 = ax6.bar(
    cust_avg.index, cust_avg.values,
    color=[C_NAVY, C_LTEAL], width=0.42,
    edgecolor="white", linewidth=0.4, zorder=3,
)
ax6.set_title("Avg Sale: Member vs Normal")
ax6.set_ylim(0, cust_avg.max() * 1.26)
ax6.bar_label(bars6,
              labels=[f"${v:,.0f}" for v in cust_avg.values],
              padding=3, fontsize=8, color=C_TEXT, fontweight="bold")
style_ax(ax6)

# ── CHART 7 — Total Sales by Gender ──────────────────────────
ax7 = card_ax(gs_charts[1, 2])
gen_sales = gender_stats["Total_Sales"]
bars7 = ax7.bar(
    gen_sales.index, gen_sales.values,
    color=[C_NAVY, C_SKY], width=0.42,
    edgecolor="white", linewidth=0.4, zorder=3,
)
ax7.set_title("Total Sales by Gender")
ax7.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"${x/1000:.0f}K"))
ax7.set_ylim(0, gen_sales.max() * 1.22)
ax7.bar_label(bars7,
              labels=[f"${v/1000:.0f}K" for v in gen_sales.values],
              padding=3, fontsize=8, color=C_TEXT, fontweight="bold")
style_ax(ax7)

# ── CHART 8 — Customer Rating Distribution ───────────────────
ax8 = card_ax(gs_charts[1, 3])
ax8.hist(df["Rating"], bins=12,
         color=C_ICE, edgecolor="white", linewidth=0.6,
         rwidth=0.82, zorder=3)
ax8.axvline(avg_rating, color=C_ACCENT, linestyle="--",
            linewidth=1.8, label=f"Mean: {avg_rating:.2f}", zorder=4)
ax8.set_title("Customer Rating Distribution")
ax8.set_xlabel("Rating (out of 10)", labelpad=4, fontsize=6.5)
ax8.legend(loc="upper left", labelcolor=C_TEXT)
style_ax(ax8)

# ── Footer ───────────────────────────────────────────────────
fig.text(
    0.5, 0.005,
    "Data Source: SuperMarket Analysis.csv   |   "
    "Jan \u2013 Mar 2019   |   1,000 Transactions   |   3 Branches",
    ha="center", fontsize=7, color=C_MUTED,
)

# ── Fine-tune internal spacing of chart zone only ────────────
# subplots_adjust affects the GridSpec subplot area; the outer
# gs_outer zones (header & KPI) are unaffected.
fig.subplots_adjust(left=0.02, right=0.99, top=0.995, bottom=0.005)

# ── Save & show ──────────────────────────────────────────────
plt.savefig(
    "supermarket_sales_dashboard.png",
    dpi=300, bbox_inches="tight", facecolor=C_BG,
)
print("  [OK] Dashboard saved: supermarket_sales_dashboard.png")

plt.show()

# ============================================================
# SECTION 14 — Business Insights Summary
# ============================================================
section("14. Key Business Insights")

best_product     = product_sales.idxmax()
worst_product    = product_sales.idxmin()
best_branch      = branch_sales.idxmax()
best_payment     = payment_sales.idxmax()
best_month       = monthly_sales.idxmax()
best_qty_product = product_qty.idxmax()
better_gender    = gender_stats["Total_Sales"].idxmax()
better_customer  = customer_stats["Total_Sales"].idxmax()

print(f"""
  [*] Best-selling product line (by revenue) : {best_product}
                                               (${product_sales[best_product]:,.2f})

  [*] Lowest-selling product line            : {worst_product}
                                               (${product_sales[worst_product]:,.2f})

  [*] Top-performing branch                  : {best_branch}
                                               (${branch_sales[best_branch]:,.2f})

  [*] Most popular payment method            : {best_payment}
                                               (${payment_sales[best_payment]:,.2f} in sales)

  [*] Best sales month                       : {best_month}
                                               (${monthly_sales[best_month]:,.2f})

  [*] Category with most units sold          : {best_qty_product}
                                               ({int(product_qty[best_qty_product]):,} units)

  [*] Customer type with higher total sales  : {better_customer}

  [*] Gender with higher total sales         : {better_gender}

  [*] Average customer rating                : {avg_rating:.2f} / 10

  [*] Overall total revenue                  : ${total_sales:,.2f}
  [*] Overall gross income (profit)          : ${total_gross_income:,.2f}
""")

print("=" * 60)
print("  Supermarket Sales Analysis Dashboard created successfully.")
print("=" * 60)
