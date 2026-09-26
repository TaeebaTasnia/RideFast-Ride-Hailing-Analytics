# Charting the Competitive Edge: BI Strategy Framework for Intercity Market Dominance

*Case context: A leading ride-hailing company holds 20% market share in the intercity segment — despite being the highest spender on promotions among all competitors. Strategies already deployed include RFM-based user segmentation, tailored in-app communication, a three-discount new user promo cycle, zonal discounts targeting business hotspots, and cross-selling from other verticals. Supply is satisfied with current pricing; supply scales with demand. The growth bottleneck is on the demand side.*

---

## Section 1 — Diagnose the Problem

### Hypotheses for persistently low intercity ride requests

Before recommending a fix, the right question is: *where exactly is demand being lost?* The strategies in place are all reasonable, well-designed interventions — but they are all focused on bringing users to the platform. The gap between promotional spending and market share suggests the loss is happening after users are acquired, not before.

Five hypotheses are worth investigating:

| # | Hypothesis | What this would look like in data | How to test |
|:--|:-----------|:---------------------------------|:------------|
| H1 | **Awareness is low among potential intercity travelers** | Few searches or app opens from non-users before a planned intercity trip | App search data, impression-to-install funnel, user survey on booking intent |
| H2 | **Users try the product once but don't return** | High first-ride completion but very low second-ride rate within 30 days | Cohort analysis on new users: did they ride again? |
| H3 | **The first ride experience fails a meaningful share of users** | High cancellation rates, long wait times, or low ratings on first intercity rides specifically | Segment all rides by "user's first intercity ride" and compare completion rate against repeat riders |
| H4 | **Promotions are reaching existing users, not new intercity demand** | Promo codes being redeemed by users who already ride intercity — not net-new converts | Split promo redemptions by user tenure and prior intercity ride history |
| H5 | **Cross-sell users from other verticals don't convert to intercity behavior** | Cross-sell campaign clicks without follow-through to booking; or booking but no repeat | Funnel from cross-sell touchpoint to first intercity ride to second intercity ride |

**The most likely root cause cluster:** Based on the information available, H2 and H3 are most concerning. When 20% market share persists despite maximum promotional spend, it typically signals that users are trying the product and not being retained — not that users are unaware of it. H4 is also high-probability: promotions that reach existing users look like success but produce no incremental rides.

---

### Are current promotions reaching the right users?

To evaluate whether the existing promo strategy is working, three questions need data:

**Question 1: What share of promo redemptions come from new intercity users?**

Assume we have data on each promo code redemption tied to a user ID. We can classify each redemption as:
- New user (first ride ever on platform)
- Existing user (first intercity ride, but used platform for other verticals before)
- Repeat intercity user (has taken intercity rides before)

If the majority of redemptions fall into the third category, the promo is subsidizing demand that already exists — not creating new demand.

| Assumed redemption split (hypothetical) | Share |
|:----------------------------------------|------:|
| Brand new users (first ride of any kind) | ~18% |
| Existing cross-vertical users (first intercity) | ~27% |
| Repeat intercity users | ~55% |

If this is what the data shows, over half the promo budget is going to users who would have ridden intercity anyway. That is a significant misallocation.

**Question 2: Do promo users retain better than non-promo users?**

The promo–retention link is the critical test. Assume we track 30-day intercity repeat ride rate for promo users vs. non-promo users:

| User group | % who take a second intercity ride within 30 days |
|:-----------|--------------------------------------------------:|
| Received 3-discount promo cycle | ~23% |
| Received no promo (organic) | ~21% |

If the gap is this small, the promo cycle is not changing behavior. The 2pp difference could easily be explained by the promo attracting users who were planning to travel anyway.

**Question 3: Are zonal discounts creating new trip demand or shifting existing trips?**

Zonal discounts at business hotspots may be capturing demand that was going to happen regardless — at a lower fare. To know if the discount is incremental, a holdout group is needed: some zones get the discount, similar zones in similar cities do not. Compare ride volume, not just completions.

