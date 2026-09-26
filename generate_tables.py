from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT_DIR = r"E:\pathao\table_images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SCALE = 2
PAD = int(14 * SCALE)
FONT_SZ = int(13 * SCALE)
LINE_H = int(20 * SCALE)
HDR_H = int(48 * SCALE)
MIN_ROW_H = int(48 * SCALE)

def load_fonts():
    paths = [
        (r"C:\Windows\Fonts\segoeui.ttf", r"C:\Windows\Fonts\segoeuib.ttf"),
        (r"C:\Windows\Fonts\arial.ttf",   r"C:\Windows\Fonts\arialbd.ttf"),
    ]
    for reg_p, bold_p in paths:
        try:
            return (ImageFont.truetype(reg_p, FONT_SZ),
                    ImageFont.truetype(bold_p, FONT_SZ))
        except:
            pass
    f = ImageFont.load_default()
    return f, f

REG, BOLD = load_fonts()

def rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def wrap(text, font, max_w):
    dummy = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    words = str(text).split(' ')
    lines, cur = [], []
    for w in words:
        test = ' '.join(cur + [w])
        bb = dummy.textbbox((0, 0), test, font=font)
        if (bb[2] - bb[0]) <= max_w or not cur:
            cur.append(w)
        else:
            lines.append(' '.join(cur))
            cur = [w]
    if cur:
        lines.append(' '.join(cur))
    return lines or ['']

def row_h(cells, col_ws):
    max_lines = 1
    for i, (txt, _, _, bold) in enumerate(cells):
        if i >= len(col_ws):
            break
        f = BOLD if bold else REG
        lines = wrap(txt, f, col_ws[i] - 2 * PAD)
        max_lines = max(max_lines, len(lines))
    return max(MIN_ROW_H, max_lines * LINE_H + 2 * PAD)

