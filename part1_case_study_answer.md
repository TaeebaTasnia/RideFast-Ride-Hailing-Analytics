# Charting the Competitive Edge: BI Strategy Framework for Intercity Market Dominance
### A Research-Backed Case Study Response — Bangladesh Context

---

> **Evidence Legend used throughout this document:**
> - **[Case Fact]** — stated directly in the case
> - **[Research]** — supported by external sourced evidence (source cited)
> - **[Inference]** — logical conclusion from case facts + research
> - **[Hypothesis]** — a testable claim, not yet established as fact
> - **[Assumption]** — stated assumption where data is unavailable

---

## Executive Summary

The company is the largest promotional spender in Bangladesh's intercity ride-hailing market yet holds only 20% market share **[Case Fact]**. The instinctive response — spend more, discount deeper — will not fix this. The evidence points to a more structural problem.

**The central diagnosis:** The company is optimizing for ride requests while losing on the dimensions that actually drive intercity demand in Bangladesh: **booking certainty, trust, and timing alignment with how Bangladeshis actually plan intercity travel.**

Three things are likely happening simultaneously:

1. **Promotions are not creating incremental demand** — they are subsidizing rides that would have happened anyway, because no holdout/control group exists to measure true uplift. This is not a hypothesis — it is an analytical gap that makes all current spend unjustifiable.

2. **RFM segmentation is structurally wrong for intercity travel.** Intercity rides in Bangladesh are occasion-driven (Eid, semester breaks, medical visits) — not habitual. RFM rewards frequency and recency. Applied to intercity, it mislabels loyal seasonal travelers as "inactive" and floods them with re-engagement promos they don't need, while missing genuinely high-propensity new travelers entirely.

3. **Competitors have differentiated on dimensions this company has not addressed.** Uber Bangladesh captures planned travelers with 90-day advance booking and confirmed drivers **[Research: Uber Bangladesh official blog]**. InDrive captures price-sensitive travelers through fare negotiation, matching Bangladeshi consumers' deep preference for price agency **[Research: TBS News, InDrive model analysis]**. This company is competing on discounts alone in a market where the other 80% is won by certainty and fairness — not just cheapness.

The path forward is not more spend. It is: measure what is actually working, fix the first-ride experience, align with how Bangladeshis plan intercity travel, and build route-level supply depth on the 5–8 routes that matter most.

---

## Real-World Bangladesh Market Context

Before diagnosing the case, it helps to understand the competitive and travel landscape.

### Competitor Snapshot

| Company | Intercity Model | Key Strength | Key Weakness |
|---------|----------------|-------------|-------------|
| **Uber Bangladesh** | Fixed-fare, cash only; advance booking up to 90 days; round trips up to 5 days **[Research]** | Booking certainty — driver confirmed at booking; available Dhaka + Chittagong | Limited to 2 cities; cash-only payment; premium positioning |
| **InDrive** | Rider proposes fare; driver accepts, rejects, or counters **[Research]** | Perceived fairness — Bangladeshis negotiate; no algorithm setting the price | Long confirmation times; not BRTA-registered as of 2023; fewer drivers; no phone customer care |
| **Pathao Car Rental** (launched Aug 2024) | Bidding system + scheduled booking; starting BDT 999 **[Research: Pathao official blog, TBS News]** | Brand trust from existing app; nationwide availability | Product is new; trust in intercity-specific service still being built |
| **Shohoz** | Bus/train/flight ticket aggregator; also offers ride-hailing **[Research]** | Strong in cross-modal intercity booking; ticketing trust | Not a direct car ride-hailing competitor |

**Key market facts:**
- Bangladesh ride-hailing market: **US$92.64M revenue in 2024**, growing at **10.66% annually** to reach US$153.7M by 2029 **[Research: Statista Market Forecast]**
- **12–15 million people leave Dhaka** in the 3–4 days before Eid-ul-Fitr and Eid-ul-Azha — the single largest demand surge in Bangladesh transport **[Research: Bangladesh University of Engineering and Technology / Tribune India]**
- Train preferred for comfort but severely capacity-constrained (43 intercity trains, ~33,315 seats total during Eid) **[Research: Bangladesh Railway data]**
- **94 identified highway congestion spots** create safety anxiety for intercity road travel **[Research: Prothomalo / Highway Police]**
- Only **Pathao and Uber** have renewed BRTA ride-sharing licences; 13 other companies have not **[Research: Dhaka Tribune / BRTA data]**

### Why Bangladesh intercity is different from intracity

| Dimension | Intracity (Dhaka) | Intercity (Dhaka → Chittagong etc.) |
|-----------|-------------------|--------------------------------------|
| Decision timing | Spontaneous (minutes before) | Planned (days to weeks ahead) |
| Price sensitivity | Moderate | High — but certainty matters more than lowest price |
| Comparison alternatives | Other ride apps | Bus (BDT 400–700), train (BDT 200–500 AC), private car |
| Key anxiety | ETA accuracy | "Will the driver actually show up? Will they cancel?" |
| Trip frequency per user | Multiple per week | 2–8 times per year |
| Occasion driver | None — daily mobility | Eid, semester breaks, medical, business, tourism |
| Trust required | Low — short trip | High — committing to a 3–5 hour journey |

---

## Section 1 — Diagnose the Problem

### 1.1 Problem Tree

The headline problem is: **low intercity ride requests despite maximum promotional spending.** Below is a structured breakdown of where demand could be leaking.

```
LOW INTERCITY RIDE REQUESTS
│
├── A. MARKET PROBLEM
│       Is the addressable market smaller than assumed?
│       [Hypothesis] Most Bangladeshi intercity travelers default to buses/trains
│       and don't consider app-based car rides at all — not because of price,
│       but because car rides feel like a "luxury" category.
│
├── B. AWARENESS PROBLEM
│       Do users know intercity rides exist on this app?
│       [Hypothesis] Intercity may be buried in the app UI — users open the app
│       for food or intracity, never discover the intercity option.
│
├── C. CONSIDERATION PROBLEM
│       Do users consider this app when planning an intercity trip?
│       [Inference] Users plan intercity trips differently — they go to bus counters,
│       call contacts, or check Shohoz/train schedules. App-based car ride is not
│       in the mental shortlist.
│
├── D. CONVERSION PROBLEM
│       Do users who search actually request?
│       [Case Fact + Inference] Case states fares are cheaper than competitors
│       after discounts. If price is not the issue, conversion drop-off may be
│       about route availability, ETA uncertainty, or driver reliability fears.
│
├── E. TRUST PROBLEM ← LIKELY HIGH IMPACT
│       Are users worried about cancellations, safety, or driver quality?
│       [Research: Dhaka Tribune] Driver cancellations are a documented pain point
│       in Bangladesh ride-hailing. For a 5-hour intercity trip, a cancellation
│       is catastrophic. This anxiety suppresses requests even among interested users.
│
├── F. PRODUCT PROBLEM ← LIKELY HIGH IMPACT
│       Is the booking experience built for spontaneous intracity rides,
│       not planned intercity travel?
│       [Inference] If users cannot book 24–72 hours in advance with a confirmed
│       driver, the product does not match how intercity travel is planned.
│       Uber Bangladesh already offers 90-day advance booking [Research].
│
├── G. PRICING / VALUE PROBLEM
│       Is the fare cheap but the total value proposition weak?
│       [Inference] A cheaper fare doesn't compensate for uncertainty. Buses are
│       also cheap. The customer is comparing not just fare but the entire journey
│       experience including reliability, comfort, and booking certainty.
│
├── H. ROUTE / NETWORK PROBLEM
│       Is supply thin on the routes users actually want?
│       [Case Fact] Supply scales with demand. BUT this creates a chicken-and-egg
│       problem: low supply → poor experience → low demand → low supply.
│       On new or lower-frequency routes, this loop traps the platform.
│
├── I. TIMING PROBLEM ← LIKELY HIGH IMPACT
│       Are promotions reaching users at the wrong moment?
│       [Hypothesis] An in-app push notification for intercity discounts reaches
│       a user when they are ordering food in Dhaka — not when they are planning
│       next week's trip to Sylhet. The promotional moment and the travel decision
│       moment are separated by days or weeks.
│
├── J. RETENTION PROBLEM ← LIKELY HIGH IMPACT
│       Are first-time intercity users coming back?
│       [Hypothesis] If repeat ride rate within 60 days is below 25%, the platform
│       is on a treadmill: constant acquisition spend just replaces churned users.
│
├── K. POSITIONING PROBLEM ← CONFIRMED LIKELY
│       Is intercity being sold as "a discounted longer ride"?
│       [Inference] The three-discount cycle, zonal discounts, and cross-sell from
│       food/intracity all treat intercity as an extension of the same product.
│       But Bangladeshi travelers perceive intercity as a different travel decision —
│       one that requires certainty, advance planning, and higher trust.
│
├── L. CANNIBALIZATION PROBLEM
│       Are promotions shifting existing behavior rather than creating new demand?
│       [Hypothesis] A user who would have booked at full price uses a 25% discount
│       instead. Ride count stays the same; margin drops. No holdout group = this
│       cannot currently be measured. [Case Fact: no holdout mentioned]
│
└── M. MEASUREMENT PROBLEM ← CONFIRMED
        Is the company optimizing the wrong metric?
        [Inference] "Ride requests" is a lagging, gross metric. It cannot distinguish
        new intercity customers from repeat riders from subsidized existing users.
        Without incrementality measurement, all current spend decisions are made blind.
```

