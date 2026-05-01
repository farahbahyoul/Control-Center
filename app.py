import os
import base64
from io import BytesIO
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from io import BytesIO

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    MATPLOTLIB_PDF_AVAILABLE = True
except Exception:
    MATPLOTLIB_PDF_AVAILABLE = False

st.set_page_config(page_title="U263 Serpentin Control Center", layout="wide")

# ============================================================
# COLOR PALETTE
# ============================================================

GREEN_DARK = "#063B34"
GREEN_MAIN = "#16A34A"
GREEN_ACCENT = "#00B894"
GREEN_SOFT = "#DFF7EA"
GREEN_LIGHT = "#F7FAF9"
ORANGE_MAIN = "#F97316"
ORANGE_SOFT = "#FFE1C2"
RED_MAIN = "#DC2626"
RED_SOFT = "#FEE2E2"
SIDEBAR_LIGHT = "#003C34"
SIDEBAR_ACCENT = "#005246"
GRAY_TEXT = "#6B7280"
CARD_BG = "#FFFFFF"
BORDER_SOFT = "#DDE7E2"

# ============================================================
# STYLE
# ============================================================

st.markdown(f"""
<style>
:root {{
    --green-dark: {GREEN_DARK};
    --green-main: {GREEN_MAIN};
    --green-accent: {GREEN_ACCENT};
    --green-soft: {GREEN_SOFT};
    --green-light: {GREEN_LIGHT};
    --orange-main: {ORANGE_MAIN};
    --orange-soft: {ORANGE_SOFT};
    --red-main: {RED_MAIN};
    --red-soft: {RED_SOFT};
    --sidebar-light: {SIDEBAR_LIGHT};
    --sidebar-accent: {SIDEBAR_ACCENT};
    --gray-text: {GRAY_TEXT};
    --card-bg: {CARD_BG};
    --border-soft: {BORDER_SOFT};
}}

.block-container {{
    padding-top: 1.4rem;
    padding-bottom: 2rem;
    background-color: var(--green-light);
}}

.main-title {{
    font-size: 32px;
    font-weight: 900;
    color: var(--green-dark);
    margin-bottom: 4px;
    text-align: center;
}}
.subtitle {{
    font-size: 15px;
    color: var(--gray-text);
    margin-bottom: 20px;
    text-align: center;
}}
.logo-container {{ display: flex; justify-content: center; margin-bottom: 10px; }}

.control-panel {{
    background: var(--card-bg);
    padding: 18px 22px;
    border-radius: 20px;
    box-shadow: 0 6px 18px rgba(15,47,42,0.08);
    border: 1px solid var(--border-soft);
    margin-bottom: 20px;
}}

.kpi-card {{
    background: var(--card-bg);
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 6px 18px rgba(15,47,42,0.08);
    border-left: 8px solid var(--green-main);
    min-height: 126px;
}}
.kpi-card.orange {{ border-left-color: var(--orange-main); }}
.kpi-card.red {{ border-left-color: var(--red-main); }}
.kpi-title {{ font-size: 15px; color: var(--gray-text); margin-bottom: 10px; }}
.kpi-value {{ font-size: 32px; font-weight: 900; color: var(--green-dark); }}
.kpi-note {{ font-size: 13px; color: #7B8794; }}

.good-box, .warning-box, .danger-box {{
    padding: 16px;
    border-radius: 14px;
    font-weight: 700;
    margin: 8px 0 12px 0;
}}
.good-box {{ background-color: var(--green-soft); border-left: 7px solid var(--green-main); color: var(--green-dark); }}
.warning-box {{ background-color: var(--orange-soft); border-left: 7px solid var(--orange-main); color: #7A4F00; }}
.danger-box {{ background-color: var(--red-soft); border-left: 7px solid var(--red-main); color: #7F1D1D; }}

.maintenance-card {{
    background: var(--card-bg);
    padding: 18px 22px;
    border-radius: 18px;
    box-shadow: 0 5px 16px rgba(15,47,42,0.08);
    margin-bottom: 14px;
}}
.card-title {{ font-size: 18px; font-weight: 850; color: var(--green-dark); }}
.card-line {{ margin-top: 8px; color: #40464f; font-size: 15px; }}

.fondoir-circle-card {{
    background: var(--card-bg);
    border: 1px solid var(--border-soft);
    border-radius: 22px;
    padding: 22px 12px 18px 12px;
    box-shadow: 0 5px 16px rgba(15,47,42,0.08);
    text-align: center;
    min-height: 230px;
}}
.fondoir-circle {{
    width: 142px;
    height: 142px;
    border-radius: 50%;
    margin: auto;
    display: flex;
    align-items: center;
    justify-content: center;
}}
.fondoir-circle-inner {{
    width: 98px;
    height: 98px;
    border-radius: 50%;
    background: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    box-shadow: inset 0 0 0 1px #E5E7EB;
}}
.fondoir-percent {{
    font-size: 24px;
    font-weight: 900;
    color: var(--green-dark);
    line-height: 1;
}}
.fondoir-name {{
    margin-top: 12px;
    font-size: 21px;
    font-weight: 900;
    color: var(--green-dark);
}}
.fondoir-status {{
    margin-top: 4px;
    font-size: 14px;
    color: var(--gray-text);
    font-weight: 700;
}}
.report-section {{
    background: var(--card-bg);
    border: 1px solid var(--border-soft);
    border-radius: 22px;
    padding: 20px 24px;
    box-shadow: 0 5px 16px rgba(15,47,42,0.06);
    margin-bottom: 16px;
}}
.report-section-title {{
    font-size: 23px;
    font-weight: 900;
    color: var(--green-dark);
    margin-bottom: 8px;
}}
.report-line {{
    color: #40464f;
    font-size: 15px;
    line-height: 1.65;
}}

[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, var(--sidebar-light), var(--sidebar-accent));
}}
[data-testid="stSidebar"] img {{
    filter: brightness(0) invert(1);
}}
[data-testid="stSidebar"] .block-container {{
    padding-top: 0.55rem;
    padding-bottom: 0.55rem;
}}
[data-testid="stSidebar"] label {{
    font-size: 12.5px !important;
    line-height: 1.15 !important;
}}
[data-testid="stSidebar"] .stNumberInput,
[data-testid="stSidebar"] .stSelectbox,
[data-testid="stSidebar"] .stDateInput,
[data-testid="stSidebar"] .stTextInput,
[data-testid="stSidebar"] .stTextArea,
[data-testid="stSidebar"] .stSlider,
[data-testid="stSidebar"] .stRadio,
[data-testid="stSidebar"] .stFileUploader {{
    margin-bottom: 0.25rem !important;
}}
[data-testid="stSidebar"] [data-testid="stExpander"] {{
    margin-bottom: 0.45rem !important;
}}
[data-testid="stSidebar"] [data-testid="stExpander"] details {{
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.22);
    border-radius: 12px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.10);
}}
[data-testid="stSidebar"] [data-testid="stExpander"] details summary {{
    padding-top: 0.35rem !important;
    padding-bottom: 0.35rem !important;
}}
[data-testid="stSidebar"] [data-baseweb="input"] {{ min-height: 34px !important; }}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p {{
    color: #F8FAFC !important;
}}
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] textarea {{
    color: #0F172A !important;
    background-color: white !important;
}}
[data-testid="stSidebar"] [data-baseweb="input"],
[data-testid="stSidebar"] [data-baseweb="select"],
[data-testid="stSidebar"] [data-baseweb="textarea"] {{
    background-color: white !important;
    border-radius: 10px;
}}
[data-testid="stSidebar"] [data-baseweb="select"] * {{ color: #0F172A !important; }}
[data-testid="stSidebar"] [role="radiogroup"] label span,
[data-testid="stSidebar"] [data-testid="stExpander"] summary p {{
    color: #F8FAFC !important;
    font-weight: 750;
}}
[data-testid="stTabs"] button {{ font-size: 16px; font-weight: 700; }}
h1, h2, h3 {{ color: var(--green-dark); }}
.stButton button, .stDownloadButton button {{
    background-color: var(--green-main);
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: 700;
}}
.stButton button:hover, .stDownloadButton button:hover {{
    background-color: var(--green-dark);
    color: white;
}}
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATA GENERATION
# ============================================================

def generate_demo_incidents():
    np.random.seed(42)
    start = datetime(2025, 1, 1)
    dates = [start + timedelta(days=int(x)) for x in np.random.randint(0, 359, 500)]
    equipments = np.random.choice(
        ["AF01", "BF01", "CF01", "DF01", "AR02", "BR02", "CR02", "DR02"],
        size=500,
        p=[0.19, 0.20, 0.23, 0.22, 0.04, 0.04, 0.04, 0.04]
    )
    causes = np.random.choice(
        [
            "Chute de pression vapeur", "Température basse", "Formation de blocs",
            "Manque vapeur", "Encrassement serpentin", "Défaut purgeur", "Fuite vapeur", "Autre"
        ],
        size=500,
        p=[0.34, 0.28, 0.20, 0.07, 0.04, 0.03, 0.02, 0.02]
    )
    return pd.DataFrame({"date": dates, "equipement": equipments, "cause": causes, "gravite": np.random.randint(1, 6, size=500)})


def generate_demo_serpentins():
    np.random.seed(20)
    rows = []
    for fondoir in ["AF01", "BF01", "CF01", "DF01"]:
        for i in range(1, 9):
            install_date = datetime(2025, 1, 1) + timedelta(days=np.random.randint(0, 300))
            status = np.random.choice(["En service", "Hors service", "Réparé"], p=[0.72, 0.18, 0.10])
            rows.append({
                "fondoir": fondoir,
                "serpentin": f"{fondoir}-S{i}",
                "etat": status,
                "date_installation": install_date,
                "derniere_maintenance": install_date + timedelta(days=np.random.randint(20, 250))
            })
    return pd.DataFrame(rows)


def generate_demo_process():
    np.random.seed(12)
    dates = pd.date_range("2025-01-01", periods=359, freq="D")
    return pd.DataFrame({
        "date": dates,
        "pression_vapeur_bar": np.random.normal(6.6, 0.7, len(dates)),
        "temperature_vapeur_c": np.random.normal(174, 6, len(dates)),
        "temperature_soufre_c": np.random.normal(140, 4, len(dates))
    })


def generate_demo_maintenance():
    today = datetime.today()
    rows = [
        [1, "Contrôle de la pression de vapeur MP à l’entrée des serpentins", "J", "Systématique", 1, "PDM", 0.25],
        [2, "Contrôle de la température de vapeur après désurchauffeur", "J", "Systématique", 1, "PDM", 0.25],
        [3, "Vérification du bon fonctionnement des purgeurs vapeur", "H", "Préventive", 2, "Inspecteur mécanique", 1],
        [4, "Contrôle de l’évacuation correcte des condensats", "H", "Préventive", 2, "Inspecteur mécanique", 1],
        [5, "Inspection visuelle des fuites vapeur et points chauds anormaux", "H", "Préventive", 2, "Inspecteur mécanique", 0.75],
        [6, "Vérification de l’état d’isolation thermique des lignes vapeur", "BM", "Préventive", 2, "Exécution mécanique", 1],
        [7, "Analyse des tendances d’incidents thermiques : température, chute P MP, blocs", "BM", "Préventive", 1, "PDM", 1],
        [8, "Inspection visuelle externe des serpentins : corrosion / traces d’attaque", "M", "Préventive", 2, "Inspecteur mécanique", 1.5],
        [9, "Contrôle de l’état des soudures et zones critiques", "M", "Préventive", 2, "Inspecteur mécanique", 2],
        [10, "Contrôle de l’encrassement externe / dépôts solides sur serpentins", "M", "Préventive", 2, "Exécution mécanique", 2],
        [11, "Vérification de stabilité des paramètres opératoires vapeur / soufre", "M", "Systématique", 1, "PDM", 1],
        [12, "Mesure d’épaisseur par ultrasons", "T", "Préventive", 2, "PDM", 3],
        [13, "Contrôle approfondi de l’intégrité mécanique des serpentins", "S", "Préventive", 3, "Inspecteur mécanique", 4],
        [14, "Nettoyage / décalaminage des dépôts accumulés", "S", "Préventive", 3, "Exécution mécanique", 4],
        [15, "Révision majeure / remplacement ciblé des tronçons dégradés", "A", "Préventive", 4, "Exécution mécanique", 12],
    ]
    df = pd.DataFrame(rows, columns=["n", "tache", "periodicite", "type_action", "nombre_intervenants", "intervenants", "duree_intervention_h"])
    freq_days = {"J": 1, "H": 7, "BM": 15, "M": 30, "T": 90, "S": 180, "A": 365}
    df["frequence_jours"] = df["periodicite"].map(freq_days)
    np.random.seed(8)
    df["derniere_intervention"] = [today - timedelta(days=np.random.randint(1, int(freq_days[p] + 20))) for p in df["periodicite"]]
    df["prochaine_intervention"] = df["derniere_intervention"] + pd.to_timedelta(df["frequence_jours"], unit="D")
    df["charge_homme_h"] = df["nombre_intervenants"] * df["duree_intervention_h"]
    return df


def generate_demo_amdec():
    return pd.DataFrame({
        "mode_defaillance": [
            "Perte efficacité thermique", "Perforation", "Perte efficacité par condensat",
            "Encrassement thermique", "Détection tardive", "Rupture soudure", "Usure interne", "Défaut fabrication"
        ],
        "G": [9, 10, 8, 8, 7, 9, 7, 6],
        "O": [8, 6, 7, 7, 6, 5, 5, 4],
        "D": [7, 6, 7, 6, 8, 5, 5, 6]
    })

# ============================================================
# HELPERS
# ============================================================

def load_file(uploaded_file):
    if uploaded_file is None:
        return None
    try:
        if uploaded_file.name.lower().endswith(".csv"):
            return pd.read_csv(uploaded_file)
        return pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Erreur de lecture du fichier : {e}")
        return None


def normalize_columns(df):
    df = df.copy()
    df.columns = df.columns.astype(str).str.strip().str.lower().str.replace(" ", "_", regex=False).str.replace("-", "_", regex=False)
    return df


def clean_label(text):
    return str(text).replace("_", " ").capitalize()


def status_color_class(status):
    if status == "red":
        return "red"
    if status == "orange":
        return "orange"
    return ""


def kpi_card(title, value, note="", status="green"):
    st.markdown(f"""
    <div class="kpi-card {status_color_class(status)}">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)


