"""
Looker Studio Data Prep — RideFast Assessment
Outputs 7 clean CSVs, each purpose-built for one part of the dashboard.
Upload each to Google Sheets → connect in Looker Studio.

Files:
  output/looker_rides.csv          — 120K rows, one per ride (main fact table)
  output/looker_drivers.csv        — 8K rows, one per driver
  output/looker_users.csv          — 35K rows, one per user
  output/looker_tickets.csv        — 22K rows, one per ticket
  output/looker_wait_cliff.csv     — 6 rows, pre-aggregated wait bracket analysis
  output/looker_zone_stats.csv     — zone-level Northgate analysis
  output/looker_promo_matrix.csv   — promo quartile × ride bracket churn matrix
"""

import pandas as pd
import numpy as np
from pathlib import Path

CSV_DIR = Path("csvs")
OUT_DIR = Path("output")
OUT_DIR.mkdir(exist_ok=True)

AS_OF = pd.Timestamp("2024-06-30")

# ── Load raw CSVs ─────────────────────────────────────────────────────────────
print("Loading raw CSVs...")
rides   = pd.read_csv(CSV_DIR / "rides (2026).csv",
                      parse_dates=["request_time", "pickup_time", "dropoff_time"])
drivers = pd.read_csv(CSV_DIR / "drivers (2026).csv",
                      parse_dates=["signup_date"])
users   = pd.read_csv(CSV_DIR / "users (2026).csv",
                      parse_dates=["signup_date", "last_ride_date"])
tickets = pd.read_csv(CSV_DIR / "support_tickets (2026).csv",
                      parse_dates=["created_at"])

print(f"  Rides:   {len(rides):,}")
print(f"  Drivers: {len(drivers):,}")
print(f"  Users:   {len(users):,}")
print(f"  Tickets: {len(tickets):,}")


# ════════════════════════════════════════════════════════════════════════
# STEP 1 — ENRICH DRIVERS
# ════════════════════════════════════════════════════════════════════════

def assign_tier(row):
    if row["acceptance_rate"] < 0.60 and row["cancellation_rate"] > 0.30:
        return "Both-Issues"
    elif row["cancellation_rate"] > 0.30:
        return "High-Cancel"
    elif row["acceptance_rate"] < 0.60:
        return "Low-Accept"
    return "Standard"

drivers["Quality Tier"]      = drivers.apply(assign_tier, axis=1)
drivers["Is Problem Driver"] = drivers["Quality Tier"].map(
    {"Both-Issues": "Problem Driver", "High-Cancel": "Problem Driver",
     "Low-Accept":  "Problem Driver", "Standard":    "Standard Driver"}
)
drivers["Tenure Months"] = ((AS_OF - drivers["signup_date"]).dt.days / 30.44).clip(lower=0).round(1)

def tenure_bracket(m):
    if m < 6:    return "1. 0-6 Months"
    elif m < 12: return "2. 6-12 Months"
    elif m < 18: return "3. 12-18 Months"
    elif m < 24: return "4. 18-24 Months"
    else:        return "5. 24+ Months"

drivers["Tenure Bracket"] = drivers["Tenure Months"].apply(tenure_bracket)


# ════════════════════════════════════════════════════════════════════════
# STEP 2 — ENRICH USERS
# ════════════════════════════════════════════════════════════════════════

first_ride = (
    rides.groupby("user_id")["request_time"]
    .min().rename("first_ride_date").reset_index()
)
users = users.merge(first_ride, on="user_id", how="left")
users["Days To First Ride"] = (users["first_ride_date"] - users["signup_date"]).dt.days

def first_ride_bracket(d):
    if pd.isna(d):  return "7. Never Rode"
    d = int(d)
    if d == 0:      return "1. Same Day"
    elif d <= 7:    return "2. 1-7 Days"
    elif d <= 30:   return "3. 8-30 Days"
    elif d <= 90:   return "4. 1-3 Months"
    elif d <= 180:  return "5. 3-6 Months"
    elif d <= 365:  return "6. 6-12 Months"
    else:           return "7. Over 1 Year"