---

### 1.2 Hypotheses — Ranked and Explained

Below are 18 hypotheses, ordered from highest to lowest estimated business impact. Each includes the mechanism, what data would test it, and how fast it can be validated.

| # | Hypothesis | Mechanism | Business Impact | Ease of Testing | Data Needed |
|---|-----------|-----------|:-:|:-:|---------|
| H1 | **RFM is mislabeling loyal intercity users as inactive** | Intercity trips happen 2–6x/year. RFM penalizes low frequency. A user who traveled Dhaka→Chittagong 3x this year looks "dormant" and gets re-engagement promos while already being loyal. Budget wastes on the already-convinced. | Very High | Easy | User ride history split by vertical |
| H2 | **Promotions are reaching existing riders, not net-new intercity demand** | Promo codes redeem across all users. Without targeting by "no prior intercity ride," the 3-discount cycle is subsidizing repeat users, not acquiring new ones. | Very High | Easy (split by user type) | Promo redemption table joined to ride history |
| H3 | **No holdout group exists — so true promo lift is unknown** | [Case Fact] The company is the biggest promo spender with 20% share. Without a holdout, there's no way to know if any spend is working. The entire strategy rests on an unmeasured assumption. | Very High | Medium (requires experiment design) | A/B test design + execution |
| H4 | **The product doesn't support advance booking — missing the planning window** | Bangladeshis planning an Eid trip book buses/trains weeks ahead. If the app only offers on-demand dispatch, it misses the entire planned-travel segment. Uber already offers 90-day advance booking [Research]. | High | Medium | Product capability audit + user intent surveys |
| H5 | **First-intercity-ride experience is poor, killing repeat intent** | Cancellations, long waits, or unfamiliar drivers on a 4-hour trip destroy trust permanently. First impression on intercity is far more consequential than on intracity. | High | Easy (segment first rides in data) | Ride completion rate, wait time, rating — filtered to "first intercity ride" per user |
| H6 | **Promotions reach users at the wrong moment in their travel decision** | An intercity promo push while a user is browsing food in Dhaka is useless. The relevant moment is when they're planning a trip — typically 2–14 days before travel. Current comms are activity-triggered, not intent-triggered. | High | Medium | Travel timing analysis vs. promo send timing |
| H7 | **Cross-sell from food/intracity reaches a huge audience with low intercity propensity** | Most food delivery users are urban Dhaka residents with immediate food needs. Their intercity propensity is not zero — but it's low and un-segmented. Sending intercity promos to all cross-sell users burns budget. | High | Easy | Cross-sell cohort → intercity ride conversion rate |
| H8 | **InDrive's bidding model is attracting price-negotiating Bangladeshi travelers** | Bangladeshis negotiate prices everywhere — from bazaars to CNG fares. InDrive gives users price agency [Research: TBS News]. A flat algorithmic fare — even cheaper — can feel less satisfying than a fare the user "won." | Medium-High | Medium (competitive research + user interviews) | Market share data, user survey on fare perception |
| H9 | **Eid demand is a massive untapped window that the company is not positioned for** | 12–15 million people need to travel in 72 hours [Research: BUET]. Trains are sold out months ahead. Buses are overcrowded. A company with guaranteed drivers on key routes 2 weeks before Eid could capture enormous demand. | High | Medium | Ride volume data during Eid vs. non-Eid periods |
| H10 | **Screen time targeting does not predict intercity intent** | A user with high app screen time is likely a frequent food orderer or intracity rider — not an intercity traveler. Using engagement as an intercity intent signal mixes two completely different user behaviors. | Medium | Easy | Correlation between screen time and intercity ride conversion |
| H11 | **Route supply is thin during non-Eid periods, creating long waits that suppress repeat usage** | On a Dhaka–Sylhet route on a Tuesday, driver supply may be very low. Users who wait 45+ minutes or get cancelled on decide not to try again. This suppresses route-level repeat even if aggregate supply looks healthy. | Medium | Medium | Route-level supply density × wait time × repeat booking |
| H12 | **Zonal discounts are a poor fit for intercity travel** | Zones are intracity constructs (neighborhoods, business districts). Intercity travel is defined by origin-destination pairs (Dhaka to Sylhet), not zones. A Gulshan zone discount does nothing for a user planning Dhaka→Chittagong. | Medium | Easy | Zone discount redemption → intercity ride rate |
| H13 | **Intercity has strong seasonality but current promotions are flat — not seasonal** | If intercity demand spikes 4–5x during Eid and semester breaks, flat monthly promotions are misaligned. Budget is spent equally across high-opportunity and low-opportunity periods. | Medium | Easy | Monthly ride volume trend analysis |
| H14 | **The company is competing against the total journey cost, not just other ride fares** | A user comparing a BDT 1,800 intercity car ride (post-discount) against a BDT 500 AC bus + rickshaw combo is doing a full journey comparison. Cheaper fare alone doesn't win this comparison — convenience, door-to-door value does. | Medium | Hard (requires competitive customer research) | User survey on booking decision factors |
| H15 | **B2B / corporate intercity travel is completely untapped** | Dhaka hosts a large number of development organizations, NGOs, corporate offices, and government agencies with regular intercity travel needs. These travelers are expense-reimbursed (price-insensitive) and travel frequently. | Medium | Medium | CRM analysis for patterns suggesting business travel |
| H16 | **Student corridor routes (university towns) are high-frequency but un-targeted** | BUET, CUET (Chittagong), SUST (Sylhet), RUET (Rajshahi) students travel home and back at semester starts/ends. This is a predictable, recurring, group-influenceable demand pattern. | Medium | Easy | Route analysis for university-city routes at semester change dates |
| H17 | **The 3-discount cycle trains users to only book with discounts, never at full price** | Sequential discounts create price anchoring — users learn the "real" fare is 25% lower and refuse to pay more. Long-term, this destroys contribution margin even as ride volume grows. | Medium | Medium | Post-promo-cycle full-price conversion rate |
| H18 | **Medical travel is a high-trust, price-inelastic segment that is being ignored** | Patients traveling to CMCH (Chittagong), SZMCH (Sylhet), or Dhaka hospitals from smaller cities need reliable, comfortable transport. They cannot risk cancellations. They will pay for certainty. | Low-Medium | Easy (route + timing analysis) | Route/timing overlap with major hospital locations |

