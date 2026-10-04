"""UrjaMitra - SME energy intelligence prototype (synthetic data).
Run:  pip install -r requirements.txt && streamlit run app.py
"""
import numpy as np, pandas as pd, plotly.graph_objects as go, streamlit as st

st.set_page_config(page_title="UrjaMitra", page_icon="⚡", layout="wide")
EF = 0.71  # kgCO2/kWh, approx. Indian grid factor (verify against latest CEA figure)

# ---------------------------------------------------------------- simulator
@st.cache_data
def simulate(days=30, seed=7, leak=0.25, idle_pct=0.40, tariff=8.0):
    rng = np.random.default_rng(seed)
    n = days * 24
    t = pd.date_range("2026-09-01", periods=n, freq="h")
    hr, dow = t.hour.values, t.dayofweek.values
    shift = ((hr >= 6) & (hr < 22) & (dow != 6)).astype(float)
    brk = ((hr == 12) | (hr == 18)).astype(float)
    run = shift * (1 - 0.5 * brk)
    temp = 30 + 6 * np.sin((hr - 9) / 24 * 2 * np.pi) + rng.normal(0, 1, n)
    units = run * rng.normal(120, 6, n).clip(0)

    def plant(opt):
        mot = 75 * run * rng.normal(1, .03, n) * (1.0 if opt else 1.06)
        furn = 60 * run + (6 * (1 - run) * shift if opt else 60 * idle_pct * (1 - run))
        lk = 0.07 if opt else leak
        comp = 22 * (run * .75 * (1 + lk) + (1 - run) * (lk * .9 if opt else .45))
        misc = 10 * (.4 + .6 * shift) * (0.9 if opt else 1)
        return dict(motors=mot, furnace=furn, compressor=comp, hvac_light=misc)

    b, o = plant(False), plant(True)
    df = pd.DataFrame({"time": t, "units": units, "temp": temp, "run": run})
    for k in b: df[f"b_{k}"], df[f"o_{k}"] = b[k], o[k]
    df["base_kw"] = df[[f"b_{k}" for k in b]].sum(axis=1)
    df["opt_kw"] = df[[f"o_{k}" for k in b]].sum(axis=1)
    df["tariff"] = np.where((hr >= 18) & (hr < 22), tariff * 1.2, np.where((hr >= 22) | (hr < 6), tariff * .8, tariff))
    return df

st.sidebar.title("⚡ UrjaMitra")
st.sidebar.caption("Factory-floor energy intelligence for Indian SMEs")
leak = st.sidebar.slider("Compressed-air leak fraction (baseline)", .05, .40, .25, .01)
idle = st.sidebar.slider("Furnace idle-hold (% of rated)", 0, 60, 40, 5) / 100
tariff = st.sidebar.number_input("Base tariff (Rs/kWh)", 4.0, 14.0, 8.0, .5)
ef = st.sidebar.number_input("Grid factor (kgCO2/kWh)", .5, 1.0, EF, .01)
df = simulate(leak=leak, idle_pct=idle, tariff=tariff)
U = df.units.sum()
bk, ok = df.base_kw.sum(), df.opt_kw.sum()
bc, oc = (df.base_kw * df.tariff).sum(), (df.opt_kw * df.tariff).sum()

st.title("UrjaMitra: Smart Manufacturing Energy Dashboard")
st.caption("Synthetic 30-day data for a two-shift SME plant. Baseline = today; Optimised = after recommended actions. Throughput identical in both.")
c = st.columns(5)
c[0].metric("Live load (kW)", f"{df.base_kw.iloc[-30]:.0f}")
c[1].metric("SEC baseline (kWh/unit)", f"{bk/U:.2f}")
c[2].metric("SEC optimised", f"{ok/U:.2f}", f"{(ok/bk-1)*100:.1f}%", delta_color="inverse")
c[3].metric("Monthly cost saved (Rs)", f"{bc-oc:,.0f}")
c[4].metric("CO2e avoided (t/month)", f"{(bk-ok)*ef/1000:.1f}")