users["First Ride Bracket"] = users["Days To First Ride"].apply(first_ride_bracket)
users["User Group"] = users["churn_flag"].map({True: "Churned (79.6%)", False: "Active (20.4%)"})
users["Promo Dependency"] = (
    users["promo_rides"] / users["total_rides"].replace(0, np.nan)
).fillna(0).round(4)
users["Promo Quartile"] = pd.qcut(
    users["Promo Dependency"], 4,
    labels=["Q1 Low Promo", "Q2", "Q3", "Q4 Heavy Promo"]
).astype(str)

def ride_bracket(n):
    if n <= 0:      return "1. 0 Rides"
    elif n == 1:    return "2. 1 Ride"
    elif n <= 5:    return "3. 2-5 Rides"
    elif n <= 10:   return "4. 6-10 Rides"
    elif n <= 25:   return "5. 11-25 Rides"
    elif n <= 50:   return "6. 26-50 Rides"
    elif n <= 100:  return "7. 51-100 Rides"
    else:           return "8. 101+ Rides"

users["Ride Count Bracket"] = users["total_rides"].apply(ride_bracket)

# Value segment
user_revenue = (
    rides[rides["status"] == "completed"]
    .groupby("user_id")["fare_amount"].sum()
    .rename("Total Spend").reset_index()
)
users = users.merge(user_revenue, on="user_id", how="left")
users["Total Spend"] = users["Total Spend"].fillna(0)

def value_segment(row):
    churned = row["churn_flag"] == True
    high    = row["Total Spend"] > 200
    if churned and high:     return "High-Value Churned"
    elif churned:            return "Standard Churned"
    elif high:               return "High-Value Active"
    else:                    return "Standard Active"

users["Value Segment"] = users.apply(value_segment, axis=1)


# ════════════════════════════════════════════════════════════════════════
# STEP 3 — ENRICH RIDES
# ════════════════════════════════════════════════════════════════════════

r = rides.copy()

# Status flags
r["Is Completed"]     = (r["status"] == "completed").astype(int)
r["Is Driver Cancel"] = (r["status"] == "cancelled_driver").astype(int)
r["Is User Cancel"]   = (r["status"] == "cancelled_user").astype(int)
r["Is No Show"]       = (r["status"] == "no_show").astype(int)

# Revenue
r["Revenue"]     = r["fare_amount"].where(r["Is Completed"] == 1, 0)
r["Net Revenue"] = (r["fare_amount"] - r["promo_discount"]).where(r["Is Completed"] == 1, 0)

# Wait time
r["Wait Minutes"] = (
    (r["pickup_time"] - r["request_time"]).dt.total_seconds() / 60
)
r["Wait Minutes"] = r["Wait Minutes"].where(r["Wait Minutes"] >= 0, np.nan).round(1)
r["Wait Over 15"] = (r["Wait Minutes"] >= 15).fillna(False).astype(int)

def wait_bracket(m):
    if pd.isna(m): return "0. Unknown"
    if m < 5:      return "1. 0-5 min"
    elif m < 10:   return "2. 5-10 min"
    elif m < 15:   return "3. 10-15 min"
    elif m < 20:   return "4. 15-20 min"
    elif m < 30:   return "5. 20-30 min"
    else:          return "6. 30+ min"

r["Wait Bracket"] = r["Wait Minutes"].apply(wait_bracket)

# Trip duration
r["Trip Minutes"] = (
    (r["dropoff_time"] - r["pickup_time"]).dt.total_seconds() / 60
).where(r["Is Completed"] == 1, np.nan).round(1)

# Time dimensions — Looker Studio needs proper date column
r["Date"] = r["request_time"].dt.date.astype(str)               # YYYY-MM-DD
r["Year Month"] = r["request_time"].dt.strftime("%Y-%m")         # 2023-07 (sorts correctly)
r["Month Name"] = r["request_time"].dt.strftime("%b '%y")        # Jul '23
r["Quarter"]    = "Q" + r["request_time"].dt.quarter.astype(str) + " " + r["request_time"].dt.year.astype(str)
r["Day of Week"] = r["request_time"].dt.strftime("%a")           # Mon
r["Hour"]        = r["request_time"].dt.hour

