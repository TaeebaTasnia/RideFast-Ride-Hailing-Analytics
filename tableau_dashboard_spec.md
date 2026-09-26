# RideFast Tableau Dashboard — Complete Build Specification

*5-page interview-ready dashboard | Directly connected to problem_statement_2.md findings*

---

## QUICK REFERENCE — THE STORY YOU'RE TELLING

| Page | Business Question | Problem Linked |
|------|-------------------|---------------|
| 1. Executive Overview | "How is RideFast performing, and where should leadership look?" | Sets up all 5 |
| 2. Ride Funnel & Wait Cliff | "Where are rides being lost?" | P2 + P3 |
| 3. User Behaviour & Churn | "Who are our users, and what did the valuable ones do before leaving?" | P1 + P5 |
| 4. Driver Operations | "Is the driver supply causing our completion problem?" | P3 + P4 |
| 5. Support & Experience | "What are users complaining about, and does it map to operations?" | P4 + P5 |

---

## STEP 0 — DATA CONNECTION & JOINS IN TABLEAU

### Connect

1. Open Tableau Desktop → **Connect → Text File**
2. Connect to `rides (2026).csv` → this becomes your **primary table**
3. Drag `drivers (2026).csv` onto the canvas → Join on `Driver ID`
   - Join type: **Left join** (keep all rides, even if no driver record)
4. Drag `users (2026).csv` onto the canvas → Join on `User ID`
   - Join type: **Left join**
5. **DO NOT join support_tickets directly here** — it joins on ride_id but multiple tickets per ride will inflate row count. Instead, create a **separate data source** for tickets.

### Duplicate the data source for tickets

1. Right-click the data source → Duplicate
2. On the duplicate, the primary table is `support_tickets (2026).csv`
3. Left-join `rides (2026).csv` on `Ride ID` (to get city and status context)
4. Use **COUNTD([Ticket ID])** everywhere to prevent double-counting

### Verify join integrity (do this BEFORE building any sheet)

Create a sheet, drag **COUNTD([Ride ID])** to Rows → should show **120,000**
If it shows more, the join is creating duplicates → switch to a relationship instead of a join.

---

## STEP 1 — CALCULATED FIELDS (create all before building sheets)

Open **rides (2026).csv** data source and create these calculated fields:

### Core Status Flags

```tableau
// Completion Flag
[Is Completed]
IF [Status] = "completed" THEN 1 ELSE 0 END

// Driver Cancel Flag
[Is Driver Cancel]
IF [Status] = "cancelled_driver" THEN 1 ELSE 0 END

// User Cancel Flag
[Is User Cancel]
IF [Status] = "cancelled_user" THEN 1 ELSE 0 END
```

### Time / Wait

```tableau
// Wait Minutes (pickup_time - request_time)
[Wait Minutes]
DATEDIFF('minute', [Request Time], [Pickup Time])

// Clean wait (exclude nulls and negatives)
[Wait Minutes Clean]
IF [Wait Minutes] >= 0 AND NOT ISNULL([Wait Minutes]) THEN [Wait Minutes] ELSE NULL END

// Wait Bracket (for the cliff chart)
[Wait Bracket]
IF [Wait Minutes Clean] < 5 THEN "0–5 min"
ELSEIF [Wait Minutes Clean] < 10 THEN "5–10 min"
ELSEIF [Wait Minutes Clean] < 15 THEN "10–15 min"
ELSEIF [Wait Minutes Clean] < 20 THEN "15–20 min"
ELSEIF [Wait Minutes Clean] < 30 THEN "20–30 min"
ELSE "30+ min"
END

// Wait Bracket Sort (so brackets appear in order)
[Wait Bracket Sort]
IF [Wait Minutes Clean] < 5 THEN 1
ELSEIF [Wait Minutes Clean] < 10 THEN 2
ELSEIF [Wait Minutes Clean] < 15 THEN 3
ELSEIF [Wait Minutes Clean] < 20 THEN 4
ELSEIF [Wait Minutes Clean] < 30 THEN 5
ELSE 6
END

// Over 15 min flag
[Wait Over 15]
IF [Wait Minutes Clean] >= 15 THEN 1 ELSE 0 END
```

### Revenue

