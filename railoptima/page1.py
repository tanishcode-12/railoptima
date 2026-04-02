import streamlit as st
import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from database import save_favorite, get_favorites, remove_favorite


@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join(os.path.dirname(__file__),
                     "railoptima_master.csv"), dtype={'train_number': str})
    df = df.drop_duplicates().dropna()
    return df


@st.cache_resource
def train_model(data):
    features = ['fare', 'duration_min', 'stops', 'distance_km']
    X = data[features]
    X_norm = (X - X.min()) / (X.max() - X.min())
    utility = (X_norm['fare'] * 0.4) + \
        (X_norm['duration_min'] * 0.4) + (X_norm['stops'] * 0.2)
    labels = (utility <= np.nanpercentile(utility, 30)).astype(int)
    X_train, X_test, y_train, y_test = train_test_split(
        X, labels, test_size=0.2, random_state=42)
    model = RandomForestClassifier(
        n_estimators=100, max_depth=8, random_state=42)
    model.fit(X_train, y_train)
    return model


@st.cache_data
def build_station_maps(df):
    src = df[["source_station", "source_code"]].drop_duplicates(
    ).set_index("source_station")["source_code"].to_dict()
    dst = df[["destination_station", "destination_code"]].drop_duplicates(
    ).set_index("destination_station")["destination_code"].to_dict()
    combined = {**src, **dst}
    name_to_label = {
        name: f"{name} ({code.strip()})" for name, code in combined.items()}
    label_to_name = {v: k for k, v in name_to_label.items()}
    return name_to_label, label_to_name