# Join driver fields (slim set only)
driver_slim = drivers[["driver_id", "Quality Tier", "Is Problem Driver",
                        "Tenure Months", "Tenure Bracket",
                        "status", "avg_rating", "acceptance_rate", "cancellation_rate"]].copy()
driver_slim.columns = ["driver_id", "Driver Quality Tier", "Driver Tier Label",
                       "Driver Tenure Months", "Driver Tenure Bracket",
                       "Driver Status", "Driver Avg Rating",
                       "Driver Acceptance Rate", "Driver Cancellation Rate"]

r = r.merge(driver_slim, on="driver_id", how="left")
r["Driver Quality Tier"] = r["Driver Quality Tier"].fillna("Standard")
r["Driver Tier Label"]   = r["Driver Tier Label"].fillna("Standard Driver")
r["Driver Status"]       = r["Driver Status"].fillna("unknown")

# Join user fields (slim set only)
user_slim = users[["user_id", "churn_flag", "User Group", "Value Segment",
                   "First Ride Bracket", "Ride Count Bracket",
                   "Promo Quartile", "Total Spend"]].copy()
user_slim.columns = ["user_id", "User Churned", "User Group", "User Value Segment",
                     "User First Ride Bracket", "User Ride Count Bracket",
                     "User Promo Quartile", "User Total Spend"]

r = r.merge(user_slim, on="user_id", how="left")

assert len(r) == 120_000, f"Row inflation after join: {len(r)}"

# Select final columns for rides file (keep it lean)
rides_out_cols = [
    "ride_id", "user_id", "driver_id", "city", "pickup_zone",
    "Date", "Year Month", "Month Name", "Quarter", "Day of Week", "Hour",
    "status", "Is Completed", "Is Driver Cancel", "Is User Cancel", "Is No Show",
    "fare_amount", "promo_discount", "Revenue", "Net Revenue",
    "surge_multiplier", "promo_code_used",
    "rating_by_user", "rating_by_driver",
    "vehicle_type", "distance_km", "payment_method",
    "Wait Minutes", "Wait Bracket", "Wait Over 15", "Trip Minutes",
    "Driver Quality Tier", "Driver Tier Label", "Driver Status",
    "Driver Avg Rating", "Driver Acceptance Rate", "Driver Cancellation Rate",
    "Driver Tenure Bracket",
    "User Churned", "User Group", "User Value Segment",
    "User First Ride Bracket", "User Ride Count Bracket",
    "User Promo Quartile", "User Total Spend",
]
r_out = r[[c for c in rides_out_cols if c in r.columns]].copy()

print(f"\nRides output: {len(r_out):,} rows, {len(r_out.columns)} columns")


# ════════════════════════════════════════════════════════════════════════
# STEP 4 — DRIVER-LEVEL FILE (one row per driver)
# ════════════════════════════════════════════════════════════════════════

# Aggregate from rides
ride_agg = r.copy()
driver_agg = ride_agg.groupby("driver_id").agg(
    Rides        = ("ride_id",           "count"),
    Completed    = ("Is Completed",      "sum"),
    Cancels      = ("Is Driver Cancel",  "sum"),
    Revenue      = ("Revenue",           "sum"),
    Avg_Wait     = ("Wait Minutes",      "mean"),
    Over15       = ("Wait Over 15",      "sum"),
    Avg_Rating   = ("rating_by_user",    "mean"),
).reset_index()

driver_agg["Completion Rate"]      = (driver_agg["Completed"] / driver_agg["Rides"]).round(4)
driver_agg["Cancel Rate (Rides)"]  = (driver_agg["Cancels"]   / driver_agg["Rides"]).round(4)
driver_agg["Pct Rides Over 15min"] = (driver_agg["Over15"]    / driver_agg["Rides"]).round(4)
driver_agg["Revenue per Ride"]     = (driver_agg["Revenue"] / driver_agg["Completed"].replace(0, np.nan)).round(2)
driver_agg.rename(columns={"Avg_Wait": "Avg Wait Minutes", "Avg_Rating": "Avg Rating from Users"}, inplace=True)

