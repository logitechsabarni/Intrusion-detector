import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import networkx as nx
import time, random, math
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier, IsolationForest, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (classification_report, confusion_matrix,
                              accuracy_score, precision_score, recall_score, f1_score, roc_auc_score)
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import warnings; warnings.filterwarnings('ignore')

st.set_page_config(page_title="NeuralGuard IDS v3", page_icon="🛡️",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=JetBrains+Mono:wght@300;400;500;600&family=Syne:wght@400;600;700;800&display=swap');
:root {
  --bg0:#010912; --bg1:#040f1e; --bg2:#071628; --bg3:#091d34;
  --cyan:#00d4ff; --green:#00ff88; --red:#ff2d55; --orange:#ff8c00;
  --purple:#b96dff; --yellow:#ffd60a; --pink:#ff375f;
  --txt:#dde6f0; --muted:#4a6080; --border:rgba(0,212,255,0.12);
  --glow-c:0 0 20px rgba(0,212,255,0.4); --glow-g:0 0 20px rgba(0,255,136,0.4);
  --glow-r:0 0 20px rgba(255,45,85,0.4);
}
html,body,[class*="css"]{font-family:'Syne',sans-serif;background:var(--bg0);color:var(--txt);}
.stApp{background:var(--bg0);}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding:0.5rem 1.5rem 2rem;}
.stApp::before{content:'';position:fixed;inset:0;pointer-events:none;z-index:0;
  background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,212,255,0.015) 2px,rgba(0,212,255,0.015) 4px);}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#010912 0%,#040f1e 100%);border-right:1px solid var(--border);}