def fondoir_circle(name, value, status_label, status="green"):
    colors = {
        "green": (GREEN_MAIN, GREEN_SOFT),
        "orange": (ORANGE_MAIN, ORANGE_SOFT),
        "red": (RED_MAIN, RED_SOFT),
    }
    color, soft = colors.get(status, colors["green"])
    value = max(0, min(float(value), 100))
    st.markdown(f"""
    <div class="fondoir-circle-card">
        <div class="fondoir-circle" style="background: conic-gradient({color} {value}%, #E5E7EB 0);">
            <div class="fondoir-circle-inner" style="background:{soft};">
                <div class="fondoir-percent">{value:.1f}%</div>
            </div>
        </div>
        <div class="fondoir-name">{name}</div>
        <div class="fondoir-status">{status_label}</div>
    </div>
    """, unsafe_allow_html=True)


def maintenance_card(row, color=GREEN_MAIN):
    date_value = row.get("prochaine_intervention", "")
    if pd.notna(date_value):
        try:
            date_value = pd.to_datetime(date_value).strftime("%d/%m/%Y")
        except Exception:
            pass
    st.markdown(f"""
    <div class="maintenance-card" style="border-left: 7px solid {color};">
        <div class="card-title">Action n°{row.get('n', '')} — {row.get('tache', '')}</div>
        <div class="card-line"><b>Périodicité :</b> {row.get('periodicite', '')} &nbsp;&nbsp; | &nbsp;&nbsp; <b>Type :</b> {row.get('type_action', '')}</div>
        <div class="card-line"><b>Intervenant :</b> {row.get('intervenants', '')} &nbsp;&nbsp; | &nbsp;&nbsp; <b>Durée :</b> {row.get('duree_intervention_h', '')} h</div>
        <div class="card-line"><b>Prochaine intervention :</b> {date_value} &nbsp;&nbsp; | &nbsp;&nbsp; <b>Statut :</b> {row.get('statut', '')}</div>
    </div>
    """, unsafe_allow_html=True)


def color_for_availability(v, target):
    if v < target - 10:
        return "Critique"
    if v < target:
        return "À surveiller"
    return "Bon"


def color_for_risk(v):
    if v >= 70:
        return "Critique"
    if v >= 35:
        return "À surveiller"
    return "Bon"


def add_maintenance_status(df):
    df = df.copy()
    today = pd.Timestamp.today().normalize()
    if "prochaine_intervention" in df.columns:
        df["prochaine_intervention"] = pd.to_datetime(df["prochaine_intervention"], errors="coerce")
        df["statut"] = np.where(
            df["prochaine_intervention"].dt.normalize() < today,
            "En retard",
            np.where(df["prochaine_intervention"].dt.normalize() == today, "À faire aujourd’hui", "Planifiée")
        )
    return df


def prepare_display_table(df):
    out = df.copy()
    out.columns = [clean_label(c) for c in out.columns]
    return out


