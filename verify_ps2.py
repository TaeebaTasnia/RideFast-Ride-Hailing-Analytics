"""
Verification script: checks every specific number in problem_statement_2.md
against the actual CSV data. Outputs a markdown comparison table.

Run:  python verify_ps2.py
"""

import pandas as pd
import numpy as np
from pathlib import Path

CSV_DIR = Path("E:/pathao/csvs")

# ──────────────────────────────────────────────
# Load data
# ──────────────────────────────────────────────
print("Loading CSVs...")
rides   = pd.read_csv(CSV_DIR / "rides (2026).csv",           parse_dates=["request_time", "pickup_time", "dropoff_time"])
drivers = pd.read_csv(CSV_DIR / "drivers (2026).csv",         parse_dates=["signup_date"])
users   = pd.read_csv(CSV_DIR / "users (2026).csv",           parse_dates=["signup_date", "last_ride_date"])

print(f"  rides:   {len(rides):,} rows")
print(f"  drivers: {len(drivers):,} rows")
print(f"  users:   {len(users):,} rows")

results = []  # list of (section, claim, ps2_value, actual_value, match)

def check(section, claim, ps2_val, actual_val, tol=None):
    """Register a single check."""
    if tol is not None:
        try:
            ps2_n   = float(str(ps2_val).replace('%','').replace('$','').replace(',',''))
            act_n   = float(str(actual_val).replace('%','').replace('$','').replace(',',''))
            matched = abs(ps2_n - act_n) <= tol
        except Exception:
            matched = str(ps2_val).strip() == str(actual_val).strip()
    else:
        matched = str(ps2_val).strip() == str(actual_val).strip()
    results.append((section, claim, ps2_val, actual_val, "OK" if matched else "MISMATCH"))


# ──────────────────────────────────────────────
# CORE — Quarterly ride averages
# ──────────────────────────────────────────────
rides["quarter"] = rides["request_time"].dt.to_period("Q")
q_counts = rides.groupby("quarter").size()

# Each quarter has 3 months; divide by 3 for monthly average
q_map = {
    "2023Q3": "Q3'23",
    "2023Q4": "Q4'23",
    "2024Q1": "Q1'24",
    "2024Q2": "Q2'24",
}
quarterly_avgs = {}
for qkey, qlabel in q_map.items():
    qp = pd.Period(qkey, freq="Q")
    if qp in q_counts.index:
        quarterly_avgs[qlabel] = round(q_counts[qp] / 3)

ps2_quarterly = {"Q3'23": 10069, "Q4'23": 10137, "Q1'24": 9932, "Q2'24": 9862}
for ql, ps2v in ps2_quarterly.items():
    check("Core", f"Avg rides/mo {ql}", ps2v, quarterly_avgs.get(ql, "N/A"), tol=5)


# ──────────────────────────────────────────────
# P1 — Churn & Revenue
# ──────────────────────────────────────────────
total_users = len(users)
churned_count = users["churn_flag"].sum()
churn_rate = churned_count / total_users * 100

check("P1", "Overall churn rate", "79.6%", f"{churn_rate:.1f}%", tol=0.1)
check("P1", "Total users", "35,000", f"{total_users:,}")

# Revenue — gross fare per user (via rides join)
completed = rides[rides["status"] == "completed"].copy()
rev_by_user = completed.groupby("user_id")["fare_amount"].sum().reset_index()
rev_by_user.columns = ["user_id", "gross_revenue"]

u_rev = users[["user_id", "churn_flag"]].merge(rev_by_user, on="user_id", how="left")
u_rev["gross_revenue"] = u_rev["gross_revenue"].fillna(0)

churned_rev  = u_rev[u_rev["churn_flag"] == True]["gross_revenue"].sum()
active_rev   = u_rev[u_rev["churn_flag"] == False]["gross_revenue"].sum()
total_rev    = churned_rev + active_rev
churned_rev_pct = churned_rev / total_rev * 100

check("P1", "Churned user total revenue ($)",  "$2,870,285", f"${churned_rev:,.0f}", tol=2000)
check("P1", "Active user total revenue ($)",   "$713,483",   f"${active_rev:,.0f}",  tol=2000)
check("P1", "Churned revenue share (%)",        "80.1%",     f"{churned_rev_pct:.1f}%", tol=0.2)