# Ticket count per driver
driver_tickets = tickets.groupby("driver_id")["ticket_id"].count().rename("Tickets Received").reset_index()

d_out = drivers.copy()
d_out = d_out.merge(driver_agg, on="driver_id", how="left")
d_out = d_out.merge(driver_tickets, on="driver_id", how="left")
d_out["Tickets Received"] = d_out["Tickets Received"].fillna(0).astype(int)

# Select output columns
d_out = d_out.rename(columns={
    "driver_id":             "Driver ID",
    "city":                  "City",
    "signup_date":           "Signup Date",
    "vehicle_type":          "Vehicle Type",
    "status":                "Status",
    "avg_rating":            "Avg Rating",
    "total_rides":           "Total Rides (Profile)",
    "acceptance_rate":       "Acceptance Rate",
    "cancellation_rate":     "Cancellation Rate (Profile)",
    "online_hours_monthly":  "Online Hours Monthly",
    "Quality Tier":          "Quality Tier",
    "Is Problem Driver":     "Driver Tier Label",
    "Tenure Months":         "Tenure Months",
    "Tenure Bracket":        "Tenure Bracket",
})

d_final_cols = [
    "Driver ID", "City", "Status", "Vehicle Type",
    "Signup Date", "Tenure Months", "Tenure Bracket",
    "Acceptance Rate", "Cancellation Rate (Profile)", "Avg Rating",
    "Online Hours Monthly", "Total Rides (Profile)",
    "Quality Tier", "Driver Tier Label",
    "Rides", "Completed", "Cancels", "Revenue",
    "Completion Rate", "Cancel Rate (Rides)", "Avg Wait Minutes",
    "Pct Rides Over 15min", "Revenue per Ride", "Avg Rating from Users",
    "Tickets Received",
]
d_out = d_out[[c for c in d_final_cols if c in d_out.columns]]
print(f"Drivers output: {len(d_out):,} rows, {len(d_out.columns)} columns")


# ════════════════════════════════════════════════════════════════════════
# STEP 5 — USER-LEVEL FILE (one row per user)
# ════════════════════════════════════════════════════════════════════════

user_ride_stats = r.groupby("user_id").agg(
    Rides             = ("ride_id",           "count"),
    Completed         = ("Is Completed",       "sum"),
    Driver_Cancels    = ("Is Driver Cancel",   "sum"),
    Gross_Spend       = ("Revenue",            "sum"),
    Avg_Wait          = ("Wait Minutes",       "mean"),
    Rides_Over_15     = ("Wait Over 15",       "sum"),
    Avg_Rating_Given  = ("rating_by_user",     "mean"),
).reset_index()

user_ride_stats["Completion Rate"]      = (user_ride_stats["Completed"] / user_ride_stats["Rides"].replace(0, np.nan)).round(4)
user_ride_stats["Pct Rides Over 15min"] = (user_ride_stats["Rides_Over_15"] / user_ride_stats["Rides"].replace(0, np.nan)).round(4)
user_ride_stats.rename(columns={
    "Driver_Cancels":   "Driver Cancels Faced",
    "Gross_Spend":      "Gross Spend",
    "Avg_Wait":         "Avg Wait Minutes",
    "Rides_Over_15":    "Rides Over 15min",
    "Avg_Rating_Given": "Avg Rating Given",
}, inplace=True)

user_tickets = tickets.groupby("user_id")["ticket_id"].count().rename("Tickets Raised").reset_index()

u_out = users.copy()
u_out = u_out.merge(user_ride_stats, on="user_id", how="left")
u_out = u_out.merge(user_tickets, on="user_id", how="left")
u_out["Tickets Raised"] = u_out["Tickets Raised"].fillna(0).astype(int)