---

### 1.3 The Intercity User Funnel — Bangladesh Specific

The standard funnel doesn't fit intercity travel. Below is a Bangladesh-specific funnel that maps where demand is created and where it leaks.

```
STAGE 1: TRAVEL NEED ARISES
  → Eid approaching / semester ending / family emergency / business meeting
  → Metric: Not directly measurable; estimated from seasonal patterns
  → Leakage: Company has no presence in the traveler's mind at this stage

STAGE 2: TRANSPORTATION MODE CONSIDERATION
  → User thinks: Bus? Train? Private car? Ride app?
  → Metric: Share of consideration (survey-based; compare to bus search data)
  → Leakage: Ride-hailing not in top-of-mind for intercity trips for most users
  → Cause: Product positioned as intracity convenience, not intercity travel
  → Intervention: Content, search ads, and Shohoz-like integrations at planning stage

STAGE 3: APP OPEN + INTERCITY DISCOVERY
  → User opens app; can they find the intercity product within 2 taps?
  → Metric: % of app opens that lead to intercity tab view
  → Leakage: Intercity buried under intracity / food options
  → Intervention: Contextual entry points (near Eid, surface intercity prominently)

STAGE 4: ROUTE SEARCH + AVAILABILITY CHECK
  → User searches Dhaka → Chittagong, checks if drivers available
  → Metric: Intercity route searches per week; % of routes showing available drivers
  → Leakage: Low driver supply on many routes → "no drivers available" → user exits
  → Cause: Demand–supply cold start problem on newer/smaller routes

STAGE 5: FARE CHECK + COMPARISON
  → User sees fare; mentally compares to bus (BDT 500–700) or train (BDT 200–500)
  → Metric: Fare view → request conversion rate
  → Leakage: Even a competitive fare loses if the comparison is total journey cost
  → Note: Case states fares are lower than competitors post-discount [Case Fact]
  → Remaining question: Are users comparing to other ride apps, or to buses?

STAGE 6: BOOKING INTENT + REQUEST
  → User tries to book; can they book 24 hours in advance?
  → Metric: Request rate among users who viewed fare
  → Leakage: If advance booking isn't available, on-demand only = planning mismatch
  → Key: A user planning Eid travel cannot use an app that only dispatches on demand

STAGE 7: DRIVER MATCH + ACCEPTANCE
  → Request sent; driver accepts within acceptable time
  → Metric: Request → acceptance rate; time to acceptance
  → Leakage: Low supply → no driver accepts → user cancels → bad impression
  → Cause: Supply–demand imbalance on specific routes and times

STAGE 8: RIDE COMPLETION
  → Driver arrives, picks up, completes 3–5 hour journey
  → Metric: Completion rate; first-intercity-ride completion rate specifically
  → Leakage: Driver cancels en route; or user cancels after long wait
  → This is the single most trust-critical moment in the entire funnel

STAGE 9: POST-TRIP → REPEAT INTENT
  → User rates the trip; did they have a good enough experience to consider booking again?
  → Metric: First-trip rating distribution; repeat booking within 60 days
  → Leakage: Poor first experience → no second trip, regardless of promos
  → [Hypothesis H5] This is likely where most of the demand permanently leaks

STAGE 10: REPEAT BOOKING
  → User books intercity again (next trip occasion)
  → Metric: 60-day repeat rate; trips per intercity user per year
  → Key insight: In Bangladesh, "repeat" may be 2–3 months later (next holiday/occasion)
  → Standard 30-day cohort analysis misses this — 60–90 day window needed

STAGE 11: WORD-OF-MOUTH / REFERRAL
  → User recommends to family/friends traveling same route
  → Metric: Referral rate among completed-intercity-trip users
  → Opportunity: Intercity travel is often a group/family decision in Bangladesh
```

---

### 1.4 Promotion Diagnosis

**The core problem: Redemption ≠ Incrementality**

The company is the biggest promotional spender in the market **[Case Fact]** but has 20% market share. This is the clearest signal that promotions are not creating proportional incremental demand.

Three diagnostic questions:

**Q1: What share of promo redemptions come from users who were already going to travel?**

Without a holdout group, this cannot be answered. This is not a measurement gap — it is a strategic gap. Every budget decision made today is based on an assumption that has never been tested.

| User classification at promo redemption | Estimated share | Business meaning |
|-----------------------------------------|:-:|-----------------|
| First intercity ride ever (net new) | [Unknown — must measure] | True incremental |
| Cross-vertical user, first intercity | [Unknown — must measure] | Partially incremental |
| Repeat intercity user who would have ridden anyway | [Unknown — must measure] | Pure subsidy — zero incremental value |

**Q2: Does the 3-discount promo cycle produce retention, or just 3 rides?**

If users who received 3 discounts ride 3 times and then stop — the promo bought 3 rides at 25% margin loss and produced no retention. The question is whether the discount-acquired user becomes a full-price repeat rider. If the post-promo full-price conversion rate is near zero, the program is manufacturing usage at the cost of training users to be discount-dependent.

**Q3: Are zonal discounts aligned with how intercity travel actually works?**

Zonal discounts make sense for intracity trips (e.g., Gulshan → Banani is a short hop within a zone). For intercity travel, the relevant unit is an **origin-destination pair** (Dhaka → Chittagong), not a geographic zone. A business hotspot discount in Motijheel does nothing for someone planning a trip to Sylhet next weekend.

---

### 1.5 Targeting Diagnosis

#### RFM — Wrong Tool for the Wrong Category

Pathao's Food vertical uses a 28-segment RFM × recency matrix, and it works well there **[Research: Pathao RFM case, Zenodo]**. Here's why that success does not transfer to intercity:

| Dimension | Food (RFM works) | Intercity (RFM fails) |
|-----------|------------------|-----------------------|
| Purchase frequency | 5–30 times/month | 2–8 times/year |
| Recency signal | Someone inactive for 2 weeks has likely churned | Someone inactive for 2 months may be your most loyal Eid traveler |
| Trigger | Hunger is daily and habitual | Travel is occasion-driven — no amount of nudging creates a trip |
| Monetary value | Predictable weekly spend | Lumpy — high when traveling, zero between trips |
| Segmentation logic | Recency + frequency = healthy proxy for engagement | Recency + frequency = irrelevant for infrequent but loyal travelers |

An intercity user who took 4 trips in the past 12 months — spending BDT 6,000 each time — is a high-value, loyal customer. But their RFM score says: inactive (last trip 3 months ago), low frequency (4 rides total), medium monetary. They get re-engagement messaging they don't need, while users with zero intercity intent get the same treatment.

**The right segmentation for intercity is: Travel Occasion × Propensity × Route**

Not: Recency × Frequency × Monetary.

#### Screen Time Targeting