def inject_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Nunito:wght@400;600;700&display=swap');
    html, body, [class*="css"] { background-color: #0a0a0f !important; color: #e0e0e0 !important; font-family: 'Nunito', sans-serif !important; }
    h1, h2, h3 { font-family: 'Rajdhani', sans-serif !important; }
    .section-title { font-family: 'Rajdhani', sans-serif; font-size: 1.8rem; font-weight: 700; margin-bottom: 1rem; }
    .card { background: #12121a; border-radius: 14px; padding: 1.2rem 1.5rem; border: 1px solid #1e1e2e; margin-bottom: 1rem; }
    .best-train-card { background: linear-gradient(135deg, #0d1f1a, #0d1a2a); border: 1px solid #00f5a0; border-radius: 14px; padding: 1.2rem 1.5rem; margin-bottom: 1rem; }
    .best-train-card h3 { color: #00f5a0; margin: 0 0 0.3rem 0; font-size: 1.4rem; }
    .best-train-card p { color: #aaa; margin: 0; font-size: 0.9rem; }
    .risk-low { background: linear-gradient(135deg, #0d2010, #0a1a0d); border: 1px solid #22c55e; border-radius: 10px; padding: 0.7rem 1rem; color: #22c55e; font-weight: 700; }
    .risk-medium { background: linear-gradient(135deg, #1f1a00, #1a1200); border: 1px solid #f59e0b; border-radius: 10px; padding: 0.7rem 1rem; color: #f59e0b; font-weight: 700; }
    .risk-high { background: linear-gradient(135deg, #1f0808, #180505); border: 1px solid #ef4444; border-radius: 10px; padding: 0.7rem 1rem; color: #ef4444; font-weight: 700; }
    .reason-chip { display: inline-block; background: #1a1a2e; border: 1px solid #a855f7; color: #a855f7; border-radius: 20px; padding: 0.3rem 0.9rem; font-size: 0.85rem; margin: 0.2rem; font-weight: 600; }
    .fav-row { background: #12121a; border: 1px solid #1e1e2e; border-radius: 10px; padding: 0.7rem 1rem; margin-bottom: 0.5rem; }
    .stTextInput input, .stSelectbox div[data-baseweb="select"] { background: #12121a !important; border-color: #2a2a3a !important; color: #e0e0e0 !important; }
    div[data-testid="stMetricValue"] { color: #00d9f5 !important; font-family: 'Rajdhani', sans-serif !important; font-size: 1.6rem !important; font-weight: 700 !important; }
    div[data-testid="stMetricLabel"] { color: #888 !important; font-size: 0.8rem !important; }
    .stButton > button { background: linear-gradient(135deg, #00f5a0, #00d9f5) !important; color: #0a0a0f !important; font-weight: 700 !important; border: none !important; border-radius: 8px !important; font-family: 'Nunito', sans-serif !important; transition: all 0.2s ease !important; }
    .stButton > button:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }
    .save-btn > button { background: linear-gradient(135deg, #f59e0b, #ef4444) !important; }
    .visualize-btn > button { background: linear-gradient(135deg, #a855f7, #6366f1) !important; color: #fff !important; }
    .stDataFrame { border-radius: 10px !important; }
    hr { border-color: #1e1e2e !important; }
    .page-title { font-family: 'Rajdhani', sans-serif; font-size: 2.5rem; font-weight: 700; background: linear-gradient(135deg, #00f5a0, #00d9f5); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.2rem; }
    </style>
    """, unsafe_allow_html=True)


def show_page1():
    inject_styles()
    df = load_data()
    model = train_model(df)
    name_to_label, label_to_name = build_station_maps(df)

    st.markdown('<div class="page-title">🚆 Train Planner</div>',
                unsafe_allow_html=True)
    st.markdown('<p style="color:#888;margin-bottom:1.5rem;">Smart AI-powered train recommendations for your journey</p>', unsafe_allow_html=True)

    # ─── TRAIN SEARCH ───────────────────────────────────────
    st.markdown('<div class="section-title">🔎 Train Search</div>',
                unsafe_allow_html=True)
    search = st.text_input("Search by Train Name or Number",
                           placeholder="e.g. Rajdhani or 12301")
    if search:
        res = df[
            df["train_name"].str.contains(search, case=False) |
            df["train_number"].astype(str).str.contains(search)
        ]
        if res.empty:
            st.warning("No trains found matching your search.")
        else:
            st.dataframe(res.head(20), use_container_width=True)

    st.divider()

    # ─── AI RECOMMENDATION ──────────────────────────────────
    st.markdown('<div class="section-title">🎯 AI Train Recommendation</div>',
                unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    # From Station with code labels
    all_sources = sorted(df["source_station"].unique())
    source_labels = [name_to_label.get(s, s) for s in all_sources]
    with c1:
        source_label = st.selectbox(
            "From Station", source_labels, key="from_station")
        source = label_to_name.get(source_label, source_label)

    # To Station — filtered to only show available destinations from selected source
    available_dests = sorted(
        df[df["source_station"] == source]["destination_station"].unique())
    dest_labels = [name_to_label.get(d, d) for d in available_dests]
    with c2:
        dest_label = st.selectbox("To Station", dest_labels, key="to_station")
        dest = label_to_name.get(dest_label, dest_label)

    with c3:
        class_type = st.selectbox(
            "Seat Class", sorted(df["class_type"].unique()))

    col_date, col_pass = st.columns(2)
    with col_date:
        travel_date = st.date_input("Travel Date")
    with col_pass:
        passengers = st.number_input("Passengers", 1, 6, 1)

    if st.button("🔍 Generate Recommendation", use_container_width=True):
        res = df[
            (df["source_station"] == source) &
            (df["destination_station"] == dest) &
            (df["class_type"] == class_type)
        ].copy()

        if res.empty:
            st.warning("⚠️ No trains found for this route.")
            st.markdown("**💡 Similar Routes You Might Consider**")
            similar = df[
                (df["source_station"] == source) | (
                    df["destination_station"] == dest)
            ][["train_name", "train_number", "source_station", "destination_station", "class_type", "fare"]].drop_duplicates().head(5)
            if not similar.empty:
                st.dataframe(similar, use_container_width=True)
        else:
            feats = ['fare', 'duration_min', 'stops', 'distance_km']
            res["score"] = model.predict_proba(res[feats])[:, 1]
            res = res.sort_values("score", ascending=False)
            top = res.iloc[0]

            st.session_state.top_train = {
                "train_number":   top["train_number"],
                "train_name":     top["train_name"],
                "fare":           top["fare"],
                "duration_hours": top["duration_hours"],
                "stops":          int(top["stops"]),
                "distance_km":    top["distance_km"],
                "departure_time": top["departure_time"],
                "arrival_time":   top["arrival_time"],
                "duration_min":   top["duration_min"],
            }
            st.session_state.rec_res = res.copy()
            st.session_state.rec_passengers = passengers
            st.session_state.rec_source = source
            st.session_state.rec_dest = dest

    # ── Show results from session state ──
    if "top_train" in st.session_state and st.session_state.top_train:
        top = st.session_state.top_train
        res = st.session_state.get("rec_res", pd.DataFrame())
        passengers = st.session_state.get("rec_passengers", 1)

        st.markdown(f"""
        <div class="best-train-card">
            <h3>🥇 {top['train_name']}</h3>
            <p>Train No: {top['train_number']} &nbsp;|&nbsp; 🕐 {top['departure_time']} → {top['arrival_time']}</p>
        </div>
        """, unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("💰 Fare / person", f"₹{top['fare']:.0f}")
        m2.metric("⏱ Duration",       f"{top['duration_hours']} hrs")
        m3.metric("🛑 Stops",          top["stops"])
        m4.metric("📏 Distance",       f"{top['distance_km']} km")

        if not res.empty:
            res2 = res.copy()
            res2["popularity_score"] = (
                (1 / res2["fare"]) * 0.4 +
                (1 / res2["duration_min"]) * 0.4 +
                (1 / (res2["stops"] + 1)) * 0.2
            ) * 100
            st.metric("⭐ Popularity Score",
                      f"{res2.iloc[0]['popularity_score']:.0f}/100")

        def delay_risk(t):
            if t["stops"] > 15:
                return "High"
            if t["distance_km"] > 1000:
                return "Medium"
            return "Low"

        risk = delay_risk(top)
        risk_class = {"Low": "risk-low",
                      "Medium": "risk-medium", "High": "risk-high"}[risk]
        risk_icon = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}[risk]
        st.markdown(
            f'<div class="{risk_class}">{risk_icon} Delay Risk: {risk.upper()}</div>', unsafe_allow_html=True)
        st.markdown("")

        st.markdown("**🤖 Why this train?**")
        reasons = []
        if not res.empty:
            if top["fare"] == res["fare"].min():
                reasons.append("✔ Lowest Fare")
            if top["duration_min"] == res["duration_min"].min():
                reasons.append("✔ Fastest")
            if top["stops"] == res["stops"].min():
                reasons.append("✔ Fewest Stops")
        if not reasons:
            reasons.append("✔ Best overall balance")
        st.markdown("".join(
            [f'<span class="reason-chip">{r}</span>' for r in reasons]), unsafe_allow_html=True)
        st.markdown("")

        # Budget Calculator
        st.markdown(
            '<div class="section-title" style="font-size:1.2rem;">💵 Budget Calculator</div>', unsafe_allow_html=True)
        bc1, bc2, bc3 = st.columns(3)
        bc1.metric("Passengers",      passengers)
        bc2.metric("Fare per Person",  f"₹{top['fare']:.0f}")
        bc3.metric("Total Fare",       f"₹{top['fare'] * passengers:.0f}")

        # Best Time to Travel
        if not res.empty:
            st.markdown(
                '<div class="section-title" style="font-size:1.2rem;">⏰ Best Time to Travel</div>', unsafe_allow_html=True)
            cheapest = res.loc[res["fare"].idxmin()]
            fastest = res.loc[res["duration_min"].idxmin()]
            bt1, bt2 = st.columns(2)
            bt1.info(
                f"💸 **Cheapest Departure:** {cheapest['departure_time']}\nTrain: {cheapest['train_name']}\nFare: ₹{cheapest['fare']:.0f}")
            bt2.info(
                f"⚡ **Fastest Departure:** {fastest['departure_time']}\nTrain: {fastest['train_name']}\nDuration: {fastest['duration_hours']} hrs")

        st.markdown("")
        save_col, _ = st.columns([1, 3])
        with save_col:
            if st.button("⭐ Save to Favorites"):
                save_favorite(st.session_state.username,
                              top["train_number"], top["train_name"])
                st.success(f"✅ {top['train_name']} saved to favorites!")

        if not res.empty:
            st.markdown(
                '<div class="section-title" style="font-size:1.2rem;">📋 Other Available Trains</div>', unsafe_allow_html=True)
            st.dataframe(
                res[["train_name", "train_number", "departure_time", "arrival_time",
                    "fare", "duration_hours", "stops", "score"]].head(10),
                use_container_width=True
            )

    st.divider()

    # ─── TRAIN COMPARISON ───────────────────────────────────
    st.markdown('<div class="section-title">⚖️ Train Comparison</div>',
                unsafe_allow_html=True)
    train_list = df["train_name"].unique()
    tc1, tc2 = st.columns(2)
    with tc1:
        t1 = st.selectbox("Train 1", train_list, key="t1")
    with tc2:
        t2 = st.selectbox("Train 2", train_list, key="t2")

    if st.button("🔄 Compare Trains", use_container_width=True):
        tr1 = df[df["train_name"] == t1].iloc[0]
        tr2 = df[df["train_name"] == t2].iloc[0]
        comp = pd.DataFrame({
            "Feature": ["Fare (₹)", "Duration (hrs)", "Stops", "Distance (km)"],
            t1: [tr1["fare"], tr1["duration_hours"], tr1["stops"], tr1["distance_km"]],
            t2: [tr2["fare"], tr2["duration_hours"],
                 tr2["stops"], tr2["distance_km"]]
        })
        st.table(comp)
        st.markdown("**🏆 Category Winners**")
        w1, w2, w3, w4 = st.columns(4)
        w1.metric("💰 Cheaper",      t1 if tr1["fare"] < tr2["fare"] else t2)
        w2.metric("⏱ Faster",
                  t1 if tr1["duration_min"] < tr2["duration_min"]else t2)
        w3.metric("🛑 Fewer Stops",  t1 if tr1["stops"] < tr2["stops"] else t2)
        w4.metric("📏 Shorter Route",
                  t1 if tr1["distance_km"] < tr2["distance_km"] else t2)

    st.divider()

    # ─── ROUTE INSIGHTS ─────────────────────────────────────
    st.markdown('<div class="section-title">📍 Route Insights</div>',
                unsafe_allow_html=True)
    st.markdown('<p style="color:#aaa;margin-bottom:1rem;">Select a station to explore detailed analytics on the next page.</p>', unsafe_allow_html=True)

    all_stations = sorted(set(df["source_station"].unique()) | set(
        df["destination_station"].unique()))
    all_station_labels = [name_to_label.get(s, s) for s in all_stations]
    sel_label = st.selectbox("🗺️ Select a Station to Explore",
                             all_station_labels, key="route_insights_station")
    selected_station = label_to_name.get(sel_label, sel_label)

    st.markdown('<div class="visualize-btn">', unsafe_allow_html=True)
    if st.button("📊 Visualize → Go to Analytics", use_container_width=True, key="visualize_btn"):
        st.session_state.selected_station = selected_station
        st.session_state.page = "📊 Analytics & Insights"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # ─── FAVORITES ──────────────────────────────────────────
    st.markdown('<div class="section-title">⭐ My Favorite Trains</div>',
                unsafe_allow_html=True)
    favs = get_favorites(st.session_state.username)
    if favs:
        for f in favs:
            col_fav, col_del = st.columns([5, 1])
            with col_fav:
                st.markdown(
                    f'<div class="card" style="padding:0.6rem 1rem;">🚆 <b>{f[1]}</b> <span style="color:#888;">({f[0]})</span></div>', unsafe_allow_html=True)
            with col_del:
                if st.button("❌", key=f"del_{f[0]}"):
                    remove_favorite(st.session_state.username, f[0])
                    st.rerun()
    else:
        st.info("No saved trains yet. Recommend a train and hit ⭐ Save!")