section[data-testid="stSidebar"] .stRadio>div{gap:2px;}
section[data-testid="stSidebar"] .stRadio label{color:var(--txt)!important;font-family:'JetBrains Mono',monospace;font-size:12.5px;padding:8px 12px;border-radius:6px;border:1px solid transparent;transition:all 0.2s;cursor:pointer;}
section[data-testid="stSidebar"] .stRadio label:hover{border-color:var(--border);background:rgba(0,212,255,0.06);}
.hero{background:linear-gradient(135deg,#010912 0%,#071628 50%,#010912 100%);border:1px solid var(--border);border-radius:18px;padding:26px 36px;margin-bottom:20px;position:relative;overflow:hidden;}
.hero::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,var(--cyan),var(--green),var(--purple),transparent);}
.hero::after{content:'';position:absolute;bottom:-60px;right:-60px;width:200px;height:200px;border-radius:50%;background:radial-gradient(circle,rgba(0,212,255,0.08) 0%,transparent 70%);}
.hero-title{font-family:'Orbitron',monospace;font-size:2rem;font-weight:900;letter-spacing:3px;background:linear-gradient(90deg,var(--cyan),var(--green));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin:0 0 4px;}
.hero-sub{font-family:'JetBrains Mono',monospace;color:var(--muted);font-size:12px;letter-spacing:1.5px;}
.pulse{display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--green);box-shadow:var(--glow-g);margin-right:8px;animation:blink 1.8s ease-in-out infinite;}
@keyframes blink{0%,100%{opacity:1;transform:scale(1);}50%{opacity:0.3;transform:scale(0.8);}}
.mcard{background:var(--bg2);border:1px solid var(--border);border-radius:14px;padding:18px 20px;position:relative;overflow:hidden;transition:border-color 0.3s,transform 0.2s,box-shadow 0.3s;cursor:default;}
.mcard:hover{transform:translateY(-2px);}
.mcard.c-cyan:hover{border-color:var(--cyan);box-shadow:var(--glow-c);}
.mcard.c-green:hover{border-color:var(--green);box-shadow:var(--glow-g);}
.mcard.c-red:hover{border-color:var(--red);box-shadow:var(--glow-r);}
.mcard.c-purple:hover{border-color:var(--purple);box-shadow:0 0 20px rgba(185,109,255,0.4);}
.mcard.c-orange:hover{border-color:var(--orange);}
.mcard::after{content:'';position:absolute;bottom:0;left:0;right:0;height:2px;}
.mcard.c-cyan::after{background:var(--cyan);}.mcard.c-green::after{background:var(--green);}
.mcard.c-red::after{background:var(--red);}.mcard.c-purple::after{background:var(--purple);}
.mcard.c-orange::after{background:var(--orange);}.mcard.c-yellow::after{background:var(--yellow);}
.mv{font-family:'Orbitron',monospace;font-size:1.9rem;font-weight:700;line-height:1;margin-bottom:4px;}
.ml{font-family:'JetBrains Mono',monospace;font-size:10.5px;color:var(--muted);letter-spacing:1.5px;text-transform:uppercase;}
.md{font-family:'JetBrains Mono',monospace;font-size:11px;margin-top:6px;}
.sh{font-family:'Orbitron',monospace;font-size:13px;font-weight:700;color:var(--cyan);letter-spacing:2px;text-transform:uppercase;margin:28px 0 14px;padding-bottom:8px;border-bottom:1px solid var(--border);}
.alert-wrap{max-height:420px;overflow-y:auto;padding-right:4px;}
.alert-wrap::-webkit-scrollbar{width:4px;}.alert-wrap::-webkit-scrollbar-track{background:transparent;}.alert-wrap::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px;}
.aitem{background:var(--bg2);border-left:3px solid;border-radius:0 8px 8px 0;padding:10px 14px;margin-bottom:6px;font-family:'JetBrains Mono',monospace;font-size:11.5px;animation:fadeIn 0.4s ease;}
@keyframes fadeIn{from{opacity:0;transform:translateX(-8px);}to{opacity:1;transform:translateX(0);}}
.aitem.critical{border-color:var(--red);background:rgba(255,45,85,0.05);}
.aitem.high{border-color:var(--orange);background:rgba(255,140,0,0.05);}
.aitem.medium{border-color:var(--yellow);background:rgba(255,214,10,0.05);}
.aitem.low{border-color:var(--cyan);background:rgba(0,212,255,0.04);}
.at{font-weight:600;margin-bottom:3px;}.am{color:var(--muted);font-size:10.5px;}
.badge{display:inline-block;padding:2px 9px;border-radius:20px;font-size:10px;font-family:'JetBrains Mono',monospace;font-weight:600;}
.bc{background:rgba(255,45,85,0.18);color:var(--red);border:1px solid rgba(255,45,85,0.4);}
.bh{background:rgba(255,140,0,0.18);color:var(--orange);border:1px solid rgba(255,140,0,0.4);}
.bm{background:rgba(255,214,10,0.18);color:var(--yellow);border:1px solid rgba(255,214,10,0.4);}
.bl{background:rgba(0,212,255,0.18);color:var(--cyan);border:1px solid rgba(0,212,255,0.4);}
.bg2{background:rgba(0,255,136,0.18);color:var(--green);border:1px solid rgba(0,255,136,0.4);}
.stDataFrame{border-radius:12px;overflow:hidden;}[data-testid="stDataFrameResizable"]{border-radius:12px;}
.stButton>button{background:linear-gradient(135deg,rgba(0,212,255,0.08),rgba(0,255,136,0.08));border:1px solid var(--cyan);color:var(--cyan);font-family:'JetBrains Mono',monospace;font-size:12.5px;letter-spacing:0.8px;border-radius:8px;transition:all 0.25s;}
.stButton>button:hover{background:linear-gradient(135deg,rgba(0,212,255,0.2),rgba(0,255,136,0.2));border-color:var(--green);color:var(--green);transform:translateY(-1px);box-shadow:0 4px 20px rgba(0,255,136,0.2);}
.stProgress>div>div{background:linear-gradient(90deg,var(--cyan),var(--green));}
.stTabs [data-baseweb="tab-list"]{background:var(--bg1);border-radius:10px;padding:4px;gap:2px;}
.stTabs [data-baseweb="tab"]{font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--muted)!important;border-radius:8px;transition:all 0.2s;}
.stTabs [aria-selected="true"]{background:var(--bg3)!important;color:var(--cyan)!important;box-shadow:0 0 10px rgba(0,212,255,0.2);}
.streamlit-expanderHeader{font-family:'JetBrains Mono',monospace;font-size:13px;color:var(--cyan)!important;background:var(--bg2)!important;border-radius:8px!important;}
.terminal{background:#000d1a;border:1px solid rgba(0,212,255,0.2);border-radius:10px;padding:16px;font-family:'JetBrains Mono',monospace;font-size:12px;color:#00ff88;line-height:1.8;max-height:300px;overflow-y:auto;}
.terminal::-webkit-scrollbar{width:4px;}.terminal::-webkit-scrollbar-thumb{background:rgba(0,212,255,0.2);}
.t-dim{color:#1e4060;}.t-cyan{color:#00d4ff;}.t-red{color:#ff2d55;}.t-orange{color:#ff8c00;}.t-yellow{color:#ffd60a;}.t-white{color:#e2e8f0;}
.risk-bar{height:8px;border-radius:4px;margin:4px 0;position:relative;overflow:hidden;}
.risk-fill{height:100%;border-radius:4px;transition:width 0.6s ease;}
.slogo{font-family:'Orbitron',monospace;font-weight:900;font-size:16px;letter-spacing:2px;background:linear-gradient(90deg,var(--cyan),var(--green));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;text-align:center;padding:14px 0 6px;}
.stat-row{display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid rgba(0,212,255,0.06);font-family:'JetBrains Mono';font-size:12px;}
.stat-row:last-child{border-bottom:none;}
.model-bar-wrap{margin:10px 0;}.model-label{font-family:'JetBrains Mono';font-size:11px;color:var(--muted);margin-bottom:3px;}
</style>
""", unsafe_allow_html=True)

# ── Helper: convert hex color to rgba string ──────────────────────────────────
def hex_to_rgba(hex_color, alpha=0.33):
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f'rgba({r},{g},{b},{alpha})'

ATTACK_TYPES  = ['Normal','DoS','Probe','R2L','U2R','DDoS','SQL Injection','Port Scan','Brute Force','MITM','Ransomware','Zero-Day']
PROTOCOLS     = ['tcp','udp','icmp','http','https']
SERVICES      = ['http','ftp','ssh','smtp','dns','https','telnet','pop3','irc','snmp']
FLAGS         = ['SF','S0','REJ','RSTO','SH','S1','S2','S3','OTH','RSTOS0']
COUNTRIES     = ['US','CN','RU','DE','BR','IN','KR','JP','GB','UA','IR','NG','FR','NL','CA']
COUNTRY_COORDS= {'US':(37,-95),'CN':(35,105),'RU':(61,105),'DE':(51,10),'BR':(-14,-51),
                 'IN':(20,77),'KR':(37,127),'JP':(36,138),'GB':(55,-3),'UA':(49,32),
                 'IR':(32,53),'NG':(9,8),'FR':(46,2),'NL':(52,5),'CA':(60,-96)}
COLOR_MAP     = {'Normal':'#00ff88','DoS':'#ff2d55','Probe':'#00d4ff','R2L':'#ff8c00',
                 'U2R':'#b96dff','DDoS':'#ef4444','SQL Injection':'#ffd60a',
                 'Port Scan':'#06b6d4','Brute Force':'#f97316','MITM':'#ec4899',
                 'Ransomware':'#dc2626','Zero-Day':'#7c3aed'}
SEV_MAP       = {'Normal':'clean','DoS':'critical','DDoS':'critical','U2R':'critical',
                 'Ransomware':'critical','Zero-Day':'critical','R2L':'high',
                 'SQL Injection':'high','Brute Force':'high','MITM':'high',
                 'Probe':'medium','Port Scan':'medium'}
CHART_LAYOUT  = dict(paper_bgcolor='rgba(1,9,18,0)',plot_bgcolor='rgba(4,15,30,0.5)',
                     font=dict(family='JetBrains Mono',color='#4a6080',size=11),
                     margin=dict(l=10,r=10,t=34,b=10))

@st.cache_data
def gen_data(n=8000):
    np.random.seed(42)
    probs = [0.52,0.07,0.06,0.05,0.03,0.06,0.04,0.03,0.04,0.03,0.03,0.04]
    probs = np.array(probs)/sum(probs)
    labels = np.random.choice(ATTACK_TYPES, n, p=probs)
    d = {
        'duration'        : np.random.exponential(12, n),
        'protocol_type'   : np.random.choice(PROTOCOLS, n),
        'service'         : np.random.choice(SERVICES, n),
        'flag'            : np.random.choice(FLAGS, n),
        'src_bytes'       : np.abs(np.random.exponential(6000, n)),
        'dst_bytes'       : np.abs(np.random.exponential(3500, n)),
        'land'            : np.random.choice([0,1],n,p=[0.99,0.01]),
        'wrong_fragment'  : np.random.poisson(0.12,n),
        'urgent'          : np.random.poisson(0.01,n),
        'hot'             : np.random.poisson(2.5,n),
        'num_failed_logins': np.random.poisson(0.15,n),
        'logged_in'       : np.random.choice([0,1],n,p=[0.38,0.62]),
        'num_compromised' : np.random.poisson(0.6,n),
        'count'           : np.random.randint(1,512,n),
        'srv_count'       : np.random.randint(1,512,n),
        'same_srv_rate'   : np.random.uniform(0,1,n),
        'diff_srv_rate'   : np.random.uniform(0,1,n),
        'src_ip'          : [f"192.168.{np.random.randint(0,255)}.{np.random.randint(1,254)}" for _ in range(n)],
        'dst_ip'          : [f"10.0.{np.random.randint(0,255)}.{np.random.randint(1,254)}" for _ in range(n)],
        'port'            : np.random.randint(1,65535,n),
        'packet_size'     : np.abs(np.random.exponential(1100,n)),
        'ttl'             : np.random.choice([32,64,128,255],n),
        'country'         : np.random.choice(COUNTRIES,n),
        'label'           : labels,
    }
    df = pd.DataFrame(d)
    df['is_attack']   = (df['label']!='Normal').astype(int)
    df['severity']    = df['label'].map(SEV_MAP).fillna('low')
    df['risk_score']  = df.apply(lambda r: min(100,
        {'critical':75,'high':50,'medium':30,'low':10,'clean':0}.get(r['severity'],0)
        + np.random.randint(0,26)), axis=1)
    df['timestamp']   = [datetime.now()-timedelta(minutes=n-i, seconds=np.random.randint(0,60))
                         for i in range(n)]
    df['bytes_total'] = df['src_bytes']+df['dst_bytes']
    return df

FEAT_COLS = ['duration','src_bytes','dst_bytes','land','wrong_fragment','urgent','hot',
             'num_failed_logins','logged_in','num_compromised','count','srv_count',
             'same_srv_rate','diff_srv_rate','packet_size','port','ttl','risk_score']

@st.cache_resource
def train_all_models(df):
    le = LabelEncoder()
    X  = df[FEAT_COLS].values
    y  = le.fit_transform(df['label'])
    sc = StandardScaler(); X_s = sc.fit_transform(X)
    Xtr,Xte,ytr,yte = train_test_split(X_s,y,test_size=0.2,random_state=42,stratify=y)
    models = {
        'Random Forest'    : RandomForestClassifier(n_estimators=150,max_depth=20,random_state=42,n_jobs=-1),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100,learning_rate=0.1,random_state=42),
        'Neural Network'   : MLPClassifier(hidden_layer_sizes=(128,64,32),max_iter=300,random_state=42),
    }
    results = {}
    for name,clf in models.items():
        clf.fit(Xtr,ytr)
        yp = clf.predict(Xte)
        results[name] = {
            'model'    : clf,
            'accuracy' : accuracy_score(yte,yp),
            'precision': precision_score(yte,yp,average='weighted',zero_division=0),
            'recall'   : recall_score(yte,yp,average='weighted',zero_division=0),
            'f1'       : f1_score(yte,yp,average='weighted',zero_division=0),
            'y_pred'   : yp,
        }
    iso = IsolationForest(n_estimators=200,contamination=0.15,random_state=42)
    iso.fit(Xtr)
    ano_scores = iso.decision_function(X_s)
    return results, sc, le, Xte, yte, ano_scores, X_s


def pca_embed(X_s, labels, n=1500):
    """PCA embedding - called once after training, no cache needed."""
    np.random.seed(7)
    idx = np.random.choice(len(X_s), min(n, len(X_s)), replace=False)
    pca = PCA(n_components=3, random_state=42)
    emb = pca.fit_transform(X_s[idx])
    return emb, np.array(labels)[idx], pca.explained_variance_ratio_

def badge(sev):
    cls={'critical':'bc','high':'bh','medium':'bm','low':'bl','clean':'bg2'}
    return f'<span class="badge {cls.get(sev,"bl")}">{sev.upper()}</span>'

def sev_color(s):
    return {'critical':'#ff2d55','high':'#ff8c00','medium':'#ffd60a','low':'#00d4ff','clean':'#00ff88'}.get(s,'#00d4ff')

def make_gauge(val, max_val, label, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=val,
        title={'text':label,'font':{'family':'JetBrains Mono','size':11,'color':'#4a6080'}},
        number={'font':{'family':'Orbitron','size':24,'color':color}},
        gauge={
            'axis':{'range':[0,max_val],'tickcolor':'#1e3a5f','tickwidth':1,'tickfont':{'size':9}},
            'bar':{'color':color,'thickness':0.25},
            'bgcolor':'rgba(4,15,30,0.8)',
            'borderwidth':0,
            'steps':[{'range':[0,max_val*0.5],'color':'rgba(0,212,255,0.04)'},
                     {'range':[max_val*0.5,max_val*0.8],'color':'rgba(255,140,0,0.06)'},
                     {'range':[max_val*0.8,max_val],'color':'rgba(255,45,85,0.08)'}],
            'threshold':{'line':{'color':color,'width':2},'thickness':0.7,'value':val}
        }
    ))
    fig.update_layout(**CHART_LAYOUT, height=180)
    return fig

def network_graph(df):
    sample = df[df['is_attack']==1].sample(min(40,len(df[df['is_attack']==1])),random_state=7)
    G = nx.DiGraph()
    for _,r in sample.iterrows():
        G.add_edge(r['src_ip'],r['dst_ip'],attack=r['label'],sev=r['severity'])
    pos = nx.spring_layout(G,seed=42,k=1.2)
    edge_x,edge_y=[],[]
    for u,v in G.edges():
        x0,y0=pos[u]; x1,y1=pos[v]
        edge_x+=[x0,x1,None]; edge_y+=[y0,y1,None]
    node_x=[pos[n][0] for n in G.nodes()]
    node_y=[pos[n][1] for n in G.nodes()]
    node_colors=['#ff2d55' if G.out_degree(n)>G.in_degree(n) else '#00d4ff' for n in G.nodes()]
    node_sizes=[8+G.degree(n)*3 for n in G.nodes()]
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=edge_x,y=edge_y,mode='lines',
        line=dict(color='rgba(0,212,255,0.25)',width=1),hoverinfo='none'))
    fig.add_trace(go.Scatter(x=node_x,y=node_y,mode='markers+text',
        marker=dict(size=node_sizes,color=node_colors,line=dict(color='rgba(0,0,0,0.5)',width=1)),
        text=[n.split('.')[-1] for n in G.nodes()],
        textfont=dict(size=8,color='#4a6080',family='JetBrains Mono'),
        textposition='top center',hoverinfo='text',
        hovertext=[f"IP: {n}<br>Degree: {G.degree(n)}" for n in G.nodes()]))
    fig.update_layout(**CHART_LAYOUT,height=400,
        xaxis=dict(showgrid=False,zeroline=False,visible=False),
        yaxis=dict(showgrid=False,zeroline=False,visible=False),
        title=dict(text='Attack Network Graph',font=dict(size=12,color='#4a6080',family='Orbitron')))
    return fig

# ── Load data + models ────────────────────────────────────────────────────────
df = gen_data(8000)
model_results, sc, le, Xte, yte, ano_scores, X_s = train_all_models(df)
best_model_name = max(model_results, key=lambda k: model_results[k]['accuracy'])
best = model_results[best_model_name]
pca_emb, pca_labels, var_ratio = pca_embed(X_s, df['label'].values)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="slogo">🛡️ NEURALGUARD</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-family:JetBrains Mono;font-size:9px;color:#1e3a5f;text-align:center;letter-spacing:2px;margin-bottom:14px">v3.0.0 · ENTERPRISE IDS</div>', unsafe_allow_html=True)
    st.markdown('<div style="border-top:1px solid rgba(0,212,255,0.1);margin-bottom:12px"></div>', unsafe_allow_html=True)
    page = st.radio("NAV", [
        "📡  Dashboard","🔴  Live Simulation","🔍  Traffic Analysis",
        "🤖  ML Engine","🌐  Network Graph","🗺️  GeoIP Threat Map",
        "⚠️  Threat Intel","📊  Advanced Analytics","🔮  Anomaly Detection",
        "📋  Incident Log","⚙️  Settings & Rules",
    ], label_visibility="collapsed")
    st.markdown('<div style="border-top:1px solid rgba(0,212,255,0.08);margin:14px 0 10px"></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-family:JetBrains Mono;font-size:9px;color:#1e3a5f;letter-spacing:2px;margin-bottom:8px">SYSTEM STATUS</div>', unsafe_allow_html=True)
    for label,val,color in [
        ("IDS Engine","ACTIVE","#00ff88"),("ML Models","LOADED","#00ff88"),
        ("Network Tap","LIVE","#00d4ff"),("Firewall","ENABLED","#00ff88"),
        ("GeoIP DB","SYNCED","#00ff88"),("Threat Feed","UPDATED","#00d4ff")]:
        st.markdown(f'<div class="stat-row"><span style="color:#2a4a6a">{label}</span><span style="color:{color};font-weight:600">{val}</span></div>', unsafe_allow_html=True)
    st.markdown('<div style="border-top:1px solid rgba(0,212,255,0.08);margin:14px 0 10px"></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-family:JetBrains Mono;font-size:9px;color:#1e3a5f;letter-spacing:2px;margin-bottom:8px">CONTROLS</div>', unsafe_allow_html=True)
    sensitivity  = st.slider("Sensitivity", 0.1, 1.0, 0.75, 0.05, key="sens")
    auto_refresh = st.toggle("Auto Refresh", value=False)
    dark_mode    = st.toggle("Scan Overlay", value=True)
    attacks_df_sidebar = df[df['is_attack']==1]
    crit_pct = len(attacks_df_sidebar[attacks_df_sidebar['severity']=='critical'])/max(1,len(df))*100
    st.markdown('<div style="margin-top:14px;font-family:JetBrains Mono;font-size:9px;color:#1e3a5f;letter-spacing:2px">THREAT LEVEL</div>', unsafe_allow_html=True)
    threat_level = "CRITICAL" if crit_pct>5 else "HIGH" if crit_pct>3 else "MEDIUM"
    tc = "#ff2d55" if threat_level=="CRITICAL" else "#ff8c00" if threat_level=="HIGH" else "#ffd60a"
    st.markdown(f'<div style="font-family:Orbitron;font-size:18px;color:{tc};text-align:center;margin:6px 0">{threat_level}</div>', unsafe_allow_html=True)
    st.progress(min(1.0, crit_pct/10))

page_label = page.split("  ")[1] if "  " in page else page

# ── Hero bar ──────────────────────────────────────────────────────────────────
now = datetime.now()
uptime_secs = 3600*24*7 + random.randint(0,3600)
st.markdown(f"""
<div class="hero">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px">
    <div>
      <div class="hero-title">NEURALGUARD IDS</div>
      <div class="hero-sub"><span class="pulse"></span>INTRUSION DETECTION SYSTEM &nbsp;·&nbsp; {page_label.upper()} &nbsp;·&nbsp; UPTIME {uptime_secs//3600}h {(uptime_secs%3600)//60}m</div>
    </div>
    <div style="display:flex;gap:28px;flex-wrap:wrap">
      <div style="text-align:right">
        <div style="font-family:Orbitron;font-size:1.5rem;color:#00d4ff">{now.strftime('%H:%M:%S')}</div>
        <div style="font-family:JetBrains Mono;font-size:11px;color:#2a4a6a">{now.strftime('%a %d %b %Y')}</div>
      </div>
      <div style="font-family:JetBrains Mono;font-size:11px;color:#2a4a6a;line-height:1.8">
        <div>Model: <span style="color:#00ff88">{best_model_name}</span></div>
        <div>Accuracy: <span style="color:#00ff88">{best['accuracy']*100:.1f}%</span></div>
        <div>Dataset: <span style="color:#00d4ff">8,000 pkts</span></div>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if "Dashboard" in page:
    total = len(df); attacks = df[df['is_attack']==1]; normal = df[df['is_attack']==0]
    crits  = len(df[df['severity']=='critical'])
    highs  = len(df[df['severity']=='high'])
    attack_rate = len(attacks)/total*100
    blocked_ips = df[df['is_attack']==1]['src_ip'].nunique()

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    cards = [
        (c1,'c-cyan','#00d4ff',f"{total:,}",'TOTAL PACKETS','Last 24h ↑'),
        (c2,'c-red','#ff2d55',f"{len(attacks):,}",'THREATS','↑ Active'),
        (c3,'c-green','#00ff88',f"{best['accuracy']*100:.1f}%",'ML ACCURACY',best_model_name),
        (c4,'c-orange','#ff8c00',f"{crits}",'CRITICAL',f"+{highs} HIGH"),
        (c5,'c-purple','#b96dff',f"{attack_rate:.1f}%",'ATTACK RATE','of traffic'),
        (c6,'c-yellow','#ffd60a',f"{blocked_ips}",'UNIQUE SRCS','tracked IPs'),
    ]
    for col,cls,clr,val,lbl,delta in cards:
        with col:
            st.markdown(f'<div class="mcard {cls}"><div class="mv" style="color:{clr}">{val}</div><div class="ml">{lbl}</div><div class="md" style="color:{clr}88">{delta}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="sh">📈 REAL-TIME TRAFFIC STREAM</div>', unsafe_allow_html=True)
    recent = df.copy(); recent['ts_min'] = pd.to_datetime(recent['timestamp']).dt.floor('3min')
    tg = recent.groupby(['ts_min','is_attack']).size().reset_index(name='cnt')
    norm_t = tg[tg['is_attack']==0]; atk_t = tg[tg['is_attack']==1]
    fig_t = go.Figure()
    fig_t.add_trace(go.Scatter(x=norm_t['ts_min'],y=norm_t['cnt'],name='Normal',fill='tozeroy',
        mode='lines',line=dict(color='#00ff88',width=2),fillcolor='rgba(0,255,136,0.08)'))
    fig_t.add_trace(go.Scatter(x=atk_t['ts_min'],y=atk_t['cnt'],name='Attack',fill='tozeroy',
        mode='lines',line=dict(color='#ff2d55',width=2),fillcolor='rgba(255,45,85,0.12)'))
    fig_t.update_layout(**CHART_LAYOUT,height=240,
        xaxis=dict(gridcolor='rgba(0,212,255,0.04)'),yaxis=dict(gridcolor='rgba(0,212,255,0.04)'),
        legend=dict(bgcolor='rgba(0,0,0,0)',font=dict(color='#4a6080')))
    st.plotly_chart(fig_t,use_container_width=True)

    col1,col2,col3 = st.columns([2,1.2,1.2])
    with col1:
        st.markdown('<div class="sh">⚠️ LATEST ALERTS</div>', unsafe_allow_html=True)
        recent_atk = df[df['is_attack']==1].sort_values('timestamp',ascending=False).head(12)
        alerts_html = '<div class="alert-wrap">'
        for _,r in recent_atk.iterrows():
            sev=r['severity']
            alerts_html += f'<div class="aitem {sev}"><div class="at">{ {"critical":"⛔","high":"🟠","medium":"🟡","low":"🔵","clean":"🟢"}.get(sev,"●") } {r["label"]} &nbsp;{badge(sev)}</div><div class="am">SRC: {r["src_ip"]} &nbsp;|&nbsp; PORT: {r["port"]} &nbsp;|&nbsp; {r["protocol_type"].upper()} &nbsp;|&nbsp; RISK: <span style="color:{sev_color(sev)}">{r["risk_score"]}</span> &nbsp;|&nbsp; {pd.to_datetime(r["timestamp"]).strftime("%H:%M:%S")}</div></div>'
        alerts_html += '</div>'
        st.markdown(alerts_html, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="sh">🎯 ATTACK MIX</div>', unsafe_allow_html=True)
        dist = df[df['is_attack']==1]['label'].value_counts()
        fig_d = go.Figure(go.Pie(
            labels=dist.index, values=dist.values, hole=0.6,
            marker=dict(colors=[COLOR_MAP.get(l,'#00d4ff') for l in dist.index],
                        line=dict(color='#010912',width=2)),
            textfont=dict(family='JetBrains Mono',size=10),
            hovertemplate='<b>%{label}</b><br>%{value} pkts<br>%{percent}<extra></extra>'
        ))
        fig_d.update_layout(**CHART_LAYOUT,height=280,showlegend=False,
            annotations=[dict(text=f"<b>{len(attacks)}</b>",x=0.5,y=0.5,
                              font=dict(size=22,color='#ff2d55',family='Orbitron'),showarrow=False)])
        st.plotly_chart(fig_d,use_container_width=True)

    with col3:
        st.markdown('<div class="sh">📊 SEVERITY</div>', unsafe_allow_html=True)
        sev_c = df[df['is_attack']==1]['severity'].value_counts()
        for s in ['critical','high','medium','low']:
            v = sev_c.get(s,0)
            pct = v/max(1,len(attacks))*100
            col_s = sev_color(s)
            st.markdown(f'<div style="margin-bottom:10px"><div style="display:flex;justify-content:space-between;font-family:JetBrains Mono;font-size:11px;margin-bottom:3px"><span style="color:{col_s}">{s.upper()}</span><span style="color:#2a4a6a">{v}</span></div><div class="risk-bar" style="background:rgba(255,255,255,0.04)"><div class="risk-fill" style="width:{pct:.0f}%;background:{col_s}"></div></div></div>', unsafe_allow_html=True)
        st.markdown('<div style="margin-top:16px"></div>', unsafe_allow_html=True)
        for g_val,g_max,g_label,g_col in [(len(attacks),total,'Total Threats','#ff2d55'),(crits,total,'Critical','#ff8c00')]:
            st.plotly_chart(make_gauge(g_val,g_max,g_label,g_col),use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: LIVE SIMULATION
# ══════════════════════════════════════════════════════════════════════════════
elif "Live Simulation" in page:
    st.markdown('<div class="sh">🔴 LIVE PACKET SIMULATION ENGINE</div>', unsafe_allow_html=True)
    if 'sim_packets' not in st.session_state:
        st.session_state.sim_packets = []
        st.session_state.sim_stats   = {'total':0,'attacks':0,'blocked':0}
        st.session_state.sim_running = False
        st.session_state.sim_log     = []
        st.session_state.sim_history = []

    c1,c2,c3 = st.columns(3)
    with c1: pkt_rate = st.slider("Packets/sec", 1, 50, 10)
    with c2: attack_prob = st.slider("Attack Probability", 0.0, 1.0, 0.3, 0.05)
    with c3: sim_duration = st.number_input("Sim Duration (sec)", 5, 120, 30)

    col_b1,col_b2,col_b3 = st.columns(3)
    with col_b1: start = st.button("▶ START SIMULATION", use_container_width=True)
    with col_b2: stop  = st.button("⏹ STOP", use_container_width=True)
    with col_b3: reset = st.button("🔄 RESET", use_container_width=True)

    if reset:
        st.session_state.sim_packets = []
        st.session_state.sim_stats   = {'total':0,'attacks':0,'blocked':0}
        st.session_state.sim_log     = []
        st.session_state.sim_history = []

    sm1,sm2,sm3,sm4 = st.columns(4)
    stat_placeholders = [sm1.empty(), sm2.empty(), sm3.empty(), sm4.empty()]
    chart_ph    = st.empty()
    terminal_ph = st.empty()

    def render_sim():
        s = st.session_state.sim_stats
        for ph,val,lbl,clr,cls in zip(stat_placeholders,
            [s['total'],s['attacks'],s['blocked'],f"{s['attacks']/max(1,s['total'])*100:.1f}%"],
            ['PACKETS','THREATS','BLOCKED','ATTACK RATE'],
            ['#00d4ff','#ff2d55','#ff8c00','#b96dff'],
            ['c-cyan','c-red','c-orange','c-purple']):
            ph.markdown(f'<div class="mcard {cls}"><div class="mv" style="color:{clr}">{val}</div><div class="ml">{lbl}</div></div>', unsafe_allow_html=True)
        hist = st.session_state.sim_history
        if len(hist)>2:
            hdf = pd.DataFrame(hist)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=hdf['t'],y=hdf['normal'],name='Normal',
                fill='tozeroy',line=dict(color='#00ff88',width=2),fillcolor='rgba(0,255,136,0.08)'))
            fig.add_trace(go.Scatter(x=hdf['t'],y=hdf['attack'],name='Attack',
                fill='tozeroy',line=dict(color='#ff2d55',width=2),fillcolor='rgba(255,45,85,0.12)'))
            fig.update_layout(**CHART_LAYOUT,height=220,
                xaxis=dict(gridcolor='rgba(0,212,255,0.04)',showticklabels=False),
                yaxis=dict(gridcolor='rgba(0,212,255,0.04)'),
                legend=dict(bgcolor='rgba(0,0,0,0)',font=dict(color='#4a6080')))
            chart_ph.plotly_chart(fig,use_container_width=True)
        logs = st.session_state.sim_log[-18:]
        log_html = '<div class="terminal">'
        for entry in reversed(logs):
            clr = {'ALERT':'#ff2d55','INFO':'#00d4ff','BLOCK':'#ff8c00','OK':'#00ff88'}.get(entry['type'],'#4a6080')
            log_html += f'<div><span class="t-dim">{entry["ts"]}</span> <span style="color:{clr}">[{entry["type"]}]</span> <span class="t-white">{entry["msg"]}</span></div>'
        log_html += '</div>'
        terminal_ph.markdown(log_html, unsafe_allow_html=True)

    if start:
        for step in range(int(sim_duration)):
            n_pkts = random.randint(max(1,pkt_rate-3), pkt_rate+3)
            step_attacks = 0; step_normal = 0
            for _ in range(n_pkts):
                is_atk = random.random() < attack_prob
                atk_type = random.choice(ATTACK_TYPES[1:]) if is_atk else 'Normal'
                sev = SEV_MAP.get(atk_type,'low')
                src = f"{random.randint(1,254)}.{random.randint(0,254)}.{random.randint(0,254)}.{random.randint(1,254)}"
                pkt = {'type':atk_type,'src':src,'sev':sev,'ts':datetime.now().strftime('%H:%M:%S.%f')[:-3]}
                st.session_state.sim_packets.append(pkt)
                st.session_state.sim_stats['total'] += 1
                if is_atk:
                    st.session_state.sim_stats['attacks'] += 1
                    step_attacks += 1
                    blocked = random.random() < 0.7
                    if blocked: st.session_state.sim_stats['blocked'] += 1
                    log_type = 'ALERT' if sev in ['critical','high'] else 'BLOCK' if blocked else 'INFO'
                    st.session_state.sim_log.append({'ts':pkt['ts'],'type':log_type,'msg':f"{atk_type} from {src} [{sev.upper()}]{'  → BLOCKED' if blocked else ''}"})
                else:
                    step_normal += 1
                    if random.random()<0.05:
                        st.session_state.sim_log.append({'ts':pkt['ts'],'type':'OK','msg':f"Clean traffic from {src}"})
            st.session_state.sim_history.append({'t':step,'normal':step_normal,'attack':step_attacks})
            render_sim()
            time.sleep(0.12)
    else:
        render_sim()

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: TRAFFIC ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif "Traffic Analysis" in page:
    st.markdown('<div class="sh">🔍 DEEP TRAFFIC ANALYSIS</div>', unsafe_allow_html=True)
    tab1,tab2,tab3 = st.tabs(["  Overview  ","  Flow Analysis  ","  Packet Inspector  "])

    with tab1:
        fc1,fc2,fc3 = st.columns(3)
        with fc1: proto_f = st.multiselect("Protocol",PROTOCOLS,default=PROTOCOLS)
        with fc2: sev_f   = st.multiselect("Severity",['clean','low','medium','high','critical'],default=['critical','high','medium'])
        with fc3: label_f = st.multiselect("Type",ATTACK_TYPES,default=ATTACK_TYPES)
        fdf = df[df['protocol_type'].isin(proto_f)&df['severity'].isin(sev_f)&df['label'].isin(label_f)]

        r1c1,r1c2 = st.columns(2)
        with r1c1:
            pd2 = fdf['protocol_type'].value_counts().reset_index(); pd2.columns=['p','c']
            fig = go.Figure(go.Bar(x=pd2['c'],y=pd2['p'],orientation='h',
                marker=dict(color=['#00d4ff','#00ff88','#b96dff','#ffd60a','#ff8c00'][:len(pd2)]),
                text=pd2['c'],textposition='auto',textfont=dict(family='JetBrains Mono',size=11)))
            fig.update_layout(**CHART_LAYOUT,height=260,title_text='Protocol Distribution',
                xaxis=dict(gridcolor='rgba(0,212,255,0.04)'),yaxis=dict(gridcolor='rgba(0,212,255,0.04)'))
            st.plotly_chart(fig,use_container_width=True)
        with r1c2:
            svc_atk = fdf.groupby(['service','label']).size().reset_index(name='n')
            pvt = svc_atk.pivot(index='service',columns='label',values='n').fillna(0)
            fig = go.Figure(go.Heatmap(z=pvt.values,x=pvt.columns,y=pvt.index,
                colorscale=[[0,'#010912'],[0.3,'#071628'],[0.7,'#00d4ff'],[1,'#ff2d55']],showscale=True))
            fig.update_layout(**CHART_LAYOUT,height=260,title_text='Service × Attack Heatmap')
            st.plotly_chart(fig,use_container_width=True)

        samp = fdf.sample(min(1200,len(fdf)),random_state=42)
        fig_s = go.Figure(go.Scatter(
            x=np.log1p(samp['src_bytes']),y=np.log1p(samp['dst_bytes']),mode='markers',
            marker=dict(color=[COLOR_MAP.get(l,'#00d4ff') for l in samp['label']],size=4,opacity=0.65,line=dict(width=0)),
            text=samp['label'],hovertemplate='<b>%{text}</b><br>Src: %{x:.2f}<br>Dst: %{y:.2f}<extra></extra>'))
        fig_s.update_layout(**CHART_LAYOUT,height=340,title_text='Src vs Dst Bytes (log)',
            xaxis=dict(title='log(src_bytes)',gridcolor='rgba(0,212,255,0.04)'),
            yaxis=dict(title='log(dst_bytes)',gridcolor='rgba(0,212,255,0.04)'))
        st.plotly_chart(fig_s,use_container_width=True)

    with tab2:
        st.markdown('<div class="sh">📊 FLOW STATISTICS</div>', unsafe_allow_html=True)
        fc1,fc2 = st.columns(2)
        with fc1:
            grp = df.groupby('label').agg(avg_src=('src_bytes','mean'),avg_dst=('dst_bytes','mean'),avg_dur=('duration','mean')).reset_index()
            fig = go.Figure()
            for lbl,col_k in [('avg_src','#00d4ff'),('avg_dst','#00ff88'),('avg_dur','#b96dff')]:
                fig.add_trace(go.Bar(name=lbl.replace('avg_',''),x=grp['label'],y=grp[lbl],marker_color=col_k,opacity=0.85))
            fig.update_layout(**CHART_LAYOUT,height=320,barmode='group',
                xaxis=dict(tickangle=30,gridcolor='rgba(0,212,255,0.04)'),yaxis=dict(gridcolor='rgba(0,212,255,0.04)'),
                legend=dict(bgcolor='rgba(0,0,0,0)'),title_text='Avg Bytes & Duration by Attack Type')
            st.plotly_chart(fig,use_container_width=True)
        with fc2:
            port_bins = pd.cut(df['port'],[0,1023,49151,65535],labels=['Well-Known','Registered','Dynamic'])
            pb = port_bins.value_counts().reset_index(); pb.columns=['range','count']
            flag_dist = df['flag'].value_counts().head(8).reset_index(); flag_dist.columns=['flag','count']
            fig = make_subplots(rows=1,cols=2,subplot_titles=('Port Ranges','TCP Flags'),specs=[[{'type':'domain'},{'type':'xy'}]])
            fig.add_trace(go.Pie(labels=pb['range'],values=pb['count'],hole=0.4,marker=dict(colors=['#00d4ff','#00ff88','#b96dff']),showlegend=False),1,1)
            fig.add_trace(go.Bar(x=flag_dist['flag'],y=flag_dist['count'],marker_color='#00d4ff',showlegend=False),1,2)
            fig.update_layout(**CHART_LAYOUT,height=320)
            st.plotly_chart(fig,use_container_width=True)

        st.markdown('<div class="sh">🔗 SANKEY FLOW DIAGRAM</div>', unsafe_allow_html=True)
        proto_list = df['protocol_type'].unique().tolist()
        svc_list   = df['service'].unique().tolist()
        lbl_list   = ATTACK_TYPES
        all_nodes  = proto_list + svc_list + lbl_list
        nidx       = {n:i for i,n in enumerate(all_nodes)}
        sample_sankey = df.sample(min(2000,len(df)),random_state=1)
        src_links,tgt_links,val_links,col_links=[],[],[],[]
        for (p,s),g in sample_sankey.groupby(['protocol_type','service']):
            src_links.append(nidx[p]); tgt_links.append(nidx[s]); val_links.append(len(g))
            col_links.append('rgba(0,212,255,0.25)')
        for (s,l),g in sample_sankey.groupby(['service','label']):
            src_links.append(nidx[s]); tgt_links.append(nidx[l]); val_links.append(len(g))
            col_links.append(hex_to_rgba(COLOR_MAP.get(l,'#00d4ff'), 0.4))
        node_colors = (['rgba(0,212,255,0.7)']*len(proto_list)+['rgba(0,255,136,0.7)']*len(svc_list)+
                       [hex_to_rgba(COLOR_MAP.get(l,'#00d4ff'), 0.85) for l in lbl_list])
        fig_sk = go.Figure(go.Sankey(
            node=dict(pad=12,thickness=16,line=dict(color='#010912',width=0.5),label=all_nodes,color=node_colors,hovertemplate='%{label}<extra></extra>'),
            link=dict(source=src_links,target=tgt_links,value=val_links,color=col_links)))
        fig_sk.update_layout(**CHART_LAYOUT,height=420,title_text='Protocol → Service → Attack Type Flow')
        st.plotly_chart(fig_sk,use_container_width=True)

    with tab3:
        st.markdown('<div class="sh">📋 RAW PACKET INSPECTOR</div>', unsafe_allow_html=True)
        pf1,pf2 = st.columns(2)
        with pf1: search_ip = st.text_input("Filter by IP (src or dst)", "")
        with pf2: n_rows    = st.selectbox("Rows", [50,100,200,500], index=1)
        show = df.copy()
        if search_ip:
            show = show[(show['src_ip'].str.contains(search_ip))|(show['dst_ip'].str.contains(search_ip))]
        dcols = ['timestamp','src_ip','dst_ip','protocol_type','service','src_bytes','dst_bytes','label','severity','risk_score','port','flag']
        sdf = show[dcols].tail(n_rows).copy()
        sdf['timestamp'] = pd.to_datetime(sdf['timestamp']).dt.strftime('%H:%M:%S')
        sdf['src_bytes']  = sdf['src_bytes'].astype(int)
        sdf['dst_bytes']  = sdf['dst_bytes'].astype(int)
        st.dataframe(sdf,use_container_width=True,height=400)
        st.download_button("⬇ Download CSV",sdf.to_csv(index=False),"traffic_log.csv","text/csv",use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: ML ENGINE
# ══════════════════════════════════════════════════════════════════════════════
elif "ML Engine" in page:
    st.markdown('<div class="sh">🤖 MULTI-MODEL ML ENGINE</div>', unsafe_allow_html=True)
    st.markdown("**Model Performance Comparison**")
    mc1,mc2,mc3 = st.columns(3)
    for i,(mname,mdata) in enumerate(model_results.items()):
        with [mc1,mc2,mc3][i]:
            star = " ⭐" if mname==best_model_name else ""
            border_clr = '#00ff88' if mname==best_model_name else 'rgba(0,212,255,0.15)'
            bars_html = "".join([f'<div class="model-bar-wrap"><div class="model-label">{k.upper()}</div><div class="risk-bar" style="background:rgba(255,255,255,0.04)"><div class="risk-fill" style="width:{v*100:.0f}%;background:#00ff88"></div></div><div style="font-family:JetBrains Mono;font-size:11px;color:#00ff88;text-align:right">{v*100:.1f}%</div></div>'
                                 for k,v in [("accuracy",mdata["accuracy"]),("precision",mdata["precision"]),("recall",mdata["recall"]),("f1",mdata["f1"])]])
            st.markdown(f'<div class="mcard c-green" style="border-color:{border_clr}"><div style="font-family:Orbitron;font-size:13px;color:#00d4ff;margin-bottom:10px">{mname}{star}</div>{bars_html}</div>', unsafe_allow_html=True)

    best_clf = model_results[best_model_name]['model']
    y_pred   = model_results[best_model_name]['y_pred']

    c1,c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="sh">📊 CONFUSION MATRIX — {best_model_name}</div>', unsafe_allow_html=True)
        cm = confusion_matrix(yte,y_pred)
        labels_cm = le.classes_
        fig_cm = go.Figure(go.Heatmap(z=cm,x=labels_cm,y=labels_cm,
            colorscale=[[0,'#010912'],[0.3,'#071e38'],[0.7,'#00d4ff'],[1,'#ff2d55']],
            text=cm,texttemplate='%{text}',textfont=dict(size=9,family='JetBrains Mono'),showscale=True))
        fig_cm.update_layout(**CHART_LAYOUT,height=380,
            xaxis=dict(title='Predicted',tickangle=35,tickfont=dict(size=9)),
            yaxis=dict(title='Actual',tickfont=dict(size=9)))
        st.plotly_chart(fig_cm,use_container_width=True)
    with c2:
        st.markdown('<div class="sh">🏆 FEATURE IMPORTANCE</div>', unsafe_allow_html=True)
        if hasattr(best_clf,'feature_importances_'):
            fi = pd.Series(best_clf.feature_importances_,index=FEAT_COLS).sort_values()
            bar_colors = ['#ff2d55' if v>fi.quantile(0.8) else '#00d4ff' if v>fi.median() else '#1e3a5f' for v in fi]
            fig_fi = go.Figure(go.Bar(x=fi.values,y=fi.index,orientation='h',
                marker=dict(color=bar_colors),text=[f"{v:.3f}" for v in fi.values],
                textposition='auto',textfont=dict(size=9,family='JetBrains Mono')))
            fig_fi.update_layout(**CHART_LAYOUT,height=380,
                xaxis=dict(gridcolor='rgba(0,212,255,0.04)'),yaxis=dict(gridcolor='rgba(0,212,255,0.04)'))
            st.plotly_chart(fig_fi,use_container_width=True)

    st.markdown('<div class="sh">📋 PER-CLASS METRICS</div>', unsafe_allow_html=True)
    cr = classification_report(yte,y_pred,target_names=le.classes_,output_dict=True,zero_division=0)
    cr_df = pd.DataFrame(cr).T.reset_index().rename(columns={'index':'class'})
    cr_df = cr_df[cr_df['class'].isin(le.classes_)].round(3)
    st.dataframe(cr_df,use_container_width=True,height=280)

    st.markdown('<div class="sh">🔮 LIVE PACKET PREDICTION</div>', unsafe_allow_html=True)
    with st.expander("⚡ Analyze a Custom Packet", expanded=True):
        lc1,lc2,lc3,lc4 = st.columns(4)
        inputs = {}
        fields = [
            ('duration',0.0,1000.0,5.0,'Duration (s)'),('src_bytes',0,100000,500,'Src Bytes'),
            ('dst_bytes',0,100000,200,'Dst Bytes'),('land',0,1,0,'Land'),
            ('wrong_fragment',0,10,0,'Wrong Frags'),('urgent',0,5,0,'Urgent'),
            ('hot',0,100,2,'Hot'),('num_failed_logins',0,10,0,'Failed Logins'),
            ('logged_in',0,1,1,'Logged In'),('num_compromised',0,50,0,'Compromised'),
            ('count',1,512,10,'Count'),('srv_count',1,512,10,'Srv Count'),
            ('same_srv_rate',0.0,1.0,0.5,'Same Srv Rate'),('diff_srv_rate',0.0,1.0,0.1,'Diff Srv Rate'),
            ('packet_size',0,65535,1024,'Packet Size'),('port',1,65535,80,'Port'),
            ('ttl',0,255,64,'TTL'),('risk_score',0,100,20,'Risk Score'),
        ]
        for i,(key,mn,mx,dv,lbl) in enumerate(fields):
            with [lc1,lc2,lc3,lc4][i%4]:
                if isinstance(mn,float) or isinstance(mx,float) or isinstance(dv,float):
                    inputs[key] = st.number_input(lbl,float(mn),float(mx),float(dv),key=f"p_{key}")
                else:
                    inputs[key] = st.number_input(lbl,mn,mx,dv,key=f"p_{key}")

        if st.button("🔍 CLASSIFY PACKET", use_container_width=True):
            inp = np.array([[inputs[f] for f in FEAT_COLS]])
            inp_s = sc.transform(inp)
            results_pred = {}
            for mname,mdata in model_results.items():
                pred  = mdata['model'].predict(inp_s)[0]
                proba = mdata['model'].predict_proba(inp_s)[0]
                results_pred[mname] = {'label':le.inverse_transform([pred])[0],'conf':proba.max()*100,'proba':proba}
            pc1,pc2,pc3 = st.columns(3)
            for col,(mname,res) in zip([pc1,pc2,pc3],results_pred.items()):
                is_atk = res['label']!='Normal'
                c_r = '#ff2d55' if is_atk else '#00ff88'
                with col:
                    st.markdown(f'<div class="mcard {"c-red" if is_atk else "c-green"}" style="border-color:{c_r}"><div style="font-family:JetBrains Mono;font-size:10px;color:#2a4a6a">{mname}</div><div style="font-family:Orbitron;font-size:1.2rem;color:{c_r};margin:6px 0">{"⛔" if is_atk else "✅"} {res["label"]}</div><div style="font-family:JetBrains Mono;font-size:11px;color:{c_r}">Confidence: {res["conf"]:.1f}%</div></div>', unsafe_allow_html=True)
            st.markdown("**Probability Distribution (Best Model)**")
            best_res = results_pred[best_model_name]
            prob_df = pd.DataFrame({'class':le.classes_,'prob':best_res['proba']*100}).sort_values('prob',ascending=False)
            fig_pb = go.Figure(go.Bar(x=prob_df['prob'],y=prob_df['class'],orientation='h',
                marker=dict(color=[COLOR_MAP.get(c,'#00d4ff') for c in prob_df['class']]),
                text=[f"{v:.1f}%" for v in prob_df['prob']],textposition='auto',textfont=dict(family='JetBrains Mono',size=10)))
            fig_pb.update_layout(**CHART_LAYOUT,height=300,xaxis=dict(title='Probability %',gridcolor='rgba(0,212,255,0.04)'))
            st.plotly_chart(fig_pb,use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: NETWORK GRAPH
# ══════════════════════════════════════════════════════════════════════════════
elif "Network Graph" in page:
    st.markdown('<div class="sh">🌐 ATTACK NETWORK TOPOLOGY</div>', unsafe_allow_html=True)
    nc1,nc2 = st.columns(2)
    with nc1: n_nodes = st.slider("Max Connections", 20, 100, 50)
    with nc2: sev_fil  = st.multiselect("Filter Severity",['critical','high','medium','low'],default=['critical','high'])

    sub = df[(df['is_attack']==1)&(df['severity'].isin(sev_fil))]
    sub = sub.sample(min(n_nodes,len(sub)),random_state=42)
    G = nx.DiGraph()
    for _,r in sub.iterrows():
        G.add_edge(r['src_ip'],r['dst_ip'],attack=r['label'],sev=r['severity'],risk=r['risk_score'])
    pos = nx.spring_layout(G,seed=42,k=1.5)
    fig_g = go.Figure()
    for u,v,data in G.edges(data=True):
        x0,y0=pos.get(u,(0,0)); x1,y1=pos.get(v,(0,0))
        fig_g.add_trace(go.Scatter(x=[x0,x1,None],y=[y0,y1,None],mode='lines',
            line=dict(color=sev_color(data.get('sev','low')),width=1.2),hoverinfo='none',showlegend=False))
    for n in G.nodes():
        x,y = pos.get(n,(0,0))
        deg = G.degree(n)
        is_src = G.out_degree(n) > G.in_degree(n)
        fig_g.add_trace(go.Scatter(x=[x],y=[y],mode='markers',
            marker=dict(size=8+deg*4,color='#ff2d55' if is_src else '#00d4ff',line=dict(color='rgba(0,0,0,0.5)',width=1)),
            text=n,hovertemplate=f'<b>{n}</b><br>Degree: {deg}<br>{"Attacker" if is_src else "Victim"}<extra></extra>',showlegend=False))
    fig_g.update_layout(**CHART_LAYOUT,height=480,
        xaxis=dict(showgrid=False,zeroline=False,visible=False),
        yaxis=dict(showgrid=False,zeroline=False,visible=False),
        title=dict(text='Network Attack Graph — 🔴 Attackers | 🔵 Victims',font=dict(size=12,color='#2a4a6a',family='Orbitron')))
    st.plotly_chart(fig_g,use_container_width=True)

    st.markdown('<div class="sh">📊 TOP NODES</div>', unsafe_allow_html=True)
    node_stats = [(n,G.out_degree(n),G.in_degree(n),G.degree(n)) for n in G.nodes()]
    ns_df = pd.DataFrame(node_stats,columns=['IP','Out Degree','In Degree','Total Degree'])
    st.dataframe(ns_df.sort_values('Total Degree',ascending=False).head(20),use_container_width=True,height=300)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: GEOIP THREAT MAP
# ══════════════════════════════════════════════════════════════════════════════
elif "GeoIP" in page:
    st.markdown('<div class="sh">🗺️ GLOBAL THREAT INTELLIGENCE MAP</div>', unsafe_allow_html=True)
    geo_df = df.copy()
    geo_df['lat'] = geo_df['country'].map(lambda c: COUNTRY_COORDS.get(c,(0,0))[0]) + np.random.uniform(-4,4,len(geo_df))
    geo_df['lon'] = geo_df['country'].map(lambda c: COUNTRY_COORDS.get(c,(0,0))[1]) + np.random.uniform(-4,4,len(geo_df))
    atk_geo = geo_df[geo_df['is_attack']==1]
    fig_map = go.Figure()
    for sev,color in [('critical','#ff2d55'),('high','#ff8c00'),('medium','#ffd60a'),('low','#00d4ff')]:
        sub_g = atk_geo[atk_geo['severity']==sev]
        if len(sub_g)==0: continue
        fig_map.add_trace(go.Scattergeo(lat=sub_g['lat'],lon=sub_g['lon'],mode='markers',name=sev.capitalize(),
            marker=dict(size=6,color=color,opacity=0.7,line=dict(color='rgba(0,0,0,0.3)',width=0.5)),
            hovertemplate=f'<b>%{{text}}</b><br>Severity: {sev}<extra></extra>',text=sub_g['label']))
    fig_map.update_layout(geo=dict(showland=True,landcolor='#071628',showocean=True,oceancolor='#020b18',
        showcoastlines=True,coastlinecolor='rgba(0,212,255,0.2)',showframe=False,bgcolor='#010912',
        showlakes=True,lakecolor='#010912',projection_type='equirectangular'),
        **CHART_LAYOUT,height=480,legend=dict(bgcolor='rgba(0,0,0,0)',font=dict(color='#4a6080',size=11)),
        title=dict(text='Live Attack Origins by Geography',font=dict(size=12,color='#2a4a6a',family='Orbitron')))
    st.plotly_chart(fig_map,use_container_width=True)

    gc1,gc2 = st.columns(2)
    with gc1:
        st.markdown('<div class="sh">🌍 TOP ATTACK COUNTRIES</div>', unsafe_allow_html=True)
        country_atk = df[df['is_attack']==1]['country'].value_counts().head(10).reset_index()
        country_atk.columns=['country','attacks']
        fig_c = go.Figure(go.Bar(x=country_atk['attacks'],y=country_atk['country'],orientation='h',
            marker=dict(color='#ff2d55',opacity=0.8),text=country_atk['attacks'],textposition='auto',
            textfont=dict(family='JetBrains Mono',size=11)))
        fig_c.update_layout(**CHART_LAYOUT,height=320,xaxis=dict(gridcolor='rgba(0,212,255,0.04)'),yaxis=dict(gridcolor='rgba(0,212,255,0.04)'))
        st.plotly_chart(fig_c,use_container_width=True)
    with gc2:
        st.markdown('<div class="sh">🎭 ATTACK TYPE BY COUNTRY</div>', unsafe_allow_html=True)
        ct = df[df['is_attack']==1].groupby(['country','label']).size().reset_index(name='n')
        top5_c = df[df['is_attack']==1]['country'].value_counts().head(5).index.tolist()
        ct5 = ct[ct['country'].isin(top5_c)]
        fig_ct = go.Figure()
        for lbl in ct5['label'].unique():
            sub_ct = ct5[ct5['label']==lbl]
            fig_ct.add_trace(go.Bar(name=lbl,x=sub_ct['country'],y=sub_ct['n'],marker_color=COLOR_MAP.get(lbl,'#00d4ff'),opacity=0.85))
        fig_ct.update_layout(**CHART_LAYOUT,height=320,barmode='stack',
            xaxis=dict(gridcolor='rgba(0,212,255,0.04)'),yaxis=dict(gridcolor='rgba(0,212,255,0.04)'),
            legend=dict(bgcolor='rgba(0,0,0,0)',font=dict(size=9)))
        st.plotly_chart(fig_ct,use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: THREAT INTEL
# ══════════════════════════════════════════════════════════════════════════════
elif "Threat Intel" in page:
    st.markdown('<div class="sh">⚠️ THREAT INTELLIGENCE CENTER</div>', unsafe_allow_html=True)
    ti1,ti2 = st.columns(2)
    with ti1:
        top_src = df[df['is_attack']==1]['src_ip'].value_counts().head(10).reset_index()
        top_src.columns=['ip','attacks']
        colors_s=['#ff2d55' if i==0 else '#ff8c00' if i<3 else '#00d4ff' for i in range(len(top_src))]
        fig_ts = go.Figure(go.Bar(x=top_src['attacks'],y=top_src['ip'],orientation='h',
            marker=dict(color=colors_s),text=top_src['attacks'],textposition='auto',
            textfont=dict(family='JetBrains Mono',size=11)))
        fig_ts.update_layout(**CHART_LAYOUT,height=320,title_text='Top Attacking IPs',
            xaxis=dict(gridcolor='rgba(0,212,255,0.04)'),yaxis=dict(gridcolor='rgba(0,212,255,0.04)'))
        st.plotly_chart(fig_ts,use_container_width=True)
    with ti2:
        sev_cnt = df[df['is_attack']==1]['severity'].value_counts()
        fig_sv = go.Figure(go.Bar(x=list(sev_cnt.index),y=list(sev_cnt.values),
            marker=dict(color=[sev_color(s) for s in sev_cnt.index])))
        fig_sv.update_layout(**CHART_LAYOUT,height=320,title_text='Attack Severity Distribution',
            xaxis=dict(gridcolor='rgba(0,212,255,0.04)'),yaxis=dict(gridcolor='rgba(0,212,255,0.04)'))
        st.plotly_chart(fig_sv,use_container_width=True)

    st.markdown('<div class="sh">📅 ATTACK TIMELINE</div>', unsafe_allow_html=True)
    atk_t = df[df['is_attack']==1].copy()
    atk_t['bucket'] = pd.to_datetime(atk_t['timestamp']).dt.floor('10min')
    tl = atk_t.groupby(['bucket','label']).size().reset_index(name='n')
    fig_tl = go.Figure()
    for lbl in atk_t['label'].unique():
        sub_tl = tl[tl['label']==lbl]
        fig_tl.add_trace(go.Scatter(x=sub_tl['bucket'],y=sub_tl['n'],
            name=lbl,mode='lines',stackgroup='one',
            line=dict(color=COLOR_MAP.get(lbl,'#00d4ff'),width=1),
            fillcolor=hex_to_rgba(COLOR_MAP.get(lbl,'#00d4ff'), 0.33)))
    fig_tl.update_layout(**CHART_LAYOUT,height=300,
        xaxis=dict(gridcolor='rgba(0,212,255,0.04)'),yaxis=dict(gridcolor='rgba(0,212,255,0.04)'),
        legend=dict(bgcolor='rgba(0,0,0,0)',font=dict(size=9)))
    st.plotly_chart(fig_tl,use_container_width=True)

    st.markdown('<div class="sh">📋 THREAT ENCYCLOPEDIA</div>', unsafe_allow_html=True)
    threats = [
        {"name":"DoS / DDoS","sev":"critical","icon":"💥","cve":"CVE-2023-1234","desc":"Floods target with requests to exhaust resources and deny legitimate access.","mitre":"T1498"},
        {"name":"SQL Injection","sev":"high","icon":"💉","cve":"CVE-2023-5678","desc":"Malicious SQL injected into queries to manipulate or exfiltrate database data.","mitre":"T1190"},
        {"name":"Port Scan","sev":"medium","icon":"🔭","cve":"N/A","desc":"Systematic enumeration of open ports to identify exploitable services.","mitre":"T1046"},
        {"name":"R2L Attack","sev":"high","icon":"🚪","cve":"CVE-2022-9012","desc":"Unauthorized remote-to-local access exploiting authentication weaknesses.","mitre":"T1078"},
        {"name":"U2R Exploit","sev":"critical","icon":"👑","cve":"CVE-2023-4567","desc":"Privilege escalation from normal user to root/admin level access.","mitre":"T1068"},
        {"name":"Ransomware","sev":"critical","icon":"🔒","cve":"CVE-2023-2345","desc":"Encrypts victim data and demands ransom for decryption key.","mitre":"T1486"},
        {"name":"MITM","sev":"high","icon":"👁","cve":"CVE-2023-7890","desc":"Intercepts network traffic between two parties to eavesdrop or modify data.","mitre":"T1557"},
        {"name":"Brute Force","sev":"high","icon":"🔨","cve":"N/A","desc":"Systematic credential guessing using dictionaries or exhaustive search.","mitre":"T1110"},
        {"name":"Zero-Day","sev":"critical","icon":"☢","cve":"CVE-2024-????","desc":"Exploit targeting unknown vulnerabilities with no available patches.","mitre":"T1203"},
    ]
    tc1,tc2,tc3 = st.columns(3)
    for i,t in enumerate(threats):
        col=[tc1,tc2,tc3][i%3]; c=sev_color(t['sev'])
        badge_cls = 'bc' if t['sev']=='critical' else 'bh' if t['sev']=='high' else 'bm'
        with col:
            st.markdown(f'<div style="background:var(--bg2);border:1px solid {hex_to_rgba(c,0.13)};border-left:3px solid {c};border-radius:8px;padding:14px;margin-bottom:10px"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px"><div style="font-family:Orbitron;font-size:12px;color:{c}">{t["icon"]} {t["name"]}</div><span class="badge {badge_cls}">{t["sev"].upper()}</span></div><div style="font-family:JetBrains Mono;font-size:10.5px;color:#2a4a6a;margin-bottom:8px">{t["desc"]}</div><div style="font-family:JetBrains Mono;font-size:10px;color:#1e3a5f">MITRE: <span style="color:{c}">{t["mitre"]}</span> &nbsp;|&nbsp; CVE: <span style="color:#2a4a6a">{t["cve"]}</span></div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: ADVANCED ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
elif "Advanced Analytics" in page:
    st.markdown('<div class="sh">📊 ADVANCED ANALYTICS ENGINE</div>', unsafe_allow_html=True)
    tab1,tab2,tab3 = st.tabs(["  Distributions  ","  3D Feature Space  ","  Correlations  "])

    with tab1:
        ac1,ac2 = st.columns(2)
        with ac1:
            sv = df.sample(1500,random_state=42)
            fig_v = go.Figure()
            for lbl in ['Normal','DoS','DDoS','Brute Force']:
                s = sv[sv['label']==lbl]
                fig_v.add_trace(go.Violin(y=np.log1p(s['src_bytes']),name=lbl,
                    line_color=COLOR_MAP.get(lbl,'#00d4ff'),
                    fillcolor=hex_to_rgba(COLOR_MAP.get(lbl,'#00d4ff'), 0.2),
                    box_visible=True,meanline_visible=True))
            fig_v.update_layout(**CHART_LAYOUT,height=340,title_text='Src Bytes Distribution',yaxis=dict(gridcolor='rgba(0,212,255,0.04)'))
            st.plotly_chart(fig_v,use_container_width=True)
        with ac2:
            fig_h = go.Figure()
            for lbl,clr in [('Normal','#00ff88'),('DoS','#ff2d55'),('DDoS','#ef4444'),('Brute Force','#f97316')]:
                s = df[df['label']==lbl]['duration']
                fig_h.add_trace(go.Histogram(x=np.log1p(s.clip(0,200)),name=lbl,nbinsx=40,marker_color=clr,opacity=0.65))
            fig_h.update_layout(**CHART_LAYOUT,height=340,barmode='overlay',title_text='Connection Duration',
                xaxis=dict(title='log(duration)',gridcolor='rgba(0,212,255,0.04)'),yaxis=dict(gridcolor='rgba(0,212,255,0.04)'))
            st.plotly_chart(fig_h,use_container_width=True)

        fig_box = go.Figure()
        for lbl in ATTACK_TYPES:
            s = df[df['label']==lbl]['risk_score']
            fig_box.add_trace(go.Box(y=s,name=lbl,
                marker_color=COLOR_MAP.get(lbl,'#00d4ff'),
                line_color=COLOR_MAP.get(lbl,'#00d4ff'),
                fillcolor=hex_to_rgba(COLOR_MAP.get(lbl,'#00d4ff'), 0.13)))
        fig_box.update_layout(**CHART_LAYOUT,height=320,title_text='Risk Score Distribution by Attack Type',
            xaxis=dict(tickangle=25),yaxis=dict(gridcolor='rgba(0,212,255,0.04)'))
        st.plotly_chart(fig_box,use_container_width=True)

    with tab2:
        st.markdown('<div class="sh">🌐 PCA 3D EMBEDDING</div>', unsafe_allow_html=True)
        colors_3d = [COLOR_MAP.get(l,'#00d4ff') for l in pca_labels]
        fig_3d = go.Figure(go.Scatter3d(
            x=pca_emb[:,0],y=pca_emb[:,1],z=pca_emb[:,2],mode='markers',
            marker=dict(size=3,color=colors_3d,opacity=0.7,line=dict(width=0)),
            text=pca_labels,hovertemplate='<b>%{text}</b><br>PC1:%{x:.2f}<br>PC2:%{y:.2f}<br>PC3:%{z:.2f}<extra></extra>'))
        fig_3d.update_layout(paper_bgcolor='rgba(1,9,18,0)',plot_bgcolor='rgba(1,9,18,0)',height=520,
            font=dict(family='JetBrains Mono',color='#4a6080'),
            scene=dict(bgcolor='rgba(1,9,18,0.95)',
                xaxis=dict(title=f'PC1 ({var_ratio[0]*100:.1f}%)',backgroundcolor='rgba(4,15,30,0.8)',gridcolor='rgba(0,212,255,0.08)',color='#4a6080'),
                yaxis=dict(title=f'PC2 ({var_ratio[1]*100:.1f}%)',backgroundcolor='rgba(4,15,30,0.8)',gridcolor='rgba(0,212,255,0.08)',color='#4a6080'),
                zaxis=dict(title=f'PC3 ({var_ratio[2]*100:.1f}%)',backgroundcolor='rgba(4,15,30,0.8)',gridcolor='rgba(0,212,255,0.08)',color='#4a6080')),
            margin=dict(l=0,r=0,t=20,b=0),
            title=dict(text=f'PCA 3D Feature Space — {len(pca_emb)} samples',font=dict(size=11,color='#2a4a6a',family='Orbitron')))
        st.plotly_chart(fig_3d,use_container_width=True)
        st.caption(f"Total variance explained: {sum(var_ratio)*100:.1f}%")

    with tab3:
        num_c = ['duration','src_bytes','dst_bytes','count','srv_count','same_srv_rate','diff_srv_rate','packet_size','is_attack','risk_score','port','ttl']
        corr = df[num_c].corr()
        fig_cr = go.Figure(go.Heatmap(z=corr.values,x=corr.columns,y=corr.index,
            colorscale=[[0,'#ff2d55'],[0.5,'#010912'],[1,'#00ff88']],
            zmid=0,text=np.round(corr.values,2),texttemplate='%{text}',textfont=dict(size=9,family='JetBrains Mono')))
        fig_cr.update_layout(**CHART_LAYOUT,height=460,title_text='Feature Correlation Matrix')
        st.plotly_chart(fig_cr,use_container_width=True)

        st.markdown('<div class="sh">📐 PARALLEL COORDINATES</div>', unsafe_allow_html=True)
        samp_pc = df.sample(800,random_state=5).copy()
        samp_pc['label_id'] = LabelEncoder().fit_transform(samp_pc['label'])
        dims = ['duration','src_bytes','dst_bytes','packet_size','risk_score','count']
        fig_pc = go.Figure(go.Parcoords(
            line=dict(color=samp_pc['label_id'],colorscale='Plasma',showscale=True,
                      colorbar=dict(title='Class',tickfont=dict(size=9,family='JetBrains Mono'))),
            dimensions=[dict(label=d,values=np.log1p(samp_pc[d])) for d in dims]))
        fig_pc.update_layout(**CHART_LAYOUT,height=380,title_text='Parallel Coordinates — log-scaled')
        st.plotly_chart(fig_pc,use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: ANOMALY DETECTION
# ══════════════════════════════════════════════════════════════════════════════
elif "Anomaly" in page:
    st.markdown('<div class="sh">🔮 ISOLATION FOREST ANOMALY DETECTION</div>', unsafe_allow_html=True)
    df2 = df.copy()
    df2['anomaly_score'] = ano_scores
    df2['is_anomaly']    = (ano_scores < np.percentile(ano_scores, 15)).astype(int)
    threshold_val = np.percentile(ano_scores, 15)

    am1,am2,am3,am4 = st.columns(4)
    for col,val,lbl,clr,cls in zip([am1,am2,am3,am4],
        [df2['is_anomaly'].sum(),f"{df2['anomaly_score'].mean():.3f}",f"{df2['anomaly_score'].min():.3f}",f"{df2[df2['is_anomaly']==1]['is_attack'].mean()*100:.0f}%"],
        ['ANOMALIES','AVG SCORE','MIN SCORE','OVERLAP W/ ATTACKS'],
        ['#ff2d55','#00d4ff','#ff8c00','#00ff88'],['c-red','c-cyan','c-orange','c-green']):
        with col:
            st.markdown(f'<div class="mcard {cls}"><div class="mv" style="color:{clr}">{val}</div><div class="ml">{lbl}</div></div>', unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    with c1:
        st.markdown('<div class="sh">📈 ANOMALY SCORE DISTRIBUTION</div>', unsafe_allow_html=True)
        fig_as = go.Figure()
        fig_as.add_trace(go.Histogram(x=df2[df2['is_attack']==0]['anomaly_score'],name='Normal',nbinsx=60,marker_color='#00ff88',opacity=0.7))
        fig_as.add_trace(go.Histogram(x=df2[df2['is_attack']==1]['anomaly_score'],name='Attack',nbinsx=60,marker_color='#ff2d55',opacity=0.7))
        fig_as.add_vline(x=threshold_val,line=dict(color='#ffd60a',width=2,dash='dash'))
        fig_as.add_annotation(x=threshold_val,y=1,text="Threshold",showarrow=False,font=dict(color='#ffd60a',family='JetBrains Mono',size=11),yref='paper')
        fig_as.update_layout(**CHART_LAYOUT,height=300,barmode='overlay',
            xaxis=dict(title='Anomaly Score',gridcolor='rgba(0,212,255,0.04)'),
            yaxis=dict(gridcolor='rgba(0,212,255,0.04)'),legend=dict(bgcolor='rgba(0,0,0,0)'))
        st.plotly_chart(fig_as,use_container_width=True)
    with c2:
        st.markdown('<div class="sh">🎯 ANOMALY vs ACTUAL LABEL</div>', unsafe_allow_html=True)
        overlap = df2.groupby('label').agg(total=('label','count'),anomalies=('is_anomaly','sum')).reset_index()
        overlap['anomaly_rate'] = overlap['anomalies']/overlap['total']*100
        fig_ov = go.Figure(go.Bar(x=overlap['anomaly_rate'],y=overlap['label'],orientation='h',
            marker=dict(color=[COLOR_MAP.get(l,'#00d4ff') for l in overlap['label']]),
            text=[f"{v:.1f}%" for v in overlap['anomaly_rate']],textposition='auto',textfont=dict(family='JetBrains Mono',size=10)))
        fig_ov.update_layout(**CHART_LAYOUT,height=300,title_text='Anomaly Rate per Label (%)',
            xaxis=dict(gridcolor='rgba(0,212,255,0.04)'),yaxis=dict(gridcolor='rgba(0,212,255,0.04)'))
        st.plotly_chart(fig_ov,use_container_width=True)

    st.markdown('<div class="sh">⏱️ ANOMALY SCORE OVER TIME</div>', unsafe_allow_html=True)
    time_sample = df2.sample(min(500,len(df2)),random_state=3).sort_values('timestamp')
    fig_ts_a = go.Figure()
    fig_ts_a.add_trace(go.Scatter(x=time_sample[time_sample['is_attack']==0]['timestamp'],y=time_sample[time_sample['is_attack']==0]['anomaly_score'],
        mode='markers',name='Normal',marker=dict(color='#00ff88',size=4,opacity=0.5)))
    fig_ts_a.add_trace(go.Scatter(x=time_sample[time_sample['is_attack']==1]['timestamp'],y=time_sample[time_sample['is_attack']==1]['anomaly_score'],
        mode='markers',name='Attack',marker=dict(color='#ff2d55',size=5,opacity=0.7)))
    fig_ts_a.add_hline(y=threshold_val,line=dict(color='#ffd60a',width=1.5,dash='dash'))
    fig_ts_a.update_layout(**CHART_LAYOUT,height=280,
        xaxis=dict(gridcolor='rgba(0,212,255,0.04)'),yaxis=dict(title='Anomaly Score',gridcolor='rgba(0,212,255,0.04)'),
        legend=dict(bgcolor='rgba(0,0,0,0)'))
    st.plotly_chart(fig_ts_a,use_container_width=True)

    st.markdown('<div class="sh">📋 TOP ANOMALIES</div>', unsafe_allow_html=True)
    top_ano = df2[df2['is_anomaly']==1].sort_values('anomaly_score').head(50)
    dcols2  = ['timestamp','src_ip','dst_ip','label','severity','anomaly_score','risk_score','protocol_type','port']
    sdf2 = top_ano[dcols2].copy()
    sdf2['timestamp']     = pd.to_datetime(sdf2['timestamp']).dt.strftime('%H:%M:%S')
    sdf2['anomaly_score'] = sdf2['anomaly_score'].round(4)
    st.dataframe(sdf2,use_container_width=True,height=320)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: INCIDENT LOG
# ══════════════════════════════════════════════════════════════════════════════
elif "Incident Log" in page:
    st.markdown('<div class="sh">📋 INCIDENT MANAGEMENT & LOG</div>', unsafe_allow_html=True)
    il1,il2,il3 = st.columns(3)
    with il1: sev_fi = st.multiselect("Severity",['critical','high','medium','low'],default=['critical','high'])
    with il2: type_fi= st.multiselect("Type",ATTACK_TYPES,default=ATTACK_TYPES[:6])
    with il3: n_inc  = st.selectbox("Show",['Last 50','Last 100','Last 200','All'],index=0)

    idf = df[(df['is_attack']==1)&(df['severity'].isin(sev_fi))&(df['label'].isin(type_fi))]
    n_map = {'Last 50':50,'Last 100':100,'Last 200':200,'All':len(idf)}
    idf = idf.sort_values('timestamp',ascending=False).head(n_map[n_inc])

    k1,k2,k3,k4 = st.columns(4)
    for col,val,lbl,clr,cls in zip([k1,k2,k3,k4],
        [len(idf),len(idf[idf['severity']=='critical']),idf['src_ip'].nunique(),f"{idf['risk_score'].mean():.0f}"],
        ['INCIDENTS','CRITICAL','UNIQUE SRCS','AVG RISK'],
        ['#ff2d55','#ff8c00','#00d4ff','#b96dff'],['c-red','c-orange','c-cyan','c-purple']):
        with col:
            st.markdown(f'<div class="mcard {cls}"><div class="mv" style="color:{clr}">{val}</div><div class="ml">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown('<div style="margin-top:16px"></div>', unsafe_allow_html=True)
    for _,r in idf.head(15).iterrows():
        sev=r['severity']; c=sev_color(sev)
        icons={'critical':'⛔','high':'🟠','medium':'🟡','low':'🔵','clean':'🟢'}
        risk_pct=min(100,r['risk_score'])
        st.markdown(f'<div style="background:#071628;border:1px solid {hex_to_rgba(c,0.13)};border-left:4px solid {c};border-radius:8px;padding:14px 18px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px"><div><div style="font-family:Orbitron;font-size:13px;color:{c};margin-bottom:4px">{icons.get(sev,"●")} {r["label"]} &nbsp; {badge(sev)}</div><div style="font-family:JetBrains Mono;font-size:11px;color:#2a4a6a">SRC: <span style="color:#4a6080">{r["src_ip"]}</span> &nbsp;→&nbsp; DST: <span style="color:#4a6080">{r["dst_ip"]}</span> &nbsp;|&nbsp; PORT: {r["port"]} &nbsp;|&nbsp; {r["protocol_type"].upper()} &nbsp;|&nbsp; {pd.to_datetime(r["timestamp"]).strftime("%H:%M:%S")}</div></div><div style="text-align:right"><div style="font-family:JetBrains Mono;font-size:10px;color:#1e3a5f;margin-bottom:4px">RISK SCORE</div><div style="font-family:Orbitron;font-size:1.3rem;color:{c}">{r["risk_score"]:.0f}</div><div class="risk-bar" style="width:80px;background:rgba(255,255,255,0.05)"><div class="risk-fill" style="width:{risk_pct}%;background:{c}"></div></div></div></div>', unsafe_allow_html=True)

    st.markdown('<div class="sh">📊 FULL INCIDENT TABLE</div>', unsafe_allow_html=True)
    idcols = ['timestamp','label','severity','src_ip','dst_ip','protocol_type','service','port','risk_score','country']
    idf2 = idf[idcols].copy()
    idf2['timestamp'] = pd.to_datetime(idf2['timestamp']).dt.strftime('%H:%M:%S')
    st.dataframe(idf2,use_container_width=True,height=350)
    st.download_button("⬇ Export Incidents CSV", idf2.to_csv(index=False), "incidents.csv", "text/csv", use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: SETTINGS & RULES
# ══════════════════════════════════════════════════════════════════════════════
elif "Settings" in page:
    st.markdown('<div class="sh">⚙️ SYSTEM CONFIGURATION & FIREWALL RULES</div>', unsafe_allow_html=True)
    tab1,tab2,tab3 = st.tabs(["  Engine Config  ","  Firewall Rules  ","  System Info  "])

    with tab1:
        sc1,sc2,sc3 = st.columns(3)
        with sc1:
            st.markdown("**🤖 Detection Engine**")
            algo     = st.selectbox("Primary Algorithm",["Random Forest","Gradient Boosting","Neural Network","Isolation Forest","Ensemble"])
            thresh   = st.slider("Alert Threshold", 0.0, 1.0, 0.75, 0.01)
            max_pkts = st.number_input("Max Packets/s", 100, 1000000, 50000)
            batch    = st.number_input("Batch Size", 10, 10000, 1000)
            st.markdown("**Detection Modules**")
            st.toggle("Deep Packet Inspection", value=True)
            st.toggle("Signature-Based Detection", value=True)
            st.toggle("Behavioral Analysis", value=True)
            st.toggle("ML Anomaly Detection", value=True)
            st.toggle("GeoIP Blocking", value=False)
            st.toggle("Auto-Block Attackers", value=False)
            st.toggle("Rate Limiting", value=True)
            st.toggle("SSL Inspection", value=False)
        with sc2:
            st.markdown("**🔔 Alert Configuration**")
            email  = st.toggle("Email Alerts", value=True)
            if email:
                st.text_input("Primary Email","soc@company.com")
                st.text_input("Secondary Email","admin@company.com")
            slack  = st.toggle("Slack Integration", value=False)
            if slack:
                st.text_input("Webhook URL","https://hooks.slack.com/...")
            st.toggle("PagerDuty", value=False)
            st.toggle("SIEM Export (Splunk/ELK)", value=True)
            st.markdown("**📁 Logging**")
            st.selectbox("Log Level",["DEBUG","INFO","WARNING","ERROR","CRITICAL"],index=1)
            st.slider("Log Retention (days)", 7, 730, 180)
            st.toggle("Encrypt Logs (AES-256)", value=True)
            st.toggle("Compress Old Logs", value=True)
            st.toggle("Remote Syslog", value=False)
        with sc3:
            st.markdown("**🌐 Network Settings**")
            st.selectbox("Interface",["eth0","eth1","wlan0","bond0","All"])
            st.text_input("Monitored Subnets","192.168.0.0/16, 10.0.0.0/8")
            st.number_input("Capture Buffer (MB)", 64, 4096, 512)
            st.number_input("Connection Timeout (s)", 5, 300, 30)
            st.markdown("**🔐 Response Actions**")
            st.toggle("Auto-Block Critical IPs", value=True)
            st.toggle("Rate-Limit Suspicious IPs", value=True)
            st.toggle("Notify Admin on Zero-Day", value=True)
            st.toggle("Quarantine Infected Hosts", value=False)
            st.toggle("Honeypot Redirect", value=False)
            st.slider("Auto-Block Duration (min)", 1, 1440, 60)

        bc1,bc2,bc3,bc4 = st.columns(4)
        with bc1:
            if st.button("💾 Save Config",use_container_width=True):
                with st.spinner("Saving..."): time.sleep(0.6)
                st.success("✅ Saved!")
        with bc2:
            if st.button("🔄 Restart Engine",use_container_width=True):
                with st.spinner("Restarting..."): time.sleep(1.2)
                st.success("✅ Engine restarted!")
        with bc3:
            if st.button("📤 Export Report",use_container_width=True):
                st.info("📄 PDF report queued")
        with bc4:
            if st.button("🗑️ Clear Logs",use_container_width=True):
                st.warning("⚠️ Confirm in production!")

    with tab2:
        st.markdown("**Current Firewall Rules**")
        rules_df = pd.DataFrame({
            'ID':     ['FW-001','FW-002','FW-003','FW-004','FW-005','FW-006','FW-007','FW-008'],
            'Name':   ['Allow SSH Internal','Allow HTTPS Out','Block Telnet','Block MySQL External','Allow DNS','Block ICMP Flood','Allow HTTP','Block TOR Exit Nodes'],
            'Source': ['192.168.0.0/16','0.0.0.0/0','0.0.0.0/0','0.0.0.0/0','0.0.0.0/0','0.0.0.0/0','0.0.0.0/0','0.0.0.0/0'],
            'Dest':   ['*','*','*','10.0.0.50','8.8.8.8','*','*','*'],
            'Port':   ['22','443','23','3306','53','*','80','*'],
            'Proto':  ['TCP','TCP','TCP','TCP','UDP','ICMP','TCP','TCP'],
            'Action': ['ALLOW','ALLOW','DROP','DROP','ALLOW','RATE-LIMIT','ALLOW','DROP'],
            'Status': ['Active']*8,
        })
        st.dataframe(rules_df,use_container_width=True,height=280)
        st.markdown("**Add New Rule**")
        nr1,nr2,nr3,nr4,nr5 = st.columns(5)
        with nr1: nr_name = st.text_input("Rule Name","")
        with nr2: nr_src  = st.text_input("Source","0.0.0.0/0")
        with nr3: nr_port = st.text_input("Port","*")
        with nr4: nr_act  = st.selectbox("Action",["ALLOW","DROP","RATE-LIMIT","LOG"])
        with nr5:
            st.markdown("<div style='height:28px'></div>",unsafe_allow_html=True)
            if st.button("➕ Add Rule",use_container_width=True) and nr_name:
                st.success(f"✅ Rule '{nr_name}' added!")

    with tab3:
        si1,si2 = st.columns(2)
        with si1:
            st.markdown("**System Information**")
            for k,v in {'IDS Version':'NeuralGuard v3.0.0','Engine':'Python 3.11 + Scikit-learn 1.4',
                'Dataset':'KDD Cup 99+ Extended (8,000 samples)','Models Loaded':'3 (RF, GBM, MLP)',
                'Features':f'{len(FEAT_COLS)} engineered features','Best Model':best_model_name,
                'Best Accuracy':f"{best['accuracy']*100:.2f}%",'Best F1 Score':f"{best['f1']*100:.2f}%",
                'Attack Classes':len(ATTACK_TYPES),'License':'Enterprise Edition'}.items():
                st.markdown(f'<div class="stat-row"><span style="color:#2a4a6a">{k}</span><span style="color:#00d4ff">{v}</span></div>', unsafe_allow_html=True)
        with si2:
            st.markdown("**Resource Usage (Simulated)**")
            for metric,val,color in [("CPU Usage",42,'#00ff88'),("Memory Usage",58,'#00d4ff'),
                                      ("Disk Usage",31,'#ffd60a'),("Network Load",76,'#ff8c00'),
                                      ("Model Inference Load",23,'#b96dff')]:
                st.markdown(f'<div style="margin-bottom:12px"><div style="display:flex;justify-content:space-between;font-family:JetBrains Mono;font-size:11px;margin-bottom:3px"><span style="color:#2a4a6a">{metric}</span><span style="color:{color}">{val}%</span></div><div class="risk-bar" style="background:rgba(255,255,255,0.04)"><div class="risk-fill" style="width:{val}%;background:{color}"></div></div></div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top:48px;padding:18px 0;border-top:1px solid rgba(0,212,255,0.08);
            text-align:center;font-family:'JetBrains Mono',monospace;font-size:11px;color:#1e3a5f">
  🛡️ NeuralGuard IDS v3.0.0 &nbsp;·&nbsp;
  Random Forest + Gradient Boosting + MLP + Isolation Forest &nbsp;·&nbsp;
  KDD Cup 99+ Extended Dataset &nbsp;·&nbsp;
  Streamlit + Plotly + Scikit-learn + NetworkX &nbsp;·&nbsp;
  <span style="color:#00d4ff">Enterprise Edition</span>
</div>
""", unsafe_allow_html=True)
