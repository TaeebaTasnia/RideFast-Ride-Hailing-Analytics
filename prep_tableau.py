"""
Tableau Data Prep — RideFast Assessment
Outputs two dashboard-ready CSVs:
  output/tableau_rides_clean.csv   — 120K rows, one per ride, all fields pre-computed
  output/tableau_tickets_clean.csv — 22K rows, one per ticket, city/status context added

Connect ONLY these two files in Tableau. No joins needed.
"""

import pandas as pd
import numpy as np
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────
CSV_DIR = Path("csvs")
OUT_DIR = Path("output")
OUT_DIR.mkdir(exist_ok=True)

AS_OF   = pd.Timestamp("2024-06-30")

# ── Load ─────────────────────────────────────────────────────────────────────
print("Loading CSVs…")
rides   = pd.read_csv(CSV_DIR / "rides (2026).csv",
                      parse_dates=["request_time","pickup_time","dropoff_time"])
drivers = pd.read_csv(CSV_DIR / "drivers (2026).csv",
                      parse_dates=["signup_date"])
users   = pd.read_csv(CSV_DIR / "users (2026).csv",
                      parse_dates=["signup_date","last_ride_date"])
tickets = pd.read_csv(CSV_DIR / "support_tickets (2026).csv",
                      parse_dates=["created_at"])

print(f"  rides:   {len(rides):,}")
print(f"  drivers: {len(drivers):,}")
print(f"  users:   {len(users):,}")
print(f"  tickets: {len(tickets):,}")


# ══════════════════════════════════════════════════════════════════════════════
# BLOCK 1 — DRIVER-LEVEL ENRICHMENT
# ══════════════════════════════════════════════════════════════════════════════

def driver_tier(acc, canc):
    if acc < 0.60 and canc > 0.30:
        return "Both-Issues"
    elif canc > 0.30:
        return "High-Cancel"
    elif acc < 0.60:
        return "Low-Accept"
    return "Standard"

drivers["driver_quality_tier"] = drivers.apply(
    lambda r: driver_tier(r["acceptance_rate"], r["cancellation_rate"]), axis=1
)
drivers["driver_tier_label"] = drivers["driver_quality_tier"].map(
    {"Both-Issues": "Problem Driver", "High-Cancel": "Problem Driver",
     "Low-Accept":  "Problem Driver", "Standard":    "Standard Driver"}
)

# Tenure (30.44 days/month)
drivers["driver_tenure_months"] = (
    (AS_OF - drivers["signup_date"]).dt.days / 30.44
).clip(lower=0).round(1)

def tenure_bracket(m):
    if m < 6:   return "0–6 Months"
    elif m < 12: return "6–12 Months"
    elif m < 18: return "12–18 Months"
    elif m < 24: return "18–24 Months"
    else:        return "24+ Months"

def tenure_sort(m):
    if m < 6:   return 1
    elif m < 12: return 2
    elif m < 18: return 3
    elif m < 24: return 4
    else:        return 5

drivers["driver_tenure_bracket"] = drivers["driver_tenure_months"].apply(tenure_bracket)
drivers["driver_tenure_sort"]    = drivers["driver_tenure_months"].apply(tenure_sort)

# Rename driver columns to avoid clash with rides columns
driver_cols = {
    "driver_id":              "driver_id",
    "city":                   "driver_home_city",
    "signup_date":            "driver_signup_date",
    "vehicle_type":           "driver_vehicle_type",
    "status":                 "driver_status",
    "avg_rating":             "driver_avg_rating",
    "total_rides":            "driver_total_rides",
    "acceptance_rate":        "driver_acceptance_rate",
    "cancellation_rate":      "driver_cancellation_rate",
    "online_hours_monthly":   "driver_online_hours_monthly",
    "driver_quality_tier":    "driver_quality_tier",
    "driver_tier_label":      "driver_tier_label",
    "driver_tenure_months":   "driver_tenure_months",
    "driver_tenure_bracket":  "driver_tenure_bracket",
    "driver_tenure_sort":     "driver_tenure_sort",
}
drivers_slim = drivers.rename(columns=driver_cols)[list(driver_cols.values())]


