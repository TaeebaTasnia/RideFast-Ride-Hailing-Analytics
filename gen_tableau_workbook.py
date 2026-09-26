#!/usr/bin/env python3
"""
gen_tableau_workbook.py — RideFast Dashboard Generator (fixed)
Generates output/ridefast_dashboard.twbx

Fixes applied vs previous version:
  1. <pane> wrapped in <panes>...</panes>  (was direct child of <table>)
  2. <sort class='computed'> placed BEFORE <aggregation> inside <view>
     (removed invalid 'from', 'type', 'using' attributes)
  3. Dashboard zone type='view'  (was type='worksheet' which is invalid)
  4. <title> removed from <dashboard>  (not in dashboard content model)
  5. <dashboard> gets required <style/><datasources/><devicelayouts/> children
"""

import zipfile
import csv
from pathlib import Path

OUT_DIR  = Path("output")
TWBX_OUT = OUT_DIR / "ridefast_dashboard.twbx"

# ─── Schema inference ──────────────────────────────────────────────────────────

def infer_dtype(vals):
    clean = [v.strip() for v in vals if v.strip()]
    if not clean:
        return 'string'
    if all(v.lower() in ('true','false') for v in clean[:20]):
        return 'boolean'
    try:
        [int(v) for v in clean[:20]]
        return 'integer'
    except Exception:
        pass
    try:
        [float(v) for v in clean[:20]]
        return 'real'
    except Exception:
        pass
    v0 = clean[0]
    if len(v0) >= 10 and v0[4:5] == '-' and v0[7:8] == '-':
        return 'date' if len(v0) == 10 else 'datetime'
    return 'string'

def read_schema(fname):
    path = OUT_DIR / fname
    with open(path, newline='', encoding='utf-8') as f:
        rdr    = csv.reader(f)
        headers = next(rdr)
        rows    = [next(rdr, []) for _ in range(10)]
    return [(h, infer_dtype([r[i] for r in rows if i < len(r)]))
            for i, h in enumerate(headers)]

# ─── XML escaping ──────────────────────────────────────────────────────────────

def esc(s):
    return (str(s).replace('&','&amp;').replace('<','&lt;')
            .replace('>','&gt;').replace('"','&quot;').replace("'",'&apos;'))

# ─── Type helpers ──────────────────────────────────────────────────────────────

TC = {'string':'129','integer':'20','real':'5','date':'7','datetime':'135','boolean':'11'}

def col_role(dt):     return 'measure'      if dt in ('integer','real') else 'dimension'
def col_qtype(dt):    return 'quantitative' if dt in ('integer','real') else 'nominal'
def col_datatype(dt):
    if dt in ('integer','boolean'): return 'integer'
    if dt == 'real':                return 'real'
    if dt in ('date','datetime'):   return dt
    return 'string'
def col_agg(dt):      return 'Sum' if dt in ('integer','real') else 'Count'

# ─── Datasource XML ────────────────────────────────────────────────────────────

def make_datasource(ds_name, caption, csv_file, schema, calcs=None):
    tbl = csv_file.replace('.csv','').replace('-','').replace(' ','') + 'csv'

    meta = '\n'.join(f"""\
          <metadata-record class='column'>
            <remote-name>{esc(col)}</remote-name>
            <remote-type>{TC.get(dt,'129')}</remote-type>
            <local-name>[{esc(col)}]</local-name>
            <parent-name>[{esc(tbl)}]</parent-name>
            <remote-alias>{esc(col)}</remote-alias>
            <ordinal>{i}</ordinal>
            <local-type>{dt}</local-type>
            <aggregation>{col_agg(dt)}</aggregation>
            <width>0</width><scale>0</scale><precision>0</precision>
            <contains-null>true</contains-null>
          </metadata-record>""" for i,(col,dt) in enumerate(schema))

    coldefs = '\n'.join(
        f"  <column datatype='{col_datatype(dt)}' name='[{esc(col)}]' "
        f"role='{col_role(dt)}' type='{col_qtype(dt)}'/>"
        for col,dt in schema)

    calcxml = ''
    for c in (calcs or []):
        fmt = " default-format='p0.0%'" if any(k in c['caption'] for k in ('Rate','Pct','%')) else ''
        calcxml += (f"\n  <column caption='{esc(c['caption'])}' datatype='real' "
                    f"name='[{esc(c['name'])}]'{fmt} role='measure' type='quantitative'>"
                    f"\n    <calculation class='tableau' formula='{esc(c['formula'])}'/>"
                    f"\n  </column>")

    return f"""\
  <datasource caption='{esc(caption)}' inline='true' name='{esc(ds_name)}' version='18.1'>
    <connection class='textscan' filename='Data/{esc(csv_file)}' separator=',' >
      <relation name='{esc(csv_file)}' table='[{esc(tbl)}]' type='table'/>
      <metadata-records>
{meta}
      </metadata-records>
    </connection>
{coldefs}{calcxml}
  </datasource>"""