High app screen time in a ride-hailing super-app means the user is active in food delivery, parcel, or intracity rides — not that they intend to travel intercity. Using aggregate screen time as an intercity intent proxy mixes signals from unrelated verticals. A heavy Pathao Food user opening the app 12 times a day to track deliveries has near-zero intercity signal. They are not a better intercity prospect than a user who opens the app twice a week but searches Dhaka→Sylhet routes.

---

## Section 2 — Key Metrics

### Level 1 — Business Outcomes

| Metric | Formula | Why It Matters | Key Segmentation | Decision Enabled | Pitfall |
|--------|---------|---------------|-----------------|------------------|---------|
| **Incremental intercity trips** | Trips in treatment group − trips in matched control group | This is the only metric that tells us if promotions are working | By promo type, user segment, route | Increase/reduce promo spend | Gross trip count hides whether growth is new demand or subsidized existing demand |
| **Intercity market share** | Platform intercity trips ÷ estimated total intercity car rides in market | Headline competitive metric | By city, route corridor | Overall strategy direction | Lags all leading indicators; hard to measure accurately |
| **Intercity contribution margin per trip** | Fare − driver payout − discount subsidy − payment fees | Tells us if growth is profitable | By route, promo vs. organic | Price/discount strategy | High ride volume with negative contribution is not growth |
| **Intercity customer LTV** | Average trips per user per year × contribution margin per trip × estimated tenure | Shows true value of each acquired intercity user | By acquisition channel, user type | CAC investment decisions | Hard to estimate without long cohort data; use 12-month proxy |

### Level 2 — Demand Metrics

| Metric | Formula | Why It Matters | Pitfall |
|--------|---------|---------------|---------|
| **Net new intercity users (monthly)** | First intercity ride users this month − intercity users who went inactive last month | Real growth signal | Gross "new users" hides churn |
| **Intercity request rate** | Intercity requests ÷ eligible active users in the period | Measures whether the product is generating demand | "Eligible" must be defined carefully — not all app users are intercity prospects |
| **Route search → request conversion** | Ride requests ÷ route price checks | Where is demand dying after product interaction? | Low conversion may mean price, supply, or product UX — needs decomposition |
| **Intercity-eligible user activation** | Users who searched intercity at least once ÷ total users communicated to | Are we reaching the right audience at all? | High impression counts with low activation means poor targeting |

### Level 3 — Funnel Metrics

| Stage | Metric | Formula | Leakage Signal |
|-------|--------|---------|---------------|
| Awareness → Discovery | Intercity tab view rate | Intercity tab views ÷ app opens | < 15% suggests buried product placement |
| Discovery → Search | Route search rate | Route searches ÷ intercity tab views | < 40% suggests poor UX or irrelevant audience |
| Search → Request | Search-to-request conversion | Requests ÷ route searches | < 50% = price/availability/trust issue |
| Request → Match | Driver match rate | Drivers accepted ÷ requests sent | < 80% = supply problem on route |
| Match → Completion | Completion rate | Completed rides ÷ accepted rides | < 85% = cancellation/reliability issue |
| Completion → Repeat | 60-day repeat rate | Users with 2+ intercity trips within 60 days ÷ users with first intercity trip | < 25% = retention crisis |

> **Note:** For intercity in Bangladesh, use a 60-day repeat window, not 30 days. Occasions like Eid, semester breaks, and monthly medical visits naturally space trips 4–8 weeks apart. A 30-day window systematically undercounts loyalty.

### Level 4 — Customer Quality

| Metric | Formula | Why It Matters | Pitfall |
|--------|---------|---------------|---------|
| **First-to-second intercity trip conversion** | Users with 2+ intercity trips ÷ users with 1 intercity trip (60-day window) | The most predictive early retention metric | Don't mix up intracity repeats with intercity repeats |
| **Intercity trips per user per year** | Total intercity trips ÷ active intercity users in last 12 months | Reveals if users are occasional or recurring | Heavily skewed by Eid spike — compute Eid-season and off-season separately |
| **CAC by channel** | Total acquisition spend per channel ÷ new intercity users from that channel | Allows channel ROI comparison | Ensure attribution is correct — promo users often have multiple touchpoints |
| **Payback period** | CAC ÷ (contribution margin per trip × trips per month) | Tells us how long it takes to recover the cost of acquiring one user | For intercity, payback period may be 3–6 months due to low trip frequency |

### Level 5 — Promotion Economics

| Metric | Formula | Why It Matters | Pitfall |
|--------|---------|---------------|---------|
| **Incremental rides per BDT 1,000 spent** | Incremental trips (vs. holdout) ÷ total promo spend in period | Core efficiency metric for promo budget | Requires holdout group to calculate; currently not measurable |
| **Cannibalization rate** | % of promo-redeming users who had an upcoming trip planned anyway | Measures how much budget subsidizes existing demand | Can only be estimated via survey or holdout |
| **Post-promo full-price conversion** | % of promo users who book at full price within 60 days after promo expires | Tests whether discount created habit or dependency | Low rate = discount training problem |
| **Discount redemption by user type** | % of redemptions split: new / cross-sell / repeat intercity | Tells you who the promo is actually reaching | Don't aggregate — the split is the insight |

### Level 6 — Route Economics