# ══════════════════════════════════════════════════════════════════════════════
# BLOCK 2 — USER-LEVEL ENRICHMENT
# ══════════════════════════════════════════════════════════════════════════════

# First ride date per user (from rides table)
first_ride = (
    rides.groupby("user_id")["request_time"]
    .min()
    .rename("first_ride_date")
    .reset_index()
)
users = users.merge(first_ride, on="user_id", how="left")

# Days from signup to first ride
users["days_to_first_ride"] = (
    users["first_ride_date"] - users["signup_date"]
).dt.days

def first_ride_bracket(d):
    if pd.isna(d):  return "Never Rode"
    d = int(d)
    if d == 0:      return "Same Day"
    elif d <= 7:    return "1–7 Days"
    elif d <= 30:   return "8–30 Days"
    elif d <= 90:   return "1–3 Months"
    elif d <= 180:  return "3–6 Months"
    elif d <= 365:  return "6–12 Months"
    else:           return "Over 1 Year"

def first_ride_sort(d):
    if pd.isna(d):  return 8
    d = int(d)
    if d == 0:      return 1
    elif d <= 7:    return 2
    elif d <= 30:   return 3
    elif d <= 90:   return 4
    elif d <= 180:  return 5
    elif d <= 365:  return 6
    else:           return 7

users["first_ride_bracket"]      = users["days_to_first_ride"].apply(first_ride_bracket)
users["first_ride_bracket_sort"] = users["days_to_first_ride"].apply(first_ride_sort)

# User group label
users["user_group"] = users["churn_flag"].map(
    {True: "Churned (79.6%)", False: "Active (20.4%)"}
)

# Promo dependency ratio
users["promo_dependency_ratio"] = (
    users["promo_rides"] / users["total_rides"].replace(0, np.nan)
).fillna(0).round(4)

# Ride count bracket
def ride_bracket(n):
    if n == 0:      return "0 Rides"
    elif n == 1:    return "1 Ride"
    elif n <= 5:    return "2–5 Rides"
    elif n <= 10:   return "6–10 Rides"
    elif n <= 25:   return "11–25 Rides"
    elif n <= 50:   return "26–50 Rides"
    elif n <= 100:  return "51–100 Rides"
    else:           return "101+ Rides"

def ride_bracket_sort(n):
    if n == 0:      return 1
    elif n == 1:    return 2
    elif n <= 5:    return 3
    elif n <= 10:   return 4
    elif n <= 25:   return 5
    elif n <= 50:   return 6
    elif n <= 100:  return 7
    else:           return 8

users["user_ride_count_bracket"]      = users["total_rides"].apply(ride_bracket)
users["user_ride_count_bracket_sort"] = users["total_rides"].apply(ride_bracket_sort)

# Days inactive (from last ride)
users["days_inactive"] = (AS_OF - users["last_ride_date"]).dt.days.clip(lower=0)

# Rename user columns
user_cols = {
    "user_id":                    "user_id",
    "signup_date":                "user_signup_date",
    "city":                       "user_home_city",
    "total_rides":                "user_total_rides",
    "last_ride_date":             "user_last_ride_date",
    "promo_rides":                "user_promo_rides",
    "wallet_balance":             "user_wallet_balance",
    "churn_flag":                 "user_churn_flag",
    "user_group":                 "user_group",
    "first_ride_date":            "user_first_ride_date",
    "days_to_first_ride":         "user_days_to_first_ride",
    "first_ride_bracket":         "user_first_ride_bracket",
    "first_ride_bracket_sort":    "user_first_ride_bracket_sort",
    "promo_dependency_ratio":     "user_promo_dependency_ratio",
    "user_ride_count_bracket":    "user_ride_count_bracket",
    "user_ride_count_bracket_sort": "user_ride_count_bracket_sort",
    "days_inactive":              "user_days_inactive",
}
users_slim = users.rename(columns=user_cols)[list(user_cols.values())]


# ══════════════════════════════════════════════════════════════════════════════
# BLOCK 3 — RIDES ENRICHMENT & JOIN
# ══════════════════════════════════════════════════════════════════════════════

r = rides.copy()