Without a holdout, the current data cannot answer whether any promo is working at all. This is the single most important gap in the current analytical setup.

---

### Where does the user funnel break?

The intercity user funnel has several steps. Each step is a potential exit point:

```
Awareness
   ↓
App Open / Search for intercity
   ↓
Price check / Route search
   ↓
Ride request
   ↓
Driver assigned & ride completes
   ↓
Return booking (within 30 days)
```

**Where to look:**

**Step 1 → Step 2 (Awareness to app open):** If users are aware of the platform but not searching for intercity options, the product presentation may be the issue — intercity may be hard to find or not prominently positioned in the app.

**Step 3 → Step 4 (Price check to request):** If search-to-request conversion is low, pricing or route availability may be deterring bookings. However, the case states that after discounts, user-facing fares are lower than competitors — so this step is probably not the primary bottleneck.

**Step 4 → Step 5 (Request to completion):** If rides are being requested but not completing — due to driver cancellations, long waits, or user drop-off during wait — this is a product experience failure, not a marketing failure.

**Step 5 → Step 6 (Completion to return):** This is the most critical gap for growth. A user who completes one intercity ride but never books again is the definition of acquisition without retention. If this rate is below 25%, the platform is on a treadmill: new users in, churned users out, volume stays flat.

Assume the following funnel estimates from internal data:

| Funnel stage | Assumed conversion | Implication |
|:-------------|:------------------:|:-----------|
| Awareness → app open | 40% | Reasonable; brand is known |
| App open → intercity search | 22% | Below average — intercity may be hard to find |
| Intercity search → ride request | 58% | Moderate — price is competitive |
| Ride request → completion | 81% | Good overall, but masking a long-wait tail |
| Ride completion → repeat in 30 days | **19%** | **Critical failure point** |

If the repeat booking rate is genuinely around 19%, the platform is losing 4 out of 5 users after their first intercity trip. No promotional campaign can compensate for a 19% repeat rate.

---

## Section 2 — Key Metrics to Monitor

### Intercity-specific demand metrics

| Metric | Definition | Why it matters |
|:-------|:-----------|:--------------|
| **Intercity repeat ride rate (30-day)** | % of users who complete a second intercity ride within 30 days of their first | The single most important metric. If this is below 25%, acquisition is irrelevant. |
| **Intercity request rate** | Intercity ride requests per active user per month | Measures whether the product is generating habit, not just one-time usage |
| **Intercity funnel drop-off by stage** | Conversion at each step from app open to completed ride | Identifies exactly where demand is lost before it becomes revenue |
| **Cross-sell intercity conversion rate** | % of cross-sell campaign recipients who complete an intercity ride | Measures whether the cross-sell strategy is actually generating intercity demand |
| **Net new intercity users** | New users who completed their first intercity ride this month minus intercity users who went inactive | The real growth number. Registrations minus losses. |

### Promo effectiveness metrics

| Metric | Definition | Why it matters |
|:-------|:-----------|:--------------|
| **Promo incremental ride lift** | Rides from promo group minus rides from holdout group (controlled experiment) | Without this, we cannot know if promos generate rides or just subsidize existing ones |
| **Cost per incremental intercity ride** | Total promo spend ÷ incremental rides generated | Allows comparison against other acquisition channels |
| **Promo redemption by user tenure** | Split of redemptions by new / cross-sell / repeat users | Shows whether budget is reaching the intended audience |
| **Promo cohort retention delta** | Difference in 30-day repeat rate between promo and non-promo users, controlled by ride history | Tests the retention hypothesis for the three-discount cycle |

### Operational quality metrics

| Metric | Definition | Why it matters |
|:-------|:-----------|:--------------|
| **First intercity ride completion rate** | % of users' first intercity rides that complete successfully | First impression drives retention. Must be tracked separately from overall completion. |
| **Driver arrival time P90 (intercity)** | 90th percentile wait time for intercity rides | Identifies tail-end bad experiences that drive churn |
| **First-ride rating distribution** | Ratings given on first intercity ride vs. repeat rides | Low first-ride ratings predict non-return |
| **Supply response time by route** | How quickly driver supply grows when demand increases on a route | Since supply scales with demand, this confirms supply is not the bottleneck — or flags if it is |