```tableau
// Revenue (only on completed rides)
[Revenue]
IF [Status] = "completed" THEN [Fare Amount] ELSE 0 END

// Net Revenue (fare minus promo discount)
[Net Revenue]
IF [Status] = "completed" THEN [Fare Amount] - [Promo Discount] ELSE 0 END
```

### Quarter / Month

```tableau
// Quarter Label
[Quarter Label]
"Q" + STR(DATEPART('quarter', [Request Time])) + "'" + RIGHT(STR(DATEPART('year', [Request Time])), 2)

// Quarter Sort
[Quarter Sort]
(DATEPART('year', [Request Time]) - 2023) * 4 + DATEPART('quarter', [Request Time]) - 2
// This gives: Q3'23=1, Q4'23=2, Q1'24=3, Q2'24=4
```

### Driver Quality Tier (from drivers.csv fields after join)

```tableau
[Driver Quality Tier]
IF [Acceptance Rate] < 0.60 AND [Cancellation Rate] > 0.30 THEN "Both-Issues"
ELSEIF [Cancellation Rate] > 0.30 THEN "High-Cancel"
ELSEIF [Acceptance Rate] < 0.60 THEN "Low-Accept"
ELSE "Standard"
END

// Simplified for the key chart
[Driver Tier Label]
IF [Acceptance Rate] < 0.60 AND [Cancellation Rate] > 0.30 THEN "Problem Driver"
ELSE "Standard Driver"
END
```

### User Churn (from users.csv fields after join)

```tableau
// Churn group label
[User Group]
IF [Churn Flag] = TRUE THEN "Churned (79.6%)" ELSE "Active (20.4%)" END
```

### Completion Rate (for sheets that need it as a measure)

```tableau
[Completion Rate]
SUM([Is Completed]) / COUNTD([Ride ID])

[Driver Cancel Rate]
SUM([Is Driver Cancel]) / COUNTD([Ride ID])
```

---

## PAGE 1 — EXECUTIVE OVERVIEW

**Dashboard title:** `RideFast Business Health — Jul 2023 to Jun 2024`

**Color palette for this page:**
- Background: `#0F1B2D` (deep navy)
- KPI card bg: `#1A2E45`
- Good metric accent: `#10B981` (emerald green)
- Warning accent: `#F59E0B` (amber)
- Critical accent: `#EF4444` (red)
- Primary chart color: `#3B82F6` (vibrant blue)
- Text: `#F1F5F9` (near white)

> Alternatively if you prefer white background, use `#1E3A5F` as primary, `#10B981` green, `#EF4444` red.

---

### KPI Row (7 cards across the top)

Create each as a **separate sheet** → drag to dashboard as small tiles.

| Card # | Label | Calculation | Format |
|--------|-------|-------------|--------|
| K1 | Total Rides | `COUNTD([Ride ID])` | `120,000` |
| K2 | Completed Rides | `SUM([Is Completed])` | `97,886` |
| K3 | Completion Rate | `SUM([Is Completed])/COUNTD([Ride ID])` | `81.6%` |
| K4 | Gross Revenue | `SUM([Revenue])` | `$3.58M` |
| K5 | Active Users | `COUNTD(IF [Churn Flag]=FALSE THEN [User ID] END)` | `7,133` |
| K6 | Avg Fare/Ride | `SUM([Revenue])/SUM([Is Completed])` | `$36.60` |
| K7 | Avg Rating (drivers) | From drivers.csv — `AVG([Avg Rating])` | `4.2★` |

**Sheet setup for each KPI:**
- Rows: the measure
- Mark type: Text
- Font: Bold, 28–32pt
- Label below: field name in 11pt
- No axes, no gridlines
- Background: KPI card bg color

---

### Sheet 1A — "12 Months, Zero Movement" (Headline chart)

**Business question:** Is demand growing?

**Chart type:** Line chart with dual axis

**Rows:** `MONTH([Request Time])`
**Columns:** Two measures on dual axis:
- Left axis: `COUNTD([Ride ID])` (Total Requests — blue line, thick)
- Right axis: `SUM([Is Completed])` (Completed Rides — teal line)

**Also add:** `SUM([Is Driver Cancel])` as a dashed red line (secondary axis)

**Title:** `"Flat demand for 12 months — every promo failed to move volume"`

**Reference line:** Add average line for total requests — color `#F59E0B`