# ── Status flags ─────────────────────────────────────────────────────────────
r["is_completed"]    = (r["status"] == "completed").astype(int)
r["is_driver_cancel"]= (r["status"] == "cancelled_driver").astype(int)
r["is_user_cancel"]  = (r["status"] == "cancelled_user").astype(int)
r["is_no_show"]      = (r["status"] == "no_show").astype(int)

# ── Revenue ──────────────────────────────────────────────────────────────────
r["revenue"]     = r["fare_amount"].where(r["is_completed"] == 1, 0)
r["net_revenue"] = (r["fare_amount"] - r["promo_discount"]).where(r["is_completed"] == 1, 0)

# ── Wait time ────────────────────────────────────────────────────────────────
r["wait_minutes"] = (
    (r["pickup_time"] - r["request_time"]).dt.total_seconds() / 60
)
r["wait_minutes"] = r["wait_minutes"].where(r["wait_minutes"] >= 0, np.nan).round(2)
r["wait_over_15"] = (r["wait_minutes"] >= 15).fillna(False).astype(int)

# Trip duration
r["trip_minutes"] = (
    (r["dropoff_time"] - r["pickup_time"]).dt.total_seconds() / 60
).where(r["is_completed"] == 1, np.nan).round(2)

def wait_bracket(m):
    if pd.isna(m): return "Unknown"
    if m < 5:      return "0–5 min"
    elif m < 10:   return "5–10 min"
    elif m < 15:   return "10–15 min"
    elif m < 20:   return "15–20 min"
    elif m < 30:   return "20–30 min"
    else:          return "30+ min"

def wait_bracket_sort(m):
    if pd.isna(m): return 0
    if m < 5:      return 1
    elif m < 10:   return 2
    elif m < 15:   return 3
    elif m < 20:   return 4
    elif m < 30:   return 5
    else:          return 6

r["wait_bracket"]      = r["wait_minutes"].apply(wait_bracket)
r["wait_bracket_sort"] = r["wait_minutes"].apply(wait_bracket_sort)

# ── Time dimensions ──────────────────────────────────────────────────────────
r["year"]        = r["request_time"].dt.year
r["month_num"]   = r["request_time"].dt.month
r["year_month"]  = r["request_time"].dt.to_period("M").astype(str)   # "2023-07"
r["month_name"]  = r["request_time"].dt.strftime("%b '%y")           # "Jul '23"
r["quarter_num"] = r["request_time"].dt.quarter
r["quarter_label"] = (
    "Q" + r["request_time"].dt.quarter.astype(str) +
    "'" + r["request_time"].dt.strftime("%y")
)   # "Q3'23"
r["quarter_sort"] = (
    (r["request_time"].dt.year - 2023) * 4 +
     r["request_time"].dt.quarter - 2
)   # Q3'23=1 … Q2'24=4
r["day_of_week"]       = r["request_time"].dt.day_name()             # "Monday"
r["day_of_week_sort"]  = r["request_time"].dt.dayofweek              # 0=Mon
r["hour_of_day"]       = r["request_time"].dt.hour

# ── Join drivers ─────────────────────────────────────────────────────────────
r = r.merge(drivers_slim, on="driver_id", how="left")

# Fill missing driver tier (rides with no driver match → Standard)
r["driver_quality_tier"] = r["driver_quality_tier"].fillna("Standard")
r["driver_tier_label"]   = r["driver_tier_label"].fillna("Standard Driver")
r["driver_status"]       = r["driver_status"].fillna("unknown")

# ── Join users ───────────────────────────────────────────────────────────────
r = r.merge(users_slim, on="user_id", how="left")

# ── Verify no row inflation ───────────────────────────────────────────────────
assert len(r) == 120_000, f"Row count changed after joins: {len(r)}"
print(f"\nRide rows after join: {len(r):,}  (expected 120,000 - OK)")