def create_pdf_report(summary_dict, recommendations, top_causes, critical_fondoirs, maintenance_summary):
    if not MATPLOTLIB_PDF_AVAILABLE:
        return None

    def card_color(kind, value):
        if kind == "risk":
            return RED_MAIN if value >= 70 else ORANGE_MAIN if value >= 35 else GREEN_MAIN
        if kind == "incidents":
            return RED_MAIN if value > 10 else ORANGE_MAIN if value > 5 else GREEN_MAIN
        if kind == "late":
            return RED_MAIN if value > 5 else ORANGE_MAIN if value > 0 else GREEN_MAIN
        if kind == "availability":
            target = float(summary_dict.get("Disponibilité cible (%)", 85))
            return RED_MAIN if value < target - 10 else ORANGE_MAIN if value < target else GREEN_MAIN
        return GREEN_MAIN

    def draw_kpi_card(ax, x, y, w, h, title, value, note, color):
        import matplotlib.patches as patches
        bg = RED_SOFT if color == RED_MAIN else ORANGE_SOFT if color == ORANGE_MAIN else GREEN_SOFT
        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.025", linewidth=0, facecolor=bg)
        ax.add_patch(card)
        ax.add_patch(patches.FancyBboxPatch((x, y), w * 0.035, h, boxstyle="round,pad=0.012,rounding_size=0.025", linewidth=0, facecolor=color))
        ax.text(x + w * 0.12, y + h * 0.70, title, fontsize=9, color=GRAY_TEXT, weight="bold")
        ax.text(x + w * 0.12, y + h * 0.36, str(value), fontsize=18, color=GREEN_DARK, weight="bold")
        ax.text(x + w * 0.12, y + h * 0.13, note, fontsize=8, color=GRAY_TEXT)

    buffer = BytesIO()
    with PdfPages(buffer) as pdf:
        fig = plt.figure(figsize=(8.27, 11.69))
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis("off")

        ax.text(0.06, 0.95, "Rapport global - U263 Serpentin Control Center", fontsize=18, weight="bold", color=GREEN_DARK)
        ax.text(0.06, 0.925, f"Date de génération : {datetime.today().strftime('%d/%m/%Y %H:%M')}", fontsize=9, color=GRAY_TEXT)

        total_inc = int(summary_dict.get("Total incidents", 0))
        inc_day = float(summary_dict.get("Incidents par jour", 0))
        av = float(summary_dict.get("Disponibilité (%)", 0))
        late = int(summary_dict.get("Actions PMP en retard", 0))
        risk = int(summary_dict.get("Score de risque", 0))

        kpis = [
            ("Total incidents", total_inc, "Historique analysé", ORANGE_MAIN if total_inc > 0 else GREEN_MAIN),
            ("Incidents / jour", f"{inc_day:.2f}", "Fréquence moyenne", card_color("incidents", inc_day)),
            ("Disponibilité", f"{av:.1f} %", "Serpentins", card_color("availability", av)),
            ("Actions en retard", late, "Maintenance PMP", card_color("late", late)),
            ("Score de risque", f"{risk}/100", "Indicateur global", card_color("risk", risk)),
        ]

        x0, y0, w, h, gap = 0.06, 0.80, 0.165, 0.105, 0.015
        for i, (title, value, note, color) in enumerate(kpis):
            draw_kpi_card(ax, x0 + i * (w + gap), y0, w, h, title, value, note, color)

        ax.text(0.06, 0.735, "Diagnostic global", fontsize=14, weight="bold", color=GREEN_DARK)
        if risk >= 70:
            diagnostic = "Critique : plusieurs paramètres dépassent les seuils de contrôle. Une action prioritaire est nécessaire."
        elif risk >= 35:
            diagnostic = "À surveiller : dérives modérées détectées."
        else:
            diagnostic = "Maîtrisé : paramètres globalement conformes."
        ax.text(0.06, 0.705, diagnostic, fontsize=10, color="#333333", wrap=True)

        ax.text(0.06, 0.665, "Indicateurs clés", fontsize=14, weight="bold", color=GREEN_DARK)
        y = 0.635
        key_lines = [
            f"Serpentins disponibles : {summary_dict.get('Serpentins disponibles', '-')}",
            f"Serpentins indisponibles : {summary_dict.get('Serpentins indisponibles', '-')}",
            f"Pression vapeur actuelle : {summary_dict.get('Pression vapeur actuelle (bar)', '-')} bar",
            f"Température soufre actuelle : {summary_dict.get('Température soufre actuelle (°C)', '-')} °C",
            f"Taux de réalisation PMP : {summary_dict.get('Taux de réalisation PMP (%)', '-')} %",
            f"Actions prévues dans 7 jours : {summary_dict.get('Actions prévues dans 7 jours', '-')}",
        ]
        for line in key_lines:
            ax.text(0.08, y, "- " + line, fontsize=10, color="#333333")
            y -= 0.026

        ax.text(0.06, y - 0.015, "Recommandations", fontsize=14, weight="bold", color=GREEN_DARK)
        y -= 0.045
        if recommendations:
            for rec in recommendations[:7]:
                ax.text(0.08, y, "- " + str(rec), fontsize=9.5, color="#333333", wrap=True)
                y -= 0.035
        else:
            ax.text(0.08, y, "Aucune action corrective urgente générée automatiquement selon les seuils actuels.", fontsize=9.5, color="#333333")

        ax.text(0.06, 0.10, "Les KPI ci-dessus sont générés automatiquement à partir des valeurs affichées dans le dashboard.", fontsize=8, color=GRAY_TEXT)
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        fig = plt.figure(figsize=(8.27, 11.69))
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis("off")
        ax.text(0.06, 0.95, "Synthèse détaillée", fontsize=18, weight="bold", color=GREEN_DARK)

        ax1 = fig.add_axes([0.10, 0.58, 0.80, 0.28])
        if top_causes is not None and len(top_causes) > 0:
            tc = top_causes.copy().head(5)
            ax1.barh(tc.iloc[:, 0].astype(str), pd.to_numeric(tc.iloc[:, 1], errors="coerce"), color=GREEN_MAIN)
            ax1.set_title("Top 5 des causes d'incidents", fontsize=12, color=GREEN_DARK)
            ax1.set_xlabel("Nombre")
            ax1.invert_yaxis()
        else:
            ax1.text(0.5, 0.5, "Aucune donnée d'incident disponible", ha="center", va="center")
            ax1.axis("off")

        ax2 = fig.add_axes([0.10, 0.25, 0.80, 0.24])
        if critical_fondoirs is not None and len(critical_fondoirs) > 0:
            cf = critical_fondoirs.copy()
            vals = pd.to_numeric(cf["Disponibilité (%)"], errors="coerce")
            target = float(summary_dict.get("Disponibilité cible (%)", 85))
            bar_colors = [RED_MAIN if v < target - 10 else ORANGE_MAIN if v < target else GREEN_MAIN for v in vals]
            ax2.bar(cf["Fondoir"].astype(str), vals, color=bar_colors)
            ax2.axhline(target, linestyle="--", color=GREEN_DARK, linewidth=1)
            ax2.set_title("Disponibilité par fondoir", fontsize=12, color=GREEN_DARK)
            ax2.set_ylabel("Disponibilité (%)")
            ax2.set_ylim(0, 100)
        else:
            ax2.text(0.5, 0.5, "Aucune donnée de disponibilité disponible", ha="center", va="center")
            ax2.axis("off")

        ax.text(0.06, 0.18, "Maintenance PMP", fontsize=14, weight="bold", color=GREEN_DARK)
        y = 0.15
        for k, v in maintenance_summary.items():
            ax.text(0.08, y, f"- {k} : {v}", fontsize=10, color="#333333")
            y -= 0.026

        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

    buffer.seek(0)
    return buffer.getvalue()

# ============================================================
# HEADER + SIDEBAR CONTROL PANEL
# ============================================================

if os.path.exists("OCP.png"):
    with open("OCP.png", "rb") as image_file:
        encoded_logo = base64.b64encode(image_file.read()).decode()

    st.sidebar.markdown(
        f"""
        <div style="text-align:center; margin-bottom:12px;">
            <img src="data:image/png;base64,{encoded_logo}" width="145">
        </div>
        """,
        unsafe_allow_html=True
    )

st.sidebar.markdown(
    f"<h2 style='text-align:center; color:{GREEN_DARK}; font-size:20px;'>U263 Control Center</h2>",
    unsafe_allow_html=True
)

st.sidebar.divider()

with st.sidebar.expander("Seuils de contrôle", expanded=False):
    sc1, sc2 = st.columns(2)

    with sc1:
        pressure_min = st.number_input("Pression vapeur min (bar)", min_value=0.0, max_value=20.0, value=5.8, step=0.1, key="pressure_min")
        sulfur_temp_min = st.number_input("Temp. soufre min (°C)", min_value=0.0, max_value=300.0, value=135.0, step=1.0, key="sulfur_temp_min")

    with sc2:
        sulfur_temp_max = st.number_input("Temp. soufre max (°C)", min_value=0.0, max_value=300.0, value=145.0, step=1.0, key="sulfur_temp_max")
        availability_target = st.number_input("Disponibilité cible (%)", min_value=0.0, max_value=100.0, value=85.0, step=1.0, key="availability_target")

    criticality_threshold = st.number_input("Seuil criticité AMDEC", min_value=0, max_value=1000, value=300, step=10, key="criticality_threshold")

st.sidebar.divider()

with st.sidebar.expander("Gestion des données", expanded=False):
    data_mode = st.radio("Mode d’alimentation des données", ["Données de démonstration", "Importation de fichiers", "Saisie manuelle"])