**Key visual:** The flat trend across Q3'23–Q2'24 makes the core business problem immediately obvious.

**Filters:** Date range filter (show as slider)

---

### Sheet 1B — City Performance Bar

**Chart type:** Horizontal bar chart, sorted descending by completion rate

**Rows:** `[City]`
**Columns:** `SUM([Is Completed])/COUNTD([Ride ID])` (Completion Rate)

**Color:** Color by completion rate using diverging palette:
- Below 79% → red `#EF4444`
- 79–83% → amber `#F59E0B`
- Above 83% → green `#10B981`

**Reference line:** Platform average 81.4%

**Label:** Show % on each bar

**Title:** `"Northgate is the only city materially below the platform average"`

**Tooltip:** 
```
City: [City]
Completion Rate: [completion rate]
vs Network: 81.4%
Gap: [diff]
Total Rides: [count]
Avg Wait: [avg wait minutes]
```

---

### Sheet 1C — Revenue by User Status (donut feel, use bar)

**Chart type:** Horizontal 2-bar comparison

**Rows:** `[User Group]`
**Columns:** `SUM([Revenue])`

**Color:**
- Churned: `#EF4444` (red — alarming because they're gone)
- Active: `#10B981` (green)

**Label:** Show `$2,870,285 (80.1%)` and `$713,483 (19.9%)`

**Title:** `"80.1% of revenue came from users who are no longer active"`

This immediately frames Problem 1.

---

### Page 1 Dashboard Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  RideFast | Jul 2023 – Jun 2024        [Date] [City] [filters]   │
├──────┬──────┬──────┬──────┬──────┬──────┬──────────────────────┤
│ 120K │ 97.9K│ 81.6%│ $3.6M│ 7,133│ $36.6│ 4.2★                │
│Rides │Compl │Cmpl% │ Rev  │Active│ Fare │Rating               │
├────────────────────────────┬─────────────────────────────────────┤
│                            │                                     │
│  "12 Months, Zero Movement"│  City Completion Rates              │
│  (line chart — full width) │  (horizontal bar, sorted)           │
│                            │                                     │
├────────────────────────────┴─────────────────────────────────────┤
│                                                                  │
│  "80.1% of Revenue Came From Users Who Left" (2-bar comparison)  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## PAGE 2 — RIDE FUNNEL & THE 15-MIN CLIFF

**Dashboard title:** `Where Rides Fall Apart — The Wait Time Cliff`

**Page color theme:**
- Background: `#FFFFFF`
- Problem chart color: `#DC2626` (danger red)
- Good zone: `#059669` (green)
- Cliff zone highlight: `#FEF3C7` (amber highlight band)

---

### Sheet 2A — The Wait Cliff (MOST IMPORTANT CHART IN DECK)

**Chart type:** Dual-axis bar/line combo

**Rows:** `[Wait Bracket]` (sorted by `[Wait Bracket Sort]`)

**Left axis (bars):** Completion Rate
- `SUM([Is Completed]) / COUNTD([Ride ID])`
- Color: `#059669` for <15min bars, `#DC2626` for 15min+ bars
- Use `[Wait Minutes Clean] < 15` as a color condition

**Right axis (line with dots):** Driver Cancel Rate
- `SUM([Is Driver Cancel]) / COUNTD([Ride ID])`
- Color: `#F97316` (orange), thickness 2.5

**Reference line:** 15 minutes — vertical dashed line in dark red with label "Cliff: 32pp drop"

**Data labels on bars:** Show %, bold

**Title:** `"After 15 minutes: completion collapses from 78% → 54% while driver cancels spike to 29%"`

**Tooltip:**
```
Wait Bracket: [bracket]
Rides: [count]
Completion Rate: [%]
Driver Cancel Rate: [%]
```

**Key numbers that must be visible:**
- 0–5 min: 86.2% completion, 5.8% driver cancel
- 15–20 min: 54.1% completion, 29.3% driver cancel (these should be highlighted/annotated)

---

### Sheet 2B — Ride Count per Bracket

**Chart type:** Bar chart (area or bar)

**Rows:** `[Wait Bracket]`
**Columns:** `COUNTD([Ride ID])`

**Color:** Same scheme — green below 15min, red above

**Reference annotation:** "7.6% of rides (9,132) cross the 15-min mark"

Place this BELOW Sheet 2A to show scale of the problem.

---

### Sheet 2C — Driver Cancel Heatmap by City × Wait Bracket

**Chart type:** Heat map / cross-tab

**Rows:** `[City]`
**Columns:** `[Wait Bracket]`
**Color:** Driver Cancel Rate — diverging: white→red (`#FEE2E2` → `#991B1B`)

**Why this exists:** Shows whether the 15-min cliff is universal or concentrated in specific cities. Northgate should light up.

**Title:** `"The wait cliff is worst in Northgate — driver cancel exceeds 30% after 15 min"`

---

### Sheet 2D — Platform Funnel

**Chart type:** Funnel/bar (use horizontal bars of decreasing length)

Create 4 calculated fields:
```
[Funnel 1 - Requests]  = COUNTD([Ride ID])                     // 120,000
[Funnel 2 - Accepted]  = SUM(IF [Status] != 'no_show' THEN 1 END) // approx
[Funnel 3 - Completed] = SUM([Is Completed])                    // 97,886
[Funnel 4 - Cancelled] = COUNTD([Ride ID]) - SUM([Is Completed]) // 22,114
```

**Visualization:** 4 horizontal bars, centered, decreasing:
- Requests: full width, `#3B82F6`
- Completed: 81.6% width, `#10B981`
- Driver cancelled: `#EF4444`
- User cancelled: `#F97316`

**Title:** `"18.4% of rides never complete — driver cancellations are 9.3% alone"`

---

### Page 2 Dashboard Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  Page 2: Where Rides Fall Apart      [City] [Date] [Ride Type]   │
├──────────────────────────────┬───────────────────────────────────┤
│                              │                                   │
│  THE 15-MIN CLIFF            │  RIDE FUNNEL                      │
│  (dual-axis bar+line)        │  (horizontal funnel bars)         │
│                              │                                   │
├──────────────────────────────┴───────────────────────────────────┤
│  Ride Count per Wait Bracket (bar chart — shows 9,132 rides >15m)│
├──────────────────────────────────────────────────────────────────┤
│  Driver Cancel Rate by City × Wait Bracket (heat map)            │
└──────────────────────────────────────────────────────────────────┘
```

---

## PAGE 3 — USER BEHAVIOUR & CHURN

**Dashboard title:** `The Users Who Left Were the Most Valuable`

**Color theme:**
- Churned users: `#DC2626` (red — alarming)
- Active users: `#2563EB` (blue)
- Revenue highlight: `#D97706` (gold)
- Background: `#F8FAFC`

---

### Sheet 3A — Revenue Concentration Bar

Already designed as Sheet 1C — reuse or embed.

Annotations to add here:
- "27,867 churned users avg $103/ride"
- "7,133 active users avg $100/ride"
- "The gap isn't spend — it's that they stopped"

---

### Sheet 3B — Churn Rate by Time to First Ride

**Chart type:** Bar chart (declining trend = good, but the numbers stay high)

**Data needed:** A calculated field that groups users by days between signup_date and their first ride request.

In Tableau, create a **Level of Detail (LOD) expression** to find first ride per user:

```tableau
// First ride date per user (LOD)
[First Ride Date]
{ FIXED [User ID] : MIN([Request Time]) }

// Days from signup to first ride
[Days to First Ride]
DATEDIFF('day', [Signup Date], [First Ride Date])

// Time-to-first-ride bracket
[First Ride Bracket]
IF [Days to First Ride] = 0 THEN "Same Day"
ELSEIF [Days to First Ride] <= 7 THEN "1–7 Days"
ELSEIF [Days to First Ride] <= 30 THEN "8–30 Days"
ELSEIF [Days to First Ride] <= 90 THEN "1–3 Months"
ELSEIF [Days to First Ride] <= 180 THEN "3–6 Months"
ELSEIF [Days to First Ride] <= 365 THEN "6–12 Months"
ELSE "Over 1 Year"
END

[First Ride Bracket Sort]
IF [Days to First Ride] = 0 THEN 1
ELSEIF [Days to First Ride] <= 7 THEN 2
ELSEIF [Days to First Ride] <= 30 THEN 3
ELSEIF [Days to First Ride] <= 90 THEN 4
ELSEIF [Days to First Ride] <= 180 THEN 5
ELSEIF [Days to First Ride] <= 365 THEN 6
ELSE 7
END
```

**Rows:** `[First Ride Bracket]` (sorted by sort field)
**Columns:** Churn Rate = `SUM([Is Churned]) / COUNTD([User ID])`

Where `[Is Churned] = IF [Churn Flag] = TRUE THEN 1 ELSE 0 END`

**Color:** gradient from green (low) to red (high)

**Labels on bars:** Show % with 1 decimal

**Title:** `"Users who ride within 7 days churn at 73.9% — waiting a year: 87.6%"`

**Key insight annotation:**
"All groups churn at 74–88% — the problem isn't which day they started. It's that the first ride experience isn't sticky enough to bring anyone back."

---

### Sheet 3C — User Ride Frequency Distribution

**Chart type:** Histogram / bar

**Calculated field:**
```tableau
[Ride Count Bracket]
// Use users.csv [Total Rides] field after join
IF [Total Rides] = 0 THEN "0 rides (never rode)"
ELSEIF [Total Rides] = 1 THEN "1 ride"
ELSEIF [Total Rides] <= 5 THEN "2–5 rides"
ELSEIF [Total Rides] <= 10 THEN "6–10 rides"
ELSEIF [Total Rides] <= 25 THEN "11–25 rides"
ELSEIF [Total Rides] <= 50 THEN "26–50 rides"
ELSE "51+ rides"
END
```

**Rows:** `[Ride Count Bracket]`
**Columns:** `COUNTD([User ID])`, colored by churn rate

**Title:** `"Most users ride infrequently — heavy users churn less but they're few"`

---

### Sheet 3D — Promo Churn Matrix

**Chart type:** Cross-tab (text table with color)

**Rows:** Ride bracket (1–10, 11–25, 26–50, 51–100)
**Columns:** Promo quartile (Q1 Low, Q4 High)
**Values:** Churn Rate (colored white→red)

```tableau
[Promo Quartile]
// Use promo_dependency_ratio = promo_rides / total_rides
// Quartile 1 = lowest promo dependency, 4 = highest
// Use NTILE(4) on users.csv — set this up in Tableau using a calculated field
// or pre-compute in Python and add as a column in users.csv prep
```

**Key values to land:**
- Row 1–10: Q1 = 82.7%, Q4 = 82.7% (ZERO difference — annotate this)
- Row 51–100: Q1 = 82.1%, Q4 = 55.6% (26.5pp gap — annotate this)

**Title:** `"Promos make zero difference for new users — the gap only appears at 51+ rides"`

---

### Page 3 Dashboard Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  Page 3: The Users Who Left          [City] [Signup Date]        │
├───────────────────────────────┬──────────────────────────────────┤
│  Revenue Split                │  Churn by Time to First Ride     │
│  Churned = 80.1% of revenue   │  (bar chart declining left→right)│
│  (2-bar comparison)           │                                  │
├───────────────────────────────┴──────────────────────────────────┤
│  User Ride Frequency Distribution                                │
│  (histogram showing most users have <5 rides)                    │
├──────────────────────────────────────────────────────────────────┤
│  Promo Effectiveness Matrix (cross-tab heat map)                 │
│  "Zero effect for new users"                                     │
└──────────────────────────────────────────────────────────────────┘
```

---

## PAGE 4 — DRIVER OPERATIONS & GEOGRAPHY

**Dashboard title:** `741 Drivers Are Causing the Wait Problem — And Northgate Proves It`

**Color theme:**
- Problem driver tier: `#DC2626`
- Standard driver: `#2563EB`
- Zone problem: `#F97316` (orange)
- Zone good: `#059669` (green)

---

### Sheet 4A — % Rides Over 15 Min by Driver Tier

**Chart type:** Bar chart (2 bars)

**Rows:** `[Driver Tier Label]`
**Columns:** `SUM([Wait Over 15]) / COUNTD([Ride ID])`

**Color:** Problem = red, Standard = blue

**Labels:** Both-Issues: 43.0%, Standard: 2.8%

**Title:** `"Problem drivers cause 15× more long waits than standard drivers"`

**Annotation:** "588 of these 741 are still active today"

---

### Sheet 4B — Driver Cancel Rate by Tier (from drivers.csv)

**Chart type:** Bar chart (3 bars)

For this sheet, switch to a **driver-level view** (one row per driver):

**Rows:** Driver tier (Both-Issues / Standard / Suspended)
**Columns:** AVG([Cancellation Rate]) from drivers.csv

**Color:**
- Both-Issues: `#DC2626`
- Standard: `#2563EB`
- Suspended: `#9CA3AF` (gray — the irony: they're suspended but perform BETTER than active problem drivers)

**Values:** 42.2% / 11.0% / 13.5%

**Title:** `"Suspended drivers cancel at 13.5% — the 588 'active' problem drivers cancel at 42.2%"`

**Annotation box:** "The suspension logic is backwards — drivers with better metrics are suspended while worse ones operate"

---

### Sheet 4C — Driver Tenure Quality Improvement

**Chart type:** Line chart with markers

**X-axis:** Tenure bracket (6–12m, 12–18m, 18–24m, 24+m)
**Y-axis (left):** AVG([Cancellation Rate]) — should show steep drop from 0.217 to 0.101
**Y-axis (right):** AVG([Avg Rating]) — shows jump from 3.92 to 4.25

```tableau
[Tenure Bracket]
IF DATEDIFF('month', [Signup Date], DATE("2024-06-30")) < 6 THEN "0–6 Months"
ELSEIF DATEDIFF('month', [Signup Date], DATE("2024-06-30")) < 12 THEN "6–12 Months"
ELSEIF DATEDIFF('month', [Signup Date], DATE("2024-06-30")) < 18 THEN "12–18 Months"
ELSEIF DATEDIFF('month', [Signup Date], DATE("2024-06-30")) < 24 THEN "18–24 Months"
ELSE "24+ Months"
END
```

Note: Divide DATEDIFF result by 30.44/30 or use month-based calculation.

**Title:** `"Driver quality jumps sharply at 12 months — the problem is they leave before then"`

**Annotation:** "34% of active drivers are in the 6–12m below-average window"

---

### Sheet 4D — Northgate Zone Comparison

**Chart type:** Bullet chart / bar chart comparing zones vs platform average

**Rows:** Zone (NOR-Z04, NOR-Z05, Platform Avg, NOR-Z01, NOR-Z03)
**Columns (dual axis):**
- Left: Completion Rate (bar)
- Right: Avg Wait Minutes (dot/lollipop)

**Color:**
- Problem zones (Z04, Z05): `#DC2626`
- Platform: `#9CA3AF`
- Good zones (Z01, Z03): `#059669`

**Reference line:** Platform average 81.4%

**Title:** `"NOR-Z04 and Z05 have 23-min waits vs 7.4 min in the same city's good zones"`

**Key annotation:** "Same driver pool. Drivers simply aren't going there."

---

### Sheet 4E — City Performance Scatter (Supply vs Demand)

**Chart type:** Scatter plot

**X-axis:** Active Drivers (from drivers.csv COUNTD per city)
**Y-axis:** Completed Rides (COUNTD per city)
**Bubble size:** Total Revenue (SUM)
**Color:** Completion Rate (diverging)
**Label:** City name

**Title:** `"City performance matrix — supply vs demand"`

**Reference lines:** Median X, Median Y → creates 4 quadrants

---

### Page 4 Dashboard Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  Page 4: Driver Operations & Geography   [City] [Driver Tier]    │
├────────────────────┬─────────────────────┬───────────────────────┤
│ % Rides >15min     │ Cancel Rate by Tier  │ Driver Tenure Quality │
│ by Driver Tier     │ (3-bar chart)        │ (dual-axis line)      │
│ (2 bars: 43% vs 3%)│                      │                       │
├────────────────────┴─────────────────────┴───────────────────────┤
│                                                                  │
│  Northgate Zone Comparison (horizontal bullet chart)             │
│  "Z04/Z05 broken — Z01/Z03 fine — same drivers"                 │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│  City Scatter: Supply vs Demand (bubble chart)                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## PAGE 5 — SUPPORT TICKETS & CUSTOMER EXPERIENCE

**Switch to the support_tickets data source for this page.**

**Dashboard title:** `What Customers Are Complaining About — And How Long It Takes`

**Color theme:**
- High severity / unresolved: `#DC2626`
- Resolved: `#059669`
- Categories: distinct vibrant palette

---

### Sheet 5A — Ticket Volume vs Ride Volume (normalized)

**Chart type:** Dual-axis line chart

**X-axis:** Month
**Left axis:** `COUNTD([Ticket ID]) / COUNTD([Ride ID]) * 1000` — Tickets per 1,000 rides
**Right axis:** `COUNTD([Ride ID])` — rides (to show both trends together)

**Title:** `"Support volume holds steady — fare disputes and safety issues never decline"`

---

### Sheet 5B — Ticket Category Breakdown

**Chart type:** Horizontal stacked bar, sorted by volume

**Rows:** `[Category]`
**Columns:** `COUNTD([Ticket ID])`

**Color by category (5 distinct vibrant colors):**
- fare_dispute: `#8B5CF6` (purple)
- safety: `#EF4444` (red)
- driver_behaviour: `#F97316` (orange)
- lost_item: `#F59E0B` (amber)
- app_issue: `#3B82F6` (blue)

**Second layer:** Color opacity by severity (critical=100%, high=75%, etc.)

**Title:** `"Fare disputes and driver behaviour make up the majority of support volume"`

---

### Sheet 5C — Resolution Rate by Category

**Chart type:** Bar chart

**Rows:** `[Category]`
**Columns:** `SUM(IF [Resolved] = TRUE THEN 1 ELSE 0 END) / COUNTD([Ticket ID])`

**Reference line:** 50% (flag anything below)

**Color:** Above 80% = green, 60–80% = amber, below 60% = red

**Title:** `"Safety and driver behaviour tickets have the lowest resolution rates"`

---

### Sheet 5D — Avg Resolution Time by Category and Severity

**Chart type:** Cross-tab (heat map)

**Rows:** `[Category]`
**Columns:** `[Severity]` (low, medium, high, critical)
**Value:** `AVG([Resolution Time Hours])`

**Color:** White → dark red (longer = worse)

**Title:** `"Critical safety issues take longest to resolve — average X hours"`

---

### Sheet 5E — Ticket Rate by City

**Chart type:** Bar chart

**Rows:** `[City]`
**Columns:** Tickets per 1,000 rides
**Color:** Same diverging scheme as completion rate (inverse — higher tickets = redder)

**Reference line:** Network average

**Title:** `"Northgate generates the most support tickets per ride — connecting to its operational failure"`

---

### Page 5 Dashboard Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  Page 5: Customer Experience & Support       [City] [Category]   │
├────────────────────────────┬─────────────────────────────────────┤
│  KPIs: Total Tickets 22K   │ Tickets/1000 Rides vs Month (line)  │
│  Resolution Rate: XX%      │                                     │
│  Avg Resolution: XX hrs    │                                     │
├────────────────────────────┴─────────────────────────────────────┤
│ Ticket Categories (bar)    │ Resolution Rate by Category (bar)   │
├────────────────────────────┴─────────────────────────────────────┤
│ Resolution Time Heatmap (Category × Severity)                    │
├──────────────────────────────────────────────────────────────────┤
│ Tickets per 1,000 Rides by City                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## DESIGN SYSTEM (apply consistently across all 5 pages)

### Typography

| Element | Font | Size | Style |
|---------|------|------|-------|
| Dashboard title | Tableau Medium | 18pt | Bold |
| Sheet title | Tableau Book | 13pt | Regular, dark |
| Axis labels | Tableau Book | 10pt | Regular |
| Data labels | Tableau Bold | 11pt | Bold |
| Annotations | Tableau Italic | 10pt | Gray |
| KPI numbers | Tableau Bold | 28–32pt | Bold |
| KPI labels | Tableau Book | 10pt | Regular, muted |

### Color Rules (apply everywhere)

| Situation | Color | Hex |
|-----------|-------|-----|
| Problem / alert / bad metric | Red | `#DC2626` |
| Caution / approaching threshold | Amber | `#F59E0B` |
| Good / healthy / above benchmark | Green | `#059669` |
| Primary / neutral data | Blue | `#2563EB` |
| Secondary / context data | Teal | `#0891B2` |
| Muted / benchmark line | Gray | `#94A3B8` |
| Suspended/inactive reference | Slate | `#64748B` |

### Consistent Global Filters (appear on ALL pages)

Create these as global filters using **Apply to All Using Related Data Sources:**

1. **Date Range** — MONTH([Request Time]) — show as "Range of Dates" slider
2. **City** — [City] — show as checkboxes (all selected by default)
3. **Ride Type (Vehicle)** — [Vehicle Type] — show as checkboxes
4. **Payment Method** — [Payment Method] — optional, collapsible

### Dashboard Actions (interactivity)

Create these **Dashboard Actions** on Page 1:

**Action 1: City Drill-Down**
- Source: Sheet 1B (City Performance Bar)
- Target: Pages 2, 4 — filter [City] to selected city
- Label: "Click a city to drill into its operations"

**Action 2: Highlight Problem Drivers**
- Source: Sheet 4A (% Rides >15min by tier)
- Target: Sheet 4B — highlight matching tier
- Type: Highlight

**Action 3: Zone Detail**
- Source: Sheet 4D (Northgate Zones)
- Target: Filter the heatmap on Page 2 to that zone

---

## TOOLTIPS — COPY-PASTE TEMPLATES

### For city charts:
```
<City>
Completion Rate: <Completion Rate>
Network Avg: 81.4%
Gap: <Completion Rate minus 81.4%>
Avg Wait: <Avg Wait Minutes> min
Driver Cancel Rate: <Driver Cancel Rate>
Active Drivers: <Count of Drivers>
```

### For driver tier charts:
```
<Driver Tier>
Drivers in this tier: <Count>
Avg Cancellation Rate: <Avg Cancel Rate>
Avg Acceptance Rate: <Avg Accept Rate>
% Rides Over 15 min: <Over 15 pct>
```

### For wait bracket charts:
```
<Wait Bracket>
Rides: <Count>
Completion Rate: <Completion Rate>
Driver Cancel Rate: <Driver Cancel Rate>
User Cancel Rate: <User Cancel Rate>
Gap vs 0-5 min bracket: <diff>
```

---

## FINAL CHECKLIST BEFORE PUBLISHING

- [ ] COUNTD([Ride ID]) = 120,000 on every sheet using rides data
- [ ] Completion rate on overview = 81.6%
- [ ] Revenue total = $3,583,768 (or $3.58M)
- [ ] All 5 chart data arrays match problem_statement_2.md numbers exactly
- [ ] No pie charts
- [ ] No 3D effects
- [ ] Every chart title states the insight, not just the metric name
- [ ] All global filters work across pages
- [ ] City drill-down action works from Page 1 → Page 2/4
- [ ] Tooltips include benchmark comparisons, not just raw values
- [ ] Published to Tableau Public — test in incognito before submitting link

---

## THE VISUAL TRAIL — HOW DASHBOARD CONNECTS TO PROBLEM STATEMENT

| Problem | Page | Chart | Key Number |
|---------|------|-------|------------|
| P1 Churned users = 80.1% of revenue | P1, P3 | Revenue bar, churn by first-ride | $2.87M vs $713K |
| P2 15-min wait cliff | P2 | Dual-axis wait cliff | 86.2% → 54.1% |
| P3 741 both-issues drivers | P2, P4 | % rides >15min by tier, cancel bar | 43.0% vs 2.8% |
| P4 Northgate Z04/Z05 | P4 | Zone bullet chart | 23 min wait, 65.5% completion |
| P5 Promos don't work for new users | P3 | Promo churn matrix | 82.7% vs 82.7% (zero gap) |

---

## QUICK WINS FOR A STRONGER INTERVIEW

1. **On Page 1**, add a text annotation: *"We analyzed 120,000 rides across 12 cities. The headline finding: ride volume is completely flat across 12 months, despite continuous promo and product activity. The root cause is not acquisition — it's that the people who tried the platform didn't come back."*

2. **On Page 2**, annotate the cliff chart: *"9,132 rides cross the 15-min threshold — that's 7.6% of all rides. After that threshold, completion rate drops 32 percentage points."*

3. **On Page 4**, add a callout box: *"The suspension logic appears inverted: 534 suspended drivers cancel at 13.5%, while 588 active both-issues drivers cancel at 42.2% — more than 3× higher."*

4. **On Page 3**, add: *"Promos cost money but don't move retention for new users. The data shows zero difference in churn rate between users who used many promos and those who used none — for users with 1–10 rides."*