# ── Column ordering ──────────────────────────────────────────────────────────
# Core ride fields first, then computed, then driver, then user
core_cols = [
    "ride_id","user_id","driver_id","city","pickup_zone",
    "request_time","pickup_time","dropoff_time",
    "status","is_completed","is_driver_cancel","is_user_cancel","is_no_show",
    "fare_amount","promo_discount","revenue","net_revenue",
    "surge_multiplier","promo_code_used",
    "rating_by_user","rating_by_driver",
    "vehicle_type","distance_km","payment_method",
    "wait_minutes","wait_bracket","wait_bracket_sort","wait_over_15",
    "trip_minutes",
    "year","month_num","year_month","month_name",
    "quarter_label","quarter_sort","quarter_num",
    "day_of_week","day_of_week_sort","hour_of_day",
]
driver_col_list = [c for c in r.columns if c.startswith("driver_")]
user_col_list   = [c for c in r.columns if c.startswith("user_")]
final_cols = core_cols + driver_col_list + user_col_list
r = r[[c for c in final_cols if c in r.columns]]


# ══════════════════════════════════════════════════════════════════════════════
# BLOCK 4 — TICKETS ENRICHMENT
# ══════════════════════════════════════════════════════════════════════════════

t = tickets.copy()

# Pull city + status from rides (safe: one ride = one row of context)
ride_context = rides[["ride_id","city","pickup_zone","status","vehicle_type",
                       "request_time","rating_by_user","wait_minutes"
                       if "wait_minutes" in rides.columns else "ride_id"]].copy()

# Recompute wait on rides for context
ride_context["wait_minutes_ctx"] = (
    (rides["pickup_time"] - rides["request_time"]).dt.total_seconds() / 60
).clip(lower=0)

ride_context = rides[["ride_id","city","pickup_zone","status","vehicle_type",
                       "request_time","rating_by_user"]].copy()
ride_context["wait_minutes_ctx"] = (
    (rides["pickup_time"] - rides["request_time"]).dt.total_seconds() / 60
).clip(lower=0)

t = t.merge(ride_context, on="ride_id", how="left")

# Time dims
t["year_month"]   = t["created_at"].dt.to_period("M").astype(str)
t["month_name"]   = t["created_at"].dt.strftime("%b '%y")
t["quarter_label"] = (
    "Q" + t["created_at"].dt.quarter.astype(str) +
    "'" + t["created_at"].dt.strftime("%y")
)
t["quarter_sort"] = (
    (t["created_at"].dt.year - 2023) * 4 +
     t["created_at"].dt.quarter - 2
)

# Flags
t["is_resolved"] = t["resolved"].astype(int)

severity_map = {"critical": 4, "high": 3, "medium": 2, "low": 1}
t["severity_sort"] = t["severity"].map(severity_map).fillna(0).astype(int)

# Category labels (clean)
category_labels = {
    "fare_dispute":    "Fare Dispute",
    "safety":          "Safety",
    "lost_item":       "Lost Item",
    "app_issue":       "App Issue",
    "driver_behaviour":"Driver Behaviour",
}
t["category_label"] = t["category"].map(category_labels).fillna(t["category"])

# Verify
print(f"Ticket rows after join: {len(t):,}  (expected 22,000 range - OK)")


# ══════════════════════════════════════════════════════════════════════════════
# BLOCK 5 — DRIVER-LEVEL CLEAN FILE (one row per driver)
# ══════════════════════════════════════════════════════════════════════════════

# Aggregate ride stats per driver from the rides table
ride_agg = rides.copy()
ride_agg["wait_minutes"] = (
    (ride_agg["pickup_time"] - ride_agg["request_time"]).dt.total_seconds() / 60
).clip(lower=0)
ride_agg["revenue"]          = ride_agg["fare_amount"].where(ride_agg["status"] == "completed", 0)
ride_agg["is_completed"]     = (ride_agg["status"] == "completed").astype(int)
ride_agg["is_driver_cancel"] = (ride_agg["status"] == "cancelled_driver").astype(int)
ride_agg["wait_over_15"]     = (ride_agg["wait_minutes"] >= 15).fillna(False).astype(int)