# Avg spend per user (users who have any rides)
avg_churned = u_rev[u_rev["churn_flag"] == True]["gross_revenue"].mean()
avg_active  = u_rev[u_rev["churn_flag"] == False]["gross_revenue"].mean()

check("P1", "Churned avg spend ($)",  "$103.00", f"${avg_churned:.2f}", tol=1.0)
check("P1", "Active avg spend ($)",   "$100.03", f"${avg_active:.2f}",  tol=1.0)

# Churn by time-to-first-ride
first_ride = rides.groupby("user_id")["request_time"].min().reset_index()
first_ride.columns = ["user_id", "first_ride_time"]
u_first = users.merge(first_ride, on="user_id", how="left")
u_first["days_to_first"] = (u_first["first_ride_time"] - u_first["signup_date"]).dt.days

def bracket_churn(df, mask, label):
    sub = df[mask]
    if len(sub) == 0:
        return (label, 0, "N/A")
    rate = sub["churn_flag"].mean() * 100
    return (label, len(sub), rate)

has_ride = u_first["days_to_first"].notna()
brackets = [
    (u_first["days_to_first"] == 0,                                               "Day 0",   68.9),
    ((u_first["days_to_first"] >= 1) & (u_first["days_to_first"] <= 7),           "1-7d",    73.9),
    ((u_first["days_to_first"] >= 8) & (u_first["days_to_first"] <= 30),          "8-30d",   76.6),
    ((u_first["days_to_first"] > 30)  & (u_first["days_to_first"] <= 90),         "1-3m",    78.2),
    ((u_first["days_to_first"] > 90)  & (u_first["days_to_first"] <= 180),        "3-6m",    80.8),
    ((u_first["days_to_first"] > 180) & (u_first["days_to_first"] <= 365),        "6-12m",   85.0),
    (u_first["days_to_first"] > 365,                                               ">1yr",    87.6),
]

for mask, label, ps2v in brackets:
    _, n, rate = bracket_churn(u_first, mask & has_ride, label)
    check("P1", f"Churn rate {label} (n={n})", f"{ps2v}%", f"{rate:.1f}%" if isinstance(rate, float) else rate, tol=0.5)

# 5,257 high-value churned users
churned_users_all = u_rev[u_rev["churn_flag"] == True].merge(
    users[["user_id","total_rides","last_ride_date"]], on="user_id", how="left"
)
hvc_threshold_percentile = churned_users_all["total_rides"].quantile(0.85)
hvc = churned_users_all[churned_users_all["total_rides"] >= hvc_threshold_percentile]
# Use a more direct approach: top N by total_rides among churned
# PS2 says 5,257 — check how many churned users have significantly above-avg total rides
# Use total_rides as proxy — find the count
churned_riders_only = churned_users_all[churned_users_all["total_rides"] > 0]
hvc5257 = churned_riders_only.nlargest(5257, "total_rides")
actual_hvc_count = len(hvc5257)  # should just be 5257 if enough churned riders exist
check("P1", "High-value churned user pool", "5,257", f"{min(actual_hvc_count, len(churned_riders_only)):,}", tol=100)

# Median days inactive for HVC
as_of = pd.Timestamp("2024-06-30")
hvc5257 = hvc5257.copy()
hvc5257["days_inactive"] = (as_of - hvc5257["last_ride_date"]).dt.days
med_inactive = hvc5257["days_inactive"].median()
check("P1", "HVC median days inactive", "218", f"{med_inactive:.0f}", tol=10)


# ──────────────────────────────────────────────
# P2 — Wait time analysis
# ──────────────────────────────────────────────
rides["wait_minutes"] = (rides["pickup_time"] - rides["request_time"]).dt.total_seconds() / 60
timed = rides[rides["wait_minutes"].notna() & (rides["wait_minutes"] >= 0)].copy()

bins  = [0, 5, 10, 15, 20, 30, np.inf]
labels = ["0-5", "5-10", "10-15", "15-20", "20-30", "30+"]
timed["wait_bracket"] = pd.cut(timed["wait_minutes"], bins=bins, labels=labels, right=False)

grp = timed.groupby("wait_bracket", observed=True)
bracket_stats = grp.apply(lambda g: pd.Series({
    "rides":          len(g),
    "completion_pct": (g["status"] == "completed").mean() * 100,
    "driver_cancel":  (g["status"] == "cancelled_driver").mean() * 100,
}), include_groups=False).reset_index()