st.markdown('<div class="subtitle">Reliability & Availability Analysis</div>', unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

if data_mode == "Données de démonstration":
    incidents = generate_demo_incidents()
    serpentins = generate_demo_serpentins()
    process = generate_demo_process()
    maintenance = generate_demo_maintenance()
    amdec = generate_demo_amdec()

elif data_mode == "Importation de fichiers":
    with st.sidebar.expander("Importation de fichiers", expanded=False):
        incident_file = st.file_uploader("Importer incidents", type=["csv", "xlsx"])
        serpentin_file = st.file_uploader("Importer état serpentins", type=["csv", "xlsx"])
        process_file = st.file_uploader("Importer pression / température", type=["csv", "xlsx"])
        maintenance_file = st.file_uploader("Importer maintenance", type=["csv", "xlsx"])
        amdec_file = st.file_uploader("Importer AMDEC", type=["csv", "xlsx"])

    incidents = load_file(incident_file) if incident_file else pd.DataFrame(columns=["date", "equipement", "cause", "gravite"])
    serpentins = load_file(serpentin_file) if serpentin_file else pd.DataFrame(columns=["fondoir", "serpentin", "etat", "date_installation", "derniere_maintenance"])
    process = load_file(process_file) if process_file else pd.DataFrame(columns=["date", "pression_vapeur_bar", "temperature_vapeur_c", "temperature_soufre_c"])
    maintenance = load_file(maintenance_file) if maintenance_file else pd.DataFrame(columns=["n", "tache", "periodicite", "type_action", "nombre_intervenants", "intervenants", "duree_intervention_h", "frequence_jours", "derniere_intervention", "prochaine_intervention", "charge_homme_h"])
    amdec = load_file(amdec_file) if amdec_file else pd.DataFrame(columns=["mode_defaillance", "G", "O", "D"])

else:
    if "manual_incidents" not in st.session_state:
        st.session_state.manual_incidents = pd.DataFrame(columns=["date", "equipement", "cause", "gravite"])
    if "manual_serpentins" not in st.session_state:
        st.session_state.manual_serpentins = pd.DataFrame(columns=["fondoir", "serpentin", "etat", "date_installation", "derniere_maintenance"])
    if "manual_process" not in st.session_state:
        st.session_state.manual_process = pd.DataFrame(columns=["date", "pression_vapeur_bar", "temperature_vapeur_c", "temperature_soufre_c"])
    if "manual_maintenance" not in st.session_state:
        st.session_state.manual_maintenance = pd.DataFrame(columns=["n", "tache", "periodicite", "type_action", "nombre_intervenants", "intervenants", "duree_intervention_h", "frequence_jours", "derniere_intervention", "prochaine_intervention", "charge_homme_h"])
    if "manual_amdec" not in st.session_state:
        st.session_state.manual_amdec = pd.DataFrame(columns=["mode_defaillance", "G", "O", "D"])

    with st.sidebar.expander("Saisie manuelle des données", expanded=False):
        manual_choice = st.sidebar.selectbox("Type de donnée à ajouter", ["Incident", "Donnée process", "État serpentin", "Action maintenance", "Ligne AMDEC"])

    if manual_choice == "Incident":
        f1, f2, f3, f4 = st.sidebar.columns(4)
        with f1:
            manual_date = st.sidebar.date_input("Date incident", value=datetime.today())
        with f2:
            manual_equipment = st.sidebar.selectbox("Équipement", ["AF01", "BF01", "CF01", "DF01", "AR02", "BR02", "CR02", "DR02"])
        with f3:
            manual_cause = st.sidebar.selectbox("Cause", ["Chute de pression vapeur", "Température basse", "Formation de blocs", "Manque vapeur", "Encrassement serpentin", "Défaut purgeur", "Fuite vapeur", "Autre"])
        with f4:
            manual_gravity = st.sidebar.slider("Gravité", 1, 5, 3)
        if st.sidebar.button("Ajouter l’incident"):
            new_row = pd.DataFrame({"date": [pd.to_datetime(manual_date)], "equipement": [manual_equipment], "cause": [manual_cause], "gravite": [manual_gravity]})
            st.session_state.manual_incidents = pd.concat([st.session_state.manual_incidents, new_row], ignore_index=True)
            st.rerun()

    elif manual_choice == "Donnée process":
        f1, f2, f3, f4 = st.sidebar.columns(4)
        with f1:
            process_date = st.sidebar.date_input("Date mesure", value=datetime.today())
        with f2:
            pressure_value = st.sidebar.number_input("Pression vapeur MP (bar)", value=6.5, step=0.1)
        with f3:
            steam_temp = st.sidebar.number_input("Température vapeur (°C)", value=174.0, step=1.0)
        with f4:
            sulfur_temp = st.sidebar.number_input("Température soufre (°C)", value=140.0, step=1.0)
        if st.sidebar.button("Ajouter la donnée process"):
            new_row = pd.DataFrame({"date": [pd.to_datetime(process_date)], "pression_vapeur_bar": [pressure_value], "temperature_vapeur_c": [steam_temp], "temperature_soufre_c": [sulfur_temp]})
            st.session_state.manual_process = pd.concat([st.session_state.manual_process, new_row], ignore_index=True)
            st.rerun()

    elif manual_choice == "État serpentin":
        f1, f2, f3, f4, f5 = st.sidebar.columns(5)
        with f1:
            fondoir = st.sidebar.selectbox("Fondoir", ["AF01", "BF01", "CF01", "DF01"])
        with f2:
            serpentin_name = st.sidebar.text_input("Code serpentin", value=f"{fondoir}-S1")
        with f3:
            etat = st.sidebar.selectbox("État", ["En service", "Hors service", "Réparé"])
        with f4:
            install_date = st.sidebar.date_input("Date installation", value=datetime.today())
        with f5:
            last_maintenance = st.sidebar.date_input("Dernière maintenance", value=datetime.today())
        if st.sidebar.button("Ajouter l’état serpentin"):
            new_row = pd.DataFrame({"fondoir": [fondoir], "serpentin": [serpentin_name], "etat": [etat], "date_installation": [pd.to_datetime(install_date)], "derniere_maintenance": [pd.to_datetime(last_maintenance)]})
            st.session_state.manual_serpentins = pd.concat([st.session_state.manual_serpentins, new_row], ignore_index=True)
            st.rerun()

    elif manual_choice == "Action maintenance":
        f1, f2, f3 = st.sidebar.columns(3)
        n = len(st.session_state.manual_maintenance) + 1
        with f1:
            task = st.sidebar.text_area("Opération de maintenance")
            periodicite = st.sidebar.selectbox("Périodicité", ["J", "H", "BM", "M", "T", "S", "A"])
        with f2:
            type_action = st.sidebar.selectbox("Type d’action", ["Préventive", "Systématique", "Corrective"])
            intervenants = st.sidebar.text_input("Intervenants", value="PDM")
            nb_intervenants = st.sidebar.number_input("Nombre d’intervenants", min_value=1, value=1)
        with f3:
            duree = st.sidebar.number_input("Durée intervention (h)", min_value=0.25, value=1.0)
            last_date = st.sidebar.date_input("Dernière intervention", value=datetime.today())
        freq_days = {"J": 1, "H": 7, "BM": 15, "M": 30, "T": 90, "S": 180, "A": 365}
        frequence = freq_days[periodicite]
        next_date = pd.to_datetime(last_date) + pd.Timedelta(days=frequence)
        if st.sidebar.button("Ajouter l’action PMP"):
            new_row = pd.DataFrame({"n": [n], "tache": [task], "periodicite": [periodicite], "type_action": [type_action], "nombre_intervenants": [nb_intervenants], "intervenants": [intervenants], "duree_intervention_h": [duree], "frequence_jours": [frequence], "derniere_intervention": [pd.to_datetime(last_date)], "prochaine_intervention": [next_date], "charge_homme_h": [nb_intervenants * duree]})
            st.session_state.manual_maintenance = pd.concat([st.session_state.manual_maintenance, new_row], ignore_index=True)
            st.rerun()

    elif manual_choice == "Ligne AMDEC":
        f1, f2, f3, f4 = st.sidebar.columns(4)
        with f1:
            mode = st.sidebar.text_input("Mode de défaillance")
        with f2:
            g = st.sidebar.number_input("Gravité G", min_value=1, max_value=10, value=5)
        with f3:
            o = st.sidebar.number_input("Occurrence O", min_value=1, max_value=10, value=5)
        with f4:
            d = st.sidebar.number_input("Détectabilité D", min_value=1, max_value=10, value=5)
        if st.sidebar.button("Ajouter la ligne AMDEC"):
            new_row = pd.DataFrame({"mode_defaillance": [mode], "G": [g], "O": [o], "D": [d]})
            st.session_state.manual_amdec = pd.concat([st.session_state.manual_amdec, new_row], ignore_index=True)
            st.rerun()

    incidents = st.session_state.manual_incidents
    serpentins = st.session_state.manual_serpentins
    process = st.session_state.manual_process
    maintenance = st.session_state.manual_maintenance
    amdec = st.session_state.manual_amdec

# ============================================================
# DATA PREP
# ============================================================

incidents = normalize_columns(incidents)
serpentins = normalize_columns(serpentins)
process = normalize_columns(process)
maintenance = normalize_columns(maintenance)
amdec = normalize_columns(amdec)

for df in [incidents, serpentins, process, maintenance]:
    for col in ["date", "date_installation", "derniere_maintenance", "derniere_intervention", "prochaine_intervention"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

for col in ["nombre_intervenants", "duree_intervention_h", "frequence_jours", "charge_homme_h"]:
    if col in maintenance.columns:
        maintenance[col] = pd.to_numeric(maintenance[col], errors="coerce")

# ============================================================
# KPIs
# ============================================================

total_incidents = len(incidents)
if "date" in incidents.columns and incidents["date"].notna().any():
    observation_days = max((incidents["date"].max() - incidents["date"].min()).days, 1)
else:
    observation_days = 1
incidents_per_day = total_incidents / observation_days

if "etat" in serpentins.columns:
    available_mask = serpentins["etat"].astype(str).str.lower().isin(["en service", "service", "disponible", "réparé", "repare"])
    available = int(available_mask.sum())
    total_serpentins = len(serpentins)
    unavailable = total_serpentins - available
    availability = available / total_serpentins * 100 if total_serpentins else 0
else:
    available = unavailable = total_serpentins = 0
    availability = 0

last_pressure = process["pression_vapeur_bar"].dropna().iloc[-1] if "pression_vapeur_bar" in process.columns and not process["pression_vapeur_bar"].dropna().empty else 0
last_sulfur_temp = process["temperature_soufre_c"].dropna().iloc[-1] if "temperature_soufre_c" in process.columns and not process["temperature_soufre_c"].dropna().empty else 0

risk_score = 0
if availability < availability_target:
    risk_score += 35
if incidents_per_day > 10:
    risk_score += 30
elif incidents_per_day > 5:
    risk_score += 15
if last_pressure < pressure_min:
    risk_score += 20
if last_sulfur_temp < sulfur_temp_min or last_sulfur_temp > sulfur_temp_max:
    risk_score += 15
risk_score = min(risk_score, 100)

maintenance = add_maintenance_status(maintenance)
if "charge_homme_h" in maintenance.columns:
    maintenance["charge_homme_h"] = pd.to_numeric(maintenance["charge_homme_h"], errors="coerce").fillna(0)
else:
    maintenance["charge_homme_h"] = 0

late_tasks = maintenance[maintenance.get("statut", pd.Series(dtype=str)) == "En retard"] if "statut" in maintenance.columns else pd.DataFrame()
today_tasks = maintenance[maintenance.get("statut", pd.Series(dtype=str)) == "À faire aujourd’hui"] if "statut" in maintenance.columns else pd.DataFrame()
planned_tasks = maintenance[maintenance.get("statut", pd.Series(dtype=str)) == "Planifiée"] if "statut" in maintenance.columns else pd.DataFrame()
today = pd.Timestamp.today().normalize()
upcoming_tasks = maintenance[(maintenance["prochaine_intervention"].dt.normalize() > today) & (maintenance["prochaine_intervention"].dt.normalize() <= today + pd.Timedelta(days=7))] if "prochaine_intervention" in maintenance.columns else pd.DataFrame()
completion_rate = ((len(maintenance) - len(late_tasks)) / len(maintenance) * 100) if len(maintenance) else 0
late_charge = late_tasks["charge_homme_h"].sum() if len(late_tasks) and "charge_homme_h" in late_tasks.columns else 0

recommendations = []
if availability < availability_target:
    recommendations.append("Disponibilité inférieure à la cible : prioriser les fondoirs les moins disponibles.")
if incidents_per_day > 10:
    recommendations.append("Fréquence d’incidents élevée : renforcer l’analyse des causes dominantes.")
if last_pressure < pressure_min:
    recommendations.append("Pression vapeur sous le seuil : vérifier purgeurs, vannes et pertes de charge.")
if last_sulfur_temp < sulfur_temp_min:
    recommendations.append("Température soufre trop basse : risque de formation de blocs et d’écoulement difficile.")
if last_sulfur_temp > sulfur_temp_max:
    recommendations.append("Température soufre trop élevée : vérifier la régulation vapeur et les risques de surchauffe locale.")
if len(late_tasks) > 0:
    recommendations.append("Actions PMP en retard : les traiter avant les actions planifiées.")

# ============================================================
# TABS
# ============================================================

tab0, tab1, tab2, tab3, tab4 = st.tabs(["Vue globale", "Incidents", "Paramètres thermiques", "Maintenance et AMDEC", "Rapport"])

# ============================================================
# TAB 0
# ============================================================

with tab0:
    st.markdown("## Vue globale du système")

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        kpi_card("Total incidents", f"{total_incidents}", "Historique analysé", "orange" if total_incidents > 0 else "green")
    with c2:
        inc_status = "red" if incidents_per_day > 10 else "orange" if incidents_per_day > 5 else "green"
        kpi_card("Incidents / jour", f"{incidents_per_day:.2f}", "Fréquence moyenne", inc_status)
    with c3:
        av_status = "red" if availability < availability_target - 10 else "orange" if availability < availability_target else "green"
        kpi_card("Disponibilité", f"{availability:.1f} %", f"Cible : {availability_target:.1f} %", av_status)
    with c4:
        late_status = "red" if len(late_tasks) > 5 else "orange" if len(late_tasks) > 0 else "green"
        kpi_card("Actions en retard", len(late_tasks), "Urgence maintenance", late_status)
    with c5:
        risk_status = "red" if risk_score >= 70 else "orange" if risk_score >= 35 else "green"
        kpi_card("Score de risque", f"{risk_score}/100", "Indicateur global", risk_status)

    if risk_score >= 70:
        st.markdown('<div class="danger-box">Situation critique : plusieurs paramètres dépassent les seuils de contrôle. Une action prioritaire est nécessaire.</div>', unsafe_allow_html=True)
    elif risk_score >= 35:
        st.markdown('<div class="warning-box">Situation à surveiller : certaines dérives sont détectées par rapport aux seuils définis.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="good-box">Situation maîtrisée selon les seuils définis.</div>', unsafe_allow_html=True)

    st.markdown("## Indicateurs clés")
    m1, m2, m3 = st.columns(3)
    with m1:
        pressure_delta = last_pressure - pressure_min
        st.metric("Pression vapeur actuelle", f"{last_pressure:.2f} bar", f"{pressure_delta:+.2f} bar vs seuil")
    with m2:
        if sulfur_temp_min <= last_sulfur_temp <= sulfur_temp_max:
            temp_note = "Dans la plage"
        elif last_sulfur_temp < sulfur_temp_min:
            temp_note = f"{last_sulfur_temp - sulfur_temp_min:+.1f} °C vs min"
        else:
            temp_note = f"{last_sulfur_temp - sulfur_temp_max:+.1f} °C vs max"
        st.metric("Température soufre actuelle", f"{last_sulfur_temp:.1f} °C", temp_note)
    with m3:
        st.metric("Actions PMP en retard", len(late_tasks), f"{len(upcoming_tasks)} prévues dans 7 jours")

    st.markdown("## Disponibilité par fondoir")
    if "fondoir" in serpentins.columns and "etat" in serpentins.columns and len(serpentins) > 0:
        temp = serpentins.copy()
        temp["disponible"] = temp["etat"].astype(str).str.lower().isin(["en service", "service", "disponible", "réparé", "repare"])
        availability_by_fondoir_global = temp.groupby("fondoir")["disponible"].mean().reset_index()
        availability_by_fondoir_global["disponibilite_%"] = availability_by_fondoir_global["disponible"] * 100
        cols = st.columns(len(availability_by_fondoir_global))
        for i, row in availability_by_fondoir_global.iterrows():
            value = float(row["disponibilite_%"])
            status_label = color_for_availability(value, availability_target)
            status = "red" if status_label == "Critique" else "orange" if status_label == "À surveiller" else "green"
            with cols[i]:
                fondoir_circle(str(row["fondoir"]), value, status_label, status)
    else:
        st.info("Aucune donnée de disponibilité par fondoir disponible.")

    st.markdown("## Recommandations prioritaires")
    if not recommendations:
        st.success("Aucune dérive majeure détectée. Continuer le suivi préventif.")
    else:
        for rec in recommendations:
            st.warning(rec)

# ============================================================
# TAB 1
# ============================================================

with tab1:
    st.markdown("## Analyse visuelle des incidents")
    col_a, col_b = st.columns(2)

    if "equipement" in incidents.columns and len(incidents) > 0:
        by_equipment = incidents["equipement"].value_counts().reset_index()
        by_equipment.columns = ["equipement", "nombre"]
        by_equipment["criticite"] = np.where(by_equipment["nombre"] >= by_equipment["nombre"].quantile(0.75), "Critique", np.where(by_equipment["nombre"] >= by_equipment["nombre"].quantile(0.45), "À surveiller", "Bon"))
        fig = px.bar(by_equipment, x="equipement", y="nombre", text="nombre", title="Incidents par équipement", color="criticite", color_discrete_map={"Bon": GREEN_MAIN, "À surveiller": ORANGE_MAIN, "Critique": RED_MAIN})
        fig.update_layout(height=430, xaxis_title="Équipement", yaxis_title="Nombre d’incidents")
        col_a.plotly_chart(fig, use_container_width=True)

    if "cause" in incidents.columns and len(incidents) > 0:
        by_cause = incidents["cause"].value_counts().reset_index()
        by_cause.columns = ["cause", "nombre"]
        fig = px.pie(by_cause, names="cause", values="nombre", hole=0.45, title="Répartition des causes d’incidents", color_discrete_sequence=[RED_MAIN, ORANGE_MAIN, GREEN_MAIN, GREEN_DARK, GREEN_ACCENT, "#FBBF24", "#2563EB", "#475569"])
        fig.update_layout(height=430)
        col_b.plotly_chart(fig, use_container_width=True)

    if "date" in incidents.columns and len(incidents) > 0:
        temp_inc = incidents.dropna(subset=["date"]).copy()
        if len(temp_inc) > 0:
            temp_inc["mois"] = temp_inc["date"].dt.to_period("M").astype(str)
            monthly = temp_inc.groupby("mois").size().reset_index(name="nombre_incidents")
            fig = px.line(monthly, x="mois", y="nombre_incidents", markers=True, title="Évolution mensuelle des incidents", color_discrete_sequence=[GREEN_DARK])
            fig.update_traces(line=dict(width=3), marker=dict(size=9))
            fig.update_layout(height=420, xaxis_title="Mois", yaxis_title="Nombre d’incidents")
            st.plotly_chart(fig, use_container_width=True)

    if "cause" in incidents.columns and len(incidents) > 0:
        pareto = incidents["cause"].value_counts().reset_index()
        pareto.columns = ["cause", "nombre"]
        pareto["pourcentage_cumule"] = pareto["nombre"].cumsum() / pareto["nombre"].sum() * 100
        pareto["niveau"] = np.where(pareto["pourcentage_cumule"] <= 80, "Causes prioritaires", "Causes secondaires")
        fig = px.bar(pareto, x="cause", y="nombre", title="Pareto des causes d’incidents", color="niveau", color_discrete_map={"Causes prioritaires": RED_MAIN, "Causes secondaires": GREEN_MAIN})
        fig.add_scatter(x=pareto["cause"], y=pareto["pourcentage_cumule"], mode="lines+markers", name="% cumulé", yaxis="y2", line=dict(color=GREEN_DARK))
        fig.update_layout(height=470, xaxis_title="Cause", yaxis_title="Nombre", yaxis2=dict(title="% cumulé", overlaying="y", side="right", range=[0, 110]))
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("Voir les données brutes des incidents"):
        st.dataframe(prepare_display_table(incidents), use_container_width=True)

# ============================================================
# TAB 2
# ============================================================

with tab2:
    st.markdown("## Contrôle pression et température")
    col_a, col_b = st.columns(2)

    if "date" in process.columns and "pression_vapeur_bar" in process.columns and len(process) > 0:
        temp_proc = process.dropna(subset=["date"]).copy()
        fig = px.line(temp_proc, x="date", y="pression_vapeur_bar", title="Évolution de la pression vapeur par rapport au temps", color_discrete_sequence=[GREEN_DARK])
        fig.add_hline(y=pressure_min, line_dash="dash", annotation_text="Seuil minimal", line_color=RED_MAIN)
        low_points = temp_proc[temp_proc["pression_vapeur_bar"] < pressure_min]
        if len(low_points) > 0:
            fig.add_scatter(x=low_points["date"], y=low_points["pression_vapeur_bar"], mode="markers", name="Sous seuil", marker=dict(color=RED_MAIN, size=8))
        fig.update_layout(height=430, xaxis_title="Date", yaxis_title="Pression vapeur (bar)")
        col_a.plotly_chart(fig, use_container_width=True)

    if "date" in process.columns and "temperature_soufre_c" in process.columns and len(process) > 0:
        temp_proc = process.dropna(subset=["date"]).copy()
        fig = px.line(temp_proc, x="date", y="temperature_soufre_c", title="Évolution de la température du soufre par rapport au temps", color_discrete_sequence=[GREEN_DARK])
        fig.add_hline(y=sulfur_temp_min, line_dash="dash", annotation_text="Seuil min", line_color=RED_MAIN)
        fig.add_hline(y=sulfur_temp_max, line_dash="dash", annotation_text="Seuil max", line_color=RED_MAIN)
        bad_points = temp_proc[(temp_proc["temperature_soufre_c"] < sulfur_temp_min) | (temp_proc["temperature_soufre_c"] > sulfur_temp_max)]
        if len(bad_points) > 0:
            fig.add_scatter(x=bad_points["date"], y=bad_points["temperature_soufre_c"], mode="markers", name="Hors plage", marker=dict(color=RED_MAIN, size=8))
        fig.update_layout(height=430, xaxis_title="Date", yaxis_title="Température soufre (°C)")
        col_b.plotly_chart(fig, use_container_width=True)

    st.markdown("## Alertes process")
    alerts = []
    if "pression_vapeur_bar" in process.columns:
        low_pressure = process[process["pression_vapeur_bar"] < pressure_min]
        if len(low_pressure) > 0:
            alerts.append(f"{len(low_pressure)} points avec pression vapeur inférieure au seuil de {pressure_min:.1f} bar.")
    if "temperature_soufre_c" in process.columns:
        low_temp = process[process["temperature_soufre_c"] < sulfur_temp_min]
        high_temp = process[process["temperature_soufre_c"] > sulfur_temp_max]
        if len(low_temp) > 0:
            alerts.append(f"{len(low_temp)} points avec température soufre inférieure à {sulfur_temp_min:.1f} °C.")
        if len(high_temp) > 0:
            alerts.append(f"{len(high_temp)} points avec température soufre supérieure à {sulfur_temp_max:.1f} °C.")
    if len(alerts) == 0:
        st.success("Aucune dérive majeure détectée.")
    else:
        for alert in alerts:
            st.warning(alert)

    with st.expander("Voir les données process brutes"):
        st.dataframe(prepare_display_table(process), use_container_width=True)

# ============================================================
# TAB 3
# ============================================================

with tab3:
    st.markdown("## Rappels de maintenance prioritaires")

    if len(late_tasks) > 0:
        st.markdown("### Actions en retard")
        for _, row in late_tasks.iterrows():
            maintenance_card(row, color=RED_MAIN)
    if len(today_tasks) > 0:
        st.markdown("### Actions à réaliser aujourd’hui")
        for _, row in today_tasks.iterrows():
            maintenance_card(row, color=ORANGE_MAIN)
    if len(upcoming_tasks) > 0:
        st.markdown("### Actions prévues dans les 7 prochains jours")
        for _, row in upcoming_tasks.iterrows():
            maintenance_card(row, color=GREEN_MAIN)
    if len(late_tasks) == 0 and len(today_tasks) == 0 and len(upcoming_tasks) == 0:
        st.success("Aucune action urgente ou proche à afficher.")

    st.markdown("## Plan de maintenance préventive")
    total_actions = len(maintenance)
    actions_late = int((maintenance["statut"] == "En retard").sum()) if "statut" in maintenance.columns else 0
    upcoming_count = len(upcoming_tasks)

    status_retard = "red" if actions_late > 5 else "orange" if actions_late > 0 else "green"
    status_perf = "red" if completion_rate < 60 else "orange" if completion_rate < 85 else "green"
    status_upcoming = "orange" if upcoming_count > 0 else "green"

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        kpi_card("Actions PMP", total_actions, "Plan préventif", "green")
    with m2:
        kpi_card("Actions en retard", actions_late, "À traiter", status_retard)
    with m3:
        kpi_card("Taux de réalisation", f"{completion_rate:.1f} %", "Respect du planning PMP", status_perf)
    with m4:
        kpi_card("Prochains 7 jours", upcoming_count, "Planification", status_upcoming)

    c1, c2 = st.columns(2)
    if "statut" in maintenance.columns and len(maintenance) > 0:
        status_count = maintenance["statut"].value_counts().reset_index()
        status_count.columns = ["statut", "nombre"]
        fig = px.pie(status_count, names="statut", values="nombre", hole=0.45, title="Statut des actions de maintenance", color="statut", color_discrete_map={"Planifiée": GREEN_MAIN, "À faire aujourd’hui": ORANGE_MAIN, "En retard": RED_MAIN})
        fig.update_layout(height=400)
        c1.plotly_chart(fig, use_container_width=True)

    if "periodicite" in maintenance.columns and len(maintenance) > 0:
        periodicity_order = ["J", "H", "BM", "M", "T", "S", "A"]
        periodicity_count = maintenance["periodicite"].value_counts().reindex(periodicity_order).fillna(0).reset_index()
        periodicity_count.columns = ["periodicite", "nombre"]
        fig = px.bar(periodicity_count, x="periodicite", y="nombre", text="nombre", title="Répartition des actions par périodicité", color_discrete_sequence=[GREEN_MAIN])
        fig.update_layout(height=400, xaxis_title="Périodicité", yaxis_title="Nombre")
        c2.plotly_chart(fig, use_container_width=True)

    st.markdown("## Gestion dynamique du PMP")
    st.info("Le plan de maintenance peut être modifié directement dans l’application. Les changements sont pris en compte dans l’export.")
    editable_columns = ["n", "tache", "periodicite", "type_action", "nombre_intervenants", "intervenants", "duree_intervention_h", "frequence_jours", "derniere_intervention", "prochaine_intervention", "statut"]
    editable_columns = [col for col in editable_columns if col in maintenance.columns]
    edited_maintenance = st.data_editor(maintenance[editable_columns], use_container_width=True, num_rows="dynamic", key="maintenance_editor")

    for col in ["derniere_intervention", "prochaine_intervention"]:
        if col in edited_maintenance.columns:
            edited_maintenance[col] = pd.to_datetime(edited_maintenance[col], errors="coerce")
    if "frequence_jours" in edited_maintenance.columns and "derniere_intervention" in edited_maintenance.columns:
        edited_maintenance["frequence_jours"] = pd.to_numeric(edited_maintenance["frequence_jours"], errors="coerce")
        edited_maintenance["prochaine_intervention"] = edited_maintenance["derniere_intervention"] + pd.to_timedelta(edited_maintenance["frequence_jours"], unit="D")
    edited_maintenance = add_maintenance_status(edited_maintenance)

    st.markdown("## Export du PMP mis à jour")
    pmp_csv = edited_maintenance.to_csv(index=False).encode("utf-8")
    st.download_button("Télécharger le PMP modifié", pmp_csv, "PMP_U263_mis_a_jour.csv", "text/csv")

    st.markdown("## Analyse AMDEC")
    if all(col in amdec.columns for col in ["g", "o", "d"]) and len(amdec) > 0:
        amdec["g"] = pd.to_numeric(amdec["g"], errors="coerce")
        amdec["o"] = pd.to_numeric(amdec["o"], errors="coerce")
        amdec["d"] = pd.to_numeric(amdec["d"], errors="coerce")
        amdec["criticite"] = amdec["g"] * amdec["o"] * amdec["d"]
        amdec = amdec.sort_values("criticite", ascending=False)
        if "mode_defaillance" in amdec.columns:
            amdec["niveau"] = np.where(amdec["criticite"] >= criticality_threshold, "Critique", np.where(amdec["criticite"] >= criticality_threshold * 0.7, "À surveiller", "Acceptable"))
            fig = px.bar(amdec, x="mode_defaillance", y="criticite", text="criticite", title="Criticité des modes de défaillance", color="niveau", color_discrete_map={"Acceptable": GREEN_MAIN, "À surveiller": ORANGE_MAIN, "Critique": RED_MAIN})
            fig.add_hline(y=criticality_threshold, line_dash="dash", annotation_text="Seuil critique", line_color=GREEN_DARK)
            fig.update_layout(height=480, xaxis_title="Mode de défaillance", yaxis_title="Criticité")
            st.plotly_chart(fig, use_container_width=True)
            critical = amdec[amdec["criticite"] >= criticality_threshold]
            if len(critical) > 0:
                st.error("Modes de défaillance critiques détectés : " + ", ".join(critical["mode_defaillance"].astype(str).tolist()))
            else:
                st.success("Aucun mode de défaillance au-dessus du seuil critique.")

    with st.expander("Voir les données serpentins"):
        st.dataframe(prepare_display_table(serpentins), use_container_width=True)
    with st.expander("Voir les données AMDEC"):
        st.dataframe(prepare_display_table(amdec), use_container_width=True)

   
from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def create_pdf_report(
    summary_dict,
    recommendations,
    top_causes,
    critical_fondoirs,
    maintenance_summary,
    maintenance,
    amdec,
    criticality_threshold
):
    try:
        buffer = BytesIO()

        GREEN = "#157347"
        DARK_GREEN = "#0B3D2E"
        ORANGE = "#F59E0B"
        RED = "#DC2626"
        LIGHT_BG = "#F7FAF8"
        DARK_TEXT = "#1F2937"

        def status_color(value):
            if "Critique" in str(value):
                return RED
            if "surveiller" in str(value):
                return ORANGE
            return GREEN

        with PdfPages(buffer) as pdf:

            # =========================
            # PAGE 1 - RESUME + KPIS
            # =========================
            fig = plt.figure(figsize=(11.69, 8.27))
            fig.patch.set_facecolor("white")
            ax = fig.add_axes([0, 0, 1, 1])
            ax.axis("off")

            ax.text(
                0.05, 0.93,
                "Rapport synthétique global - U263",
                fontsize=24,
                fontweight="bold",
                color=DARK_GREEN
            )

            ax.text(
                0.05, 0.89,
                "Suivi des serpentins : incidents, disponibilité, maintenance et criticité",
                fontsize=12,
                color="#6B7280"
            )

            risk_score_pdf = float(summary_dict.get("Score de risque", 0))
            availability_pdf = float(summary_dict.get("Disponibilité (%)", 0))

            if risk_score_pdf >= 70:
                box_color = RED
                status_text = "CRITIQUE"
                message = "Plusieurs dérives majeures sont détectées. Les actions de maintenance et les paramètres vapeur doivent être traités en priorité."
            elif risk_score_pdf >= 35:
                box_color = ORANGE
                status_text = "A SURVEILLER"
                message = "Le système fonctionne, mais certaines dérives dépassent les seuils définis."
            else:
                box_color = GREEN
                status_text = "MAITRISE"
                message = "Les indicateurs restent globalement conformes aux seuils définis."

            ax.add_patch(plt.Rectangle((0.05, 0.77), 0.90, 0.08, color=box_color, alpha=0.15))
            ax.text(0.07, 0.815, status_text, fontsize=15, fontweight="bold", color=box_color)
            ax.text(0.07, 0.785, message, fontsize=10.5, color=DARK_TEXT)

            kpis = [
                ("Total incidents", summary_dict.get("Total incidents", "-")),
                ("Incidents / jour", summary_dict.get("Incidents par jour", "-")),
                ("Disponibilité", f"{availability_pdf:.1f} %"),
                ("Actions en retard", summary_dict.get("Actions PMP en retard", "-")),
                ("Score de risque", f"{risk_score_pdf:.0f}/100"),
            ]

            x0 = 0.05
            y0 = 0.60
            card_w = 0.17
            card_h = 0.12

            for i, (label, value) in enumerate(kpis):
                x = x0 + i * 0.18
                ax.add_patch(plt.Rectangle((x, y0), card_w, card_h, color=LIGHT_BG, ec="#D1D5DB", lw=1))
                ax.text(x + 0.015, y0 + 0.075, str(value), fontsize=18, fontweight="bold", color=DARK_GREEN)
                ax.text(x + 0.015, y0 + 0.035, label, fontsize=9.5, color="#6B7280")

            ax.text(0.05, 0.50, "Diagnostic opérationnel", fontsize=16, fontweight="bold", color=DARK_GREEN)

            dominant_cause = "Indisponible"
            dominant_count = 0

            if top_causes is not None and len(top_causes) > 0:
                dominant_cause = top_causes.iloc[0]["Cause"]
                dominant_count = int(top_causes.iloc[0]["Nombre"])

            worst_fondoir = "Indisponible"
            worst_availability = "-"
            worst_status = "-"

            if critical_fondoirs is not None and len(critical_fondoirs) > 0:
                worst = critical_fondoirs.sort_values("Disponibilité (%)").iloc[0]
                worst_fondoir = worst["Fondoir"]
                worst_availability = worst["Disponibilité (%)"]
                worst_status = worst["Statut"]

            diagnostic = [
                ("Cause dominante", f"{dominant_cause}\n{dominant_count} incidents observés"),
                ("Fondoir critique", f"{worst_fondoir}\nDisponibilité : {worst_availability} %\nStatut : {worst_status}"),
                (
                    "Maintenance PMP",
                    f"{maintenance_summary.get('Actions en retard', 0)} actions en retard\n"
                    f"{maintenance_summary.get('Actions prévues dans les 7 jours', 0)} actions dans les 7 jours\n"
                    f"{maintenance_summary.get('Taux de réalisation', '-')}"
                )
            ]

            for i, (title, content) in enumerate(diagnostic):
                x = 0.05 + i * 0.30
                ax.add_patch(plt.Rectangle((x, 0.31), 0.27, 0.15, color="white", ec="#D1D5DB", lw=1))
                ax.text(x + 0.015, 0.425, title, fontsize=11, fontweight="bold", color=DARK_GREEN)
                ax.text(x + 0.015, 0.365, content, fontsize=9.5, color=DARK_TEXT, va="top")

            ax.text(0.05, 0.25, "Tableau des indicateurs", fontsize=15, fontweight="bold", color=DARK_GREEN)

            summary_df = pd.DataFrame({
                "Indicateur": list(summary_dict.keys()),
                "Valeur": list(summary_dict.values())
            }).head(12)

            table = ax.table(
                cellText=summary_df.values,
                colLabels=summary_df.columns,
                cellLoc="left",
                colLoc="left",
                bbox=[0.05, 0.04, 0.90, 0.18]
            )

            table.auto_set_font_size(False)
            table.set_fontsize(8)

            for (row, col), cell in table.get_celld().items():
                cell.set_edgecolor("#E5E7EB")
                if row == 0:
                    cell.set_facecolor(DARK_GREEN)
                    cell.set_text_props(color="white", weight="bold")
                else:
                    cell.set_facecolor("#FFFFFF" if row % 2 == 0 else "#F9FAFB")

            pdf.savefig(fig, bbox_inches="tight")
            plt.close(fig)

            # =========================
            # PAGE 2 - FIGURES
            # =========================
            fig = plt.figure(figsize=(11.69, 8.27))
            fig.patch.set_facecolor("white")

            fig.suptitle(
                "Figures principales",
                fontsize=22,
                fontweight="bold",
                color=DARK_GREEN,
                x=0.05,
                ha="left"
            )

            ax1 = fig.add_axes([0.08, 0.54, 0.38, 0.32])
            if top_causes is not None and len(top_causes) > 0:
                causes = top_causes.sort_values("Nombre", ascending=True)
                ax1.barh(causes["Cause"], causes["Nombre"], color=ORANGE)
                ax1.set_title("Top 5 des causes d’incidents", fontsize=12, fontweight="bold")
                ax1.set_xlabel("Nombre")
                ax1.grid(axis="x", alpha=0.25)
            else:
                ax1.text(0.5, 0.5, "Aucune donnée d’incident disponible", ha="center", va="center")
                ax1.axis("off")

            ax2 = fig.add_axes([0.58, 0.54, 0.32, 0.32])
            if "statut" in maintenance.columns and len(maintenance) > 0:
                status_count = maintenance["statut"].value_counts().reset_index()
                status_count.columns = ["Statut", "Nombre"]

                colors = []
                for statut in status_count["Statut"]:
                    if "retard" in str(statut).lower():
                        colors.append(RED)
                    elif "aujourd" in str(statut).lower():
                        colors.append(ORANGE)
                    else:
                        colors.append(GREEN)

                ax2.pie(
                    status_count["Nombre"],
                    labels=status_count["Statut"],
                    autopct="%1.0f%%",
                    startangle=90,
                    colors=colors,
                    wedgeprops={"width": 0.45}
                )
                ax2.set_title("Répartition des actions PMP", fontsize=12, fontweight="bold")
            else:
                ax2.text(0.5, 0.5, "Aucune donnée maintenance", ha="center", va="center")
                ax2.axis("off")

            ax3 = fig.add_axes([0.08, 0.12, 0.38, 0.32])
            if critical_fondoirs is not None and len(critical_fondoirs) > 0:
                colors = [status_color(s) for s in critical_fondoirs["Statut"]]
                ax3.bar(
                    critical_fondoirs["Fondoir"],
                    critical_fondoirs["Disponibilité (%)"],
                    color=colors
                )
                ax3.axhline(
                    y=float(summary_dict.get("Disponibilité cible (%)", 0)),
                    color=DARK_GREEN,
                    linestyle="--",
                    linewidth=1
                )
                ax3.set_ylim(0, 100)
                ax3.set_title("Disponibilité par fondoir", fontsize=12, fontweight="bold")
                ax3.set_ylabel("Disponibilité (%)")
                ax3.grid(axis="y", alpha=0.25)
            else:
                ax3.text(0.5, 0.5, "Aucune donnée de disponibilité", ha="center", va="center")
                ax3.axis("off")

            ax4 = fig.add_axes([0.64, 0.10, 0.30, 0.30])
            if all(col in amdec.columns for col in ["g", "o", "d"]) and len(amdec) > 0:
                amdec_report = amdec.copy()
                amdec_report["g"] = pd.to_numeric(amdec_report["g"], errors="coerce")
                amdec_report["o"] = pd.to_numeric(amdec_report["o"], errors="coerce")
                amdec_report["d"] = pd.to_numeric(amdec_report["d"], errors="coerce")
                amdec_report["criticite"] = amdec_report["g"] * amdec_report["o"] * amdec_report["d"]
                amdec_report = amdec_report.sort_values("criticite", ascending=True).tail(5)

                if "mode_defaillance" in amdec_report.columns:
                    ax4.barh(
                        amdec_report["mode_defaillance"],
                        amdec_report["criticite"],
                        color=RED
                    )
                    ax4.axvline(
                        criticality_threshold,
                        linestyle="--",
                        color=DARK_GREEN,
                        linewidth=1
                    )
                    ax4.set_title("Top 5 criticités AMDEC", fontsize=12, fontweight="bold")
                    ax4.set_xlabel("Criticité")
                    ax4.grid(axis="x", alpha=0.25)
                else:
                    ax4.text(0.5, 0.5, "Colonne mode_defaillance absente", ha="center", va="center")
                    ax4.axis("off")
            else:
                ax4.text(0.5, 0.5, "Données AMDEC indisponibles", ha="center", va="center")
                ax4.axis("off")

            pdf.savefig(fig, bbox_inches="tight")
            plt.close(fig)

            # =========================
            # PAGE 3 - ACTIONS
            # =========================
            fig = plt.figure(figsize=(11.69, 8.27))
            fig.patch.set_facecolor("white")
            ax = fig.add_axes([0, 0, 1, 1])
            ax.axis("off")

            ax.text(
                0.05, 0.93,
                "Actions recommandées",
                fontsize=22,
                fontweight="bold",
                color=DARK_GREEN
            )

            if recommendations is None or len(recommendations) == 0:
                ax.add_patch(plt.Rectangle((0.05, 0.80), 0.90, 0.08, color=GREEN, alpha=0.12))
                ax.text(
                    0.07, 0.83,
                    "Aucune action corrective urgente n’est générée automatiquement selon les seuils actuels.",
                    fontsize=11,
                    color=DARK_TEXT
                )
            else:
                y = 0.84
                for i, rec in enumerate(recommendations[:10], start=1):
                    ax.add_patch(plt.Rectangle((0.05, y - 0.055), 0.90, 0.055, color=ORANGE, alpha=0.12))
                    ax.text(
                        0.07,
                        y - 0.025,
                        f"{i}. {rec}",
                        fontsize=10,
                        color=DARK_TEXT,
                        va="center"
                    )
                    y -= 0.075

            ax.text(
                0.05, 0.12,
                "Conclusion",
                fontsize=16,
                fontweight="bold",
                color=DARK_GREEN
            )

            ax.text(
                0.05, 0.07,
                "Ce rapport consolide les indicateurs affichés dans l’application afin de faciliter "
                "le suivi opérationnel, la priorisation des actions PMP et l’identification des fondoirs critiques.",
                fontsize=10.5,
                color=DARK_TEXT,
                wrap=True
            )

            pdf.savefig(fig, bbox_inches="tight")
            plt.close(fig)

        buffer.seek(0)
        return buffer.getvalue()

    except Exception as e:
        st.error(f"Erreur lors de la génération du PDF : {e}")
        return None


with tab4:
    st.markdown("## Rapport synthétique global")

    report_recommendations = recommendations

    if "cause" in incidents.columns and len(incidents) > 0:
        top_causes = incidents["cause"].value_counts().head(5).reset_index()
        top_causes.columns = ["Cause", "Nombre"]
    else:
        top_causes = pd.DataFrame(columns=["Cause", "Nombre"])

    if "fondoir" in serpentins.columns and "etat" in serpentins.columns and len(serpentins) > 0:
        temp_av = serpentins.copy()
        temp_av["disponible"] = temp_av["etat"].astype(str).str.lower().isin(
            ["en service", "service", "disponible", "réparé", "repare"]
        )

        critical_fondoirs = temp_av.groupby("fondoir")["disponible"].mean().reset_index()
        critical_fondoirs["Disponibilité (%)"] = (critical_fondoirs["disponible"] * 100).round(1)
        critical_fondoirs["Statut"] = critical_fondoirs["Disponibilité (%)"].apply(
            lambda x: color_for_availability(x, availability_target)
        )
        critical_fondoirs = critical_fondoirs[["fondoir", "Disponibilité (%)", "Statut"]]
        critical_fondoirs.columns = ["Fondoir", "Disponibilité (%)", "Statut"]
    else:
        critical_fondoirs = pd.DataFrame(columns=["Fondoir", "Disponibilité (%)", "Statut"])

    st.markdown('<div class="report-section">', unsafe_allow_html=True)
    st.markdown('<div class="report-section-title">Résumé exécutif</div>', unsafe_allow_html=True)

    if risk_score >= 70:
        st.markdown(
            '<div class="danger-box">Critique : plusieurs dérives majeures sont détectées. '
            'Les actions de maintenance et les paramètres vapeur doivent être traités en priorité.</div>',
            unsafe_allow_html=True
        )
    elif risk_score >= 35:
        st.markdown(
            '<div class="warning-box">À surveiller : le système fonctionne, mais certaines dérives dépassent les seuils définis.</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="good-box">Maîtrisé : les indicateurs restent globalement conformes aux seuils définis.</div>',
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("## Indicateurs clés du rapport")

    r1, r2, r3, r4, r5 = st.columns(5)

    with r1:
        kpi_card(
            "Total incidents",
            total_incidents,
            "Historique analysé",
            "orange" if total_incidents > 0 else "green"
        )

    with r2:
        inc_status = "red" if incidents_per_day > 10 else "orange" if incidents_per_day > 5 else "green"
        kpi_card(
            "Incidents / jour",
            f"{incidents_per_day:.2f}",
            "Fréquence moyenne",
            inc_status
        )

    with r3:
        av_status = "red" if availability < availability_target - 10 else "orange" if availability < availability_target else "green"
        kpi_card(
            "Disponibilité",
            f"{availability:.1f} %",
            f"Cible : {availability_target:.1f} %",
            av_status
        )

    with r4:
        late_status = "red" if len(late_tasks) > 5 else "orange" if len(late_tasks) > 0 else "green"
        kpi_card(
            "Actions en retard",
            len(late_tasks),
            "Maintenance",
            late_status
        )

    with r5:
        risk_status = "red" if risk_score >= 70 else "orange" if risk_score >= 35 else "green"
        kpi_card(
            "Score de risque",
            f"{risk_score}/100",
            "Indicateur global",
            risk_status
        )

    st.markdown("## État visuel des fondoirs")

    if len(critical_fondoirs) > 0:
        cols = st.columns(len(critical_fondoirs))

        for i, row in critical_fondoirs.iterrows():
            value = float(row["Disponibilité (%)"])
            status_label = str(row["Statut"])
            status = "red" if status_label == "Critique" else "orange" if status_label == "À surveiller" else "green"

            with cols[i]:
                fondoir_circle(str(row["Fondoir"]), value, status_label, status)
    else:
        st.info("Aucune donnée de disponibilité par fondoir disponible.")

    st.markdown("## Diagnostic opérationnel")

    d1, d2, d3 = st.columns(3)

    with d1:
        if len(top_causes) > 0:
            st.markdown(
                '<div class="report-section"><div class="report-section-title">Cause dominante</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="report-line"><b>{top_causes.iloc[0]["Cause"]}</b><br>'
                f'{int(top_causes.iloc[0]["Nombre"])} incidents observés</div></div>',
                unsafe_allow_html=True
            )
        else:
            st.info("Cause dominante indisponible")

    with d2:
        if len(critical_fondoirs) > 0:
            worst = critical_fondoirs.sort_values("Disponibilité (%)").iloc[0]
            st.markdown(
                '<div class="report-section"><div class="report-section-title">Fondoir critique</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="report-line"><b>{worst["Fondoir"]}</b><br>'
                f'Disponibilité : {worst["Disponibilité (%)"]:.1f} %</div></div>',
                unsafe_allow_html=True
            )
        else:
            st.info("Fondoir critique indisponible")

    with d3:
        st.markdown(
            '<div class="report-section"><div class="report-section-title">Maintenance PMP</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="report-line"><b>{len(late_tasks)}</b> actions en retard<br>'
            f'<b>{len(upcoming_tasks)}</b> actions dans les 7 prochains jours<br>'
            f'<b>{completion_rate:.1f} %</b> de réalisation</div></div>',
            unsafe_allow_html=True
        )

    st.markdown("## Figures principales")

    col_r1, col_r2 = st.columns(2)

    with col_r1:
        st.markdown("### Causes dominantes")

        if len(top_causes) > 0:
            fig = px.bar(
                top_causes,
                x="Nombre",
                y="Cause",
                orientation="h",
                title="Top 5 des causes d’incidents",
                color="Nombre",
                color_continuous_scale=[GREEN_MAIN, ORANGE_MAIN, RED_MAIN]
            )
            fig.update_layout(
                height=360,
                coloraxis_showscale=False,
                yaxis={"categoryorder": "total ascending"}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée d’incident disponible.")

    with col_r2:
        st.markdown("### Statut maintenance")

        if "statut" in maintenance.columns and len(maintenance) > 0:
            status_count = maintenance["statut"].value_counts().reset_index()
            status_count.columns = ["Statut", "Nombre"]

            fig = px.pie(
                status_count,
                names="Statut",
                values="Nombre",
                hole=0.55,
                title="Répartition des actions PMP",
                color="Statut",
                color_discrete_map={
                    "Planifiée": GREEN_MAIN,
                    "À faire aujourd’hui": ORANGE_MAIN,
                    "En retard": RED_MAIN
                }
            )
            fig.update_layout(height=360)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée de maintenance disponible.")

    if all(col in amdec.columns for col in ["g", "o", "d"]) and len(amdec) > 0:
        st.markdown("### AMDEC - modes les plus critiques")

        amdec_report = amdec.copy()
        amdec_report["g"] = pd.to_numeric(amdec_report["g"], errors="coerce")
        amdec_report["o"] = pd.to_numeric(amdec_report["o"], errors="coerce")
        amdec_report["d"] = pd.to_numeric(amdec_report["d"], errors="coerce")
        amdec_report["criticite"] = amdec_report["g"] * amdec_report["o"] * amdec_report["d"]
        amdec_report = amdec_report.sort_values("criticite", ascending=False).head(5)

        if "mode_defaillance" in amdec_report.columns:
            fig = px.bar(
                amdec_report,
                x="criticite",
                y="mode_defaillance",
                orientation="h",
                text="criticite",
                title="Top 5 criticités AMDEC",
                color="criticite",
                color_continuous_scale=[GREEN_MAIN, ORANGE_MAIN, RED_MAIN]
            )
            fig.add_vline(
                x=criticality_threshold,
                line_dash="dash",
                line_color=GREEN_DARK,
                annotation_text="Seuil"
            )
            fig.update_layout(
                height=360,
                coloraxis_showscale=False,
                yaxis={"categoryorder": "total ascending"},
                xaxis_title="Criticité",
                yaxis_title="Mode de défaillance"
            )
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("## Actions recommandées")

    if len(report_recommendations) == 0:
        st.success("Aucune action corrective urgente n’est générée automatiquement selon les seuils actuels.")
    else:
        for rec in report_recommendations:
            st.warning(rec)

    st.markdown("## Export du rapport")

    summary = pd.DataFrame({
        "Indicateur": [
            "Total incidents",
            "Incidents par jour",
            "Disponibilité (%)",
            "Disponibilité cible (%)",
            "Serpentins disponibles",
            "Serpentins indisponibles",
            "Pression vapeur actuelle (bar)",
            "Température soufre actuelle (°C)",
            "Score de risque",
            "Actions PMP en retard",
            "Taux de réalisation PMP (%)",
            "Actions prévues dans 7 jours"
        ],
        "Valeur": [
            total_incidents,
            round(incidents_per_day, 2),
            round(availability, 2),
            round(availability_target, 2),
            available,
            unavailable,
            round(last_pressure, 2),
            round(last_sulfur_temp, 2),
            risk_score,
            len(late_tasks),
            round(completion_rate, 2),
            len(upcoming_tasks)
        ]
    })

    with st.expander("Voir les indicateurs sous forme de tableau"):
        st.dataframe(summary, use_container_width=True)

    csv = summary.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Télécharger le rapport CSV",
        csv,
        "rapport_controle_serpentins_U263.csv",
        "text/csv"
    )

    summary_dict = dict(zip(summary["Indicateur"], summary["Valeur"]))

    maintenance_summary = {
        "Actions PMP totales": len(maintenance),
        "Actions en retard": len(late_tasks),
        "Actions à faire aujourd’hui": len(today_tasks),
        "Actions prévues dans les 7 jours": len(upcoming_tasks),
        "Taux de réalisation": f"{completion_rate:.1f} %"
    }

    pdf_data = create_pdf_report(
        summary_dict,
        report_recommendations,
        top_causes,
        critical_fondoirs,
        maintenance_summary,
        maintenance,
        amdec,
        criticality_threshold
    )

    if pdf_data is not None:
        st.download_button(
            "Télécharger le rapport PDF global",
            pdf_data,
            "rapport_global_U263.pdf",
            "application/pdf"
        )
    else:
        st.error("L’export PDF n’a pas pu être généré.")

    
       
