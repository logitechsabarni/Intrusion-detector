# 🛡️ NeuralGuard IDS — Intrusion Detection System

A full-featured, ML-powered Network Intrusion Detection System built with Streamlit.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 🧠 Technologies Used

| Layer | Technology |
|-------|-----------|
| **UI Framework** | Streamlit 1.32+ |
| **ML Engine** | Scikit-learn (Random Forest, Isolation Forest) |
| **Visualization** | Plotly (interactive charts, 3D scatter, heatmaps) |
| **Data Processing** | Pandas, NumPy |
| **Design** | Custom CSS with Orbitron + JetBrains Mono fonts |
| **Dataset** | KDD Cup 99 (synthetic replica) |

## 📡 Features

### 1. Live Monitor
- Real-time traffic ingestion display
- KPI metrics: packets, threats, model accuracy, critical alerts
- Live alert feed with severity badges
- Attack type breakdown donut chart

### 2. Traffic Analysis
- Multi-filter: Protocol, Severity, Attack Type
- Protocol distribution bar chart
- Service × Attack heatmap
- Source vs Destination byte scatter plot (log scale)
- Raw packet log table

### 3. ML Detection
- Random Forest classifier (100 estimators, 16 features)
- Confusion matrix heatmap
- Feature importance ranking
- **Live packet prediction** — enter packet params, get classification + probability distribution

### 4. Threat Intelligence
- Top attacking IP ranking
- Attack severity distribution
- Stacked area timeline by attack type
- Threat reference cards (DoS, SQLi, Port Scan, R2L, U2R, Probe)

### 5. Analytics
- Violin plots by class
- Duration histogram overlay
- **3D feature space** scatter (src_bytes, dst_bytes, duration)
- Feature correlation matrix

### 6. Settings
- Algorithm selection, threshold tuning
- Alert configuration (email, Slack)
- Log retention and encryption toggles
- Firewall rule table
- Export / reload controls

## 🎨 Design System

- **Color Palette**: Deep navy `#020b18` base, cyan `#00d4ff`, green `#00ff88`, red `#ff3366`
- **Typography**: Orbitron (headers/metrics), JetBrains Mono (code/data), Inter (body)
- **Theme**: Cyberpunk/terminal aesthetic with glowing accents
- **Charts**: All Plotly with transparent dark backgrounds matching theme

## 📁 Project Structure

```
ids_app/
├── app.py            # Main Streamlit application
├── requirements.txt  # Python dependencies
└── README.md         # This file
```