# ─── Column-instance helpers ───────────────────────────────────────────────────

_DERIV = {
    'None':  ('none','nk','nominal'),
    'Sum':   ('sum', 'qk','quantitative'),
    'Avg':   ('avg', 'qk','quantitative'),
    'Count': ('cnt', 'qk','quantitative'),
    'CountD':('cntd','qk','quantitative'),
    'Min':   ('min', 'qk','quantitative'),
    'Max':   ('max', 'qk','quantitative'),
}

def inst(col, deriv='None'):
    p,k,_ = _DERIV.get(deriv,('none','nk','nominal'))
    return f'[{p}:{col}:{k}]'

def inst_elem(col, deriv='None'):
    p,k,qt = _DERIV.get(deriv,('none','nk','nominal'))
    name = f'[{p}:{col}:{k}]'
    return (f"        <column-instance column='[{esc(col)}]' derivation='{esc(deriv)}' "
            f"name='{esc(name)}' pivot='key' type='{qt}'/>")

# ─── Worksheet builder ─────────────────────────────────────────────────────────

def make_worksheet(ws_name, ds_name, ds_cap,
                   col_insts,        # list of inst_elem() strings
                   rows_ref, cols_ref,
                   mark_class, encodings_xml,
                   filter_xml='', sort_col=None, sort_dir='DESC'):
    """
    Correct TWB structure (version 18.1):
      <table>
        <view>  ...datasource-deps... <sort/> <aggregation/>  </view>
        <style/>
        <panes>
          <pane>
            <view/>           ← required FIRST child of pane (empty marker)
            <mark class='X'/>
            <encodings>
              <color .../>    ← only: color|size|text|shape|... NO <label>
            </encodings>
          </pane>
        </panes>
        <rows/><cols/>
      </table>
    """
    insts_xml = '\n'.join(col_insts)

    filt_block = f"\n        {filter_xml}" if filter_xml else ''

    sort_block = ''
    if sort_col:
        sort_block = f"\n        <sort class='computed' column='[{esc(sort_col)}]' direction='{sort_dir}'/>"

    return f"""\
  <worksheet name='{esc(ws_name)}'>
    <table>
      <view>
        <datasources>
          <datasource caption='{esc(ds_cap)}' name='{esc(ds_name)}'/>
        </datasources>
        <datasource-dependencies datasource='{esc(ds_name)}'>
{insts_xml}
        </datasource-dependencies>{filt_block}{sort_block}
        <aggregation value='true'/>
      </view>
      <style/>
      <panes>
        <pane>
          <breakdown value='auto'>
            <mark class='{mark_class}'/>
            <encodings>
{encodings_xml}
            </encodings>
          </breakdown>
        </pane>
      </panes>
      <rows>{rows_ref}</rows>
      <cols>{cols_ref}</cols>
    </table>
  </worksheet>"""

# ─── Chart-type helpers ────────────────────────────────────────────────────────