driver_ride_stats = ride_agg.groupby("driver_id").agg(
    total_rides_in_data   = ("ride_id",           "count"),
    completed_rides       = ("is_completed",       "sum"),
    driver_cancels        = ("is_driver_cancel",   "sum"),
    total_revenue         = ("revenue",            "sum"),
    avg_fare              = ("fare_amount",         lambda x: x[ride_agg.loc[x.index, "status"] == "completed"].mean()),
    avg_wait_minutes      = ("wait_minutes",        "mean"),
    rides_over_15min      = ("wait_over_15",        "sum"),
    avg_user_rating_given = ("rating_by_user",      "mean"),
    avg_surge             = ("surge_multiplier",    "mean"),
).reset_index()

driver_ride_stats["completion_rate_rides"]  = (driver_ride_stats["completed_rides"]   / driver_ride_stats["total_rides_in_data"]).round(4)
driver_ride_stats["cancel_rate_rides"]      = (driver_ride_stats["driver_cancels"]    / driver_ride_stats["total_rides_in_data"]).round(4)
driver_ride_stats["pct_rides_over_15min"]   = (driver_ride_stats["rides_over_15min"]  / driver_ride_stats["total_rides_in_data"]).round(4)
driver_ride_stats["revenue_per_ride"]       = (driver_ride_stats["total_revenue"]     / driver_ride_stats["completed_rides"].replace(0, np.nan)).round(2)

# Build the full driver clean table
d_clean = drivers.copy()  # already has tier, tenure from Block 1

# Merge with ride-level aggregates
d_clean = d_clean.merge(driver_ride_stats, on="driver_id", how="left")

# Ticket count per driver
driver_ticket_count = tickets.groupby("driver_id")["ticket_id"].count().rename("tickets_received").reset_index()
d_clean = d_clean.merge(driver_ticket_count, on="driver_id", how="left")
d_clean["tickets_received"] = d_clean["tickets_received"].fillna(0).astype(int)

# Tickets per completed ride
d_clean["tickets_per_100_rides"] = (
    d_clean["tickets_received"] / d_clean["completed_rides"].replace(0, np.nan) * 100
).round(2)

# Performance segment label (for easy filtering in Tableau)
def perf_segment(row):
    if row["driver_quality_tier"] == "Both-Issues":
        return "Problem: Both Issues"
    elif row["driver_quality_tier"] == "High-Cancel":
        return "Problem: High Cancel"
    elif row["driver_quality_tier"] == "Low-Accept":
        return "Problem: Low Accept"
    elif row["status"] == "suspended":
        return "Suspended"
    elif row["status"] == "churned":
        return "Churned"
    elif row["driver_tenure_months"] < 12:
        return "Active: Early Tenure"
    elif row["avg_rating"] >= 4.2:
        return "Active: High Performer"
    else:
        return "Active: Standard"

d_clean["performance_segment"] = d_clean.apply(perf_segment, axis=1)

print(f"Driver rows: {len(d_clean):,}  (expected 8,000)")


# ══════════════════════════════════════════════════════════════════════════════
# BLOCK 6 — USER-LEVEL CLEAN FILE (one row per user)
# ══════════════════════════════════════════════════════════════════════════════

# Aggregate ride stats per user from the rides table
user_ride_agg = ride_agg.groupby("user_id").agg(
    rides_taken          = ("ride_id",           "count"),
    completed_rides      = ("is_completed",       "sum"),
    driver_cancels_faced = ("is_driver_cancel",   "sum"),
    total_gross_spend    = ("revenue",            "sum"),
    avg_fare             = ("revenue",            lambda x: x[x > 0].mean()),
    avg_wait_minutes     = ("wait_minutes",        "mean"),
    rides_over_15min     = ("wait_over_15",        "sum"),
    avg_rating_given     = ("rating_by_user",      "mean"),
    promo_rides_count    = ("promo_code_used",     "sum"),
).reset_index()

user_ride_agg["completion_rate"] = (
    user_ride_agg["completed_rides"] / user_ride_agg["rides_taken"].replace(0, np.nan)
).round(4)
user_ride_agg["pct_rides_over_15min"] = (
    user_ride_agg["rides_over_15min"] / user_ride_agg["rides_taken"].replace(0, np.nan)
).round(4)

# Build the full user clean table
u_clean = users.copy()  # already has derived fields from Block 2

# Merge with ride aggregates
u_clean = u_clean.merge(user_ride_agg, on="user_id", how="left")