### Competitive and market metrics

| Metric | Definition | Why it matters |
|:-------|:-----------|:--------------|
| **Intercity market share estimate** | Platform's intercity trips as % of estimated total intercity market | The headline number — but lags all the leading indicators above |
| **NPS vs. competitor benchmark** | Net Promoter Score, ideally with a competitor comparison question | Measures brand consideration gap against whoever holds the other 80% |

---

## Section 3 — Analytical Methodologies

### 3.1 Funnel Decomposition Analysis

**What it answers:** At which step is intercity demand being lost — and in which route, city, or user segment?

Break the full intercity booking funnel into stages using event log data: app open → intercity tab viewed → route searched → price checked → request submitted → driver assigned → ride completed → second ride within 30 days. Calculate drop-off rates at each stage. Then cut by:
- City and route
- Vehicle type
- User source (organic, cross-sell, promo)
- Time of day and day of week (intercity demand peaks around weekends and holidays)

The goal is a precise answer to: "where does the majority of demand die?" This shapes every other decision.

**Data needed:** App event logs (screen views, search events), rides table (request, assignment, completion timestamps), user source attribution.

---

### 3.2 Promo Holdout Experiment (Incremental Lift Test)

**What it answers:** Does the three-discount new user promo cycle generate rides that would not have happened without it?

**Design:**
- New users are randomly split at signup: 80% receive the full three-discount cycle, 20% receive one discount
- Both groups are tracked for 90 days
- Primary metric: number of intercity rides completed in 90 days
- Guardrail metric: first-ride completion rate must not fall in either group

If both groups complete the same number of rides, the extra two discounts are not generating incremental demand — they are subsidizing rides that would have happened anyway. Redirect that budget.

If the promo group significantly outrides the control group, the program is working and should be maintained or expanded.

**Why this is the most important experiment to run:** The company is the highest promotional spender among all competitors with 20% market share. Before increasing spend or changing strategy, the fundamental question — *does this spend generate rides?* — must be answered. Right now it cannot be answered because no holdout exists.

---

### 3.3 Cohort Retention Analysis

**What it answers:** Are any signup cohorts retaining better? Is there a month, campaign, or period where something worked?

Group users by signup month. For each cohort, calculate: intercity rides in month 1, month 2, month 3; 60-day churn rate; 30-day repeat ride rate. Look for cohorts that outperform.

An outperforming cohort is a signal worth investigating: what was different that month? Was there a route launch? A specific campaign? A supply event? Identifying what caused the better outcome is the basis for replicating it.

If no cohort outperforms — if all cohorts look the same — that is itself a finding: the platform has not discovered a retention formula, and the focus must shift to product fixes before acquisition spend.

---

### 3.4 Cross-Sell Attribution Analysis

**What it answers:** Are users from other verticals (food delivery, intracity) actually converting to intercity rides? And if they convert, do they retain?

For every cross-sell campaign, track the full funnel:
- Users reached by the campaign
- Users who clicked or engaged
- Users who completed their first intercity ride within 30 days
- Users who completed a second intercity ride within 60 days

Compare these rates against organic intercity user acquisition on the same metrics. If cross-sell users convert but don't retain, the problem is in the product — and more cross-sell investment will not help. If cross-sell users retain better than organic users (because they already trust the platform brand), that is a strong argument for expanding the program.

---

### 3.5 Product Feature Evaluation Framework

**What it answers:** Did the new features the product team launched actually improve anything?

Every feature needs a measurement plan before launch. Without one, there is no baseline and no way to distinguish feature effect from natural variation.