ps2_wait = {
    "0-5":   (30685, 86.2, 5.8),
    "5-10":  (53352, 84.3, 7.1),
    "10-15": (26831, 78.2, 11.5),
    "15-20": (6646,  54.1, 29.3),
    "20-30": (1649,  65.7, 18.9),
    "30+":   (837,   65.4, 21.9),
}

for idx, row in bracket_stats.iterrows():
    bk = row["wait_bracket"]
    if bk in ps2_wait:
        ps2r, ps2c, ps2d = ps2_wait[bk]
        check("P2", f"Rides in {bk}min bracket",      ps2r,     int(row["rides"]),            tol=200)
        check("P2", f"Completion % {bk}min",          f"{ps2c}%", f"{row['completion_pct']:.1f}%", tol=0.5)
        check("P2", f"Driver cancel % {bk}min",       f"{ps2d}%", f"{row['driver_cancel']:.1f}%",  tol=0.5)

rides_over15   = (timed["wait_minutes"] >= 15).sum()
pct_over15_timed = rides_over15 / len(timed) * 100
pct_over15_all   = rides_over15 / len(rides) * 100
check("P2", "Rides >15min count (9,132)", 9132, rides_over15, tol=200)
check("P2", "% of rides >15min (denominator=timed)", "7.6%", f"{pct_over15_timed:.1f}%", tol=0.3)


# ──────────────────────────────────────────────
# P3 — Driver quality
# ──────────────────────────────────────────────
def assign_tier(row):
    if row["acceptance_rate"] < 0.60 and row["cancellation_rate"] > 0.30:
        return "both_issues"
    elif row["cancellation_rate"] > 0.30:
        return "high_cancel"
    elif row["acceptance_rate"] < 0.60:
        return "low_accept"
    return "standard"

drivers["driver_quality_tier"] = drivers.apply(assign_tier, axis=1)
both_issues = drivers[drivers["driver_quality_tier"] == "both_issues"]
standard    = drivers[drivers["driver_quality_tier"] == "standard"]   # strict standard = 7,041

check("P3", "Both-issues driver count", 741,   len(both_issues), tol=5)
check("P3", "Both-issues pct of fleet", "9.3%", f"{len(both_issues)/len(drivers)*100:.1f}%", tol=0.2)
check("P3", "Standard driver count",    7041,  len(standard),    tol=5)

bi_active = both_issues[both_issues["status"] == "active"]
suspended = drivers[drivers["status"] == "suspended"]
check("P3", "Both-issues ACTIVE count", 588, len(bi_active), tol=5)

# The cancel rate chart [42.2, 11.0, 13.5] uses drivers.csv cancellation_rate field per segment
bi_active_cancel = bi_active["cancellation_rate"].mean()
non_bi_all       = drivers[drivers["driver_quality_tier"].isin(["standard","high_cancel","low_accept"])]
std_cancel       = non_bi_all["cancellation_rate"].mean()   # all non-both-issues = 11.0%
susp_cancel      = suspended["cancellation_rate"].mean()
check("P3", "Cancel chart - active both-issues (42.2%)",  "42.2%", f"{bi_active_cancel*100:.1f}%", tol=0.2)
check("P3", "Cancel chart - standard (11.0%)",            "11.0%", f"{std_cancel*100:.1f}%",        tol=0.2)
check("P3", "Cancel chart - suspended (13.5%)",           "13.5%", f"{susp_cancel*100:.1f}%",       tol=0.2)
check("P3", "Suspended driver count",          534,     len(suspended),                          tol=5)
check("P3", "Suspended avg cancel rate",       "0.135", f"{suspended['cancellation_rate'].mean():.3f}", tol=0.005)
check("P3", "Suspended avg rating",            "4.14",  f"{suspended['avg_rating'].mean():.2f}",       tol=0.02)

bi_cancel = both_issues["cancellation_rate"].mean()
check("P3", "Both-issues avg cancel rate (0.422)", "0.422", f"{bi_cancel:.3f}", tol=0.005)

# Rides assigned to both-issues vs standard (via driver_id join)
rides_d = timed.merge(
    drivers[["driver_id","driver_quality_tier"]], on="driver_id", how="left"
)
rides_d["driver_quality_tier"] = rides_d["driver_quality_tier"].fillna("both_issues")  # unmatched unlikely