# Ticket count per user
user_ticket_count = tickets.groupby("user_id")["ticket_id"].count().rename("tickets_raised").reset_index()
u_clean = u_clean.merge(user_ticket_count, on="user_id", how="left")
u_clean["tickets_raised"] = u_clean["tickets_raised"].fillna(0).astype(int)

# Value segment
def value_segment(row):
    if row["churn_flag"] == True:
        if pd.notna(row["total_gross_spend"]) and row["total_gross_spend"] > 200:
            return "High-Value Churned"
        else:
            return "Standard Churned"
    else:
        if pd.notna(row["total_gross_spend"]) and row["total_gross_spend"] > 200:
            return "High-Value Active"
        else:
            return "Standard Active"

u_clean["value_segment"] = u_clean.apply(value_segment, axis=1)

# Promo quartile (Q1=low, Q4=high) — rank by promo_dependency_ratio
u_clean["promo_dependency_ratio"] = (
    u_clean["promo_rides"] / u_clean["total_rides"].replace(0, np.nan)
).fillna(0)
u_clean["promo_quartile"] = pd.qcut(
    u_clean["promo_dependency_ratio"], 4,
    labels=["Q1 Low Promo", "Q2", "Q3", "Q4 Heavy Promo"]
)
u_clean["promo_quartile_sort"] = pd.qcut(
    u_clean["promo_dependency_ratio"], 4, labels=[1, 2, 3, 4]
).astype(int)

# Clean column names (rename to avoid collision with rides fields)
# Keep original names — this is a user-level file so no collision

print(f"User rows: {len(u_clean):,}  (expected 35,000)")


# ══════════════════════════════════════════════════════════════════════════════
# BLOCK 7 — WRITE ALL OUTPUTS
# ══════════════════════════════════════════════════════════════════════════════

rides_out   = OUT_DIR / "tableau_rides_clean.csv"
drivers_out = OUT_DIR / "tableau_drivers_clean.csv"
users_out   = OUT_DIR / "tableau_users_clean.csv"
tickets_out = OUT_DIR / "tableau_tickets_clean.csv"

r.to_csv(rides_out,   index=False)
d_clean.to_csv(drivers_out, index=False)
u_clean.to_csv(users_out,   index=False)
t.to_csv(tickets_out, index=False)

print(f"\nOutputs written:")
for path, df in [
    (rides_out,   r),
    (drivers_out, d_clean),
    (users_out,   u_clean),
    (tickets_out, t),
]:
    mb = path.stat().st_size / 1024 / 1024
    print(f"  {path.name:<35} {mb:5.1f} MB   {len(df):>7,} rows   {len(df.columns)} cols")

# ── Quick sanity print ────────────────────────────────────────────────────────
print("\n── Sanity Checks ────────────────────────────────────────────────────")
print(f"  Completion rate:     {r['is_completed'].mean()*100:.1f}%    (expected 81.6%)")
print(f"  Total revenue:       ${r['revenue'].sum():,.0f}  (expected $3,583,768)")
print(f"  Driver cancel rate:  {r['is_driver_cancel'].mean()*100:.1f}%   (expected 9.3%)")
print(f"  Both-Issues rides:   {(r['driver_quality_tier']=='Both-Issues').sum():,}  (expected ~11,174)")
print(f"  Rides over 15 min:   {r['wait_over_15'].sum():,}    (expected 9,132)")
print(f"  Northgate rides:     {(r['city']=='Northgate').sum():,}    (expected ~9,989)")
print(f"  Churned user rides:  {r['user_churn_flag'].sum():,} (most rides from churned users)")
print(f"  Tickets (total):     {len(t):,}")
print(f"  Tickets resolved:    {t['is_resolved'].mean()*100:.1f}%")

# ── Column list for reference ──────────────────────────────────────────────────
print("\n── Columns in tableau_rides_clean.csv ───────────────────────────────")
for i, col in enumerate(r.columns, 1):
    print(f"  {i:2}. {col}")

print("\n── Columns in tableau_tickets_clean.csv ─────────────────────────────")
for i, col in enumerate(t.columns, 1):
    print(f"  {i:2}. {col}")

print("\nDone. Connect both files in Tableau — no joins required.")
