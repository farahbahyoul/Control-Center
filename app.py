import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="U263 Serpentin Control Center",
    layout="wide"
)

# ============================================================
# STYLE
# ============================================================

st.markdown("""
<style>
:root {
    --green-dark: #0B3D2E;
    --green-main: #157347;
    --green-soft: #E8F5EF;
    --green-light: #F4FBF7;
}

.block-container {
    padding-top: 1.7rem;
    padding-bottom: 2rem;
}

.main-title {
    font-size: 42px;
    font-weight: 850;
    color: var(--green-dark);
    margin-bottom: 4px;
}

.subtitle {
    font-size: 18px;
    color: #5f6368;
    margin-bottom: 28px;
}

.kpi-card {
    background: linear-gradient(135deg, #ffffff, #F4FBF7);
    padding: 22px;
    border-radius: 20px;
    box-shadow: 0 6px 20px rgba(11,61,46,0.10);
    border-left: 7px solid var(--green-main);
    min-height: 130px;
}

.kpi-title {
    font-size: 15px;
    color: #667085;
    margin-bottom: 10px;
}

.kpi-value {
    font-size: 34px;
    font-weight: 850;
    color: var(--green-dark);
}

.kpi-note {
    font-size: 13px;
    color: #8a8f98;
}

.good-box {
    padding: 16px;
    border-radius: 14px;
    background-color: #E8F5E9;
    border-left: 7px solid #157347;
    font-weight: 600;
    color: #0B3D2E;
}

.warning-box {
    padding: 16px;
    border-radius: 14px;
    background-color: #FFF7E6;
    border-left: 7px solid #F59E0B;
    font-weight: 600;
    color: #7A4F00;
}

.danger-box {
    padding: 16px;
    border-radius: 14px;
    background-color: #FDECEA;
    border-left: 7px solid #C62828;
    font-weight: 600;
    color: #8B1A1A;
}

.maintenance-card {
    background: linear-gradient(135deg, #ffffff, #F4FBF7);
    padding: 18px 22px;
    border-radius: 18px;
    box-shadow: 0 5px 18px rgba(11,61,46,0.10);
    margin-bottom: 14px;
}

.card-title {
    font-size: 18px;
    font-weight: 800;
    color: #0B3D2E;
}

.card-line {
    margin-top: 8px;
    color: #40464f;
    font-size: 15px;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B3D2E, #145A3D);
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p {
    color: white !important;
}

[data-testid="stSidebar"] input {
    color: #0B3D2E !important;
    background-color: white !important;
}

[data-testid="stSidebar"] [data-baseweb="input"] {
    background-color: white !important;
    border-radius: 10px;
}

[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #0B3D2E !important;
}

[data-testid="stSidebar"] [role="radiogroup"] label span {
    color: white !important;
}

[data-testid="stTabs"] button {
    font-size: 16px;
    font-weight: 600;
}

h1, h2, h3 {
    color: var(--green-dark);
}

.stButton button {
    background-color: #157347;
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: 600;
}

.stButton button:hover {
    background-color: #0B3D2E;
    color: white;
}
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
            "Chute de pression vapeur",
            "Température basse",
            "Formation de blocs",
            "Manque vapeur",
            "Encrassement serpentin",
            "Défaut purgeur",
            "Fuite vapeur",
            "Autre"
        ],
        size=500,
        p=[0.34, 0.28, 0.20, 0.07, 0.04, 0.03, 0.02, 0.02]
    )

    return pd.DataFrame({
        "date": dates,
        "equipement": equipments,
        "cause": causes,
        "gravite": np.random.randint(1, 6, size=500)
    })


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

    df = pd.DataFrame(rows, columns=[
        "n",
        "tache",
        "periodicite",
        "type_action",
        "nombre_intervenants",
        "intervenants",
        "duree_intervention_h"
    ])

    freq_days = {"J": 1, "H": 7, "BM": 15, "M": 30, "T": 90, "S": 180, "A": 365}
    df["frequence_jours"] = df["periodicite"].map(freq_days)

    np.random.seed(8)
    df["derniere_intervention"] = [
        today - timedelta(days=np.random.randint(1, int(freq_days[p] + 20)))
        for p in df["periodicite"]
    ]

    df["prochaine_intervention"] = df["derniere_intervention"] + pd.to_timedelta(
        df["frequence_jours"],
        unit="D"
    )

    df["charge_homme_h"] = df["nombre_intervenants"] * df["duree_intervention_h"]

    return df


def generate_demo_amdec():
    return pd.DataFrame({
        "mode_defaillance": [
            "Perte efficacité thermique",
            "Perforation",
            "Perte efficacité par condensat",
            "Encrassement thermique",
            "Détection tardive",
            "Rupture soudure",
            "Usure interne",
            "Défaut fabrication"
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
        if uploaded_file.name.endswith(".csv"):
            return pd.read_csv(uploaded_file)
        return pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Erreur de lecture du fichier : {e}")
        return None


def normalize_columns(df):
    df = df.copy()
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )
    return df


def kpi_card(title, value, note=""):
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)


def maintenance_card(row, color="#157347"):
    date_value = row.get("prochaine_intervention", "")
    if pd.notna(date_value):
        try:
            date_value = pd.to_datetime(date_value).strftime("%d/%m/%Y")
        except Exception:
            pass

    st.markdown(f"""
    <div class="maintenance-card" style="border-left: 7px solid {color};">
        <div class="card-title">
            Action n°{row.get("n", "")} — {row.get("tache", "")}
        </div>
        <div class="card-line">
            <b>Périodicité :</b> {row.get("periodicite", "")} &nbsp;&nbsp; | &nbsp;&nbsp;
            <b>Type :</b> {row.get("type_action", "")}
        </div>
        <div class="card-line">
            <b>Intervenant :</b> {row.get("intervenants", "")} &nbsp;&nbsp; | &nbsp;&nbsp;
            <b>Durée :</b> {row.get("duree_intervention_h", "")} h
        </div>
        <div class="card-line">
            <b>Prochaine intervention :</b> {date_value} &nbsp;&nbsp; | &nbsp;&nbsp;
            <b>Statut :</b> {row.get("statut", "")}
        </div>
    </div>
    """, unsafe_allow_html=True)


def gauge_chart(value, title, min_value, max_value, threshold=None):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=float(value),
        title={"text": title},
        gauge={
            "axis": {"range": [min_value, max_value]},
            "bar": {"color": "#157347"},
            "steps": [
                {"range": [min_value, max_value * 0.6], "color": "#FDECEA"},
                {"range": [max_value * 0.6, max_value * 0.85], "color": "#FFF7E6"},
                {"range": [max_value * 0.85, max_value], "color": "#E8F5E9"},
            ],
            "threshold": {
                "line": {"color": "#0B3D2E", "width": 4},
                "thickness": 0.75,
                "value": threshold if threshold is not None else value
            }
        }
    ))
    fig.update_layout(height=260, margin=dict(l=20, r=20, t=50, b=20))
    return fig


# ============================================================
# SIDEBAR
# ============================================================

if os.path.exists("OCP.png"):
    st.sidebar.image("OCP.png", width=170)

st.sidebar.markdown(
    "<h2 style='text-align:center; color:white; font-size:20px;'>U263 Control Center</h2>",
    unsafe_allow_html=True
)

st.sidebar.divider()
st.sidebar.title("Seuils de contrôle")

pressure_min = st.sidebar.number_input(
    "Pression vapeur minimale acceptable (bar)",
    min_value=0.0,
    max_value=20.0,
    value=5.8,
    step=0.1,
    key="pressure_min"
)

sulfur_temp_min = st.sidebar.number_input(
    "Température soufre minimale (°C)",
    min_value=0.0,
    max_value=300.0,
    value=135.0,
    step=1.0,
    key="sulfur_temp_min"
)

sulfur_temp_max = st.sidebar.number_input(
    "Température soufre maximale (°C)",
    min_value=0.0,
    max_value=300.0,
    value=145.0,
    step=1.0,
    key="sulfur_temp_max"
)

availability_target = st.sidebar.number_input(
    "Disponibilité cible (%)",
    min_value=0.0,
    max_value=100.0,
    value=85.0,
    step=1.0,
    key="availability_target"
)

criticality_threshold = st.sidebar.number_input(
    "Seuil criticité AMDEC",
    min_value=0,
    max_value=1000,
    value=300,
    step=10,
    key="criticality_threshold"
)

st.sidebar.divider()
st.sidebar.title("Gestion des données")

data_mode = st.sidebar.radio(
    "Mode d’alimentation des données",
    ["Données de démonstration", "Importation de fichiers", "Saisie manuelle"]
)

# ============================================================
# LOAD DATA — FIXED
# ============================================================

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
    incident_file = st.sidebar.file_uploader("Importer incidents", type=["csv", "xlsx"])
    serpentin_file = st.sidebar.file_uploader("Importer état serpentins", type=["csv", "xlsx"])
    process_file = st.sidebar.file_uploader("Importer pression / température", type=["csv", "xlsx"])
    maintenance_file = st.sidebar.file_uploader("Importer maintenance", type=["csv", "xlsx"])
    amdec_file = st.sidebar.file_uploader("Importer AMDEC", type=["csv", "xlsx"])

    incidents = load_file(incident_file) if incident_file else pd.DataFrame(
        columns=["date", "equipement", "cause", "gravite"]
    )

    serpentins = load_file(serpentin_file) if serpentin_file else pd.DataFrame(
        columns=["fondoir", "serpentin", "etat", "date_installation", "derniere_maintenance"]
    )

    process = load_file(process_file) if process_file else pd.DataFrame(
        columns=["date", "pression_vapeur_bar", "temperature_vapeur_c", "temperature_soufre_c"]
    )

    maintenance = load_file(maintenance_file) if maintenance_file else pd.DataFrame(
        columns=[
            "n", "tache", "periodicite", "type_action", "nombre_intervenants",
            "intervenants", "duree_intervention_h", "frequence_jours",
            "derniere_intervention", "prochaine_intervention", "charge_homme_h"
        ]
    )

    amdec = load_file(amdec_file) if amdec_file else pd.DataFrame(
        columns=["mode_defaillance", "G", "O", "D"]
    )


elif data_mode == "Saisie manuelle":

    if "manual_incidents" not in st.session_state:
        st.session_state.manual_incidents = pd.DataFrame(
            columns=["date", "equipement", "cause", "gravite"]
        )

    if "manual_serpentins" not in st.session_state:
        st.session_state.manual_serpentins = pd.DataFrame(
            columns=["fondoir", "serpentin", "etat", "date_installation", "derniere_maintenance"]
        )

    if "manual_process" not in st.session_state:
        st.session_state.manual_process = pd.DataFrame(
            columns=["date", "pression_vapeur_bar", "temperature_vapeur_c", "temperature_soufre_c"]
        )

    if "manual_maintenance" not in st.session_state:
        st.session_state.manual_maintenance = pd.DataFrame(
            columns=[
                "n", "tache", "periodicite", "type_action", "nombre_intervenants",
                "intervenants", "duree_intervention_h", "frequence_jours",
                "derniere_intervention", "prochaine_intervention", "charge_homme_h"
            ]
        )

    if "manual_amdec" not in st.session_state:
        st.session_state.manual_amdec = pd.DataFrame(
            columns=["mode_defaillance", "G", "O", "D"]
        )

    incidents = st.session_state.manual_incidents
    serpentins = st.session_state.manual_serpentins
    process = st.session_state.manual_process
    maintenance = st.session_state.manual_maintenance
    amdec = st.session_state.manual_amdec

    manual_choice = st.sidebar.selectbox(
        "Type de donnée à ajouter",
        [
            "Incident",
            "Donnée process",
            "État serpentin",
            "Action maintenance",
            "Ligne AMDEC"
        ]
    )

    if manual_choice == "Incident":
        st.sidebar.subheader("Ajouter un incident")

        manual_date = st.sidebar.date_input("Date incident", value=datetime.today())
        manual_equipment = st.sidebar.selectbox(
            "Équipement",
            ["AF01", "BF01", "CF01", "DF01", "AR02", "BR02", "CR02", "DR02"]
        )
        manual_cause = st.sidebar.selectbox(
            "Cause",
            [
                "Chute de pression vapeur",
                "Température basse",
                "Formation de blocs",
                "Manque vapeur",
                "Encrassement serpentin",
                "Défaut purgeur",
                "Fuite vapeur",
                "Autre"
            ]
        )
        manual_gravity = st.sidebar.slider("Gravité", 1, 5, 3)

        if st.sidebar.button("Ajouter l’incident"):
            new_row = pd.DataFrame({
                "date": [pd.to_datetime(manual_date)],
                "equipement": [manual_equipment],
                "cause": [manual_cause],
                "gravite": [manual_gravity]
            })
            st.session_state.manual_incidents = pd.concat(
                [st.session_state.manual_incidents, new_row],
                ignore_index=True
            )
            st.rerun()


    elif manual_choice == "Donnée process":
        st.sidebar.subheader("Ajouter une donnée process")

        process_date = st.sidebar.date_input("Date mesure", value=datetime.today())
        pressure_value = st.sidebar.number_input("Pression vapeur MP (bar)", value=6.5, step=0.1)
        steam_temp = st.sidebar.number_input("Température vapeur (°C)", value=174.0, step=1.0)
        sulfur_temp = st.sidebar.number_input("Température soufre (°C)", value=140.0, step=1.0)

        if st.sidebar.button("Ajouter la donnée process"):
            new_row = pd.DataFrame({
                "date": [pd.to_datetime(process_date)],
                "pression_vapeur_bar": [pressure_value],
                "temperature_vapeur_c": [steam_temp],
                "temperature_soufre_c": [sulfur_temp]
            })
            st.session_state.manual_process = pd.concat(
                [st.session_state.manual_process, new_row],
                ignore_index=True
            )
            st.rerun()


    elif manual_choice == "État serpentin":
        st.sidebar.subheader("Ajouter un état serpentin")

        fondoir = st.sidebar.selectbox("Fondoir", ["AF01", "BF01", "CF01", "DF01"])
        serpentin_name = st.sidebar.text_input("Code serpentin", value=f"{fondoir}-S1")
        etat = st.sidebar.selectbox("État", ["En service", "Hors service", "Réparé"])
        install_date = st.sidebar.date_input("Date installation", value=datetime.today())
        last_maintenance = st.sidebar.date_input("Dernière maintenance", value=datetime.today())

        if st.sidebar.button("Ajouter l’état serpentin"):
            new_row = pd.DataFrame({
                "fondoir": [fondoir],
                "serpentin": [serpentin_name],
                "etat": [etat],
                "date_installation": [pd.to_datetime(install_date)],
                "derniere_maintenance": [pd.to_datetime(last_maintenance)]
            })
            st.session_state.manual_serpentins = pd.concat(
                [st.session_state.manual_serpentins, new_row],
                ignore_index=True
            )
            st.rerun()


    elif manual_choice == "Action maintenance":
        st.sidebar.subheader("Ajouter une action PMP")

        n = len(st.session_state.manual_maintenance) + 1
        task = st.sidebar.text_area("Opération de maintenance")
        periodicite = st.sidebar.selectbox("Périodicité", ["J", "H", "BM", "M", "T", "S", "A"])
        type_action = st.sidebar.selectbox("Type d’action", ["Préventive", "Systématique", "Corrective"])
        intervenants = st.sidebar.text_input("Intervenants", value="PDM")
        nb_intervenants = st.sidebar.number_input("Nombre d’intervenants", min_value=1, value=1)
        duree = st.sidebar.number_input("Durée intervention (h)", min_value=0.25, value=1.0)
        last_date = st.sidebar.date_input("Dernière intervention", value=datetime.today())

        freq_days = {
            "J": 1,
            "H": 7,
            "BM": 15,
            "M": 30,
            "T": 90,
            "S": 180,
            "A": 365
        }

        frequence = freq_days[periodicite]
        next_date = pd.to_datetime(last_date) + pd.Timedelta(days=frequence)

        if st.sidebar.button("Ajouter l’action PMP"):
            new_row = pd.DataFrame({
                "n": [n],
                "tache": [task],
                "periodicite": [periodicite],
                "type_action": [type_action],
                "nombre_intervenants": [nb_intervenants],
                "intervenants": [intervenants],
                "duree_intervention_h": [duree],
                "frequence_jours": [frequence],
                "derniere_intervention": [pd.to_datetime(last_date)],
                "prochaine_intervention": [next_date],
                "charge_homme_h": [nb_intervenants * duree]
            })
            st.session_state.manual_maintenance = pd.concat(
                [st.session_state.manual_maintenance, new_row],
                ignore_index=True
            )
            st.rerun()


    elif manual_choice == "Ligne AMDEC":
        st.sidebar.subheader("Ajouter une ligne AMDEC")

        mode = st.sidebar.text_input("Mode de défaillance")
        g = st.sidebar.number_input("Gravité G", min_value=1, max_value=10, value=5)
        o = st.sidebar.number_input("Occurrence O", min_value=1, max_value=10, value=5)
        d = st.sidebar.number_input("Détectabilité D", min_value=1, max_value=10, value=5)

        if st.sidebar.button("Ajouter la ligne AMDEC"):
            new_row = pd.DataFrame({
                "mode_defaillance": [mode],
                "G": [g],
                "O": [o],
                "D": [d]
            })
            st.session_state.manual_amdec = pd.concat(
                [st.session_state.manual_amdec, new_row],
                ignore_index=True
            )
            st.rerun()

# ============================================================
# DATA PREP
# ============================================================

incidents = normalize_columns(incidents)
serpentins = normalize_columns(serpentins)
process = normalize_columns(process)
maintenance = normalize_columns(maintenance)
amdec = normalize_columns(amdec)

for df in [incidents, serpentins, process, maintenance]:
    for col in df.columns:
        if "date" in col or "intervention" in col:
            df[col] = pd.to_datetime(df[col], errors="coerce")

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
    available_mask = serpentins["etat"].astype(str).str.lower().isin(
        ["en service", "service", "disponible", "réparé", "repare"]
    )
    available = int(available_mask.sum())
    total_serpentins = len(serpentins)
    unavailable = total_serpentins - available
    availability = available / total_serpentins * 100 if total_serpentins else 0
else:
    available = 0
    unavailable = 0
    total_serpentins = len(serpentins)
    availability = 0

last_pressure = process["pression_vapeur_bar"].dropna().iloc[-1] if "pression_vapeur_bar" in process.columns and not process["pression_vapeur_bar"].dropna().empty else 0
last_sulfur_temp = process["temperature_soufre_c"].dropna().iloc[-1] if "temperature_soufre_c" in process.columns and not process["temperature_soufre_c"].dropna().empty else 0

risk_score = 0

if availability < availability_target:
    risk_score += 35
if incidents_per_day > 10:
    risk_score += 30
if last_pressure < pressure_min:
    risk_score += 20
if last_sulfur_temp < sulfur_temp_min or last_sulfur_temp > sulfur_temp_max:
    risk_score += 15

risk_score = min(risk_score, 100)

# ============================================================
# MAIN HEADER
# ============================================================

st.markdown('<div class="main-title">U263 Serpentin Control Center</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Plateforme de suivi, visualisation et maîtrise des performances des serpentins de chauffage</div>',
    unsafe_allow_html=True
)

st.markdown("## Vue globale du système")

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    kpi_card("Total incidents", f"{total_incidents}", "Historique analysé")
with c2:
    kpi_card("Incidents / jour", f"{incidents_per_day:.2f}", "Fréquence moyenne")
with c3:
    kpi_card("Disponibilité", f"{availability:.1f} %", f"Cible : {availability_target:.1f} %")
with c4:
    kpi_card("Serpentins disponibles", f"{available}/{total_serpentins}", "État opérationnel")
with c5:
    kpi_card("Score de risque", f"{risk_score}/100", "Indicateur global")

st.write("")

if risk_score >= 70:
    st.markdown('<div class="danger-box">Situation critique : plusieurs paramètres dépassent les seuils de contrôle.</div>', unsafe_allow_html=True)
elif risk_score >= 35:
    st.markdown('<div class="warning-box">Situation à surveiller : certaines dérives sont détectées.</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="good-box">Situation maîtrisée selon les seuils définis.</div>', unsafe_allow_html=True)

st.write("")

# ============================================================
# TABS
# ============================================================

tab0, tab1, tab2, tab3, tab4 = st.tabs([
    "Vue globale",
    "Incidents",
    "Paramètres thermiques",
    "Maintenance et AMDEC",
    "Rapport"
])

# ============================================================
# TAB 0
# ============================================================

with tab0:
    st.markdown("## Synthèse visuelle")

    g1, g2, g3 = st.columns(3)

    with g1:
        st.plotly_chart(
            gauge_chart(availability, "Disponibilité (%)", 0, 100, availability_target),
            use_container_width=True
        )

    with g2:
        st.plotly_chart(
            gauge_chart(last_pressure, "Pression vapeur (bar)", 0, 10, pressure_min),
            use_container_width=True
        )

    with g3:
        st.plotly_chart(
            gauge_chart(risk_score, "Score de risque", 0, 100, 70),
            use_container_width=True
        )

    st.markdown("## Recommandations prioritaires")

    recommendations = []

    if availability < availability_target:
        recommendations.append("Planifier une inspection prioritaire des serpentins hors service.")
    if incidents_per_day > 10:
        recommendations.append("Renforcer le suivi des incidents thermiques et analyser les causes dominantes.")
    if last_pressure < pressure_min:
        recommendations.append("Vérifier les purgeurs, les vannes vapeur et les pertes de pression.")
    if last_sulfur_temp < sulfur_temp_min:
        recommendations.append("Risque de formation de blocs : contrôler l’encrassement et la qualité du transfert thermique.")
    if last_sulfur_temp > sulfur_temp_max:
        recommendations.append("Contrôler la régulation vapeur afin d’éviter les surchauffes locales.")

    if len(recommendations) == 0:
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

    if "equipement" in incidents.columns:
        by_equipment = incidents["equipement"].value_counts().reset_index()
        by_equipment.columns = ["equipement", "nombre"]

        fig = px.bar(
            by_equipment,
            x="equipement",
            y="nombre",
            text="nombre",
            title="Incidents par équipement",
            color_discrete_sequence=["#157347"]
        )
        fig.update_layout(height=430)
        col_a.plotly_chart(fig, use_container_width=True)

    if "cause" in incidents.columns:
        by_cause = incidents["cause"].value_counts().reset_index()
        by_cause.columns = ["cause", "nombre"]

        fig = px.pie(
            by_cause,
            names="cause",
            values="nombre",
            hole=0.45,
            title="Répartition des causes d’incidents",
            color_discrete_sequence=px.colors.sequential.Greens
        )
        fig.update_layout(height=430)
        col_b.plotly_chart(fig, use_container_width=True)

    if "date" in incidents.columns:
        temp_inc = incidents.copy()
        temp_inc = temp_inc.dropna(subset=["date"])
        temp_inc["mois"] = temp_inc["date"].dt.to_period("M").astype(str)

        monthly = temp_inc.groupby("mois").size().reset_index(name="nombre_incidents")

        fig = px.line(
            monthly,
            x="mois",
            y="nombre_incidents",
            markers=True,
            title="Évolution mensuelle des incidents",
            color_discrete_sequence=["#157347"]
        )
        fig.update_layout(height=420)
        st.plotly_chart(fig, use_container_width=True)

    if "cause" in incidents.columns:
        pareto = incidents["cause"].value_counts().reset_index()
        pareto.columns = ["cause", "nombre"]
        pareto["pourcentage_cumule"] = pareto["nombre"].cumsum() / pareto["nombre"].sum() * 100

        fig = px.bar(
            pareto,
            x="cause",
            y="nombre",
            title="Pareto des causes d’incidents",
            color_discrete_sequence=["#157347"]
        )
        fig.add_scatter(
            x=pareto["cause"],
            y=pareto["pourcentage_cumule"],
            mode="lines+markers",
            name="% cumulé",
            yaxis="y2",
            line=dict(color="#0B3D2E")
        )
        fig.update_layout(
            height=470,
            yaxis2=dict(title="% cumulé", overlaying="y", side="right", range=[0, 110])
        )
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("Voir les données brutes des incidents"):
        st.dataframe(incidents, use_container_width=True)

# ============================================================
# TAB 2
# ============================================================

with tab2:
    st.markdown("## Contrôle pression et température")

    col_a, col_b = st.columns(2)

    if "date" in process.columns and "pression_vapeur_bar" in process.columns:
        fig = px.line(
            process,
            x="date",
            y="pression_vapeur_bar",
            title="Évolution de la pression vapeur",
            color_discrete_sequence=["#157347"]
        )
        fig.add_hline(y=pressure_min, line_dash="dash", annotation_text="Seuil minimal")
        fig.update_layout(height=430)
        col_a.plotly_chart(fig, use_container_width=True)

    if "date" in process.columns and "temperature_soufre_c" in process.columns:
        fig = px.line(
            process,
            x="date",
            y="temperature_soufre_c",
            title="Évolution de la température du soufre",
            color_discrete_sequence=["#0B3D2E"]
        )
        fig.add_hline(y=sulfur_temp_min, line_dash="dash", annotation_text="Seuil min")
        fig.add_hline(y=sulfur_temp_max, line_dash="dash", annotation_text="Seuil max")
        fig.update_layout(height=430)
        col_b.plotly_chart(fig, use_container_width=True)

    st.markdown("## Alertes process")

    alerts = []

    if "pression_vapeur_bar" in process.columns:
        low_pressure = process[process["pression_vapeur_bar"] < pressure_min]
        if len(low_pressure) > 0:
            alerts.append(f"{len(low_pressure)} points avec pression vapeur inférieure au seuil.")

    if "temperature_soufre_c" in process.columns:
        low_temp = process[process["temperature_soufre_c"] < sulfur_temp_min]
        high_temp = process[process["temperature_soufre_c"] > sulfur_temp_max]

        if len(low_temp) > 0:
            alerts.append(f"{len(low_temp)} points avec température soufre trop basse.")
        if len(high_temp) > 0:
            alerts.append(f"{len(high_temp)} points avec température soufre trop élevée.")

    if len(alerts) == 0:
        st.success("Aucune dérive majeure détectée.")
    else:
        for alert in alerts:
            st.warning(alert)

    with st.expander("Voir les données process brutes"):
        st.dataframe(process, use_container_width=True)

# ============================================================
# TAB 3
# ============================================================

with tab3:
    st.markdown("## Disponibilité par fondoir")

    if "fondoir" in serpentins.columns and "etat" in serpentins.columns:
        temp = serpentins.copy()
        temp["disponible"] = temp["etat"].astype(str).str.lower().isin(
            ["en service", "service", "disponible", "réparé", "repare"]
        )

        availability_by_fondoir = temp.groupby("fondoir")["disponible"].mean().reset_index()
        availability_by_fondoir["disponibilite_%"] = availability_by_fondoir["disponible"] * 100

        fig = px.bar(
            availability_by_fondoir,
            x="fondoir",
            y="disponibilite_%",
            text=availability_by_fondoir["disponibilite_%"].round(1),
            title="Disponibilité des serpentins par fondoir",
            color_discrete_sequence=["#157347"]
        )
        fig.add_hline(y=availability_target, line_dash="dash", annotation_text="Cible")
        fig.update_layout(height=430)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("## Plan de maintenance préventive")

    if "prochaine_intervention" in maintenance.columns:
        today = pd.Timestamp.today().normalize()

        maintenance["prochaine_intervention"] = pd.to_datetime(
            maintenance["prochaine_intervention"],
            errors="coerce"
        )

        maintenance["statut"] = np.where(
            maintenance["prochaine_intervention"].dt.normalize() < today,
            "En retard",
            np.where(
                maintenance["prochaine_intervention"].dt.normalize() == today,
                "À faire aujourd’hui",
                "Planifiée"
            )
        )

        total_actions = len(maintenance)
        actions_late = int((maintenance["statut"] == "En retard").sum())
        total_charge = maintenance["charge_homme_h"].sum() if "charge_homme_h" in maintenance.columns else 0
        avg_duration = maintenance["duree_intervention_h"].mean() if "duree_intervention_h" in maintenance.columns else 0

        m1, m2, m3, m4 = st.columns(4)

        with m1:
            kpi_card("Actions PMP", total_actions, "Plan préventif")
        with m2:
            kpi_card("Actions en retard", actions_late, "À traiter")
        with m3:
            kpi_card("Charge totale", f"{total_charge:.1f} h.h", "Homme-heures")
        with m4:
           kpi_card("Durée moyenne", f"{avg_duration:.1f} h", "Par intervention")

        st.write("")

        c1, c2 = st.columns(2)

        status_count = maintenance["statut"].value_counts().reset_index()
        status_count.columns = ["statut", "nombre"]

        fig = px.pie(
            status_count,
            names="statut",
            values="nombre",
            hole=0.45,
            title="Statut des actions de maintenance",
            color_discrete_sequence=px.colors.sequential.Greens
        )
        fig.update_layout(height=400)
        c1.plotly_chart(fig, use_container_width=True)

        if "periodicite" in maintenance.columns:
            periodicity_order = ["J", "H", "BM", "M", "T", "S", "A"]
            periodicity_count = maintenance["periodicite"].value_counts().reindex(periodicity_order).fillna(0).reset_index()
            periodicity_count.columns = ["periodicite", "nombre"]

            fig = px.bar(
                periodicity_count,
                x="periodicite",
                y="nombre",
                text="nombre",
                title="Répartition des actions par périodicité",
                color_discrete_sequence=["#157347"]
            )
            fig.update_layout(height=400)
            c2.plotly_chart(fig, use_container_width=True)

        st.markdown("## Gestion dynamique du PMP")
        st.info("Le plan de maintenance peut être modifié directement dans l’application. Les changements peuvent ensuite être exportés.")

        editable_columns = [
            "n",
            "tache",
            "periodicite",
            "type_action",
            "nombre_intervenants",
            "intervenants",
            "duree_intervention_h",
            "frequence_jours",
            "derniere_intervention",
            "prochaine_intervention",
            "statut"
        ]

        editable_columns = [col for col in editable_columns if col in maintenance.columns]

        maintenance = st.data_editor(
            maintenance[editable_columns],
            use_container_width=True,
            num_rows="dynamic",
            key="maintenance_editor"
        )

        if "derniere_intervention" in maintenance.columns:
            maintenance["derniere_intervention"] = pd.to_datetime(
                maintenance["derniere_intervention"],
                errors="coerce"
            )

        if "prochaine_intervention" in maintenance.columns:
            maintenance["prochaine_intervention"] = pd.to_datetime(
                maintenance["prochaine_intervention"],
                errors="coerce"
            )

        if "frequence_jours" in maintenance.columns and "derniere_intervention" in maintenance.columns:
            maintenance["prochaine_intervention"] = maintenance["derniere_intervention"] + pd.to_timedelta(
                maintenance["frequence_jours"],
                unit="D"
            )

        maintenance["statut"] = np.where(
            maintenance["prochaine_intervention"].dt.normalize() < today,
            "En retard",
            np.where(
                maintenance["prochaine_intervention"].dt.normalize() == today,
                "À faire aujourd’hui",
                "Planifiée"
            )
        )

        st.markdown("## Rappels de maintenance")

        tasks_today = maintenance[maintenance["statut"] == "À faire aujourd’hui"]
        late_tasks = maintenance[maintenance["statut"] == "En retard"]
        upcoming_tasks = maintenance[
            (maintenance["prochaine_intervention"].dt.normalize() > today) &
            (maintenance["prochaine_intervention"].dt.normalize() <= today + pd.Timedelta(days=7))
        ]

        r1, r2, r3 = st.columns(3)

        with r1:
            kpi_card("À faire aujourd’hui", len(tasks_today), "Actions PMP du jour")
        with r2:
            kpi_card("En retard", len(late_tasks), "Actions dépassées")
        with r3:
            kpi_card("Prochains 7 jours", len(upcoming_tasks), "Actions à venir")

        if len(late_tasks) > 0:
            st.markdown("### Actions en retard")
            for _, row in late_tasks.iterrows():
                maintenance_card(row, color="#C62828")

        if len(tasks_today) > 0:
            st.markdown("### Actions à réaliser aujourd’hui")
            for _, row in tasks_today.iterrows():
                maintenance_card(row, color="#F59E0B")

        if len(upcoming_tasks) > 0:
            st.markdown("### Actions prévues dans les 7 prochains jours")
            for _, row in upcoming_tasks.iterrows():
                maintenance_card(row, color="#157347")

        if len(late_tasks) == 0 and len(tasks_today) == 0 and len(upcoming_tasks) == 0:
            st.success("Aucune action urgente ou proche à afficher.")

        st.markdown("## Export du PMP mis à jour")

        pmp_csv = maintenance.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Télécharger le PMP modifié",
            data=pmp_csv,
            file_name="PMP_U263_mis_a_jour.csv",
            mime="text/csv"
        )

    st.markdown("## Analyse AMDEC")

    if all(col in amdec.columns for col in ["g", "o", "d"]):
        amdec["criticite"] = amdec["g"] * amdec["o"] * amdec["d"]
        amdec = amdec.sort_values("criticite", ascending=False)

        if "mode_defaillance" in amdec.columns:
            fig = px.bar(
                amdec,
                x="mode_defaillance",
                y="criticite",
                text="criticite",
                title="Criticité des modes de défaillance",
                color_discrete_sequence=["#157347"]
            )
            fig.add_hline(y=criticality_threshold, line_dash="dash", annotation_text="Seuil critique")
            fig.update_layout(height=480)
            st.plotly_chart(fig, use_container_width=True)

            critical = amdec[amdec["criticite"] >= criticality_threshold]

            if len(critical) > 0:
                st.error("Modes de défaillance critiques détectés.")
                st.write(", ".join(critical["mode_defaillance"].astype(str).tolist()))
            else:
                st.success("Aucun mode de défaillance au-dessus du seuil critique.")

    with st.expander("Voir les données serpentins"):
        st.dataframe(serpentins, use_container_width=True)

    with st.expander("Voir les données AMDEC"):
        st.dataframe(amdec, use_container_width=True)

# ============================================================
# TAB 4
# ============================================================

with tab4:
    st.markdown("## Rapport synthétique")

    summary = pd.DataFrame({
        "Indicateur": [
            "Total incidents",
            "Incidents par jour",
            "Disponibilité (%)",
            "Serpentins disponibles",
            "Serpentins indisponibles",
            "Pression vapeur actuelle (bar)",
            "Température soufre actuelle (°C)",
            "Score de risque"
        ],
        "Valeur": [
            total_incidents,
            round(incidents_per_day, 2),
            round(availability, 2),
            available,
            unavailable,
            round(last_pressure, 2),
            round(last_sulfur_temp, 2),
            risk_score
        ]
    })

    st.dataframe(summary, use_container_width=True)

    csv = summary.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Télécharger le rapport CSV",
        data=csv,
        file_name="rapport_controle_serpentins_U263.csv",
        mime="text/csv"
    )

    st.success("Ce rapport peut être intégré dans la phase Control de la démarche DMAIC.")