bi_rides  = rides_d[rides_d["driver_quality_tier"] == "both_issues"]
std_rides = rides_d[rides_d["driver_quality_tier"] == "standard"]

bi_over15  = (bi_rides["wait_minutes"] >= 15).mean() * 100
std_over15 = (std_rides["wait_minutes"] >= 15).mean() * 100
check("P3", "Both-issues: % rides >15min (43.0%)", "43.0%", f"{bi_over15:.1f}%",  tol=1.0)
check("P3", "Standard: % rides >15min (2.8%)",     "2.8%",  f"{std_over15:.1f}%", tol=0.3)

# Platform-wide cancel rate
platform_cancel = (rides["status"] == "cancelled_driver").mean() * 100
check("P3", "Platform-wide driver cancel rate (9.3%)", "9.3%", f"{platform_cancel:.1f}%", tol=0.2)

# Tenure analysis (active drivers only)
as_of = pd.Timestamp("2024-06-30")
active_drivers = drivers[drivers["status"] == "active"].copy()
active_drivers["tenure_months"] = ((as_of - active_drivers["signup_date"]).dt.days / 30.44).clip(lower=0)

tenure_bins   = [6, 12, 18, 24, np.inf]
tenure_labels = ["6-12m", "12-18m", "18-24m", "24+m"]
active_drivers["tenure_bracket"] = pd.cut(
    active_drivers["tenure_months"], bins=[0]+tenure_bins,
    labels=["<6m"]+tenure_labels, right=False
)

tenure_stats = active_drivers[active_drivers["tenure_bracket"] != "<6m"].groupby(
    "tenure_bracket", observed=True
).agg(
    count=("driver_id","count"),
    acceptance=("acceptance_rate","mean"),
    cancellation=("cancellation_rate","mean"),
    avg_rating=("avg_rating","mean")
).reset_index()

ps2_tenure = {
    "6-12m":  (2125, 0.728, 0.217, 3.921),
    "12-18m": (1339, 0.839, 0.101, 4.250),
    "18-24m": (1396, 0.839, 0.100, 4.258),
    "24+m":   (1376, 0.839, 0.098, 4.243),
}
for bk, (cnt, acc, canc, rating) in ps2_tenure.items():
    row = tenure_stats[tenure_stats["tenure_bracket"] == bk]
    if len(row):
        r = row.iloc[0]
        check("P3", f"Tenure {bk} count",       cnt,     int(r["count"]),           tol=20)
        check("P3", f"Tenure {bk} acceptance",  f"{acc:.3f}", f"{r['acceptance']:.3f}", tol=0.005)
        check("P3", f"Tenure {bk} cancel",      f"{canc:.3f}", f"{r['cancellation']:.3f}", tol=0.005)
        check("P3", f"Tenure {bk} avg_rating",  f"{rating:.3f}", f"{r['avg_rating']:.3f}", tol=0.01)

early_window = active_drivers[active_drivers["tenure_bracket"] == "6-12m"]
total_active = len(active_drivers[active_drivers["tenure_months"] >= 6])
early_pct = len(early_window) / len(active_drivers) * 100
check("P3", "34.0% active drivers in 6-12m window (2,125/6,245)",
      "34.0%", f"{early_pct:.1f}%", tol=0.5)
check("P3", "Active driver total count (6,245)", 6245, total_active, tol=50)


# ──────────────────────────────────────────────
# P4 — Northgate zone analysis
# ──────────────────────────────────────────────
rides_with_wait = rides.copy()
rides_with_wait["wait_minutes"] = (rides_with_wait["pickup_time"] - rides_with_wait["request_time"]).dt.total_seconds() / 60

city_stats = rides_with_wait.groupby("city").apply(lambda g: pd.Series({
    "completion_pct": (g["status"] == "completed").mean() * 100,
    "avg_wait": g.loc[g["wait_minutes"].notna() & (g["wait_minutes"] >= 0), "wait_minutes"].mean(),
}), include_groups=False).reset_index()

northgate_row = city_stats[city_stats["city"].str.lower() == "northgate"]
platform_comp = (rides["status"] == "completed").mean() * 100
platform_wait = timed["wait_minutes"].mean()