| Metric | Formula | Why It Matters | Pitfall |
|--------|---------|---------------|---------|
| **Route-level completion rate** | Completed trips ÷ accepted trips, by route | Identifies routes where supply quality is hurting trust | Aggregate completion rate hides route-level failures |
| **Route-level repeat rate** | Users who took 2+ trips on same route ÷ users who took 1 trip | Reveals which routes build habit vs. one-time usage | Some routes (e.g., Cox's Bazar tourism) are legitimately one-way events |
| **Request density per route** | Intercity requests per route per week | Prioritize supply investment where demand already exists | Dense-looking routes in terms of tries may have low completions |
| **Fare competitiveness gap** | Platform fare − cheapest bus fare on same route | How much the user is paying for convenience over the cheapest alternative | A BDT 1,500 gap may be acceptable; BDT 4,000 may not be |

---

## Section 3 — Analytical Methodologies

### 3.1 Funnel Decomposition Analysis

**Question:** At which step in the intercity booking funnel is demand being permanently lost?

**Analysis:**
Use app event logs to build a sequential funnel:
`App open → Intercity tab → Route search → Fare view → Request submitted → Driver matched → Completed → Repeat in 60 days`

**Critical cuts:**
- By city (Dhaka vs. Chittagong vs. Sylhet — where are we weakest?)
- By route (Dhaka→Chittagong vs. Dhaka→Sylhet — which routes convert better?)
- By user type (first intercity trip vs. repeat rider)
- By acquisition source (organic vs. cross-sell vs. promo)
- By time period (Eid week vs. off-peak — are we converting differently during peaks?)

**Data needed:** App event logs, ride request table, user source attribution, timestamp data.

**Decision:** If the main leak is at Stage 2 (app open → intercity tab), the problem is product discovery. If at Stage 6 (fare view → request), it's price or trust. If at Stage 9 (completion → repeat), it's first-experience quality.

---

### 3.2 Promo Holdout Experiment — The Most Important Test

**Question:** Do promotions create incremental intercity rides, or do they just subsidize rides that would happen anyway?

**This is not optional.** The company is the biggest promotional spender with 20% share. Without this test, no budget decision is justified.

**Design:**

| Element | Detail |
|---------|--------|
| **Treatment group** | New intercity users receive the full 3-discount cycle (as today) |
| **Control group** | New intercity users receive 1 discount (or no discount) — randomly assigned at first intercity booking |
| **Randomization unit** | User-level (not route or city — to avoid supply contamination) |
| **Duration** | 90 days from first intercity booking |
| **Primary metric** | Total intercity trips completed within 90 days |
| **Guardrail metrics** | First-ride completion rate (must not fall); app uninstall rate (must not increase) |
| **Sample needed** | Aim for 1,000+ users per group for 80% power to detect a 15% difference |
| **Interpretation** | If treatment rides control by > 15%, the extra discounts are working. If < 5% difference, the 2 extra discounts are pure margin loss. |
| **Failure condition** | If first-ride completion rate falls in the discount group, the promo is attracting the wrong users (e.g., users who request but expect to cancel anyway) |

> **Anti-hallucination note:** The specific numbers above (1,000 users, 15% threshold) are illustrative guidance, not calculated results. Actual power calculations require estimated baseline trip rates.

---

### 3.3 RFM Suitability Audit

**Question:** Is the current RFM segmentation actually identifying users with intercity travel propensity, or just users who were recently active in other verticals?

**Analysis:**

Step 1 — For each RFM segment, calculate their intercity ride conversion rate over the past 6 months:

```
RFM Segment | Intercity message sent | Intercity ride within 30 days | Conversion %
Champions    |         X              |           Y                   |    Y/X
At Risk      |         X              |           Y                   |    Y/X
Lost         |         X              |           Y                   |    Y/X
```

Step 2 — For each RFM segment, calculate what vertical drove their RFM score (food, intracity, parcel). If a "Champion" segment is dominated by food-heavy users, their intercity conversion will be near zero despite their high RFM score.

Step 3 — Build a simple cross-tab: RFM score vs. prior intercity rides. If there is no correlation (high-RFM users are no more likely to have taken intercity trips than low-RFM users), RFM is not a valid proxy for intercity propensity.

**Decision:** If RFM shows < 10% correlation with prior intercity trips, stop using it for intercity targeting and replace with propensity scoring.

---

### 3.4 Cohort Retention Analysis

**Question:** Is any month's acquisition cohort retaining significantly better? If so, what was different?

**Analysis:**

Group all first-time intercity users by the month they took their first intercity trip. For each cohort:
- Month 1 rides (the onboarding month)
- Month 2 rides (first real retention test)
- Month 3 rides
- Eid-month rides (even if they signed up 6+ months ago — this tests seasonal reactivation)

Look for cohorts that outperform on Month 2 and Month 3 retention. Then investigate:
- Was there a supply improvement on a specific route that month?
- Was there a product feature launch?
- Was there a different acquisition campaign that attracted a different user type?

If no cohort shows meaningfully better retention — this confirms the platform has not yet found a retention formula. That means: stop pouring money into top-of-funnel acquisition until the product experience is fixed.

---

### 3.5 Cross-Sell Attribution Analysis

**Question:** Are cross-sell users (from food/intracity) actually converting to intercity rides? And if they convert, do they stay?

**Full funnel to track per cross-sell campaign:**

| Step | Metric | Expected benchmark |
|------|--------|--------------------|
| Campaign recipients | N users reached | — |
| Engaged (clicked/opened) | % of recipients | > 15% = good engagement |
| First intercity trip within 30 days | % of engaged users | > 8% = reasonable cross-sell conversion |
| Second intercity trip within 60 days | % of first-trip completers | > 25% = cross-sell is producing quality users |
| Full-price trip after promo expires | % of promo-converted users | > 30% = no discount dependency |

**Bangladesh-specific insight [Inference]:** Most Pathao food delivery users in Dhaka are internal migrants who have a home district to return to. Their intercity travel propensity is real — but it's tied to Eid and semester breaks, not to any particular week. Cross-sell campaigns sent without occasion-timing will reach them at the wrong moment. Cross-sell campaigns sent 10–14 days before Eid could be significantly more effective.

**Decision trigger:** If cross-sell users convert but don't retain → product problem, not targeting problem. If they don't convert at all → audience problem.

---

### 3.6 Product Feature Evaluation Framework

The case mentions "several new features" launched by the product team **[Case Fact]**. Without a measurement plan for each, it is impossible to know if any of them are contributing to ride volume.

**Framework for every feature:**

| Element | Required answer before launch | Required answer 30 days after launch |
|---------|-------------------------------|--------------------------------------|
| Primary metric | Which single number does this feature aim to move? | Did it move? By how much vs. control? |
| Guardrail metric | What must NOT get worse? | Did any guardrail worsen? |
| Randomization unit | User? Route? City? | Was contamination controlled? |
| Minimum detectable effect | What's the smallest improvement worth detecting? | Was the test powered for this? |
| Analysis cut | New vs. returning user; route type | Do results differ by segment? |

**Example for a "scheduled booking" feature:**

| Element | Value |
|---------|-------|
| Primary metric | Request-to-completion rate (scheduled vs. on-demand) |
| Guardrail | Driver cancellation rate must not increase |
| Randomization | User-level (50% see scheduled option, 50% don't) |
| Primary hypothesis | Scheduled bookings will have 15–20% higher completion rates because driver is committed in advance |
| Success condition | Scheduled ride completion ≥ 5pp higher than on-demand; repeat booking rate 10% higher in feature group |

For features already launched without a measurement plan, run a synthetic control analysis: compare cities/routes where the feature was available earliest vs. where it rolled out later. This is noisier than an RCT but better than no measurement.

---

### 3.7 Route-Level Opportunity Matrix

Not all routes deserve equal investment. The following framework classifies routes to guide supply investment and marketing focus.

| Route Category | Definition | Strategic Action |
|----------------|-----------|-----------------|
| **Core routes** | High request volume, good completion, repeat usage | Defend with supply guarantees; loyalty program activation |
| **Growth routes** | High search volume, moderate conversion, improving trend | Supply investment + targeted promo to break through cold-start |
| **Seasonal routes** | Low volume year-round but spikes 3–5x during Eid/holidays | Pre-position supply 2 weeks ahead; skip off-season spend |
| **Occasion routes** | One-direction: tourism, hospital, airport | Partner with hotels/hospitals; no loyalty needed; price for the occasion |
| **Thin routes** | Low search, low completion, no repeat | Do not invest; flag for potential drop if no improvement in 3 months |

**Bangladesh route categorization [Inference — requires validation with data]:**

| Route | Estimated Category | Key Occasion | Competitor Benchmark |
|-------|--------------------|-------------|----------------------|
| Dhaka–Chittagong | Core | Year-round business; Eid spike | Uber operates here; flat BDT 6,000 to Cox's Bazar [Research] |
| Dhaka–Sylhet | Growth/Seasonal | Eid (major exodus); NRB family visits | Train preferred; ride-hailing fills comfort gap |
| Dhaka–Cox's Bazar | Seasonal/Occasion | Tourism; peak Oct–Feb and summer | Tourism season demand; partner with resort ecosystem |
| Dhaka–Khulna | Thin/Growth | Eid; less business traffic | Mostly bus; ride-hailing still new here |
| Dhaka–Rajshahi | Thin | Eid; university (RUET) | Mostly bus; low ride-hailing penetration |
| Chittagong–Cox's Bazar | Occasion | Tourism | Uber offers flat BDT 6,000 rate [Research]; price-competitive here |

---

### 3.8 Better Targeting — What to Replace RFM With

The goal is not "better machine learning." The goal is reaching users who have a real intercity travel need in the near future.

| Approach | Problem It Solves | Data Required | Complexity | Expected Value |
|----------|-------------------|---------------|:----------:|---------------|
| **Travel-occasion calendar targeting** | Miss-timed promotions | Bangla calendar dates (Eid, Puja, university exam calendars) + send date logic | Low | High — changes nothing in the model, just the timing |
| **Route-affinity scoring** | Sending intercity promos to urban food users with no travel need | Prior intercity search events, completed trips, district of phone registration | Low-Medium | High — prunes the wrong audience cheaply |
| **Propensity model (logistic regression)** | Cross-sell audience has low intercity propensity | User demographics, prior searches, verticals used, registration address, prior trips | Medium | Medium-High — better than RFM for rare-event prediction |
| **Uplift modeling** | Promos reaching people who'd travel anyway | Requires prior holdout experiment results as training data | High | High — but only after holdout data exists |
| **Occasion-based segmentation** | Flat, non-contextual campaigns | Travel calendar + behavioral clusters | Low-Medium | High — segment by "likely Eid traveler," "medical corridor user," "student" |

**Recommendation:** Start with travel-occasion timing (zero model needed) and route-affinity pruning (simple filter). These two changes alone will improve targeting efficiency meaningfully without requiring a data science team.

---

### 3.9 Competitive Benchmarking Framework

| Dimension | Our platform | Uber Bangladesh | InDrive | What to do |
|-----------|:------------:|:---------------:|:-------:|------------|
| Advance booking | [Unknown — assess] | Up to 90 days [Research] | No — on-demand bidding | If we don't offer advance booking, build it |
| Price certainty | Fixed fare (post-discount) | Fixed fare | Negotiated — user proposes | Consider "price guarantee" for scheduled rides |
| Driver confirmation at booking | [Unknown] | Yes (advance booking) [Research] | No — after bidding | Confirm driver at booking for scheduled rides |
| Round trips / multi-day | [Unknown] | Up to 5 days [Research] | No | High-value for business travelers |
| BRTA license | Yes [Research] | Yes [Research] | Not as of 2023 [Research] | Communicate compliance as trust signal |
| Cash only vs. digital | [Unknown] | Cash only [Research] | [Unknown] | Digital payment is a differentiator if available |
| Customer support | [Unknown] | [Unknown] | No phone support [Research] | Phone/chat support for intercity is a trust builder |

---

## Section 4 — Strategic Recommendations

### 4.1 STOP / START / CONTINUE

#### STOP

| What to Stop | Why | Condition to Resume |
|-------------|-----|---------------------|
| **Spending promo budget without a holdout group** | Impossible to know if any spend generates incremental rides. The biggest spender with 20% share is the clearest signal that current spending is not efficient. | Resume after 90-day holdout experiment produces results |
| **Applying RFM for intercity targeting** | Structurally wrong for low-frequency, occasion-driven travel. Mislabels loyal users as inactive; misidentifies food users as intercity prospects. | Resume only if audit proves RFM segments predict intercity conversion at statistically significant rates |
| **Using screen time as intercity intent signal** | Screen time in a super-app reflects food/intracity activity, not intercity propensity. | Stop entirely; replace with route-affinity + occasion-calendar signals |
| **Treating intercity as "a longer intracity ride" in product and marketing** | Intercity is a different travel category requiring advance booking, confirmed drivers, and journey-level trust. | Never resume — intercity needs its own product experience |
| **Running flat monthly discount cycles without seasonal alignment** | Intercity demand spikes 4–5x during Eid and semester breaks. Flat spend across low-demand months wastes budget. | Replace with a seasonal budget calendar immediately |

#### START

| What to Start | Mechanism | Priority | Realistic Cost |
|--------------|-----------|:--------:|--------------|
| **Promo holdout experiment** | Randomly assign new intercity users to treatment (3 discounts) vs. control (1 or 0 discounts). Run 90 days. Measure incremental trips. | Immediate — Week 1 | Near zero — design cost only |
| **Occasion-calendar targeting** | Build a promotion send schedule aligned to Eid, Puja, university calendars, and national holidays. Send intercity promos 10–14 days before peak travel dates, not as always-on messages. | Week 1–2 | Near zero — scheduling change only |
| **60-day repeat rate as the primary growth KPI** | Replace "ride requests" with "first-to-second intercity trip conversion rate within 60 days" as the team's headline metric. This forces focus on retention, not just acquisition. | Week 1 | Zero cost — just redefine the metric |
| **Route-affinity filter for cross-sell campaigns** | Before sending intercity promos to food/intracity users, filter to users who have: (a) searched an intercity route, or (b) have a registration address in a major intercity origin city. | Week 2–3 | Low — SQL filter on targeting |
| **Advance booking / scheduled intercity ride** | Allow users to book 24–72 hours in advance with a confirmed driver. This is the single product gap most likely to explain why planned travelers use Uber (which has 90-day advance booking) instead. | Month 1–2 | Medium — product development needed |
| **First-intercity-ride experience guarantee** | For any user's first intercity ride: if the driver cancels or doesn't arrive within 20 minutes of scheduled pickup, issue a service credit automatically. Cost is low; trust impact is high. | Month 1 | Low — some service credit cost |
| **Eid supply pre-commitment program** | 3–4 weeks before Eid, recruit intercity drivers specifically with a guaranteed incentive (e.g., minimum earnings guarantee per day). Build a supply buffer before demand spikes. Communicate "Eid Guaranteed Rides" to users. | 6 weeks before each Eid | Medium — incentive budget required |

#### CONTINUE (Conditionally)

| What to Continue | Condition |
|-----------------|-----------|
| **Cross-selling from other verticals** | Continue, but only after adding attribution tracking and filtering to occasion-calendar timing. If post-measurement cross-sell shows < 5% intercity conversion, scale down. |
| **RFM for food/intracity reactivation** | RFM works for high-frequency verticals. Continue there. Do not extend to intercity. |
| **Product feature development** | Continue, but require a measurement plan (primary metric + guardrail + randomization unit) for every feature before launch. |
| **Competitive pricing** | Continue maintaining fare parity. However, once advance booking and driver guarantees are in place, price becomes less critical. Trust > price for high-stakes intercity trips. |

---

### 4.2 Bangladesh-Specific White Space Opportunities

These are opportunities that the current strategy does not address and that competitors have not fully captured.

#### A. Eid Guaranteed Rides Program
**Customer problem:** Trains sold out months ahead. Buses overcrowded and dangerous. Users need certainty 2–3 weeks before Eid.

**Mechanism:** Pre-launch supply commitment program where drivers register in advance for Eid intercity routes with minimum earnings guarantees. Users see "Eid Guaranteed" badge on intercity booking. Pre-booking opens 3 weeks before Eid.

**Why it works in Bangladesh:** Eid creates the highest-stakes travel in the calendar. A user who successfully gets home for Eid via your platform is a loyal customer for years. Conversely, a cancellation at 2am on Eid-eve is remembered forever.

**Economics:** Supply incentive cost is a one-time event investment. The LTV of an Eid-converted loyal user with 4–8 annual trips easily justifies a BDT 500–1,000 per-driver daily guarantee.

**Risk:** If supply commitment is made but not delivered (drivers no-show), the trust damage is catastrophic. Only launch this program when driver pre-commitment is operationally verified.

---

#### B. University Student Corridor Program
**Customer problem:** BUET, DU, NSU, CUET (Chittagong), SUST (Sylhet), RUET (Rajshahi) students all travel home at semester start/end and exam times. They travel on tight budgets but in groups — splitting a car among 3–4 students makes a car ride price-competitive with a bus.

**Mechanism:** A group-booking feature where a student can book an intercity ride and share the link for 3 additional riders on the same route. Fare splits automatically. Targeted at known university-destination routes during known exam/holiday periods.

**Why it works in Bangladesh:** University schedules are public. Exam dates and semester breaks are predictable. Group travel is culturally normal.

**Evidence:** [Hypothesis — requires validation with route data at university calendar times]

**Investment:** Low — group booking feature + targeted student campaign per semester.

---

#### C. Corporate/NGO Travel Accounts
**Customer problem:** Dhaka-based NGOs, development organizations, banks, and corporate offices send staff to field offices in Chittagong, Sylhet, Rajshahi regularly. These trips are expense-reimbursed. The traveler is not personally price-sensitive. They need a reliable, documented, invoiced service.

**Mechanism:** A B2B corporate account with centralized billing, monthly invoice, digital receipts, and priority booking. No negotiation needed — flat rate with reliability guarantee.

**Why the current strategy misses this:** Promotional discount cycles and RFM re-engagement are entirely consumer-focused. Corporate travelers are not reached by consumer promos.

**Bangladesh-specific relevance:** Bangladesh has one of the largest concentrations of development organization and NGO offices in South Asia (BRAC, Grameen, UN agencies, bilateral donor offices, etc.). Their staff travel patterns are predictable and high-frequency.

**Investment:** Medium — requires a corporate dashboard, invoicing system, and a dedicated account management function.

---

#### D. Medical Travel Corridor
**Customer problem:** Patients traveling from smaller cities to CMCH (Chittagong Medical College Hospital), SZMCH (Sylhet MAG Osmani Medical College Hospital), or Dhaka's major hospitals. Cancellations are catastrophic. These users are willing to pay for certainty.

**Mechanism:** Partner with hospitals (or simply target users in hospital vicinity at arrival times) to offer "Medical Assured Rides" — guaranteed pickup with 24-hour advance booking. Premium pricing acceptable.

**Why this is white space:** No competitor is specifically addressing medical travel as a segment. It is small in absolute volume but has very high trust elasticity (users will pay more and remain loyal if the service is reliable).

---

#### E. Tourism Ecosystem Partnerships
**Customer problem:** Tourists going to Cox's Bazar, Sundarbans area, Sylhet tea gardens, or Chittagong Hill Tracts need reliable onward transport from Dhaka or Chittagong.

**Mechanism:** Partner with 3–5 resort operators in Cox's Bazar and Sylhet to offer bundled booking (resort + intercity ride). User books the resort and gets an intercity ride offer. Driver takes them door-to-resort.

**Bangladesh relevance:** Cox's Bazar tourism has grown significantly. Uber already offers a fixed Chittagong→Cox's Bazar rate of BDT 6,000 [Research]. This is a validated route with established willingness to pay.

**Investment:** Low — commercial partnership agreements + product integration.

---

### 4.3 Investment Allocation Framework

The current strategy is: **spend more on discounts, reach more users.** The proposed transition:

```
Phase 1: Measure (Months 1–3)
  → Holdout experiment: understand true promo ROI
  → Funnel audit: find the exact leak point
  → Cohort analysis: find if any retention formula has worked
  → Cost: Analytics / BI time only

Phase 2: Fix (Months 3–6)
  → Build advance booking / scheduled ride capability
  → First-ride guarantee program
  → Occasion-calendar targeting rollout
  → Redirect promo budget from flat monthly → Eid + semester spikes
  → Cost: Product development + targeted promo budget

Phase 3: Grow (Months 6–12)
  → Corporate account program launch
  → Student corridor group booking
  → Route-level supply pre-commitment for Eid
  → Reduce blanket discount spend; increase loyalty/repeat incentives
  → Cost: Sales / partnerships + loyalty program budget

Phase 4: Defend (Months 12–24)
  → Route density leadership on top 5–8 routes
  → Data advantage from repeat users' route preferences
  → Ecosystem partnerships (tourism, medical, corporate)
  → Cost: Primarily operational and partnership management
```

---

### 4.4 Causal Logic Chain

For each major recommendation, here is the chain from intervention to competitive advantage:

**Recommendation: Run promo holdout experiment**
→ Discover true incremental lift per BDT spent
→ Reallocate budget from zero-lift promos to high-lift occasions
→ Same or lower spend produces more incremental trips
→ Improved contribution margin per trip
→ Sustainable growth rather than subsidized volume

**Recommendation: Build scheduled/advance intercity booking**
→ Planned travelers can commit 24–72 hours ahead
→ Driver is confirmed at booking → cancellation risk near zero
→ First-ride experience dramatically improves
→ Repeat booking rate rises (60-day window)
→ Each acquired user generates more lifetime trips
→ LTV increases; CAC payback period shortens
→ Route density grows organically as repeat users fill supply slots

**Recommendation: Eid Guaranteed Rides**
→ Pre-position driver supply 3 weeks before Eid
→ Users discover "Eid Guaranteed" product 2 weeks before Eid
→ First-time intercity users converted during highest-motivation travel window
→ Successful Eid trip creates strong positive memory
→ These users return at every subsequent Eid and increasingly off-season
→ Word-of-mouth among family groups amplifies without paid acquisition
→ Market share grows on the most important annual travel occasion

---

### 4.5 Red Team — What Could Make This Strategy Fail?

| Recommendation | Risk | How to Detect | Mitigation |
|---------------|------|--------------|------------|
| **Holdout experiment** | Holdout group has worse experience (fewer drivers) which biases the test | Monitor holdout group completion rate separately | Ensure holdout gets same driver pool; only vary promo, not supply |
| **Advance booking** | Drivers commit and cancel → worse trust than no commitment | Track confirmed-but-cancelled rate for scheduled rides | Introduce driver penalty for scheduled cancellations; build a driver reliability score |
| **Eid supply guarantee** | Drivers register but don't show up | Track committed vs. actual show rate | Overbook supply by 20%; release guarantee if show rate is historically low |
| **Occasion-calendar targeting** | 10-day advance promo is too early — users haven't finalized plans | A/B test send timing: 3 days vs. 7 days vs. 14 days before occasion | Let data choose the optimal window |
| **Corporate account program** | Sales cycle is long; won't show ROI in 90 days | Track pipeline separately from consumer metrics | Set a 6-month corporate pipeline target, not a 90-day revenue target |
| **Reducing promo budget** | Ride volume drops in the short term before long-term quality improvements show | Monitor weekly active intercity users alongside rides | Do not cut budget before the holdout results confirm low incremental lift |

---

## Section 5 — 90-Day Analytics Plan

### Days 1–30: Diagnostic Phase

| Activity | Question Answered | Owner | Output |
|----------|-------------------|-------|--------|
| Build full intercity funnel with drop-off rates by stage | Where is demand dying? | BI | Funnel waterfall chart by stage, segmented by city and acquisition source |
| RFM suitability audit | Are RFM segments predictive of intercity conversion? | BI | Cross-tab: RFM segment × intercity ride conversion; recommendation: keep or replace |
| Screen time vs. intercity conversion analysis | Is screen time predictive? | BI | Correlation analysis; if r < 0.2, recommend removing from targeting criteria |
| Promo redemption by user type | Is promo reaching new users or repeat riders? | BI + Growth | Split: new / cross-sell / repeat; if repeat > 40% of redemptions, propose targeting fix |
| Cohort retention analysis | Has any cohort retained better? | BI | Monthly cohort table: M1/M2/M3 rides and 60-day repeat rate; flag outlier cohorts |
| Route-level performance audit | Which routes are completing, which are failing? | BI + Operations | Route scorecard: requests, completion rate, repeat rate, wait time P90 |
| Seasonal demand analysis | When does intercity demand spike? | BI | Monthly/weekly ride volume trend vs. Bangladesh calendar events |
| Holdout experiment design and launch | — | BI + Growth | A/B test spec; randomly assign new intercity users to treatment/control starting Day 1 |

**Day 30 deliverable:** A diagnostic report identifying the top 3 leak points in the funnel, a recommendation on whether to continue or modify RFM targeting, and a confirmation that the holdout experiment is running.

---

### Days 31–60: Experiment Phase

| Activity | Question Answered | Owner | Output |
|----------|-------------------|-------|--------|
| Occasion-calendar targeting pilot | Does sending promos 10–14 days before Eid/occasions improve conversion? | Growth | Compare conversion rate of occasion-timed vs. standard promos (if next occasion falls in this window) |
| Route-affinity targeting filter | Does filtering cross-sell audience by prior intercity searches improve conversion? | Growth + BI | Route-affinity filtered campaign vs. broad cross-sell campaign: compare intercity trip conversion |
| First-ride experience audit | What % of first intercity rides have a wait time > 20 min or end in cancellation? | BI + Operations | First-ride specific quality report; flag routes and times with worst first-impression metrics |
| Advance booking product spec | Is advance booking feasible and what would the test look like? | Product + BI | Product requirements doc; user research on booking timing preferences |
| Student corridor timing test | Do intercity rides spike at semester change dates on university routes? | BI | Route volume by date: Dhaka→Chittagong around CUET exam dates; Dhaka→Sylhet around SUST |

**Day 60 deliverable:** Mid-point holdout results (30 days of data — early read). Targeting filter test results. List of product priorities ranked by funnel impact.

---

### Days 61–90: Scale Phase

| Activity | Question Answered | Owner | Output |
|----------|-------------------|-------|--------|
| Holdout experiment final read (90 days) | Is the 3-discount cycle generating incremental rides? | BI | Incremental lift report; recommendation: continue / modify / stop the promo cycle |
| Occasion-targeting rollout | Scale timing-aligned campaigns to all major occasions | Growth | Campaign calendar for next 6 months; tied to Bangladesh national holiday schedule |
| Route investment prioritization | Which routes deserve supply investment? | Operations + BI | Route opportunity matrix: prioritize by demand × completion gap × repeat potential |
| Corporate account pilot | Are there corporate leads we can convert in 30 days? | Sales/Partnerships | 5 corporate pilot accounts; track trip volume vs. baseline |
| 90-day recap and next-phase planning | What did we learn? What changes for the next quarter? | BI + Growth + Product | 90-day findings report; updated growth strategy for Q2 |

**Day 90 deliverable:** A clear answer to: "does our promo spend generate incremental demand?" + a revised targeting approach + a product roadmap item for advance booking + a route investment recommendation.

---

## Section 6 — Long-Term Strategy (12–24 Months)

### From Promotional Growth to Sustainable Demand

The company currently competes on price in a market where the other 80% is won by different dimensions. The long-term path:

```
TODAY                   → MONTH 6              → MONTH 12            → MONTH 24
─────────────────────────────────────────────────────────────────────────────────
Promo-led acquisition      Measurement-led        Reliability-led       Ecosystem-led
                           spend optimization     differentiation       advantage

Biggest promo spender,    Know true promo ROI;   Advance booking;      Route density leader
20% share                 cut waste; focus on    Eid Guaranteed;       on top 8 routes;
                          occasions              Corporate accounts;   B2B + tourism
                                                 Student corridors     partnerships;
                                                                       Data flywheel
```

### Competitive Moats — What Would Be Hard to Copy

| Moat | How It Builds | Why Competitors Can't Copy Quickly |
|------|--------------|-----------------------------------|
| **Route density on top 8 intercity routes** | Years of supply relationships and repeat riders per route | Requires time + driver loyalty — cannot be bought overnight with discounts |
| **Eid reliability brand** | If we successfully guarantee rides for 2 consecutive Eids, we own the occasion in user memory | Trust is earned over events, not purchased with coupons |
| **Corporate account relationships** | Long-term contracts with 20–50 large organizations | Sales cycles + invoicing infrastructure + account management creates switching cost |
| **Occasion-timing data** | The more occasions we convert, the better our prediction of who will travel when and on what route | Proprietary travel-intent prediction improves with each Eid, semester, and holiday served |
| **First-ride experience standard** | If we set and maintain the highest first-intercity-ride experience in Bangladesh | Standard must be operationally maintained — hard to sustain but also hard to replicate once established |

### One Caution on "Network Effects"

Intercity ride-hailing in Bangladesh does not currently have strong network effects. More riders on the platform do not directly benefit other riders (unlike a social network). What intercity does have is **route-level supply-demand concentration** — the more trips on a given route, the more drivers commit to that route, the faster matching happens, the more reliable the experience becomes, the more riders prefer that platform for that route. This is a **route-specific supply depth advantage**, not a platform-wide network effect. It is valuable — but it must be built route by route, not claimed platform-wide.

---

*All quantitative examples and assumed market share figures in this document are illustrative based on the case context and cited research. Actual numbers must be derived from internal operational data. All hypotheses are labeled as such and require testing before being treated as conclusions.*

---

## Sources Referenced

- [Uber Bangladesh Intercity — official blog](https://www.uber.com/bd/en/blog/bangladesh-intercity/)
- [Uber Intercity in Chattogram — official blog](https://www.uber.com/en-BD/blog/dhaka/intercity-chattogram/)
- [Pathao Car Rental launch — TBS News](https://www.tbsnews.net/economy/corporates/pathao-car-rental-effortless-journeys-919331)
- [Pathao Car Rental — official blog](https://pathao.com/blog/press/pathao-car-rental-for-effortless-journeys/)
- [InDrive in Bangladesh — TBS News](https://www.tbsnews.net/features/panorama/indrive-mysterious-inner-workings-new-ridesharing-app-684294)
- [Pathao Food RFM case study — Zenodo](https://zenodo.org/records/7267590)
- [Bangladesh ride-hailing market size — Statista](https://www.statista.com/outlook/mmo/shared-mobility/ride-hailing/bangladesh)
- [Eid travel demand (12–15M) — Tribune India / BUET research](https://www.tribuneindia.com/news/world/dhaka-witness-annual-mass-departure-as-eid-approaches-transport-networks-face-nationwide-pressure/)
- [Bangladesh ride-sharing at 7.5M rides/month — TBS News](https://www.tbsnews.net/economy/75m-rides-month-ridesharing-services-take-over-bangladesh-45453)
- [Driver cancellations and declining service quality — Dhaka Tribune](https://www.dhakatribune.com/bangladesh/258760/users-suffer-as-ride-hailing-services-get-worse)
- [Trust as loyalty driver in BD ride-hailing — ResearchGate](https://www.researchgate.net/publication/339091102_Security_Concerns_of_Ridesharing_Services_in_Bangladesh)
- [94 highway congestion spots — Prothomalo](https://en.prothomalo.com/amp/story/bangladesh/ocn6k98657)
- [Service quality of intercity bus/rail in Bangladesh — ResearchGate](https://www.researchgate.net/publication/353614192_Service_Quality_of_Intercity_Bus_and_Rail_Transportation_in_Bangladesh_Two_Distinctive_Population_Study)