**For each launched feature, define before rollout:**
1. **Primary metric:** One number that the feature is designed to move. For booking experience features: request-to-completion rate. For user convenience features: repeat ride rate at 30 days.
2. **Guardrail metrics:** What must not get worse. Driver arrival time, first-ride rating, support ticket rate. If any guardrail worsens, the feature has failed regardless of the primary metric.
3. **Minimum detectable effect:** The smallest improvement that would change a business decision. Calculate the sample size needed to detect this reliably.
4. **Randomization unit:** User-level randomization. Do not use city-level rollouts as a control group — supply effects contaminate city comparisons.
5. **Analysis cuts:** Every result should be broken down by new vs. returning user, by city, and by route type. A feature that works for frequent riders but not first-timers is a completely different finding.

**For features already launched without a measurement plan:**

Run a retrospective analysis using pre/post comparison on the primary metric, with a synthetic control group built from cities or segments that did not receive the feature. This is noisier than a proper experiment but better than no measurement at all.

---

### 3.6 RFM Segment Performance Audit

**What it answers:** Which RFM segments are responding to re-engagement campaigns, and are they actually riding after responding?

Track each RFM campaign from message sent → app open → ride requested → ride completed → repeat ride within 30 days. The question is not just whether users open the message — it is whether they ride after they arrive, and whether they come back.

If segments respond (open the message) but don't ride, the message is succeeding but the product is failing. If segments ride but don't return, the retention problem is in the experience, not the segmentation.

---

## Section 4 — Strategic Recommendations

### Stop doing these

**Stop measuring growth by ride requests without segmenting by user type.**
A ride request from a user's fifth intercity trip is fundamentally different from a first-time user requesting their first intercity ride. Aggregate ride count hides whether the platform is growing its user base or just keeping existing users. Track new intercity users separately.

**Stop running the three-discount new user promo cycle without a holdout.**
This is the single most important thing to stop. The company is the highest promotional spender among all competitors, yet market share is 20%. Without a holdout test, it is impossible to know whether any of this spend is generating incremental rides. Running the experiment costs almost nothing compared to the current spend. Not running it means every future budget decision is made in the dark.

**Stop treating market share as the primary KPI without decomposing it.**
Market share at 20% could mean: (a) 20% of travelers know the platform and always use it, or (b) 60% of travelers try it once but don't come back. These are completely different problems requiring completely different solutions. Market share alone cannot tell you which one you have.

**Stop expanding to new routes or cities before fixing the repeat booking rate.**
If the repeat ride rate is below 25%, every new route and every new city just generates a new pool of churning users. The growth math does not work until retention is solved first.

---

### Start doing these

**Run the promo holdout experiment immediately.**
Design it this week. It should run for 90 days. Until the results are in, no additional promo investment should be approved. The current $X in annual promo spend needs an evidence-based answer before scaling.

**Establish a first-intercity-ride experience guarantee.**
Create a commitment for first-time intercity riders: if the driver does not arrive within a defined window (e.g., 15 minutes), the user receives a service credit. This directly addresses the first-impression failure hypothesis. It costs something in service credits but protects the most important moment in the user relationship — the first ride.

**Build a repeat booking trigger within 48 hours of first intercity ride.**
After a user completes their first intercity ride, a targeted message within 48 hours offering a route reminder or an upcoming-trip nudge is the highest-leverage retention intervention possible. The user is warm, the product is fresh, and the window is open. Do not wait until they re-enter the app on their own.

**Set route-level supply density targets.**
Since supply scales with demand — but demand is currently limited — there is a risk that certain high-potential routes have insufficient supply, which produces long waits, which suppresses demand further. Identify the top 10 intercity routes by potential demand (from search data, not completed rides) and set a minimum supply density target for each. This breaks the demand–supply catch-22.

---

### Continue doing these

**Continue cross-selling from other verticals — but measure it properly.**
Cross-selling users who already trust the platform is structurally correct. The current measurement is insufficient (if any exists). Add the attribution tracking described in Section 3.4. If cross-sell users convert AND retain better than organic users, double the cross-sell investment. If they convert but don't retain, the problem is in the product experience and more cross-sell investment will not help.