def render(fname, headers, rows, col_ws_base):
    col_ws = [int(w * SCALE) for w in col_ws_base]
    W = sum(col_ws)

    # calc heights
    rhs = [row_h(r, col_ws) for r in rows]
    H = HDR_H + sum(rhs) + int(4 * SCALE)

    img = Image.new('RGB', (W, H), rgb('#ffffff'))
    d = ImageDraw.Draw(img)

    # header
    x = 0
    for hdr, cw in zip(headers, col_ws):
        d.rectangle([x, 0, x + cw - 1, HDR_H - 1], fill=rgb('#dbeafe'))
        d.line([x, HDR_H - int(2*SCALE), x + cw, HDR_H - int(2*SCALE)],
               fill=rgb('#93c5fd'), width=int(2 * SCALE))
        bb = d.textbbox((0, 0), hdr, font=BOLD)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        d.text((x + PAD, HDR_H // 2 - th // 2), hdr, font=BOLD, fill=rgb('#1e3a5f'))
        x += cw

    # rows
    y = HDR_H
    for row, rh in zip(rows, rhs):
        x = 0
        for i, (cw, (txt, bg, fg, is_bold)) in enumerate(zip(col_ws, row)):
            d.rectangle([x, y, x + cw - 1, y + rh - 1], fill=rgb(bg))
            d.line([x, y + rh - 1, x + cw, y + rh - 1],
                   fill=rgb('#e5e7eb'), width=1)
            if txt:
                font = BOLD if is_bold else REG
                lines = wrap(txt, font, cw - 2 * PAD)
                block_h = len(lines) * LINE_H
                ty = y + (rh - block_h) // 2
                for line in lines:
                    d.text((x + PAD, ty), line, font=font, fill=rgb(fg))
                    ty += LINE_H
            x += cw
        y += rh

    path = os.path.join(OUTPUT_DIR, fname)
    img.save(path, 'PNG')
    print(f"  Saved {fname}")

# ── COLOUR TOKENS ───────────────────────────────────────────────────
W = '#ffffff'
T = '#374151'   # body text
M = '#6b7280'   # muted text
HB = '#dbeafe'  # header bg (unused here, drawn above)

BUS_B, BUS_T  = '#eff6ff', '#1e40af'
DEM_B, DEM_T  = '#faf5ff', '#6b21a8'
RET_B, RET_T  = '#f0fdf4', '#166534'
PRO_B, PRO_T  = '#fff7ed', '#9a3412'
QUA_B, QUA_T  = '#fdf4ff', '#86198f'
ROU_B, ROU_T  = '#fefce8', '#854d0e'

GRN_B, GRN_T  = '#f0fdf4', '#166534'
RED_B, RED_T  = '#fef2f2', '#991b1b'
BLU_B, BLU_T  = '#eff6ff', '#1e40af'
PUR_B, PUR_T  = '#faf5ff', '#6b21a8'
YEL_B, YEL_T  = '#fefce8', '#854d0e'
ORG_B, ORG_T  = '#fff7ed', '#9a3412'

STP_B, STP_T  = '#fef2f2', '#dc2626'
STR_B, STR_T  = '#f0fdf4', '#166534'
CON_B, CON_T  = '#fefce8', '#d97706'

URG = '#dc2626'
HGH = '#ea580c'
MED = '#d97706'

# ── TABLE 1 — METRIC HIERARCHY ───────────────────────────────────────
print("Rendering Table 1 — Metric Hierarchy...")
render(
    "01_metric_hierarchy.png",
    ["Level", "Metric", "Formula", "Priority"],
    [
        [(  "Business",        BUS_B, BUS_T, True),
         (  "Incremental intercity trips", BUS_B, T, False),
         (  "Treatment rides − Control rides", BUS_B, M, False),
         (  "Urgent",          BUS_B, URG, True)],

        [(  "Business",        BUS_B, BUS_T, True),
         (  "Contribution margin per trip", BUS_B, T, False),
         (  "Fare − driver payout − discount − fees", BUS_B, M, False),
         (  "Urgent",          BUS_B, URG, True)],

        [(  "Demand",          DEM_B, DEM_T, True),
         (  "Net new intercity users / month", DEM_B, T, False),
         (  "New first-timers − churned users", DEM_B, M, False),
         (  "Urgent",          DEM_B, URG, True)],

        [(  "Demand",          DEM_B, DEM_T, True),
         (  "Route search to request conversion", DEM_B, T, False),
         (  "Requests ÷ fare-checks", DEM_B, M, False),
         (  "High",            DEM_B, HGH, True)],

        [(  "Retention",       RET_B, RET_T, True),
         (  "First-to-second trip conversion rate", RET_B, T, False),
         (  "2nd trip completed ÷ first-trip users", RET_B, M, False),
         (  "Urgent",          RET_B, URG, True)],

        [(  "Promotion",       PRO_B, PRO_T, True),
         (  "Cost per incremental ride", PRO_B, T, False),
         (  "Promo spend ÷ incremental rides", PRO_B, M, False),
         (  "High",            PRO_B, HGH, True)],

        [(  "Promotion",       PRO_B, PRO_T, True),
         (  "Post-promo full-price conversion", PRO_B, T, False),
         (  "Full-price bookings ÷ post-promo users", PRO_B, M, False),
         (  "Medium",          PRO_B, MED, True)],

        [(  "Quality",         QUA_B, QUA_T, True),
         (  "First-ride completion rate", QUA_B, T, False),
         (  "Completed first rides ÷ accepted first rides", QUA_B, M, False),
         (  "High",            QUA_B, HGH, True)],

        [(  "Route",           ROU_B, ROU_T, True),
         (  "Route-level completion rate", ROU_B, T, False),
         (  "Completed ÷ accepted, per route", ROU_B, M, False),
         (  "Medium",          ROU_B, MED, True)],
    ],
    [120, 260, 300, 90]
)

# ── TABLE 2 — PROMO HOLDOUT ──────────────────────────────────────────
print("Rendering Table 2 — Promo Holdout...")
render(
    "02_promo_holdout.png",
    ["Element", "Detail"],
    [
        [("Treatment",     GRN_B, GRN_T, True),
         ("New intercity users receive the full 3-discount cycle as currently designed", GRN_B, T, False)],

        [("Control",       RED_B, RED_T, True),
         ("Randomly assigned users receive 1 discount only — assigned at signup, not self-selected", RED_B, T, False)],

        [("Duration",      BLU_B, BLU_T, True),
         ("90 days — long enough to observe at least one repeat trip given the natural spacing of intercity travel", BLU_B, T, False)],

        [("Primary metric", BLU_B, BLU_T, True),
         ("Total intercity trips completed per user within the measurement window", BLU_B, T, False)],

        [("Guardrail",     PUR_B, PUR_T, True),
         ("First-ride completion rate must not fall in either group", PUR_B, T, False)],

        [("Decision rule", YEL_B, YEL_T, True),
         ("If treatment shows no statistically significant lift over control, redirect the extra discount budget to supply quality fixes", YEL_B, T, False)],
    ],
    [160, 620]
)

# ── TABLE 3 — PRODUCT FEATURE EVALUATION ────────────────────────────
print("Rendering Table 3 — Product Feature Evaluation...")
render(
    "03_product_features.png",
    ["Feature Type", "Primary Metric to Move", "Guardrail (Must Not Worsen)"],
    [
        [("Scheduling / advance booking", BLU_B, BLU_T, True),
         ("Request-to-completion rate for scheduled rides", BLU_B, T, False),
         ("Driver cancellation rate", BLU_B, T, False)],

        [("Driver quality filters", GRN_B, GRN_T, True),
         ("Repeat trip conversion rate", GRN_B, T, False),
         ("Wait time at pickup", GRN_B, T, False)],

        [("Booking convenience", PUR_B, PUR_T, True),
         ("Search-to-request conversion rate", PUR_B, T, False),
         ("Support ticket rate", PUR_B, T, False)],
    ],
    [220, 280, 260]
)

# ── TABLE 4 — HEALTH CHECK ────────────────────────────────────────────
print("Rendering Table 4 — Health Check: Existing Strategies...")
render(
    "04_health_check.png",
    ["Strategy", "Health Check Question", "Pass Condition", "Risk If Failing"],
    [
        [("RFM segmentation",    PUR_B, PUR_T, True),
         ("Do high-RFM users convert to intercity at a meaningfully higher rate than low-RFM users?", PUR_B, T, False),
         ("Statistically significant conversion gap between segments", PUR_B, T, False),
         ("Segmentation has no predictive power — budget targeted on wrong signal", PUR_B, T, False)],

        [("Screen time targeting", YEL_B, YEL_T, True),
         ("Does high app screen time correlate with upcoming intercity bookings?", YEL_B, T, False),
         ("Positive and statistically meaningful correlation specific to intercity", YEL_B, T, False),
         ("Wrong signal — reflects food and intracity usage, not intercity intent", YEL_B, T, False)],

        [("3-discount cycle",    RED_B, RED_T, True),
         ("Does the promo group complete more rides than the control group?", RED_B, T, False),
         ("Statistically significant positive lift — requires holdout to measure at all", RED_B, T, False),
         ("Spending budget with no measurable incremental return", RED_B, T, False)],

        [("Zonal discounts",     GRN_B, GRN_T, True),
         ("Do discount zones show higher ride volume than comparable non-discount zones?", GRN_B, T, False),
         ("Statistically significant uplift in treated zones vs control zones", GRN_B, T, False),
         ("Subsidising rides that would have happened without the discount", GRN_B, T, False)],

        [("Cross-selling",       ORG_B, ORG_T, True),
         ("What share of cross-sell campaign users complete an intercity trip after receiving the promo?", ORG_B, T, False),
         ("Conversion rate materially above organic intercity baseline for same user type", ORG_B, T, False),
         ("Budget burning on users with no near-term intercity travel need", ORG_B, T, False)],
    ],
    [150, 250, 230, 230]
)

# ── TABLE 5 — STOP / START / CONTINUE ───────────────────────────────
print("Rendering Table 5 — Stop / Start / Continue...")
render(
    "05_stop_start_continue.png",
    ["Signal", "What", "Why"],
    [
        [("STOP", STP_B, STP_T, True),
         ("Promo spend without a holdout group", STP_B, T, False),
         ("Cannot justify any spend without knowing what is incremental", STP_B, T, False)],

        [("STOP", STP_B, STP_T, True),
         ("Using RFM for intercity targeting (until audit confirms otherwise)", STP_B, T, False),
         ("Structurally wrong for low-frequency, occasion-driven travel", STP_B, T, False)],

        [("STOP", STP_B, STP_T, True),
         ("Treating intercity as a longer intracity ride", STP_B, T, False),
         ("Different trust threshold, different booking behaviour, different product need", STP_B, T, False)],

        [("STOP", STP_B, STP_T, True),
         ("Flat promotional calendar across the whole year", STP_B, T, False),
         ("Intercity demand is occasion-driven — matching spend to high-intent windows is more efficient", STP_B, T, False)],

        [("START", STR_B, STR_T, True),
         ("Promo holdout experiment", STR_B, T, False),
         ("Foundation of every future spend decision — run it first", STR_B, T, False)],

        [("START", STR_B, STR_T, True),
         ("Occasion-calendar targeting", STR_B, T, False),
         ("Send promos before major travel windows (Eid, semester breaks, long weekends)", STR_B, T, False)],

        [("START", STR_B, STR_T, True),
         ("Advance booking / scheduled rides", STR_B, T, False),
         ("Planned travellers cannot confirm transport on an on-demand-only product", STR_B, T, False)],

        [("START", STR_B, STR_T, True),
         ("First-ride guarantee", STR_B, T, False),
         ("Auto credit if driver cancels on first intercity trip — highest churn risk moment", STR_B, T, False)],

        [("CONTINUE", CON_B, CON_T, True),
         ("Cross-selling from other verticals", CON_B, T, False),
         ("Sound in principle — add attribution tracking and occasion-timing first", CON_B, T, False)],

        [("CONTINUE", CON_B, CON_T, True),
         ("Investing in driver quality", CON_B, T, False),
         ("Long-tenure drivers are more reliable; supply quality is product quality for intercity", CON_B, T, False)],
    ],
    [90, 280, 370]
)

# ── TABLE 6 — INVESTMENT SHIFT ────────────────────────────────────────
print("Rendering Table 6 — Investment Shift...")
render(
    "06_investment_shift.png",
    ["Today", "Months 1–6", "Year 2"],
    [
        [("Biggest promo spender, 20% share",    RED_B, T, False),
         ("Holdout experiment running",           ORG_B, T, False),
         ("Route depth on top routes",            GRN_B, T, False)],

        [("No holdout data — spend unjustifiable", RED_B, T, False),
         ("Advance booking built",                ORG_B, T, False),
         ("Corporate accounts live",              GRN_B, T, False)],

        [("RFM applied to wrong category",        RED_B, T, False),
         ("First-ride guarantee active",          ORG_B, T, False),
         ("Peak season reliability brand",        GRN_B, T, False)],

        [("Flat calendar spend year-round",       RED_B, T, False),
         ("Occasion-based targeting",             ORG_B, T, False),
         ("Ecosystem partnerships",               GRN_B, T, False)],

        [("Funnel leaks unidentified",            RED_B, T, False),
         ("Funnel leaks mapped and fixed",        ORG_B, T, False),
         ("Data flywheel building",               GRN_B, T, False)],
    ],
    [250, 250, 250]
)

# ── TABLE 7 — LONG-TERM COMPETITIVE ADVANTAGE ────────────────────────
print("Rendering Table 7 — Long-Term Competitive Advantage...")
render(
    "07_competitive_advantage.png",
    ["Competitive Moat", "How It Builds", "Why Competitors Cannot Copy Quickly"],
    [
        [("Route depth",                BLU_B, BLU_T, True),
         ("Deep driver supply on key routes through loyalty programs", BLU_B, T, False),
         ("Takes years of relationship-building — cannot be bought overnight with discounts", BLU_B, T, False)],

        [("Peak season reliability brand", GRN_B, GRN_T, True),
         ("Successful peak seasons with guaranteed rides delivered consistently", GRN_B, T, False),
         ("Trust is earned across events, not purchased with coupons", GRN_B, T, False)],

        [("Corporate relationships",    PUR_B, PUR_T, True),
         ("Long-term contracts with high-travel organisations", PUR_B, T, False),
         ("Switching cost from invoicing workflows, account management, billing integration", PUR_B, T, False)],
    ],
    [200, 280, 320]
)

print("\nAll tables saved to:", OUTPUT_DIR)