def ws_bar(name, ds_name, ds_cap, dim, meas, meas_deriv='Avg',
           horizontal=True, filter_col=None, filter_vals=None, sort_desc=True):
    col_insts = [inst_elem(dim,'None'), inst_elem(meas, meas_deriv)]
    dim_ref   = inst(dim,'None')
    meas_ref  = inst(meas, meas_deriv)
    rows_ref  = dim_ref  if horizontal else meas_ref
    cols_ref  = meas_ref if horizontal else dim_ref

    filt = ''
    if filter_col and filter_vals:
        members = ''.join(
            f"<groupfilter function='member' level='[{esc(filter_col)}]' member='{esc(v)}'/>"
            for v in filter_vals)
        filt = (f"<filter class='categorical' column='[{esc(filter_col)}]'>"
                f"<groupfilter function='union'>{members}</groupfilter></filter>")

    sort_col = meas if sort_desc else None
    sort_dir = 'DESC' if sort_desc else 'ASC'

    # encodings: only color|size|text|shape valid — NO <label>
    enc = f"          <color column='{esc(dim_ref)}'/>"

    return make_worksheet(name, ds_name, ds_cap, col_insts,
                          rows_ref, cols_ref, 'Bar', enc,
                          filter_xml=filt, sort_col=sort_col, sort_dir=sort_dir)


def ws_line(name, ds_name, ds_cap, dim, measures_derivs):
    col_insts = [inst_elem(dim,'None')]
    for m,d in measures_derivs:
        col_insts.append(inst_elem(m,d))
    dim_ref  = inst(dim,'None')
    meas_ref = inst(measures_derivs[0][0], measures_derivs[0][1])
    enc = f"          <color column='{esc(dim_ref)}'/>"
    return make_worksheet(name, ds_name, ds_cap, col_insts,
                          meas_ref, dim_ref, 'Line', enc)


def ws_text_kpi(name, ds_name, ds_cap, meas, meas_deriv):
    insts = [inst_elem(meas, meas_deriv)]
    meas_ref = inst(meas, meas_deriv)
    enc = f"          <text column='{esc(meas_ref)}'/>"
    return make_worksheet(name, ds_name, ds_cap, insts, '', '', 'Text', enc)


def ws_heatmap(name, ds_name, ds_cap, row_dim, col_dim, meas, meas_deriv='Avg'):
    col_insts = [inst_elem(row_dim,'None'), inst_elem(col_dim,'None'),
                 inst_elem(meas, meas_deriv)]
    row_ref  = inst(row_dim,'None')
    col_ref  = inst(col_dim,'None')
    meas_ref = inst(meas, meas_deriv)
    enc = f"          <color column='{esc(meas_ref)}'/>"
    return make_worksheet(name, ds_name, ds_cap, col_insts,
                          row_ref, col_ref, 'Square', enc)

# ─── Dashboard XML ─────────────────────────────────────────────────────────────

_ZID = [300]
def zid():
    _ZID[0] += 1
    return _ZID[0]

def make_dashboard(db_name, rows):
    """
    rows = list of row-lists, each entry: (sheet_name, w_frac, h_frac)
    w_frac across a row should sum to 1.0; h_frac across rows should sum to 1.0.

    FIX 3: zone type='view'  (not 'worksheet')
    FIX 4: no <title> element inside <dashboard>
    FIX 5: dashboard needs <style/> <datasources/> <devicelayouts/>
    """
    outer = zid()
    flow  = zid()

    y = 0
    inner_zones = []
    for row in rows:
        if not row:
            continue
        row_h = int(row[0][2] * 100000)
        # Each row is itself a horizontal flow zone
        hflow = zid()
        x = 0
        child_zones = []
        for sheet, w_frac, _ in row:
            w = int(w_frac * 100000)
            z = zid()
            child_zones.append(
                f"            <zone h='{row_h}' id='{z}' name='{esc(sheet)}' "
                f"w='{w}' x='{x}' y='0'/>"
            )
            x += w
        children = '\n'.join(child_zones)
        inner_zones.append(
            f"          <zone h='{row_h}' id='{hflow}' param='horz' "
            f"type='layout-flow' w='100000' x='0' y='{y}'>\n"
            f"{children}\n"
            f"          </zone>"
        )
        y += row_h

    zones_body = '\n'.join(inner_zones)
    phone_id1  = zid()
    phone_id2  = zid()

    return f"""\
  <dashboard name='{esc(db_name)}'>
    <style/>
    <size maxheight='2000' maxwidth='1400' minheight='600' minwidth='800'/>
    <datasources/>
    <zones>
      <zone h='100000' id='{outer}' type='layout-basic' w='100000' x='0' y='0'>
        <zone h='100000' id='{flow}' param='vert' type='layout-flow' w='100000' x='0' y='0'>
{zones_body}
        </zone>
      </zone>
    </zones>
    <devicelayouts>
      <devicelayout name='Phone'>
        <size maxheight='2000' maxwidth='375' minheight='400' minwidth='320'/>
        <zones>
          <zone h='100000' id='{phone_id1}' type='layout-basic' w='100000' x='0' y='0'>
            <zone h='100000' id='{phone_id2}' param='vert' type='layout-flow' w='100000' x='0' y='0'/>
          </zone>
        </zones>
      </devicelayout>
    </devicelayouts>
  </dashboard>"""

