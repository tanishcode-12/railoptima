import streamlit as st
import pandas as pd
import numpy as np
import os
from sklearn.linear_model import LinearRegression
import io
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go


@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join(os.path.dirname(__file__),
                     "railoptima_master.csv"), dtype={'train_number': str})
    df = df.drop_duplicates().dropna()
    return df


CO2_PER_KM = 12.0

STATION_COORDS = {
    # Maharashtra
    "Chhatrapati Shivaji Maharaj Terminus": (18.9398, 72.8355),
    "Mumbai Central":                       (18.9690, 72.8194),
    "PUNE JN":                              (18.5204, 73.8567),
    "NAGPUR":                               (21.1458, 79.0882),
    "C SHAHU M RAJ KOLHAPUR TERM":          (16.7050, 74.2433),
    "C SHAHU M RAJ K...":                   (16.7050, 74.2433),
    # Delhi / NCR
    "NEW DELHI":                            (28.6448, 77.2167),
    "OLD DELHI":                            (28.6580, 77.2310),
    "REWARI":                               (28.1927, 76.6194),
    "Loharu":                               (28.4333, 75.8000),
    "SAHARANPUR":                           (29.9640, 77.5460),
    # Rajasthan / Gujarat
    "JAIPUR":                               (26.9124, 75.7873),
    "AHMEDABAD JN":                         (23.0225, 72.5714),
    "MAHESANA JN":                          (23.5996, 72.3714),
    "RATLAM JN":                            (23.3315, 75.0367),
    # Punjab / Himachal
    "AMRITSAR JN":                          (31.6340, 74.8723),
    "Shimla":                               (31.1048, 77.1734),
    "Kalka":                                (30.8406, 76.9468),
    # UP / Bihar
    "LUCKNOW":                              (26.8467, 80.9462),
    "PATNA JN":                             (25.5941, 85.1376),
    "GAYA JN":                              (24.7955, 85.0000),
    "GONDA JN":                             (27.1333, 81.9667),
    "SAHARSA JN":                           (25.8833, 86.6000),
    "SAKRI JN":                             (26.3500, 86.0833),
    "NIRMALI":                              (26.3167, 86.5833),
    "Nirmali":                              (26.3167, 86.5833),
    "FORBESGANJ":                           (26.3000, 87.2667),
    "KATIHAR JN":                           (25.5500, 87.5667),
    "JOGBANI":                              (26.3333, 87.2667),
    # West Bengal
    "HOWRAH JN":                            (22.5839, 88.3424),
    "KOLKATA SEALDAH":                      (22.5626, 88.3700),
    "BARDDHAMAN JN":                        (23.2324, 87.8615),
    "ASANSOL JN":                           (23.6833, 86.9667),
    "PANSKURA":                             (22.4167, 87.7000),
    "AZIMGANJ JN":                          (24.0667, 88.2667),
    "KATWA":                                (23.6500, 88.1333),
    "Lalgola":                              (24.4167, 88.2500),
    "Gede":                                 (23.9667, 88.5667),
    # Odisha
    "PURI":                                 (19.8135, 85.8312),
    # MP / Chhattisgarh
    "JABALPUR":                             (23.1815, 79.9864),
    "Balaghat Junction":                    (21.8167, 80.1833),
    "Mhow":                                 (22.5500, 75.7667),
    "Anand Nagar":                          (21.8333, 80.3500),
    # Andhra / Telangana
    "SULLURUPETA":                          (13.7167, 79.9500),
    "HYDERABAD DECCAN":                     (17.3850, 78.4867),
    # Tamil Nadu
    "CHENNAI CENTRAL":                      (13.0827, 80.2750),
    "CHENNAI BEACH":                        (13.1067, 80.2900),
    "CHENGALPATTU":                         (12.6931, 79.9768),
    "COIMBATORE JN":                        (11.0018, 76.9628),
    "NAGERCOIL JN":                         (8.1833,  77.4333),
    # Karnataka
    "BANGALORE CITY JN":                    (12.9791, 77.5718),
    "MYSORE JN":                            (12.2958, 76.6394),
    "HUBLI JN":                             (15.3647, 75.1240),
    # Kerala
    "KOLLAM JN":                            (8.8932,  76.6141),
    # Goa
    "MADGAON":                              (15.3573, 73.9946),
}