tabs = st.tabs(["1 Live & load profile", "2 Savings finder", "3 Baseline model & SEC", "4 Predictive maintenance",
                "5 Tariff optimiser", "6 Carbon ledger", "7 ROI calculator"])

with tabs[0]:
    day = df[df.time.dt.day == 9]
    f = go.Figure()
    f.add_scatter(x=day.time, y=day.base_kw, name="Baseline", line=dict(color="#D64545"))
    f.add_scatter(x=day.time, y=day.opt_kw, name="With UrjaMitra", line=dict(color="#12A06B"))
    f.update_layout(title="Plant load, one day (kW)", height=380, margin=dict(t=40, b=10))
    st.plotly_chart(f, width="stretch")
    parts = {"Motors": "motors", "Furnace": "furnace", "Compressor": "compressor", "HVAC/lights": "hvac_light"}
    comp = pd.DataFrame({"Baseline": [df[f"b_{v}"].sum() for v in parts.values()],
                         "Optimised": [df[f"o_{v}"].sum() for v in parts.values()]}, index=parts.keys())
    st.bar_chart(comp, y_label="kWh per month")

with tabs[1]:
    rows = []
    idle_f = df.b_furnace.sum() - df.o_furnace.sum()
    leak_c = df.b_compressor.sum() - df.o_compressor.sum()
    mot = df.b_motors.sum() - df.o_motors.sum()
    misc = df.b_hvac_light.sum() - df.o_hvac_light.sum()
    avg = (df.base_kw * df.tariff).sum() / bk
    rows = [("Furnace idle-hold outside production", idle_f, "Switch to managed hold / schedule pre-heat", "Low"),
            ("Compressed-air leaks + unloaded running", leak_c, "Ultrasonic leak survey; auto-unload after shift", "Low"),
            ("Motor drawing excess current (bearing/misalignment)", mot, "Planned maintenance before failure", "Medium"),
            ("HVAC/lighting running unoccupied", misc, "Occupancy/time schedule", "Low")]
    t = pd.DataFrame(rows, columns=["Loss", "kWh/month", "Action", "Effort"])
    t["Rs/month"] = (t["kWh/month"] * avg).round(0)
    t["tCO2e/month"] = (t["kWh/month"] * ef / 1000).round(2)
    st.subheader("Ranked actions (largest rupee impact first)")
    st.dataframe(t.sort_values("Rs/month", ascending=False).style.format({"kWh/month": "{:,.0f}", "Rs/month": "{:,.0f}"}), hide_index=True, width="stretch")
    st.info("Every alert shows expected vs actual consumption and a rupee impact, so operators act on what they understand.")

with tabs[2]:
    st.markdown("**Expected-energy model:** `kWh = a + b·units + c·temp` fitted on a reference (healthy) period, then used to flag drift.")
    ref = df[df.run > 0]
    X = np.c_[np.ones(len(ref)), ref.units, ref.temp]
    w, *_ = np.linalg.lstsq(X, ref.opt_kw.values, rcond=None)
    pred = np.c_[np.ones(len(df)), df.units, df.temp] @ w
    df_m = df.assign(expected=pred)
    d = df_m[df_m.run > 0]
    r2 = 1 - ((d.opt_kw - d.expected) ** 2).sum() / ((d.opt_kw - d.opt_kw.mean()) ** 2).sum()
    f = go.Figure()
    f.add_scatter(x=d.units, y=d.base_kw, mode="markers", name="Baseline", marker=dict(color="#D64545", size=4))
    f.add_scatter(x=d.units, y=d.opt_kw, mode="markers", name="Optimised", marker=dict(color="#12A06B", size=4))
    f.update_layout(title=f"Hourly kW vs units produced (fit R² on healthy ops = {r2:.2f})", xaxis_title="units/hour", yaxis_title="kW", height=380)
    st.plotly_chart(f, width="stretch")
    daily = df.groupby(df.time.dt.date).agg(b=("base_kw", "sum"), o=("opt_kw", "sum"), u=("units", "sum"))
    daily = daily[daily.u > 0]
    st.line_chart(pd.DataFrame({"Baseline SEC": daily.b / daily.u, "Optimised SEC": daily.o / daily.u}), y_label="kWh/unit")