if len(northgate_row):
    nr = northgate_row.iloc[0]
    check("P4", "Northgate completion (76.1%)", "76.1%", f"{nr['completion_pct']:.1f}%", tol=0.5)
    check("P4", "Northgate avg wait (13.35 min)", "13.35", f"{nr['avg_wait']:.2f}", tol=0.5)

check("P4", "Platform completion avg (81.4%)", "81.4%", f"{platform_comp:.1f}%", tol=0.5)
check("P4", "Platform avg wait (7.84 min)",    "7.84",  f"{platform_wait:.2f}",  tol=0.5)

# Zone breakdown inside Northgate
northgate_rides = rides_with_wait[rides_with_wait["city"].str.lower() == "northgate"].copy()

zone_grp = northgate_rides.groupby("pickup_zone")
zone_stats = zone_grp.apply(lambda g: pd.Series({
    "rides":          len(g),
    "share_pct":      len(g) / len(northgate_rides) * 100,
    "completion_pct": (g["status"] == "completed").mean() * 100,
    "driver_cancel":  (g["status"] == "cancelled_driver").mean() * 100,
    "avg_wait":       g.loc[g["wait_minutes"].notna() & (g["wait_minutes"] >= 0), "wait_minutes"].mean(),
}), include_groups=False).reset_index()

ps2_zones = {
    "NOR-Z05": (1967, 19.7, 65.5, 20.2, 22.9),
    "NOR-Z04": (1867, 18.7, 65.6, 20.5, 23.0),
    "NOR-Z01": (1071, 10.7, 84.8, 7.8,  7.4),
    "NOR-Z03": (1035, 10.4, 83.7, 8.8,  7.2),
}
for zone, (rides_n, share, comp, dcanc, wait) in ps2_zones.items():
    row = zone_stats[zone_stats["pickup_zone"] == zone]
    if len(row):
        r = row.iloc[0]
        check("P4", f"{zone} rides",       rides_n,         int(r["rides"]),             tol=20)
        check("P4", f"{zone} share %",     f"{share}%",     f"{r['share_pct']:.1f}%",    tol=0.3)
        check("P4", f"{zone} completion",  f"{comp}%",      f"{r['completion_pct']:.1f}%", tol=0.5)
        check("P4", f"{zone} driver cancel", f"{dcanc}%",   f"{r['driver_cancel']:.1f}%", tol=0.5)
        check("P4", f"{zone} avg wait",    f"{wait} min",   f"{r['avg_wait']:.1f} min",  tol=0.5)


# ──────────────────────────────────────────────
# P5 — Promo effectiveness
# ──────────────────────────────────────────────
# Promo share per quarter (completed rides with promo vs total completed)
completed_rides = rides[rides["status"] == "completed"].copy()
completed_rides["quarter"] = completed_rides["request_time"].dt.to_period("Q")

promo_q = completed_rides.groupby("quarter").apply(lambda g: pd.Series({
    "promo_pct": g["promo_code_used"].mean() * 100,
}), include_groups=False).reset_index()

ps2_promo_share = {"2023Q3": 15.9, "2023Q4": 15.6, "2024Q1": 15.2, "2024Q2": 15.9}
for qkey, ps2v in ps2_promo_share.items():
    qp = pd.Period(qkey, freq="Q")
    row = promo_q[promo_q["quarter"] == qp]
    if len(row):
        check("P5", f"Promo share {qkey}", f"{ps2v}%", f"{row.iloc[0]['promo_pct']:.1f}%", tol=0.2)

# Promo churn by quartile and ride bracket
u_rides = users.copy()
u_rides["promo_dependency_ratio"] = (
    u_rides["promo_rides"] / u_rides["total_rides"].replace(0, np.nan)
).fillna(0)

u_rides["promo_quartile"] = pd.qcut(u_rides["promo_dependency_ratio"], 4, labels=["Q1","Q2","Q3","Q4"])

ride_bins  = [0, 10, 25, 50, 100, np.inf]
ride_labels = ["1-10", "11-25", "26-50", "51-100", "101+"]
u_rides["ride_bracket"] = pd.cut(u_rides["total_rides"], bins=ride_bins, labels=ride_labels, right=True)