def inject_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Nunito:wght@400;600;700&display=swap');
    html, body, [class*="css"] { background-color: #0a0a0f !important; color: #e0e0e0 !important; font-family: 'Nunito', sans-serif !important; }
    h1, h2, h3 { font-family: 'Rajdhani', sans-serif !important; }
    .page-title { font-family: 'Rajdhani', sans-serif; font-size: 2.5rem; font-weight: 700; background: linear-gradient(135deg, #a855f7, #6366f1, #00d9f5); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.2rem; }
    .section-title { font-family: 'Rajdhani', sans-serif; font-size: 1.8rem; font-weight: 700; margin: 1.5rem 0 0.8rem 0; }
    .station-badge { display: inline-block; background: linear-gradient(135deg, #a855f7, #6366f1); color: #fff; border-radius: 20px; padding: 0.3rem 1rem; font-size: 0.9rem; font-weight: 700; margin-bottom: 1.5rem; }
    .stat-card { background: #12121a; border-radius: 14px; padding: 1.2rem 1.5rem; border: 1px solid #1e1e2e; text-align: center; margin-bottom: 1rem; }
    .stat-card .number { font-family: 'Rajdhani', sans-serif; font-size: 2rem; font-weight: 700; }
    .stat-card .label { color: #888; font-size: 0.85rem; }
    .green-card { border-color: #22c55e !important; } .green-card .number { color: #22c55e; }
    .teal-card  { border-color: #00d9f5 !important; } .teal-card .number  { color: #00d9f5; }
    .purple-card{ border-color: #a855f7 !important; } .purple-card .number{ color: #a855f7; }
    .orange-card{ border-color: #f59e0b !important; } .orange-card .number{ color: #f59e0b; }
    div[data-testid="stMetricValue"] { color: #00d9f5 !important; font-family: 'Rajdhani', sans-serif !important; font-size: 1.6rem !important; font-weight: 700 !important; }
    div[data-testid="stMetricLabel"] { color: #888 !important; font-size: 0.8rem !important; }
    .stButton > button { background: linear-gradient(135deg, #a855f7, #6366f1) !important; color: #fff !important; font-weight: 700 !important; border: none !important; border-radius: 8px !important; font-family: 'Nunito', sans-serif !important; }
    .stButton > button:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }
    .predict-btn > button { background: linear-gradient(135deg, #f59e0b, #ef4444) !important; }
    .carbon-btn  > button { background: linear-gradient(135deg, #22c55e, #00d9f5) !important; color: #0a0a0f !important; }
    .export-btn  > button { background: linear-gradient(135deg, #00d9f5, #6366f1) !important; }
    .stSelectbox div[data-baseweb="select"], .stTextInput input { background: #12121a !important; border-color: #2a2a3a !important; color: #e0e0e0 !important; }
    .info-box    { background: #0d1a2a; border: 1px solid #00d9f5; border-radius: 10px; padding: 1rem; margin: 0.5rem 0; }
    .success-box { background: #0d2010; border: 1px solid #22c55e; border-radius: 10px; padding: 1rem; margin: 0.5rem 0; }
    .map-caption { color: #888; font-size: 0.8rem; text-align: center; margin-top: 0.3rem; }
    hr { border-color: #1e1e2e !important; }
    </style>
    """, unsafe_allow_html=True)


def show_page2():
    inject_styles()
    df = load_data()

    selected_station = st.session_state.get("selected_station", None)

    st.markdown('<div class="page-title">📊 Analytics & Insights</div>',
                unsafe_allow_html=True)

    if selected_station:
        st.markdown(
            f'<div class="station-badge">📍 Showing data for: {selected_station}</div>', unsafe_allow_html=True)
        station_df = df[(df["source_station"] == selected_station) | (
            df["destination_station"] == selected_station)].copy()
    else:
        st.markdown('<div class="station-badge">📍 All Stations</div>',
                    unsafe_allow_html=True)
        station_df = df.copy()

    # ── Quick Stats ───────────────────────────────────────
    total_trains = station_df["train_number"].nunique()
    avg_fare = station_df["fare"].mean()
    avg_duration = station_df["duration_hours"].mean()
    total_routes = station_df.groupby(
        ["source_station", "destination_station"]).ngroups

    s1, s2, s3, s4 = st.columns(4)
    s1.markdown(
        f'<div class="stat-card teal-card"><div class="number">{total_trains}</div><div class="label">Unique Trains</div></div>', unsafe_allow_html=True)
    s2.markdown(
        f'<div class="stat-card green-card"><div class="number">₹{avg_fare:.0f}</div><div class="label">Avg Fare</div></div>', unsafe_allow_html=True)
    s3.markdown(
        f'<div class="stat-card purple-card"><div class="number">{avg_duration:.1f} hrs</div><div class="label">Avg Duration</div></div>', unsafe_allow_html=True)
    s4.markdown(
        f'<div class="stat-card orange-card"><div class="number">{total_routes}</div><div class="label">Routes</div></div>', unsafe_allow_html=True)

    st.divider()

    # ── 💰 Fare Trends by Class — Line Chart ─────────────
    st.markdown('<div class="section-title">💰 Fare Trends by Class</div>',
                unsafe_allow_html=True)
    sdf = station_df.copy()
    sdf["dist_bin"] = pd.cut(
        sdf["distance_km"],
        bins=[0, 100, 250, 500, 750, 1000, 1500, 2000, 5000],
        labels=["0-100", "100-250", "250-500", "500-750",
                "750-1k", "1k-1.5k", "1.5k-2k", "2k+"]
    )
    fare_line = sdf.groupby(["dist_bin", "class_type"])[
        "fare"].mean().reset_index()
    fare_line.columns = ["Distance (km)", "Class", "Avg Fare (₹)"]
    fig_line = px.line(
        fare_line, x="Distance (km)", y="Avg Fare (₹)", color="Class", markers=True,
        color_discrete_map={"SL": "#00f5a0", "3A": "#00d9f5", "2A": "#a855f7"},
        template="plotly_dark"
    )
    fig_line.update_layout(
        paper_bgcolor="#12121a", plot_bgcolor="#0a0a0f",
        font=dict(family="Nunito", color="#e0e0e0"),
        legend=dict(bgcolor="#12121a", bordercolor="#2a2a3a"),
        margin=dict(l=20, r=20, t=20, b=20),
    )
    fig_line.update_traces(line=dict(width=3), marker=dict(size=7))
    st.plotly_chart(fig_line, use_container_width=True)
    st.caption("SL = Sleeper | 3A = 3-Tier AC | 2A = 2-Tier AC")

    st.divider()

    # ── 🏙️ Top Stations — Horizontal Bar Chart ───────────
    st.markdown('<div class="section-title">🏙️ Top Stations</div>',
                unsafe_allow_html=True)
    ts1, ts2 = st.columns(2)

    with ts1:
        st.markdown("**📤 Top Departure Stations**")
        top_src = station_df["source_station"].value_counts().head(
            8).reset_index()
        top_src.columns = ["Station", "Count"]
        fig_src = px.bar(top_src, x="Count", y="Station", orientation="h",
                         color="Count", color_continuous_scale=["#1e1e2e", "#00d9f5"], template="plotly_dark")
        fig_src.update_layout(paper_bgcolor="#12121a", plot_bgcolor="#0a0a0f",
                              font=dict(family="Nunito", color="#e0e0e0"), coloraxis_showscale=False,
                              margin=dict(l=10, r=10, t=10, b=10), yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_src, use_container_width=True)

    with ts2:
        st.markdown("**📥 Top Arrival Stations**")
        top_dst = station_df["destination_station"].value_counts().head(
            8).reset_index()
        top_dst.columns = ["Station", "Count"]
        fig_dst = px.bar(top_dst, x="Count", y="Station", orientation="h",
                         color="Count", color_continuous_scale=["#1e1e2e", "#a855f7"], template="plotly_dark")
        fig_dst.update_layout(paper_bgcolor="#12121a", plot_bgcolor="#0a0a0f",
                              font=dict(family="Nunito", color="#e0e0e0"), coloraxis_showscale=False,
                              margin=dict(l=10, r=10, t=10, b=10), yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_dst, use_container_width=True)

    st.divider()

    # ── 🗺️ Busiest Routes — Geographic Arc Map ───────────
    st.markdown('<div class="section-title">🗺️ Busiest Routes</div>',
                unsafe_allow_html=True)

    busiest = (
        station_df.groupby(["source_station", "destination_station"])
        .size().reset_index(name="count")
        .sort_values("count", ascending=False).head(15)
    )

    arc_data = []
    point_data = []
    seen = set()

    for _, row in busiest.iterrows():
        src, dst = row["source_station"], row["destination_station"]
        if src in STATION_COORDS and dst in STATION_COORDS:
            s_lat, s_lon = STATION_COORDS[src]
            d_lat, d_lon = STATION_COORDS[dst]
            arc_data.append({
                "source_station": src, "destination_station": dst,
                "count": int(row["count"]),
                "src_lat": s_lat, "src_lon": s_lon,
                "dst_lat": d_lat, "dst_lon": d_lon,
            })
            for name, lat, lon in [(src, s_lat, s_lon), (dst, d_lat, d_lon)]:
                if name not in seen:
                    point_data.append(
                        {"station": name, "lat": lat, "lon": lon})
                    seen.add(name)

    if arc_data:
        arc_df = pd.DataFrame(arc_data)
        point_df = pd.DataFrame(point_data)
        max_c = arc_df["count"].max()
        arc_df["width"] = (arc_df["count"] / max_c * 8).clip(lower=1)

        arc_layer = pdk.Layer("ArcLayer", data=arc_df,
                              get_source_position=["src_lon", "src_lat"],
                              get_target_position=["dst_lon", "dst_lat"],
                              get_source_color=[0, 245, 160, 200],
                              get_target_color=[168, 85, 247, 200],
                              get_width="width", auto_highlight=True, pickable=True)

        scatter_layer = pdk.Layer("ScatterplotLayer", data=point_df,
                                  get_position=["lon", "lat"],
                                  get_color=[0, 217, 245, 230],
                                  get_radius=30000, pickable=True)

        text_layer = pdk.Layer("TextLayer", data=point_df,
                               get_position=["lon", "lat"], get_text="station",
                               get_size=11, get_color=[255, 255, 255, 200],
                               get_alignment_baseline="'bottom'")

        view = pdk.ViewState(
            latitude=20.5937, longitude=78.9629, zoom=4.2, pitch=40)

        deck = pdk.Deck(
            layers=[arc_layer, scatter_layer, text_layer],
            initial_view_state=view,
            map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
            tooltip={
                "html": "<b>{source_station}</b> → <b>{destination_station}</b><br/>Trains: {count}",
                "style": {"backgroundColor": "#12121a", "color": "#e0e0e0", "fontFamily": "Nunito"}
            }
        )
        st.pydeck_chart(deck)
        st.markdown(
            '<p class="map-caption">🟢 Source → 🟣 Destination | Arc thickness = train frequency</p>', unsafe_allow_html=True)

        with st.expander("📋 View Route Table"):
            disp = busiest[["source_station",
                            "destination_station", "count"]].copy()
            disp.columns = ["From", "To", "Train Count"]
            st.dataframe(disp, use_container_width=True, hide_index=True)
    else:
        st.info(
            "Not enough coordinate data for this selection. Showing bar chart instead.")
        busiest["Route"] = busiest["source_station"] + \
            " → " + busiest["destination_station"]
        st.bar_chart(busiest.set_index("Route")["count"])

    st.divider()

    # ── ⚠️ Delay Risk — Pie + Stacked Bar ────────────────
    st.markdown('<div class="section-title">⚠️ Delay Risk Overview</div>',
                unsafe_allow_html=True)

    def delay_risk(row):
        if row["stops"] > 15:
            return "High"
        if row["distance_km"] > 1000:
            return "Medium"
        return "Low"

    station_df = station_df.copy()
    station_df["delay_risk"] = station_df.apply(delay_risk, axis=1)
    risk_counts = station_df["delay_risk"].value_counts().reset_index()
    risk_counts.columns = ["Risk Level", "Count"]

    dr1, dr2 = st.columns(2)

    with dr1:
        fig_pie = px.pie(risk_counts, names="Risk Level", values="Count",
                         color="Risk Level",
                         color_discrete_map={
                             "Low": "#22c55e", "Medium": "#f59e0b", "High": "#ef4444"},
                         hole=0.45, template="plotly_dark")
        fig_pie.update_layout(
            paper_bgcolor="#12121a",
            font=dict(family="Nunito", color="#e0e0e0"),
            legend=dict(bgcolor="#12121a", bordercolor="#2a2a3a"),
            margin=dict(l=10, r=10, t=10, b=10))
        fig_pie.update_traces(textfont_size=13, pull=[0.03, 0.03, 0.05])
        st.plotly_chart(fig_pie, use_container_width=True)

    with dr2:
        st.markdown("**Delay Risk by Seat Class**")
        risk_class = station_df.groupby(
            ["class_type", "delay_risk"]).size().reset_index(name="count")
        fig_stack = px.bar(risk_class, x="class_type", y="count", color="delay_risk",
                           barmode="stack",
                           color_discrete_map={
                               "Low": "#22c55e", "Medium": "#f59e0b", "High": "#ef4444"},
                           template="plotly_dark",
                           labels={"class_type": "Class", "count": "Count", "delay_risk": "Risk"})
        fig_stack.update_layout(
            paper_bgcolor="#12121a", plot_bgcolor="#0a0a0f",
            font=dict(family="Nunito", color="#e0e0e0"),
            legend=dict(bgcolor="#12121a", bordercolor="#2a2a3a"),
            margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_stack, use_container_width=True)

    st.divider()

    # ── 🔮 Price Predictor — Unchanged ───────────────────
    st.markdown('<div class="section-title">🔮 Price Predictor</div>',
                unsafe_allow_html=True)
    st.markdown('<p style="color:#aaa;">Predict expected fare based on distance and class using ML.</p>',
                unsafe_allow_html=True)

    @st.cache_resource
    def train_price_model(data):
        models = {}
        for cls in data["class_type"].unique():
            sub = data[data["class_type"] == cls]
            m = LinearRegression()
            m.fit(sub[["distance_km"]].values, sub["fare"].values)
            models[cls] = m
        return models

    price_models = train_price_model(df)

    pp1, pp2 = st.columns(2)
    with pp1:
        pred_dist = st.slider("Distance (km)", 50, 4500, 500, step=50)
    with pp2:
        pred_class = st.selectbox("Seat Class", sorted(
            df["class_type"].unique()), key="pred_class")

    st.markdown('<div class="predict-btn">', unsafe_allow_html=True)
    if st.button("💡 Predict Fare", use_container_width=True):
        predicted = price_models[pred_class].predict([[pred_dist]])[0]
        st.markdown(
            f'<div class="info-box">💰 Estimated Fare for <b>{pred_dist} km</b> in <b>{pred_class}</b>: <span style="color:#00d9f5;font-size:1.4rem;font-family:Rajdhani,sans-serif;font-weight:700;">₹{predicted:.0f}</span></div>', unsafe_allow_html=True)
        all_preds = {cls: round(price_models[cls].predict(
            [[pred_dist]])[0], 0) for cls in price_models}
        pred_df = pd.DataFrame(list(all_preds.items()), columns=[
                               "Class", "Predicted Fare (₹)"])
        st.table(pred_df)
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # ── 🌱 Carbon Footprint Estimator ─────────────────────
    st.markdown('<div class="section-title">🌱 Carbon Footprint Estimator</div>',
                unsafe_allow_html=True)
    st.markdown('<p style="color:#aaa;">Estimate your CO₂ emissions and compare with car travel.</p>',
                unsafe_allow_html=True)

    cf1, cf2, cf3 = st.columns(3)
    with cf1:
        cf_source = st.selectbox("From Station", sorted(
            df["source_station"].unique()), key="cf_src")
    with cf2:
        cf_dest = st.selectbox("To Station",   sorted(
            df["destination_station"].unique()), key="cf_dst")
    with cf3:
        cf_pass = st.number_input("Passengers", 1, 6, 1, key="cf_pass")

    st.markdown('<div class="carbon-btn">', unsafe_allow_html=True)
    if st.button("🌍 Calculate Carbon Footprint", use_container_width=True):
        route = df[(df["source_station"] == cf_source) &
                   (df["destination_station"] == cf_dest)]
        if route.empty:
            st.warning("No route found between these stations.")
        else:
            dist = route["distance_km"].iloc[0]
            co2_kg = (CO2_PER_KM * dist * cf_pass) / 1000
            car_co2 = (dist * cf_pass * 120) / 1000
            saving = car_co2 - co2_kg
            cg1, cg2, cg3 = st.columns(3)
            cg1.metric("📏 Distance",   f"{dist:.0f} km")
            cg2.metric("🚆 Train CO₂",  f"{co2_kg:.2f} kg")
            cg3.metric("🌿 Saved vs Car", f"{saving:.2f} kg")
            st.markdown(f"""
            <div class="success-box">
                🚗 By car: <b>{car_co2:.2f} kg CO₂</b> &nbsp;|&nbsp;
                🚆 By train: <b>{co2_kg:.2f} kg CO₂</b><br>
                🌿 You save <b style="color:#22c55e">{saving:.2f} kg CO₂</b> by choosing the train!
            </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # ── 📥 Export Train Data ──────────────────────────────
    st.markdown('<div class="section-title">📥 Export Train Data</div>',
                unsafe_allow_html=True)
    st.markdown('<p style="color:#aaa;">Download filtered train data as a CSV file.</p>',
                unsafe_allow_html=True)

    exp1, exp2 = st.columns(2)
    with exp1:
        exp_src = st.selectbox("From (optional)", [
                               "All"] + sorted(df["source_station"].unique()), key="exp_src")
    with exp2:
        exp_dst = st.selectbox("To (optional)",   [
                               "All"] + sorted(df["destination_station"].unique()), key="exp_dst")

    export_df = df.copy()
    if exp_src != "All":
        export_df = export_df[export_df["source_station"] == exp_src]
    if exp_dst != "All":
        export_df = export_df[export_df["destination_station"] == exp_dst]

    st.markdown(
        f'<p style="color:#a855f7;font-weight:700;">{len(export_df)} records ready to export</p>', unsafe_allow_html=True)

    csv_buf = io.StringIO()
    export_df.to_csv(csv_buf, index=False)

    st.markdown('<div class="export-btn">', unsafe_allow_html=True)
    st.download_button("⬇️ Download CSV", data=csv_buf.getvalue(),
                       file_name="railoptima_export.csv", mime="text/csv", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