with tabs[3]:
    rng = np.random.default_rng(3)
    d = np.arange(60)
    cur = 100 + rng.normal(0, .8, 60) + np.where(d > 35, (d - 35) * 0.45, 0)
    vib = 2.0 + rng.normal(0, .08, 60) + np.where(d > 40, (d - 40) * 0.07, 0)
    ew = pd.Series(cur).ewm(span=7).mean()
    z = (cur - cur[:30].mean()) / cur[:30].std()
    alarm = int(np.argmax(z > 3)) if (z > 3).any() else None
    f = go.Figure()
    f.add_scatter(x=d, y=cur, name="Motor M4 current (A)", line=dict(color="#94a3b8"))
    f.add_scatter(x=d, y=ew, name="EWMA trend", line=dict(color="#12A06B"))
    if alarm: f.add_vline(x=alarm, line_color="#D64545", annotation_text="Early alert")
    f.add_vline(x=58, line_dash="dot", annotation_text="Projected failure")
    f.update_layout(height=340, title="Motor M4: current signature drift", xaxis_title="day")
    st.plotly_chart(f, width="stretch")
    st.line_chart(pd.DataFrame({"Vibration RMS (mm/s)": vib}))
    if alarm: st.warning(f"Early alert on day {alarm}, about {58-alarm} days before projected failure: schedule a bearing check at the next planned stop.")

with tabs[4]:
    st.markdown("Shift a movable batch (pre-heat) out of the Rs/kWh peak window while respecting the deadline.")
    mv = st.slider("Movable load (kW)", 0, 100, 40)
    hrs = st.slider("Hours per day it can move", 0, 4, 4)
    prof = df.groupby(df.time.dt.hour).tariff.mean()
    save = mv * hrs * (prof.loc[18:21].mean() - prof.loc[22:23].mean()) * 26
    st.metric("Monthly cost saving from shifting (Rs)", f"{save:,.0f}")
    st.bar_chart(prof, y_label="Rs/kWh by hour")

with tabs[5]:
    st.markdown("**Scope 2 (grid) and Scope 1 (fuel) per product unit**, exportable for buyer audits (CBAM / BRSR).")
    fuel_l = st.number_input("Diesel/FO burned (litres/month)", 0, 50000, 1500, 100)
    s2b, s2o = bk * ef / 1000, ok * ef / 1000
    s1 = fuel_l * 2.68 / 1000  # approx kgCO2/litre diesel
    led = pd.DataFrame({"Baseline": [s2b, s1, s2b + s1, (s2b + s1) * 1000 / U],
                        "Optimised": [s2o, s1, s2o + s1, (s2o + s1) * 1000 / U]},
                       index=["Scope 2 (tCO2e)", "Scope 1 (tCO2e)", "Total (tCO2e)", "Intensity (kgCO2e/unit)"])
    st.dataframe(led.style.format("{:,.2f}"), width="stretch")
    st.download_button("Download carbon report (CSV)", led.to_csv().encode(), "carbon_report.csv")

with tabs[6]:
    bill = st.number_input("Annual energy bill (Rs lakh)", 5.0, 500.0, 30.0, 5.0)
    sv = st.slider("Realised savings (%)", 3, 20, 7)
    capex = st.number_input("Install cost (Rs lakh)", .5, 5.0, 1.5, .1)
    saas = st.number_input("SaaS (Rs/month)", 0, 20000, 3000, 500)
    net = bill * 100000 * sv / 100 - saas * 12
    pb = capex * 100000 / net * 12 if net > 0 else float("inf")
    a, b2, c2 = st.columns(3)
    a.metric("Annual saving (Rs)", f"{bill*1e5*sv/100:,.0f}")
    b2.metric("Net of SaaS (Rs)", f"{net:,.0f}")
    c2.metric("Payback (months)", f"{pb:.1f}")
    st.caption("Shared-savings alternative: zero capex, 30% of verified savings for 24 months.")