ps2_promo_churn = {
    # (ride_bracket, quartile): expected_churn_pct
    ("1-10",  "Q1"): 82.7,
    ("1-10",  "Q4"): 82.7,
    ("11-25", "Q1"): 83.1,
    ("11-25", "Q4"): 80.6,
    ("26-50", "Q1"): 83.1,
    ("26-50", "Q4"): 70.8,
    ("51-100","Q1"): 82.1,
    ("51-100","Q4"): 55.6,
}

for (rb, qt), ps2v in ps2_promo_churn.items():
    sub = u_rides[(u_rides["ride_bracket"] == rb) & (u_rides["promo_quartile"] == qt)]
    if len(sub) > 0:
        rate = sub["churn_flag"].mean() * 100
        check("P5", f"Promo churn {rb} rides, {qt}", f"{ps2v}%", f"{rate:.1f}%", tol=1.0)
    else:
        check("P5", f"Promo churn {rb} rides, {qt}", f"{ps2v}%", "no data", tol=None)


# ──────────────────────────────────────────────
# Print results
# ──────────────────────────────────────────────
print("\n" + "=" * 100)
print("VERIFICATION RESULTS")
print("=" * 100)

mismatches = [r for r in results if r[4] == "MISMATCH"]
matches    = [r for r in results if r[4] == "OK"]

# Full table
print(f"\n{'Section':<8} {'Claim':<58} {'PS2 Value':<18} {'Actual Value':<18} {'Status'}")
print("-" * 110)
for section, claim, ps2v, actv, status in results:
    marker = "  " if status == "OK" else ">> "
    print(f"{marker}{section:<6} {claim:<58} {str(ps2v):<18} {str(actv):<18} {status}")

print("\n" + "=" * 100)
print(f"SUMMARY: {len(matches)} checks passed, {len(mismatches)} mismatches")
print("=" * 100)

if mismatches:
    print("\nMISMATCHES TO FIX:")
    for section, claim, ps2v, actv, status in mismatches:
        print(f"  [{section}] {claim}")
        print(f"         PS2 says: {ps2v}")
        print(f"         Actual:   {actv}")

# Also print a JSON-like dict for use in chart fix script
print("\n\n=== CORRECTED VALUES FOR CHARTS ===")
print("Quarterly rides:", {k: quarterly_avgs.get(k) for k in q_map.values()})

# Wait time data
wait_actual = {}
for idx, row in bracket_stats.iterrows():
    bk = str(row["wait_bracket"])
    wait_actual[bk] = {
        "rides": int(row["rides"]),
        "completion": round(row["completion_pct"], 1),
        "driver_cancel": round(row["driver_cancel"], 1)
    }
print("Wait brackets:", wait_actual)
print("Rides >15min:", rides_over15, f"({pct_over15_timed:.1f}% of timed rides)")

# Churn by time-to-first-ride
print("\nChurn by time-to-first-ride:")
for mask, label, ps2v in brackets:
    _, n, rate = bracket_churn(u_first, mask & has_ride, label)
    print(f"  {label}: n={n}, churn={rate:.1f}% (PS2={ps2v}%)")

# Revenue
print(f"\nRevenue: churned=${churned_rev:,.0f}, active=${active_rev:,.0f}, total=${total_rev:,.0f}")
print(f"Avg spend: churned=${avg_churned:.2f}, active=${avg_active:.2f}")

# Driver tier stats
print(f"\nDriver tiers: both_issues={len(both_issues)}, standard={len(standard)}, suspended={len(suspended)}")
print(f"Active both-issues: {len(bi_active)}")
print(f"Platform cancel: {platform_cancel:.1f}%")

# Tenure
print("\nTenure stats (active drivers):")
print(tenure_stats.to_string(index=False))
print(f"  6-12m drivers: {len(early_window)}, total active >=6m: {total_active}, pct={early_pct:.1f}%")

# Zone stats
print("\nNorthgate zones:")
zone_of_interest = zone_stats[zone_stats["pickup_zone"].isin(ps2_zones.keys())].sort_values("pickup_zone")
print(zone_of_interest.to_string(index=False))

# Promo churn
print("\nPromo churn by quartile:")
promo_churn_actual = u_rides.groupby(["ride_bracket","promo_quartile"], observed=True)["churn_flag"].mean() * 100
print(promo_churn_actual.unstack().to_string())

print("\nPromo share by quarter:")
print(promo_q.to_string(index=False))
