# 🚆 RailOptima — AI-Powered Indian Railway Planner

A smart **Streamlit** web app that combines AI-driven train recommendations, real-time analytics, fare prediction, and carbon footprint estimation — all wrapped in a sleek dark-themed UI.

---

## 📌 Overview

Planning a train journey in India is overwhelming — hundreds of trains, multiple classes, varying fares, and unpredictable delays. RailOptima solves this by using a **Random Forest ML model** to intelligently recommend the best train for your route based on fare, duration, stops, and distance.

It also gives you interactive analytics, a price predictor, a geographic route map, and even an eco-friendly carbon footprint calculator — all in one place.

🔗 **GitHub Repository:** [tanishcode-12/railoptima](https://github.com/tanishcode-12/railoptima)

---

## ✨ Features

- 🔐 **Secure User Authentication** — Register and log in with bcrypt-hashed passwords stored in a local SQLite database.
- 🤖 **AI Train Recommendation** — A trained `RandomForestClassifier` scores trains by fare, duration, stops, and distance to surface the best option for your journey.
- 🔎 **Train Search** — Instantly search trains by name or number across the full dataset.
- ⚖️ **Train Comparison Tool** — Compare any two trains head-to-head across fare, speed, stops, and route distance.
- ⭐ **Favorites System** — Save recommended trains to a personal favorites list, backed by SQLite persistence.
- 📊 **Analytics & Insights Dashboard** — Explore fare trends by class, top departure/arrival stations, and delay risk breakdowns via rich Plotly charts.
- 🗺️ **Geographic Arc Map** — Visualize the busiest train routes across India on an interactive 3D PyDeck map.
- 🔮 **ML Fare Predictor** — Predict expected ticket prices for any distance and seat class using Linear Regression.
- 🌱 **Carbon Footprint Estimator** — Calculate your CO₂ emissions per journey and see how much you save versus travelling by car.
- 📥 **Data Export** — Filter and download train data as a CSV file directly from the app.

---

## 🗂️ Project Structure

```
📦 railoptima/
├── 🚀 app.py                    # Main entry point — routing, sidebar, login gate
├── 🔐 login.py                  # Login & registration UI (Streamlit page)
├── 🗄️ database.py               # SQLite setup, user auth, favorites CRUD
├── 🚆 page1.py                  # Train Planner — search, AI recommendation, comparison
├── 📊 page2.py                  # Analytics & Insights — charts, map, predictor, export
├── 📋 railoptima_master.csv     # Master dataset of Indian trains
└── 🛑 .gitignore
```

---

## ⚙️ Installation

### 🧰 Prerequisites

- 🐍 Python 3.8 or higher
- 📦 pip

### 🪜 Steps

**📥 Clone the repository**
```bash
git clone https://github.com/tanishcode-12/railoptima.git
cd railoptima/railoptima
```

**📦 Install dependencies**
```bash
pip install -r requirements.txt
```

> ⚠️ If you don't have a `requirements.txt`, install manually:
> ```bash
> pip install streamlit pandas numpy scikit-learn bcrypt plotly pydeck
> ```

**▶️ Run the app**
```bash
streamlit run app.py
```

**🌐 Open in browser**

The app will automatically open at `http://localhost:8501`

> ⚠️ Make sure `railoptima_master.csv` is in the same directory as `app.py` before launching.

---

## 🚀 Usage

1. 🔐 **Register or log in** — Create an account on the login screen to access the app.
2. 🔎 **Search for trains** — Use the search bar on the Train Planner page to find trains by name or number.
3. 🎯 **Get an AI recommendation** — Select your source station, destination, seat class, travel date, and number of passengers, then click **Generate Recommendation**.
4. 💰 **Check your budget** — The Budget Calculator instantly shows total fare for all passengers.
5. ⭐ **Save favourites** — Hit **Save to Favorites** on any recommended train to bookmark it.
6. ⚖️ **Compare trains** — Use the Train Comparison section to pit two trains against each other.
7. 📊 **Explore analytics** — Click **Visualize → Go to Analytics** to dive into charts, the route map, the price predictor, and the carbon estimator.
8. 📥 **Export data** — Filter by source/destination and download the results as a CSV.

> 📁 **Tip:** Select a station in the Route Insights section and click **Visualize** to pre-filter the entire Analytics page to that station's data.

---

## 📁 Data Files

### 📋 railoptima_master.csv

The core dataset powering all recommendations, analytics, and predictions.

| Column | Description |
|---|---|
| 🔢 `train_number` | Unique identifier for each train (stored as string) |
| 🚆 `train_name` | Full name of the train (e.g. Rajdhani Express) |
| 🏙️ `source_station` | Full name of the departure station |
| 🔤 `source_code` | Short station code for the source (e.g. CSTM) |
| 🏙️ `destination_station` | Full name of the arrival station |
| 🔤 `destination_code` | Short station code for the destination |
| 💺 `class_type` | Seat class — SL (Sleeper), 3A (3-Tier AC), or 2A (2-Tier AC) |
| 💰 `fare` | Ticket price in Indian Rupees (₹) |
| ⏱️ `duration_min` | Total journey duration in minutes |
| 🕐 `duration_hours` | Total journey duration in hours |
| 🛑 `stops` | Number of intermediate stops |
| 📏 `distance_km` | Total route distance in kilometres |
| 🕓 `departure_time` | Scheduled departure time |
| 🕗 `arrival_time` | Scheduled arrival time |

---

## 🗄️ Database Schema

RailOptima uses a local **SQLite** database (`railoptima_users.db`) with two tables:

### 👤 users

| Column | Type | Description |
|---|---|---|
| 🔑 `id` | INTEGER | Auto-incremented primary key |
| 👤 `username` | TEXT UNIQUE | User's login name |
| 🔒 `password` | BLOB | bcrypt-hashed password |

### ⭐ favorites

| Column | Type | Description |
|---|---|---|
| 🔑 `id` | INTEGER | Auto-incremented primary key |
| 👤 `username` | TEXT | Owner of the favourite |
| 🔢 `train_number` | TEXT | Saved train's number |
| 🚆 `train_name` | TEXT | Saved train's name |

---

## 🤖 Model Details

### 🌲 Train Recommendation — RandomForestClassifier

| Parameter | Value |
|---|---|
| 🧠 Model | `RandomForestClassifier` |
| 🌳 Estimators | 100 |
| 📏 Max Depth | 8 |
| 🎲 Random State | 42 |
| ✂️ Test Split | 20% |
| 🏷️ Label Logic | Bottom 30th percentile of weighted utility score = "best train" |
| ⚖️ Utility Weights | Fare 40% · Duration 40% · Stops 20% |
| 📥 Features | `fare`, `duration_min`, `stops`, `distance_km` |

### 📈 Fare Prediction — LinearRegression

| Parameter | Value |
|---|---|
| 🧠 Model | `LinearRegression` (per class) |
| 📥 Feature | `distance_km` |
| 🎯 Target | `fare` |
| 🗂️ Strategy | One model trained per seat class (SL, 3A, 2A) |

---

## 📦 Dependencies

| Library | Purpose |
|---|---|
| 🌐 `streamlit` | Web app framework and UI |
| 🐼 `pandas` | Data loading, filtering, and manipulation |
| 🔢 `numpy` | Numerical operations and percentile calculations |
| 🤖 `scikit-learn` | RandomForestClassifier and LinearRegression models |
| 🔐 `bcrypt` | Secure password hashing and verification |
| 📊 `plotly` | Interactive charts (line, bar, pie, stacked bar) |
| 🗺️ `pydeck` | 3D geographic arc map for route visualization |

---

## 🤝 Contributing

🙌 Contributions are welcome! Here's how you can help:

1. 🍴 Fork the repository
2. 🌿 Create a new branch (`git checkout -b feature/your-feature`)
3. 💾 Make your changes and commit (`git commit -m 'Add your feature'`)
4. 📤 Push to the branch (`git push origin feature/your-feature`)
5. 🔁 Open a Pull Request

✅ Please make sure your code is clean and well-commented.

---

## 👤 Author

**Tanish** — [@tanishcode-12](https://github.com/tanishcode-12)

---

> ⭐ If you found this project helpful, consider giving it a star on GitHub!