u_out = u_out.rename(columns={
    "user_id":           "User ID",
    "signup_date":       "Signup Date",
    "city":              "City",
    "total_rides":       "Total Rides (Profile)",
    "last_ride_date":    "Last Ride Date",
    "promo_rides":       "Promo Rides",
    "wallet_balance":    "Wallet Balance",
    "churn_flag":        "Churn Flag",
    "User Group":        "User Group",
    "Total Spend":       "Total Gross Spend",
    "First Ride Bracket":"First Ride Bracket",
    "Ride Count Bracket":"Ride Count Bracket",
    "Promo Quartile":    "Promo Quartile",
    "Value Segment":     "Value Segment",
    "Days To First Ride":"Days To First Ride",
    "Promo Dependency":  "Promo Dependency Ratio",
})

u_final_cols = [
    "User ID", "City", "Signup Date", "Last Ride Date",
    "Churn Flag", "User Group", "Value Segment",
    "Total Rides (Profile)", "Promo Rides", "Wallet Balance",
    "Days To First Ride", "First Ride Bracket", "Ride Count Bracket",
    "Promo Quartile", "Promo Dependency Ratio",
    "Total Gross Spend",
    "Rides", "Completed", "Completion Rate",
    "Driver Cancels Faced", "Rides Over 15min", "Pct Rides Over 15min",
    "Avg Wait Minutes", "Avg Rating Given",
    "Tickets Raised",
]
u_out = u_out[[c for c in u_final_cols if c in u_out.columns]]
print(f"Users output: {len(u_out):,} rows, {len(u_out.columns)} columns")


# ════════════════════════════════════════════════════════════════════════
# STEP 6 — TICKETS FILE
# ════════════════════════════════════════════════════════════════════════

ride_ctx = rides[["ride_id", "city", "pickup_zone", "status", "vehicle_type",
                  "request_time", "rating_by_user"]].copy()
ride_ctx["Wait Minutes"] = (
    (rides["pickup_time"] - rides["request_time"]).dt.total_seconds() / 60
).clip(lower=0).round(1)

t = tickets.copy()
t = t.merge(ride_ctx, on="ride_id", how="left")

t["Date"]          = t["created_at"].dt.date.astype(str)
t["Year Month"]    = t["created_at"].dt.strftime("%Y-%m")
t["Month Name"]    = t["created_at"].dt.strftime("%b '%y")
t["Quarter"]       = "Q" + t["created_at"].dt.quarter.astype(str) + " " + t["created_at"].dt.year.astype(str)
t["Is Resolved"]   = t["resolved"].astype(int)

severity_map = {"critical": 4, "high": 3, "medium": 2, "low": 1}
t["Severity Sort"] = t["severity"].map(severity_map).fillna(0).astype(int)

category_labels = {
    "fare_dispute":     "Fare Dispute",
    "safety":           "Safety",
    "lost_item":        "Lost Item",
    "app_issue":        "App Issue",
    "driver_behaviour": "Driver Behaviour",
}
t["Category Label"] = t["category"].map(category_labels).fillna(t["category"])

t_out = t.rename(columns={
    "ticket_id":            "Ticket ID",
    "ride_id":              "Ride ID",
    "user_id":              "User ID",
    "driver_id":            "Driver ID",
    "created_at":           "Created At",
    "category":             "Category",
    "severity":             "Severity",
    "resolved":             "Resolved",
    "resolution_time_hours":"Resolution Time Hours",
    "city":                 "City",
    "pickup_zone":          "Zone",
    "status":               "Ride Status",
    "vehicle_type":         "Vehicle Type",
    "rating_by_user":       "User Rating on Ride",
    "Wait Minutes":         "Ride Wait Minutes",
})

t_final_cols = [
    "Ticket ID", "Ride ID", "User ID", "Driver ID",
    "Created At", "Date", "Year Month", "Month Name", "Quarter",
    "Category", "Category Label", "Severity", "Severity Sort",
    "Resolved", "Is Resolved", "Resolution Time Hours",
    "City", "Zone", "Ride Status", "Vehicle Type",
    "User Rating on Ride", "Ride Wait Minutes",
]
t_out = t_out[[c for c in t_final_cols if c in t_out.columns]]
print(f"Tickets output: {len(t_out):,} rows, {len(t_out.columns)} columns")