**Continue the RFM segmentation program — but pair it with operational fixes.**
RFM is the right tool for re-engagement. The limitation is not how users are segmented — it is what they encounter when they respond. A segmented re-engagement message that brings a user back to a product experience with long waits and driver cancellations produces churn, not retention. Pair the segmentation with operational improvements so that users who respond to re-engagement have a better experience than the one that caused them to leave.

**Continue investing in supply quality and driver tenure.**
The case confirms that supply scales with demand. As demand grows, supply will follow. The long-term quality of the supply side — driver acceptance rates, cancellation rates, on-time performance — is what converts intercity trips into repeat intercity trips. Drivers who have been on the platform longer are typically more reliable. Programs that reduce early driver attrition are investments in the long-term quality of the platform.

---

### New strategies for competitive advantage

**Route-level demand forecasting and guaranteed scheduling**
Intercity rides are often planned, not spontaneous. A user booking a trip from City A to City B tomorrow morning is very different from a user hailing a ride 5 minutes from now. Build a scheduled-booking feature that allows users to book intercity rides 12–72 hours in advance, with a guaranteed driver confirmed at booking. This matches the planning behavior of intercity travelers, improves supply predictability, and gives users a reason to prefer this platform over competitors who rely on last-minute dispatch.

**Certified intercity driver tier**
Create a two-tier system: standard drivers and certified intercity drivers. Certification requirements: minimum tenure, acceptance rate above a threshold, cancellation rate below a threshold, and a minimum number of prior intercity trips. Certified drivers are given priority dispatch on intercity rides and a small fare premium. Users can choose to wait slightly longer for a certified driver. This creates a quality signal, gives high-performing drivers a retention incentive, and gives users a way to reduce first-impression failure on their most important rides.

**Route-specific loyalty program**
Users who travel a specific route regularly (e.g., a weekly business commute between two cities) are the most valuable intercity users. A route-loyalty program — where rides on the same route accumulate toward a discount — creates both retention incentive and behavioral data on repeat travelers. This is a low-cost structural change that rewards the highest-value users without subsidizing occasional riders.

**Segment: business travelers on recurring routes**
Corporate travelers taking intercity rides on expense accounts are price-insensitive, high-frequency, and predictable. A corporate account program with centralized billing, trip reporting, and priority dispatch would capture this segment with minimal promotional cost. This is the segment least likely to be won by competitor discounting.

---

### How to build long-term sustainable competitive advantage

The company currently competes on price (discounts, promo cycles, low post-discount fares) while holding 20% market share. This is an unsustainable position — spending the most on promotions while competitors hold 80% of the market means either those competitors are solving something that promotions cannot, or the promotions are not reaching the conversion bottleneck.

Long-term competitive advantage in intercity rides comes from three sources that are not easily replicated by spending:

**1. Reliability as a brand promise**
If the platform can credibly say "when you book an intercity ride with us, your driver will arrive within X minutes and your ride will complete," that is a differentiation that a discount cannot match. Building this requires fixing the product experience (wait times, driver quality, route coverage) before advertising it. The brand promise must be true before it becomes a brand asset.

**2. Supply depth on key routes**
Supply is not currently the binding constraint — but supply on specific high-demand routes at peak times is what separates a great experience from an average one. The competitor with the deepest supply on the 20 most-traveled intercity routes will win those routes permanently. Invest in supply density on the routes that matter most, not breadth across all routes.

**3. Data advantage from repeat users**
Every repeat user generates data: their preferred routes, their booking windows, their vehicle preferences, their sensitivity to pricing and wait time. This data improves dispatch, demand forecasting, pricing, and personalization. A competitor who successfully retains intercity users builds a data flywheel that becomes harder to displace over time. The value of a retained user is not just the fare — it is every future ride and the data that makes those future rides better.

The company's goal should not be to outspend competitors. It should be to create a product experience so reliable and so well-matched to intercity travelers' needs that each user acquired becomes a long-term repeat rider — reducing the cost of the next ride and making competitive displacement progressively harder.

---

*Note: All quantitative examples in this document are hypothetical illustrations based on the case context. Actual analysis requires access to the operational datasets described in each section.*