# ─── Build ─────────────────────────────────────────────────────────────────────

def build():
    print("Reading schemas...")
    rides_s   = read_schema('looker_rides.csv')
    drivers_s = read_schema('looker_drivers.csv')
    users_s   = read_schema('looker_users.csv')
    tickets_s = read_schema('looker_tickets.csv')
    wait_s    = read_schema('looker_wait_cliff.csv')
    zone_s    = read_schema('looker_zone_stats.csv')
    promo_s   = read_schema('looker_promo_matrix.csv')

    rides_calcs = [
        {'name':'Calc_CompRate',  'caption':'Completion Rate',     'formula':'AVG([Is Completed])'},
        {'name':'Calc_DrvCancel', 'caption':'Driver Cancel Rate',  'formula':'AVG([Is Driver Cancel])'},
        {'name':'Calc_Over15',    'caption':'% Rides Over 15 Min', 'formula':'AVG([Wait Over 15])'},
        {'name':'Calc_Revenue',   'caption':'Total Revenue',       'formula':'SUM([Revenue])'},
    ]

    print("Building datasources...")
    ds_xml = '\n'.join([
        make_datasource('rides_ds',   'Rides',       'looker_rides.csv',       rides_s,  rides_calcs),
        make_datasource('drivers_ds', 'Drivers',     'looker_drivers.csv',     drivers_s),
        make_datasource('users_ds',   'Users',       'looker_users.csv',       users_s),
        make_datasource('tickets_ds', 'Tickets',     'looker_tickets.csv',     tickets_s),
        make_datasource('wait_ds',    'Wait Cliff',  'looker_wait_cliff.csv',  wait_s),
        make_datasource('zone_ds',    'Zone Stats',  'looker_zone_stats.csv',  zone_s),
        make_datasource('promo_ds',   'Promo Matrix','looker_promo_matrix.csv',promo_s),
    ])

    print("Building worksheets...")
    sheets = []

    # KPI cards
    sheets.append(ws_text_kpi('KPI Total Rides',        'rides_ds',   'Rides',   'ride_id',         'Count'))
    sheets.append(ws_text_kpi('KPI Revenue',            'rides_ds',   'Rides',   'Revenue',          'Sum'))
    sheets.append(ws_text_kpi('KPI Completion Rate',    'rides_ds',   'Rides',   'Is Completed',     'Avg'))
    sheets.append(ws_text_kpi('KPI Driver Cancel Rate', 'rides_ds',   'Rides',   'Is Driver Cancel', 'Avg'))
    sheets.append(ws_text_kpi('KPI Active Users',       'users_ds',   'Users',   'User ID',          'Count'))
    sheets.append(ws_text_kpi('KPI Total Tickets',      'tickets_ds', 'Tickets', 'Ticket ID',        'Count'))
    sheets.append(ws_text_kpi('KPI Avg Wait',           'rides_ds',   'Rides',   'Wait Minutes',     'Avg'))

    # P1
    sheets.append(ws_line(
        'Monthly Rides Trend','rides_ds','Rides','Year Month',
        [('ride_id','Count'),('Is Completed','Sum'),('Is Driver Cancel','Sum')]))
    sheets.append(ws_bar('City Completion Rate','rides_ds','Rides',
                         'city','Is Completed','Avg', horizontal=True))
    sheets.append(ws_bar('Revenue by User Group','rides_ds','Rides',
                         'User Group','Revenue','Sum', horizontal=True))
    sheets.append(ws_bar('Ride Status Funnel','rides_ds','Rides',
                         'status','ride_id','Count', horizontal=True))

    # P2
    sheets.append(ws_bar('Wait Cliff Completion','wait_ds','Wait Cliff',
                         'Wait Bracket','Completion Rate','Avg',
                         horizontal=False, sort_desc=False))
    sheets.append(ws_bar('Wait Cliff Driver Cancel','wait_ds','Wait Cliff',
                         'Wait Bracket','Driver Cancel Rate','Avg',
                         horizontal=False, sort_desc=False))
    sheets.append(ws_bar('Rides by Wait Bracket','wait_ds','Wait Cliff',
                         'Wait Bracket','Rides','Sum',
                         horizontal=False, sort_desc=False))

    # P3
    sheets.append(ws_bar('Churn by First Ride','users_ds','Users',
                         'First Ride Bracket','Churn Flag','Avg',
                         horizontal=True, sort_desc=False))
    sheets.append(ws_bar('Ride Frequency','users_ds','Users',
                         'Ride Count Bracket','User ID','Count',
                         horizontal=True, sort_desc=False))
    sheets.append(ws_heatmap('Promo Churn Matrix','promo_ds','Promo Matrix',
                             'Ride Count Bracket','Promo Quartile','Churn Rate','Avg'))
    sheets.append(ws_bar('Revenue by Value Segment','users_ds','Users',
                         'Value Segment','Total Gross Spend','Sum',
                         horizontal=True, sort_desc=True))

    # P4
    sheets.append(ws_bar('Driver Tier Long Waits','rides_ds','Rides',
                         'Driver Quality Tier','Wait Over 15','Avg',
                         horizontal=True, sort_desc=True,
                         filter_col='Driver Quality Tier',
                         filter_vals=['Both-Issues','Standard']))
    sheets.append(ws_bar('Cancel Rate by Tier','drivers_ds','Drivers',
                         'Quality Tier','Cancellation Rate (Profile)','Avg',
                         horizontal=True, sort_desc=True))
    sheets.append(ws_bar('Northgate Zone Completion','zone_ds','Zone Stats',
                         'Zone','Completion Rate','Avg',
                         horizontal=True, sort_desc=False,
                         filter_col='City', filter_vals=['Northgate']))
    sheets.append(ws_line('Driver Tenure Quality','drivers_ds','Drivers',
                          'Tenure Bracket',
                          [('Cancellation Rate (Profile)','Avg'),('Avg Rating','Avg')]))

    # P5
    sheets.append(ws_bar('Ticket Categories','tickets_ds','Tickets',
                         'Category Label','Ticket ID','Count',
                         horizontal=True, sort_desc=True))
    sheets.append(ws_bar('Resolution Rate by Category','tickets_ds','Tickets',
                         'Category Label','Is Resolved','Avg',
                         horizontal=True, sort_desc=True))
    sheets.append(ws_bar('Tickets by City','tickets_ds','Tickets',
                         'City','Ticket ID','Count',
                         horizontal=True, sort_desc=True))
    sheets.append(ws_heatmap('Resolution Time Heatmap','tickets_ds','Tickets',
                             'Category Label','Severity','Resolution Time Hours','Avg'))

    ws_xml = '\n'.join(sheets)

    print("Building dashboards...")
    dbs = []

    dbs.append(make_dashboard('P1 - Executive Overview', [
        [('KPI Total Rides',       0.143,0.12),('KPI Revenue',         0.143,0.12),
         ('KPI Completion Rate',   0.143,0.12),('KPI Driver Cancel Rate',0.143,0.12),
         ('KPI Active Users',      0.143,0.12),('KPI Total Tickets',    0.143,0.12),
         ('KPI Avg Wait',          0.142,0.12)],
        [('Monthly Rides Trend',   0.60, 0.42),('City Completion Rate', 0.40, 0.42)],
        [('Revenue by User Group', 0.50, 0.36),('Ride Status Funnel',   0.50, 0.36)],
    ]))

    dbs.append(make_dashboard('P2 - Ride Funnel and Wait Cliff', [
        [('Wait Cliff Completion',    0.50, 0.45),('Wait Cliff Driver Cancel',0.50,0.45)],
        [('Rides by Wait Bracket',    0.50, 0.30),('Ride Status Funnel',      0.50,0.30)],
    ]))

    dbs.append(make_dashboard('P3 - User Behaviour and Churn', [
        [('Revenue by Value Segment', 0.45, 0.28),('Churn by First Ride',     0.55,0.28)],
        [('Ride Frequency',           0.50, 0.28),('Revenue by User Group',    0.50,0.28)],
        [('Promo Churn Matrix',       1.00, 0.44)],
    ]))

    dbs.append(make_dashboard('P4 - Driver Operations', [
        [('Driver Tier Long Waits',   0.34, 0.35),('Cancel Rate by Tier',     0.33,0.35),
         ('Driver Tenure Quality',    0.33, 0.35)],
        [('Northgate Zone Completion',1.00, 0.45)],
    ]))

    dbs.append(make_dashboard('P5 - Support and Experience', [
        [('KPI Total Tickets',        0.34, 0.12),('KPI Completion Rate',      0.33,0.12),
         ('KPI Driver Cancel Rate',   0.33, 0.12)],
        [('Ticket Categories',        0.50, 0.38),('Resolution Rate by Category',0.50,0.38)],
        [('Tickets by City',          0.45, 0.38),('Resolution Time Heatmap',  0.55,0.38)],
    ]))

    db_xml = '\n'.join(dbs)

    print("Assembling workbook XML...")
    twb = f"""<?xml version='1.0' encoding='utf-8' ?>
<workbook source-build='20222.22.1012.1006' source-platform='win' version='18.1' xmlns:user='http://www.tableausoftware.com/xml/user'>
  <preferences>
    <color-palette name='ridefast' type='regular'>
      <color>#7C3AED</color>
      <color>#10B981</color>
      <color>#EF4444</color>
      <color>#F59E0B</color>
      <color>#3B82F6</color>
      <color>#EC4899</color>
      <color>#06B6D4</color>
      <color>#9CA3AF</color>
    </color-palette>
  </preferences>
  <datasources>
{ds_xml}
  </datasources>
  <worksheets>
{ws_xml}
  </worksheets>
  <dashboards>
{db_xml}
  </dashboards>
</workbook>"""

    return twb


def package(twb_xml):
    csv_files = [
        'looker_rides.csv','looker_drivers.csv','looker_users.csv','looker_tickets.csv',
        'looker_wait_cliff.csv','looker_zone_stats.csv','looker_promo_matrix.csv',
    ]
    print(f"\nPackaging {TWBX_OUT}...")
    with zipfile.ZipFile(TWBX_OUT, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('ridefast_dashboard.twb', twb_xml.encode('utf-8'))
        for fname in csv_files:
            src = OUT_DIR / fname
            if src.exists():
                zf.write(src, f'Data/{fname}')
                print(f"  + Data/{fname}  ({src.stat().st_size//1024:,} KB)")
            else:
                print(f"  MISSING: {fname}")
    mb = TWBX_OUT.stat().st_size / 1024 / 1024
    print(f"\nDone: {TWBX_OUT}  ({mb:.1f} MB)")
    print("\n1. Open output/ridefast_dashboard.twbx in Tableau Desktop/Public")
    print("2. File -> Save to Tableau Public -> copy URL")


if __name__ == '__main__':
    twb = build()
    package(twb)