# ════════════════════════════════════════════════════════════════════════
# STEP 7 — PRE-AGGREGATED: WAIT CLIFF (6 rows — one per bracket)
# ════════════════════════════════════════════════════════════════════════

wait_agg = r.groupby("Wait Bracket").agg(
    Rides               = ("ride_id",           "count"),
    Completed           = ("Is Completed",       "sum"),
    Driver_Cancels      = ("Is Driver Cancel",   "sum"),
    User_Cancels        = ("Is User Cancel",     "sum"),
    Avg_Wait_In_Bracket = ("Wait Minutes",       "mean"),
).reset_index()

wait_agg["Completion Rate"]   = (wait_agg["Completed"]      / wait_agg["Rides"]).round(4)
wait_agg["Driver Cancel Rate"]= (wait_agg["Driver_Cancels"] / wait_agg["Rides"]).round(4)
wait_agg["User Cancel Rate"]  = (wait_agg["User_Cancels"]   / wait_agg["Rides"]).round(4)
wait_agg["Pct of All Rides"]  = (wait_agg["Rides"]          / wait_agg["Rides"].sum()).round(4)
wait_agg.rename(columns={
    "Wait Bracket":         "Wait Bracket",
    "Avg_Wait_In_Bracket":  "Avg Wait in Bracket (min)",
    "Driver_Cancels":       "Driver Cancels",
    "User_Cancels":         "User Cancels",
}, inplace=True)
# Remove unknown bracket
wait_agg = wait_agg[wait_agg["Wait Bracket"] != "0. Unknown"].sort_values("Wait Bracket")

print(f"Wait cliff output: {len(wait_agg)} rows")


# ════════════════════════════════════════════════════════════════════════
# STEP 8 — PRE-AGGREGATED: ZONE STATS (Northgate detail)
# ════════════════════════════════════════════════════════════════════════

zone_agg = r.groupby(["city", "pickup_zone"]).agg(
    Rides           = ("ride_id",           "count"),
    Completed       = ("Is Completed",       "sum"),
    Driver_Cancels  = ("Is Driver Cancel",   "sum"),
    Avg_Wait        = ("Wait Minutes",       "mean"),
    Revenue         = ("Revenue",            "sum"),
    Rides_Over_15   = ("Wait Over 15",       "sum"),
).reset_index()

zone_agg["Completion Rate"]   = (zone_agg["Completed"]      / zone_agg["Rides"]).round(4)
zone_agg["Driver Cancel Rate"]= (zone_agg["Driver_Cancels"] / zone_agg["Rides"]).round(4)
zone_agg["Pct Rides Over 15"] = (zone_agg["Rides_Over_15"]  / zone_agg["Rides"]).round(4)

# Platform averages
platform_completion = r["Is Completed"].mean()
platform_wait       = r["Wait Minutes"].mean()

zone_agg["Platform Completion Rate"] = round(platform_completion, 4)
zone_agg["Platform Avg Wait"]        = round(platform_wait, 1)
zone_agg["Completion vs Platform"]   = (zone_agg["Completion Rate"] - platform_completion).round(4)
zone_agg["Wait vs Platform"]         = (zone_agg["Avg_Wait"] - platform_wait).round(1)

zone_agg.rename(columns={
    "city":          "City",
    "pickup_zone":   "Zone",
    "Driver_Cancels":"Driver Cancels",
    "Avg_Wait":      "Avg Wait Minutes",
    "Rides_Over_15": "Rides Over 15min",
}, inplace=True)

print(f"Zone stats output: {len(zone_agg)} rows (all cities/zones)")


# ════════════════════════════════════════════════════════════════════════
# STEP 9 — PRE-AGGREGATED: PROMO CHURN MATRIX
# ════════════════════════════════════════════════════════════════════════

# For each (Promo Quartile × Ride Count Bracket): churn rate
promo_matrix = users.groupby(["Promo Quartile", "Ride Count Bracket"]).agg(
    Users       = ("user_id", "count"),
    Churned     = ("churn_flag", "sum"),
).reset_index()

promo_matrix["Churn Rate"] = (promo_matrix["Churned"] / promo_matrix["Users"]).round(4)

# Sort orders
quartile_order = {"Q1 Low Promo": 1, "Q2": 2, "Q3": 3, "Q4 Heavy Promo": 4}
bracket_order  = {
    "1. 0 Rides": 1, "2. 1 Ride": 2, "3. 2-5 Rides": 3, "4. 6-10 Rides": 4,
    "5. 11-25 Rides": 5, "6. 26-50 Rides": 6, "7. 51-100 Rides": 7, "8. 101+ Rides": 8
}
promo_matrix["Quartile Sort"] = promo_matrix["Promo Quartile"].map(quartile_order)
promo_matrix["Bracket Sort"]  = promo_matrix["Ride Count Bracket"].map(bracket_order)
promo_matrix = promo_matrix.sort_values(["Bracket Sort", "Quartile Sort"])
promo_matrix.rename(columns={
    "Promo Quartile":     "Promo Quartile",
    "Ride Count Bracket": "Ride Count Bracket",
}, inplace=True)

print(f"Promo matrix output: {len(promo_matrix)} rows")


# ════════════════════════════════════════════════════════════════════════
# STEP 10 — WRITE ALL FILES
# ════════════════════════════════════════════════════════════════════════

outputs = {
    "looker_rides.csv":        r_out,
    "looker_drivers.csv":      d_out,
    "looker_users.csv":        u_out,
    "looker_tickets.csv":      t_out,
    "looker_wait_cliff.csv":   wait_agg,
    "looker_zone_stats.csv":   zone_agg,
    "looker_promo_matrix.csv": promo_matrix,
}

print("\nWriting files...")
for fname, df in outputs.items():
    path = OUT_DIR / fname
    df.to_csv(path, index=False)
    mb = path.stat().st_size / 1024 / 1024
    print(f"  {fname:<30} {mb:5.1f} MB   {len(df):>7,} rows   {len(df.columns)} cols")

# ── Sanity checks ─────────────────────────────────────────────────────
print("\nSanity Checks:")
print(f"  Total rides:          {len(r_out):,}           (expect 120,000)")
print(f"  Completion rate:      {r_out['Is Completed'].mean()*100:.1f}%         (expect 81.6%)")
print(f"  Total revenue:        ${r_out['Revenue'].sum():,.0f}   (expect $3,583,768)")
print(f"  Driver cancel rate:   {r_out['Is Driver Cancel'].mean()*100:.1f}%          (expect 9.3%)")
print(f"  Rides over 15 min:    {r_out['Wait Over 15'].sum():,}          (expect 9,132)")
print(f"  Both-Issues rides:    {(r_out['Driver Quality Tier']=='Both-Issues').sum():,}        (expect ~11,174)")
print(f"  Active users:         {(u_out['Churn Flag']==False).sum():,}          (expect 7,133)")
print(f"  Churned users:        {(u_out['Churn Flag']==True).sum():,}         (expect 27,867)")
print(f"  Wait cliff rows:      {len(wait_agg)} brackets")
print(f"  Zone rows:            {len(zone_agg)}")

print("\nDone. Upload all 7 files to Google Sheets, then connect in Looker Studio.")
print("\nFile purposes:")
print("  looker_rides.csv        -> Main data source for Pages 1, 2, 4")
print("  looker_drivers.csv      -> Driver analysis charts on Page 4")
print("  looker_users.csv        -> User/churn analysis on Page 3")
print("  looker_tickets.csv      -> Support ticket charts on Page 5")
print("  looker_wait_cliff.csv   -> The 15-min wait cliff chart (pre-computed)")
print("  looker_zone_stats.csv   -> Northgate zone breakdown on Page 4")
print("  looker_promo_matrix.csv -> Promo vs churn heatmap on Page 3")
