import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import re
from datetime import datetime, timedelta


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI-Assisted Hospital Capacity Simulation",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --navy:#12355b; --blue:#3976e8; --cyan:#35c2d7; --teal:#49c7aa;
        --purple:#8b72e8; --pink:#ec7fa5; --peach:#ffad86; --yellow:#f5c86a;
        --surface:#ffffff; --canvas:#f4f8fc; --text:#18324c; --muted:#71839a; --line:#e3ebf3;
    }
    html,body,[class*="css"],.stApp{font-family:'Inter',sans-serif}
    html,body,[data-testid="stAppViewContainer"],.stApp{
        color:var(--text)!important;
        background:
          radial-gradient(circle at 10% 8%,rgba(64,169,235,.28),transparent 30%),
          radial-gradient(circle at 92% 12%,rgba(54,132,224,.22),transparent 32%),
          radial-gradient(circle at 78% 88%,rgba(47,196,220,.20),transparent 30%),
          linear-gradient(135deg,#c8e8fb 0%,#d8effc 30%,#e4f5fc 55%,#d2ecfa 78%,#c3e4f8 100%)!important;
        background-attachment:fixed!important;
    }
    [data-testid="stHeader"]{background:rgba(199,232,250,.80)!important;backdrop-filter:blur(18px);border-bottom:1px solid rgba(225,235,244,.8)}
    .block-container{max-width:1480px;padding-top:1.7rem;padding-bottom:4rem}
    .stApp p,.stApp span,.stApp label,.stApp li,.stApp strong,.stApp em,.stApp b,.stApp h1,.stApp h2,.stApp h3,.stApp h4,.stApp h5,.stApp h6{color:var(--text)}
    h1,h2,h3{letter-spacing:-.025em} h1{font-weight:800!important} h2,h3{font-weight:750!important}

    [data-testid="stSidebar"]{
        background:
          radial-gradient(circle at 18% 8%,rgba(255,255,255,.32),transparent 24%),
          linear-gradient(165deg,#78bff0 0%,#94cff4 24%,#b4ddf7 52%,#d1eafb 76%,#e3f2fc 100%)!important;
        border-right:1px solid rgba(69,145,205,.28);
        box-shadow:12px 0 34px rgba(42,119,178,.14)
    }
    [data-testid="stSidebar"]>div:first-child{
        padding-top:1.4rem;
        background:linear-gradient(180deg,rgba(255,255,255,.05),rgba(255,255,255,.16))!important;
    }
    [data-testid="stSidebar"] h1{color:var(--navy)!important;font-size:1.42rem!important;font-weight:800!important}
    [data-testid="stSidebar"] p,[data-testid="stSidebar"] span,[data-testid="stSidebar"] label{color:var(--text)!important}
    [data-testid="stTextArea"] textarea{background:rgba(255,255,255,.94)!important;color:var(--text)!important;-webkit-text-fill-color:var(--text)!important;border:1px solid #d8e6ef!important;border-radius:16px!important;min-height:260px!important;box-shadow:0 8px 22px rgba(18,53,91,.05);transition:.2s ease}
    [data-testid="stTextArea"] textarea:focus{border-color:#5ecbd3!important;box-shadow:0 0 0 4px rgba(53,194,215,.13),0 10px 26px rgba(18,53,91,.07)!important;transform:translateY(-1px)}
    [data-testid="stTextArea"] textarea::placeholder{color:#8a99aa!important;-webkit-text-fill-color:#8a99aa!important}

    .stButton>button,[data-testid="stDownloadButton"] button{
        width:100%;min-height:48px;background:linear-gradient(110deg,#3976e8 0%,#35c2d7 52%,#49c7aa 100%)!important;
        background-size:180% 180%!important;color:#fff!important;border:0!important;border-radius:14px!important;font-weight:800!important;
        box-shadow:0 10px 25px rgba(57,118,232,.22);transition:transform .2s ease,box-shadow .2s ease,background-position .35s ease
    }
    .stButton>button:hover,[data-testid="stDownloadButton"] button:hover{transform:translateY(-2px) scale(1.005);box-shadow:0 15px 30px rgba(53,194,215,.28);background-position:100% 50%!important}
    .stButton>button:active,[data-testid="stDownloadButton"] button:active{transform:translateY(0) scale(.99)}
    .stButton>button p,.stButton>button span,[data-testid="stDownloadButton"] button p,[data-testid="stDownloadButton"] button span{color:#fff!important}

    .stTabs [data-baseweb="tab-list"]{gap:7px;background:rgba(255,255,255,.82);backdrop-filter:blur(14px);padding:8px;border:1px solid var(--line);border-radius:17px;box-shadow:0 9px 26px rgba(18,53,91,.06);overflow-x:auto}
    .stTabs [data-baseweb="tab"]{min-height:43px;background:transparent;border-radius:11px;padding:8px 13px;border:0;transition:all .18s ease}
    .stTabs [data-baseweb="tab"]:hover{background:linear-gradient(135deg,#edf5ff,#edfdf9);transform:translateY(-1px)}
    .stTabs [data-baseweb="tab"] p{color:#68788a!important;font-size:.83rem;font-weight:750!important;white-space:nowrap}
    .stTabs [aria-selected="true"]{background:linear-gradient(120deg,#e7f0ff 0%,#e8fbf8 55%,#f0ebff 100%)!important;box-shadow:inset 0 0 0 1px rgba(57,118,232,.12)}
    .stTabs [aria-selected="true"] p{color:#285fc2!important}

    [data-testid="stMetric"]{position:relative;overflow:hidden;background:linear-gradient(145deg,rgba(255,255,255,.98),rgba(247,251,255,.92))!important;border:1px solid rgba(218,230,240,.95)!important;border-radius:20px!important;padding:19px 20px!important;min-height:114px;box-shadow:0 10px 28px rgba(18,53,91,.07);transition:transform .22s ease,box-shadow .22s ease,border-color .22s ease}
    [data-testid="stMetric"]:hover{transform:translateY(-5px);box-shadow:0 18px 38px rgba(18,53,91,.13);border-color:rgba(53,194,215,.45)!important}
    [data-testid="stMetric"]:before{content:'';position:absolute;left:0;right:0;top:0;height:5px;background:linear-gradient(90deg,#3976e8,#35c2d7,#49c7aa,#8b72e8,#ec7fa5);background-size:220% 100%;transition:background-position .4s ease}
    [data-testid="stMetric"]:hover:before{background-position:100% 0}
    [data-testid="stMetric"]:after{content:'';position:absolute;width:90px;height:90px;right:-32px;bottom:-42px;border-radius:50%;background:linear-gradient(135deg,rgba(53,194,215,.11),rgba(139,114,232,.12));transition:transform .25s ease}
    [data-testid="stMetric"]:hover:after{transform:scale(1.25)}
    [data-testid="stMetricLabel"] p{color:var(--muted)!important;font-size:.77rem!important;font-weight:700!important;text-transform:uppercase;letter-spacing:.045em}
    [data-testid="stMetricValue"]{color:var(--navy)!important;font-size:1.58rem!important;font-weight:800!important;letter-spacing:-.03em}

    [data-testid="stDataFrame"]{background:#fff!important;border:1px solid var(--line);border-radius:18px;overflow:hidden;box-shadow:0 10px 28px rgba(18,53,91,.06);transition:box-shadow .2s ease,transform .2s ease}
    [data-testid="stDataFrame"]:hover{box-shadow:0 15px 34px rgba(18,53,91,.09);transform:translateY(-1px)}
    [data-testid="stDataFrame"] *{color:var(--text)!important}
    [data-testid="stAlert"]{border-radius:16px!important;border-width:1px!important;box-shadow:0 8px 22px rgba(18,53,91,.045)!important}
    [data-testid="stExpander"]{background:rgba(255,255,255,.92);border:1px solid var(--line)!important;border-radius:16px!important;box-shadow:0 8px 22px rgba(18,53,91,.045)}
    [data-testid="stCodeBlock"],pre{background:#f8fafc!important;border:1px solid var(--line);border-radius:14px!important}
    [data-testid="stCodeBlock"] *,pre *,code{color:var(--text)!important} hr{border-color:var(--line)!important}

    .hospital-hero{background:linear-gradient(120deg,#eaf4ff 0%,#e8fbf6 34%,#f0ecff 68%,#fff0ea 100%);background-size:180% 180%;border:1px solid rgba(218,230,240,.9);border-radius:27px;padding:32px 34px;margin:0 0 22px 0;box-shadow:0 16px 40px rgba(18,53,91,.09);position:relative;overflow:hidden;animation:heroGradient 10s ease infinite}
    @keyframes heroGradient{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
    .hospital-hero:before{content:'';position:absolute;width:180px;height:180px;left:-60px;bottom:-95px;border-radius:50%;background:linear-gradient(135deg,rgba(57,118,232,.12),rgba(53,194,215,.18))}
    .hospital-hero:after{content:'';position:absolute;width:250px;height:250px;right:-70px;top:-115px;border-radius:50%;background:linear-gradient(135deg,rgba(139,114,232,.15),rgba(236,127,165,.12))}
    .hospital-kicker{color:#3371dc;font-size:.76rem;font-weight:800;letter-spacing:.13em;text-transform:uppercase;margin-bottom:8px;position:relative;z-index:1}
    .hospital-title{color:var(--navy);font-size:2.08rem;line-height:1.12;font-weight:800;letter-spacing:-.035em;margin:0;position:relative;z-index:1}
    .hospital-subtitle{color:#667c92;font-size:.98rem;line-height:1.65;max-width:840px;margin-top:10px;margin-bottom:0;position:relative;z-index:1}
    .section-card{background:linear-gradient(145deg,#fff,#f8fbff);border:1px solid var(--line);border-radius:20px;padding:19px 21px;box-shadow:0 10px 28px rgba(18,53,91,.055);transition:transform .2s ease,box-shadow .2s ease}
    .section-card:hover{transform:translateY(-3px);box-shadow:0 16px 35px rgba(18,53,91,.09)}

    div[data-testid="stVerticalBlockBorderWrapper"]{border-radius:20px!important}
    [data-baseweb="select"]>div{border-radius:12px!important}
    input{border-radius:12px!important}
    ::-webkit-scrollbar{width:10px;height:10px} ::-webkit-scrollbar-track{background:#eef4f8} ::-webkit-scrollbar-thumb{background:linear-gradient(#7db6f3,#66d3c4);border-radius:20px;border:2px solid #eef4f8}

    @media(max-width:900px){.block-container{padding-left:1rem;padding-right:1rem}.hospital-hero{padding:23px;border-radius:20px}.hospital-title{font-size:1.58rem}}
    </style>

    """,
    unsafe_allow_html=True
)


# ============================================================
# HELPERS
# ============================================================

def rupiah(value):
    return (
        "Rp{:,.0f}"
        .format(value)
        .replace(",", ".")
    )


def safe_divide(a, b):
    if b == 0:
        return 0

    return a / b


# ============================================================
# SESSION STATE
# ============================================================

if "simulation_data" not in st.session_state:
    st.session_state.simulation_data = None

if "ai_plan" not in st.session_state:
    st.session_state.ai_plan = None

if "hospital_parameters" not in st.session_state:

    st.session_state.hospital_parameters = {

        # SIMULATION
        "simulation_days": 30,
        "patients_per_day": 180,
        "patient_growth": 0,

        # CAPACITY
        "total_beds": 300,
        "icu_beds": 40,
        "er_beds": 50,
        "operation_rooms": 10,

        # STAFF
        "doctors": 80,
        "nurses": 160,

        # FLOW
        "avg_length_stay": 3.0,
        "emergency_rate": 25,
        "icu_rate": 10,
        "discharge_rate": 30,

        # FINANCE
        "monthly_budget": 300000000,
        "doctor_monthly_cost": 20000000,
        "nurse_monthly_cost": 8000000,
        "bed_addition_cost": 15000000,
        "icu_bed_addition_cost": 75000000,
        "average_revenue_per_patient": 2500000,

        # STAFF CAPACITY
        "doctor_capacity_per_day": 12,
        "nurse_capacity_per_day": 8,

        # FORECAST
        "forecast_days": 30,
        "weekly_peak_increase": 15,
        "surge_threshold": 25
    }


# ============================================================
# OPENROUTER API
# ============================================================

try:
    OPENROUTER_API_KEY = (
        st.secrets["OPENROUTER_API_KEY"]
    )

except Exception:
    OPENROUTER_API_KEY = None


# ============================================================
# AI PARAMETER EXTRACTION
# ============================================================

def extract_parameters_with_ai(user_prompt):

    defaults = (
        st.session_state
        .hospital_parameters
        .copy()
    )

    extraction_prompt = f"""
Anda adalah AI Parameter Extractor untuk sistem
Hospital Capacity Planning.

Tugas Anda membaca kondisi rumah sakit dari pengguna
dan mengubahnya menjadi parameter simulasi.

Kembalikan HANYA JSON VALID.

Jangan gunakan markdown.
Jangan berikan penjelasan.
Jangan membuat field baru.

Gunakan struktur:

{{
    "simulation_days": {defaults["simulation_days"]},
    "patients_per_day": {defaults["patients_per_day"]},
    "patient_growth": {defaults["patient_growth"]},

    "total_beds": {defaults["total_beds"]},
    "icu_beds": {defaults["icu_beds"]},
    "er_beds": {defaults["er_beds"]},
    "operation_rooms": {defaults["operation_rooms"]},

    "doctors": {defaults["doctors"]},
    "nurses": {defaults["nurses"]},

    "avg_length_stay": {defaults["avg_length_stay"]},
    "emergency_rate": {defaults["emergency_rate"]},
    "icu_rate": {defaults["icu_rate"]},
    "discharge_rate": {defaults["discharge_rate"]},

    "monthly_budget": {defaults["monthly_budget"]},

    "doctor_monthly_cost":
        {defaults["doctor_monthly_cost"]},

    "nurse_monthly_cost":
        {defaults["nurse_monthly_cost"]},

    "bed_addition_cost":
        {defaults["bed_addition_cost"]},

    "icu_bed_addition_cost":
        {defaults["icu_bed_addition_cost"]},

    "average_revenue_per_patient":
        {defaults["average_revenue_per_patient"]},

    "doctor_capacity_per_day":
        {defaults["doctor_capacity_per_day"]},

    "nurse_capacity_per_day":
        {defaults["nurse_capacity_per_day"]},

    "forecast_days":
        {defaults["forecast_days"]},

    "weekly_peak_increase":
        {defaults["weekly_peak_increase"]},

    "surge_threshold":
        {defaults["surge_threshold"]}
}}

ATURAN:

- Gunakan angka pengguna jika tersedia.
- Jika tidak tersedia, gunakan default.
- Rp300 juta = 300000000.
- Rp20 juta = 20000000.
- Rp2,5 juta = 2500000.
- 25% = 25.
- satu bulan = 30 hari.
- Semua nilai harus numerik.
- Jangan membuat data historis palsu.

PROMPT PENGGUNA:

{user_prompt}
"""

    response = requests.post(

        "https://openrouter.ai/api/v1/chat/completions",

        headers={
            "Authorization":
                f"Bearer {OPENROUTER_API_KEY}",

            "Content-Type":
                "application/json"
        },

        json={
            "model":
                "openrouter/free",

            "messages": [
                {
                    "role": "user",
                    "content":
                        extraction_prompt
                }
            ]
        },

        timeout=60
    )

    if response.status_code != 200:

        raise Exception(
            f"OpenRouter Error "
            f"{response.status_code}: "
            f"{response.text}"
        )

    result = response.json()

    content = (
        result["choices"][0]
        ["message"]["content"]
    )

    if not content:

        raise Exception(
            "AI tidak mengembalikan parameter."
        )

    content = content.strip()

    content = re.sub(
        r"^```json\s*",
        "",
        content,
        flags=re.IGNORECASE
    )

    content = re.sub(
        r"^```\s*",
        "",
        content
    )

    content = re.sub(
        r"\s*```$",
        "",
        content
    )

    start = content.find("{")
    end = content.rfind("}")

    if start == -1 or end == -1:

        raise Exception(
            "Format parameter AI tidak valid."
        )

    data = json.loads(
        content[start:end + 1]
    )

    final = defaults.copy()

    for key in final:

        if key in data:
            final[key] = data[key]

    integer_fields = [

        "simulation_days",
        "patients_per_day",
        "patient_growth",

        "total_beds",
        "icu_beds",
        "er_beds",
        "operation_rooms",

        "doctors",
        "nurses",

        "emergency_rate",
        "icu_rate",
        "discharge_rate",

        "monthly_budget",

        "doctor_monthly_cost",
        "nurse_monthly_cost",

        "bed_addition_cost",
        "icu_bed_addition_cost",

        "average_revenue_per_patient",

        "doctor_capacity_per_day",
        "nurse_capacity_per_day",

        "forecast_days",
        "weekly_peak_increase",
        "surge_threshold"
    ]

    for field in integer_fields:

        final[field] = int(
            float(final[field])
        )

    final["avg_length_stay"] = float(
        final["avg_length_stay"]
    )

    final["simulation_days"] = max(
        1,
        min(
            365,
            final["simulation_days"]
        )
    )

    final["forecast_days"] = max(
        7,
        min(
            90,
            final["forecast_days"]
        )
    )

    final["patients_per_day"] = max(
        1,
        final["patients_per_day"]
    )

    final["total_beds"] = max(
        1,
        final["total_beds"]
    )

    final["doctors"] = max(
        1,
        final["doctors"]
    )

    final["nurses"] = max(
        1,
        final["nurses"]
    )

    final["doctor_capacity_per_day"] = max(
        1,
        final["doctor_capacity_per_day"]
    )

    final["nurse_capacity_per_day"] = max(
        1,
        final["nurse_capacity_per_day"]
    )

    return final


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title(
        "Hospital Command Center"
    )

    st.caption(
        "Capacity, Flow, Forecast & AI Planning"
    )

    st.divider()

    st.subheader(
        "Describe Hospital Condition"
    )

    hospital_prompt = st.text_area(

        "Hospital Condition",


        height=320,

        label_visibility="collapsed"
    )

    st.caption(
        "Masukkan kondisi rumah sakit dengan bahasa biasa."
    )

    st.divider()

    run_simulation = st.button(
        "RUN AI SIMULATION",
        use_container_width=True
    )

    if run_simulation:

        if not hospital_prompt.strip():

            st.error(
                "Masukkan kondisi rumah sakit terlebih dahulu."
            )

        elif not OPENROUTER_API_KEY:

            st.error(
                "OPENROUTER_API_KEY belum ditemukan."
            )

        else:

            try:

                with st.spinner(
                    "AI sedang membaca kondisi rumah sakit..."
                ):

                    new_parameters = (
                        extract_parameters_with_ai(
                            hospital_prompt
                        )
                    )

                st.session_state[
                    "hospital_parameters"
                ] = new_parameters

                st.session_state[
                    "simulation_data"
                ] = None

                st.session_state[
                    "ai_plan"
                ] = None

                st.success(
                    "Parameter berhasil dibuat oleh AI."
                )

            except Exception as error:

                st.error(
                    "AI gagal membaca parameter."
                )

                st.code(
                    str(error)
                )


# ============================================================
# PARAMETERS
# ============================================================

p = st.session_state.hospital_parameters

simulation_days = p["simulation_days"]
patients_per_day = p["patients_per_day"]
patient_growth = p["patient_growth"]

total_beds = p["total_beds"]
icu_beds = p["icu_beds"]
er_beds = p["er_beds"]
operation_rooms = p["operation_rooms"]

doctors = p["doctors"]
nurses = p["nurses"]

avg_length_stay = p["avg_length_stay"]
emergency_rate = p["emergency_rate"]
icu_rate = p["icu_rate"]
discharge_rate = p["discharge_rate"]

monthly_budget = p["monthly_budget"]

doctor_monthly_cost = (
    p["doctor_monthly_cost"]
)

nurse_monthly_cost = (
    p["nurse_monthly_cost"]
)

bed_addition_cost = (
    p["bed_addition_cost"]
)

icu_bed_addition_cost = (
    p["icu_bed_addition_cost"]
)

average_revenue_per_patient = (
    p["average_revenue_per_patient"]
)

doctor_capacity_per_day = (
    p["doctor_capacity_per_day"]
)

nurse_capacity_per_day = (
    p["nurse_capacity_per_day"]
)

forecast_days = p["forecast_days"]

weekly_peak_increase = (
    p["weekly_peak_increase"]
)

surge_threshold = (
    p["surge_threshold"]
)


adjusted_patients = int(

    patients_per_day *

    (
        1 +
        patient_growth / 100
    )
)


# ============================================================
# SIMULATION ENGINE
# ============================================================

def hospital_simulation(

    beds,
    doctor_count,
    nurse_count,

    discharge_improvement=0,
    demand_multiplier=1.0,

    seed=10
):

    rng = np.random.default_rng(
        seed
    )

    records = []

    occupied = int(
        beds * 0.55
    )

    queue = 0

    effective_discharge = min(

        95,

        discharge_rate +
        discharge_improvement
    )

    for day in range(
        1,
        simulation_days + 1
    ):

        variation = rng.normal(

            adjusted_patients *
            demand_multiplier,

            max(
                1,
                adjusted_patients *
                demand_multiplier *
                0.08
            )
        )

        arrivals = max(
            0,
            int(variation)
        )

        doctor_capacity = (

            doctor_count *

            doctor_capacity_per_day
        )

        nurse_capacity = (

            nurse_count *

            nurse_capacity_per_day
        )

        service_capacity = max(

            1,

            min(
                doctor_capacity,
                nurse_capacity
            )
        )

        total_demand = (
            arrivals +
            queue
        )

        served = min(

            total_demand,

            service_capacity
        )

        service_queue = max(

            0,

            total_demand -
            served
        )

        admission_rate = 0.30

        admissions_requested = int(

            served *
            admission_rate
        )

        discharged = int(

            occupied *

            effective_discharge /

            100
        )

        occupied = max(

            0,

            occupied -
            discharged
        )

        available_before = max(

            0,

            beds -
            occupied
        )

        admitted = min(

            admissions_requested,

            available_before
        )

        bed_queue = max(

            0,

            admissions_requested -
            admitted
        )

        occupied += admitted

        occupied = min(
            occupied,
            beds
        )

        queue = (
            service_queue +
            bed_queue
        )

        available = max(
            0,
            beds - occupied
        )

        icu_patients = min(

            icu_beds,

            int(
                occupied *
                icu_rate /
                100
            )
        )

        occupancy_rate_day = (

            safe_divide(
                occupied,
                beds
            )

            * 100
        )

        doctor_utilization = (

            safe_divide(
                served,
                doctor_capacity
            )

            * 100
        )

        nurse_utilization = (

            safe_divide(
                served,
                nurse_capacity
            )

            * 100
        )

        combined_staff = max(

            1,

            doctor_count +
            nurse_count
        )

        waiting_time = (

            queue /
            combined_staff *
            60
        )

        records.append(
            {
                "Day": day,

                "Patient Arrival":
                    arrivals,

                "Patients Served":
                    served,

                "Occupied Beds":
                    occupied,

                "Available Beds":
                    available,

                "Queue":
                    queue,

                "Waiting Time (Min)":
                    waiting_time,

                "Discharged":
                    discharged,

                "ICU Patients":
                    icu_patients,

                "Occupancy Rate (%)":
                    occupancy_rate_day,

                "Doctor Utilization (%)":
                    doctor_utilization,

                "Nurse Utilization (%)":
                    nurse_utilization
            }
        )

    return pd.DataFrame(
        records
    )


# ============================================================
# BASE SIMULATION
# ============================================================

if st.session_state.simulation_data is None:

    st.session_state.simulation_data = (
        hospital_simulation(
            total_beds,
            doctors,
            nurses
        )
    )

df = st.session_state.simulation_data


# ============================================================
# SUMMARY
# ============================================================

def summarize_simulation(
    data,
    scenario_cost=0
):

    served = int(
        data[
            "Patients Served"
        ].sum()
    )

    revenue = (
        served *
        average_revenue_per_patient
    )

    return {

        "occupied":
            int(
                data[
                    "Occupied Beds"
                ].iloc[-1]
            ),

        "occupancy":
            float(
                data[
                    "Occupancy Rate (%)"
                ].iloc[-1]
            ),

        "queue":
            int(
                data[
                    "Queue"
                ].iloc[-1]
            ),

        "avg_queue":
            float(
                data[
                    "Queue"
                ].mean()
            ),

        "waiting":
            float(
                data[
                    "Waiting Time (Min)"
                ].mean()
            ),

        "served":
            served,

        "arrivals":
            int(
                data[
                    "Patient Arrival"
                ].sum()
            ),

        "doctor_util":
            float(
                data[
                    "Doctor Utilization (%)"
                ].mean()
            ),

        "nurse_util":
            float(
                data[
                    "Nurse Utilization (%)"
                ].mean()
            ),

        "cost":
            scenario_cost,

        "revenue":
            revenue
    }


base = summarize_simulation(
    df
)


# ============================================================
# CURRENT CONDITION
# ============================================================

current_occupied = base["occupied"]

available_beds = max(
    0,
    total_beds -
    current_occupied
)

occupancy_rate = base["occupancy"]

current_queue = base["queue"]

average_queue = base["avg_queue"]

maximum_queue = int(
    df["Queue"].max()
)

average_waiting_time = (
    base["waiting"]
)

total_arrivals = (
    base["arrivals"]
)

total_served = (
    base["served"]
)

total_discharge = int(
    df["Discharged"].sum()
)

doctor_utilization = (
    base["doctor_util"]
)

nurse_utilization = (
    base["nurse_util"]
)

estimated_revenue = (
    base["revenue"]
)


icu_used = int(
    df["ICU Patients"].iloc[-1]
)

icu_available = max(
    0,
    icu_beds - icu_used
)

icu_occupancy = (

    safe_divide(
        icu_used,
        icu_beds
    )

    * 100
)


# ============================================================
# STATUS
# ============================================================

if occupancy_rate < 75:

    hospital_status = "NORMAL"

elif occupancy_rate < 90:

    hospital_status = "WARNING"

else:

    hospital_status = "CRITICAL"


# ============================================================
# PATIENT DEMAND FORECAST
# ============================================================

def create_patient_forecast():

    """
    IMPORTANT:
    This is a simulation-based demand projection.

    It does NOT claim to be a clinical/epidemiological
    forecast because historical hospital data has not
    been provided.
    """

    rng = np.random.default_rng(
        42
    )

    today = datetime.now().date()

    records = []

    baseline = adjusted_patients

    for i in range(
        forecast_days
    ):

        forecast_date = (
            today +
            timedelta(days=i + 1)
        )

        # -----------------------------------------------
        # TREND
        # -----------------------------------------------

        trend_multiplier = (

            1 +

            (
                patient_growth /
                100
            )

            *

            (
                i /
                max(
                    1,
                    forecast_days
                )
            )
        )

        # -----------------------------------------------
        # WEEKLY PATTERN
        # -----------------------------------------------

        weekday = (
            forecast_date.weekday()
        )

        weekly_multiplier = 1.0

        # Monday
        if weekday == 0:

            weekly_multiplier += (
                weekly_peak_increase /
                100
            )

        # Friday
        elif weekday == 4:

            weekly_multiplier += (

                weekly_peak_increase /
                100 *
                0.75
            )

        # Weekend slightly lower
        elif weekday in [5, 6]:

            weekly_multiplier -= 0.08

        # -----------------------------------------------
        # RANDOM UNCERTAINTY
        # -----------------------------------------------

        random_multiplier = (
            rng.normal(
                1.0,
                0.06
            )
        )

        predicted = int(

            baseline *

            trend_multiplier *

            weekly_multiplier *

            random_multiplier
        )

        predicted = max(
            0,
            predicted
        )

        # -----------------------------------------------
        # SURGE DETECTION
        # -----------------------------------------------

        increase_percent = (

            (
                predicted -
                baseline
            )

            /
            baseline

            *
            100
        )

        if (
            increase_percent >=
            surge_threshold
        ):

            surge_status = "SURGE"

        elif (
            increase_percent >=
            surge_threshold * 0.60
        ):

            surge_status = "HIGH"

        elif (
            increase_percent >=
            surge_threshold * 0.30
        ):

            surge_status = "WARNING"

        else:

            surge_status = "NORMAL"

        records.append(
            {
                "Date":
                    forecast_date,

                "Day":
                    i + 1,

                "Predicted Patients":
                    predicted,

                "Increase (%)":
                    increase_percent,

                "Demand Status":
                    surge_status
            }
        )

    return pd.DataFrame(
        records
    )


forecast_df = (
    create_patient_forecast()
)


# ============================================================
# FORECAST ANALYSIS
# ============================================================

forecast_average = int(

    forecast_df[
        "Predicted Patients"
    ].mean()
)


peak_index = (

    forecast_df[
        "Predicted Patients"
    ].idxmax()
)


peak_row = (
    forecast_df.loc[
        peak_index
    ]
)


peak_patients = int(
    peak_row[
        "Predicted Patients"
    ]
)


peak_date = (
    peak_row["Date"]
)


peak_day = int(
    peak_row["Day"]
)


peak_increase = float(
    peak_row[
        "Increase (%)"
    ]
)


surge_days_df = (

    forecast_df[

        forecast_df[
            "Demand Status"
        ] == "SURGE"

    ].copy()
)


high_days_df = (

    forecast_df[

        forecast_df[
            "Demand Status"
        ].isin(
            [
                "HIGH",
                "SURGE"
            ]
        )

    ].copy()
)


surge_day_count = len(
    surge_days_df
)


if surge_day_count > 0:

    first_surge_date = (
        surge_days_df[
            "Date"
        ].iloc[0]
    )

    last_surge_date = (
        surge_days_df[
            "Date"
        ].iloc[-1]
    )

    forecast_risk = "CRITICAL"

elif len(high_days_df) > 0:

    first_surge_date = (
        high_days_df[
            "Date"
        ].iloc[0]
    )

    last_surge_date = (
        high_days_df[
            "Date"
        ].iloc[-1]
    )

    forecast_risk = "HIGH"

else:

    first_surge_date = None
    last_surge_date = None

    forecast_risk = "NORMAL"


# ============================================================
# PEAK DEMAND CAPACITY PROJECTION
# ============================================================

peak_doctor_capacity = (

    doctors *
    doctor_capacity_per_day
)

peak_nurse_capacity = (

    nurses *
    nurse_capacity_per_day
)


peak_doctor_load = (

    safe_divide(
        peak_patients,
        peak_doctor_capacity
    )

    * 100
)


peak_nurse_load = (

    safe_divide(
        peak_patients,
        peak_nurse_capacity
    )

    * 100
)


# ============================================================
# BOTTLENECK DETECTION
# ============================================================

bottlenecks = []

if occupancy_rate >= 90:

    bottlenecks.append(
        "Bed Capacity"
    )

if doctor_utilization >= 90:

    bottlenecks.append(
        "Doctor Capacity"
    )

if nurse_utilization >= 90:

    bottlenecks.append(
        "Nurse Capacity"
    )

if average_queue >= 20:

    bottlenecks.append(
        "Patient Queue"
    )

if average_waiting_time >= 30:

    bottlenecks.append(
        "Waiting Time"
    )

if peak_doctor_load >= 100:

    bottlenecks.append(
        "Forecast Doctor Surge Capacity"
    )

if peak_nurse_load >= 100:

    bottlenecks.append(
        "Forecast Nurse Surge Capacity"
    )

if not bottlenecks:

    bottlenecks.append(
        "No Major Bottleneck"
    )


# ============================================================
# WHAT-IF SCENARIOS
# ============================================================

# OPERATIONAL

operational_df = hospital_simulation(

    total_beds,
    doctors,
    nurses,

    discharge_improvement=5,

    seed=10
)

operational = summarize_simulation(
    operational_df,
    0
)


# +1 DOCTOR

doctor_plan_cost = (
    doctor_monthly_cost
)

doctor_df = hospital_simulation(

    total_beds,
    doctors + 1,
    nurses,

    seed=10
)

doctor_plan = summarize_simulation(

    doctor_df,
    doctor_plan_cost
)


# +3 NURSES

nurse_plan_cost = (

    nurse_monthly_cost *
    3
)

nurse_df = hospital_simulation(

    total_beds,
    doctors,
    nurses + 3,

    seed=10
)

nurse_plan = summarize_simulation(

    nurse_df,
    nurse_plan_cost
)


# +10 BEDS

bed_plan_cost = (

    bed_addition_cost *
    10
)

bed_df = hospital_simulation(

    total_beds + 10,
    doctors,
    nurses,

    seed=10
)

bed_plan = summarize_simulation(

    bed_df,
    bed_plan_cost
)


# BALANCED

balanced_cost = (

    doctor_monthly_cost

    +

    nurse_monthly_cost * 2

    +

    bed_addition_cost * 5
)

balanced_df = hospital_simulation(

    total_beds + 5,
    doctors + 1,
    nurses + 2,

    discharge_improvement=3,

    seed=10
)

balanced = summarize_simulation(

    balanced_df,
    balanced_cost
)


# ============================================================
# SCENARIO DATAFRAME
# ============================================================

scenario_data = pd.DataFrame(

    [
        {
            "Scenario":
                "Current",

            "Action":
                "No change",

            "Additional Cost":
                0,

            "Patients Served":
                base["served"],

            "Occupancy (%)":
                base["occupancy"],

            "Final Queue":
                base["queue"],

            "Waiting Time":
                base["waiting"],

            "Doctor Utilization (%)":
                base["doctor_util"],

            "Nurse Utilization (%)":
                base["nurse_util"]
        },

        {
            "Scenario":
                "Operational",

            "Action":
                "Improve discharge flow",

            "Additional Cost":
                operational["cost"],

            "Patients Served":
                operational["served"],

            "Occupancy (%)":
                operational["occupancy"],

            "Final Queue":
                operational["queue"],

            "Waiting Time":
                operational["waiting"],

            "Doctor Utilization (%)":
                operational["doctor_util"],

            "Nurse Utilization (%)":
                operational["nurse_util"]
        },

        {
            "Scenario":
                "Doctor Plan",

            "Action":
                "+1 doctor",

            "Additional Cost":
                doctor_plan["cost"],

            "Patients Served":
                doctor_plan["served"],

            "Occupancy (%)":
                doctor_plan["occupancy"],

            "Final Queue":
                doctor_plan["queue"],

            "Waiting Time":
                doctor_plan["waiting"],

            "Doctor Utilization (%)":
                doctor_plan["doctor_util"],

            "Nurse Utilization (%)":
                doctor_plan["nurse_util"]
        },

        {
            "Scenario":
                "Nurse Plan",

            "Action":
                "+3 nurses",

            "Additional Cost":
                nurse_plan["cost"],

            "Patients Served":
                nurse_plan["served"],

            "Occupancy (%)":
                nurse_plan["occupancy"],

            "Final Queue":
                nurse_plan["queue"],

            "Waiting Time":
                nurse_plan["waiting"],

            "Doctor Utilization (%)":
                nurse_plan["doctor_util"],

            "Nurse Utilization (%)":
                nurse_plan["nurse_util"]
        },

        {
            "Scenario":
                "Bed Plan",

            "Action":
                "+10 beds",

            "Additional Cost":
                bed_plan["cost"],

            "Patients Served":
                bed_plan["served"],

            "Occupancy (%)":
                bed_plan["occupancy"],

            "Final Queue":
                bed_plan["queue"],

            "Waiting Time":
                bed_plan["waiting"],

            "Doctor Utilization (%)":
                bed_plan["doctor_util"],

            "Nurse Utilization (%)":
                bed_plan["nurse_util"]
        },

        {
            "Scenario":
                "Balanced",

            "Action":
                "+1 doctor, +2 nurses, +5 beds",

            "Additional Cost":
                balanced["cost"],

            "Patients Served":
                balanced["served"],

            "Occupancy (%)":
                balanced["occupancy"],

            "Final Queue":
                balanced["queue"],

            "Waiting Time":
                balanced["waiting"],

            "Doctor Utilization (%)":
                balanced["doctor_util"],

            "Nurse Utilization (%)":
                balanced["nurse_util"]
        }
    ]
)


scenario_data[
    "Within Budget"
] = (

    scenario_data[
        "Additional Cost"
    ]

    <=

    monthly_budget
)


scenario_data[
    "Budget Remaining"
] = (

    monthly_budget

    -

    scenario_data[
        "Additional Cost"
    ]
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="hospital-hero">
        <div class="hospital-kicker">Hospital Operations Intelligence</div>
        <div class="hospital-title">AI-Assisted Hospital Capacity Simulation</div>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# TABS
# ============================================================

(
    tab_overview,
    tab_capacity,
    tab_flow,
    tab_queue,
    tab_simulation,
    tab_forecast,
    tab_scenario,
    tab_ai,
    tab_report

) = st.tabs(

    [
        "OVERVIEW",
        "CAPACITY",
        "PATIENT FLOW",
        "QUEUE",
        "SIMULATION",
        "FORECAST",
        "SCENARIO",
        "AI PLANNER",
        "REPORT"
    ]
)


# ============================================================
# OVERVIEW
# ============================================================

with tab_overview:

    st.header(
        "Hospital Overview"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Beds",
        total_beds
    )

    c2.metric(
        "Occupied Beds",
        current_occupied
    )

    c3.metric(
        "Available Beds",
        available_beds
    )

    c4.metric(
        "Occupancy Rate",
        f"{occupancy_rate:.1f}%"
    )

    c5, c6, c7, c8 = st.columns(4)

    c5.metric(
        "Doctors",
        doctors
    )

    c6.metric(
        "Nurses",
        nurses
    )

    c7.metric(
        "Current Queue",
        current_queue
    )

    c8.metric(
        "Hospital Status",
        hospital_status
    )

    st.subheader(
        "Occupancy Overview"
    )

    st.line_chart(

        df.set_index("Day")[

            [
                "Occupied Beds",
                "Available Beds"
            ]
        ]
    )

    if hospital_status == "NORMAL":

        st.success(
            "Hospital capacity is within normal threshold."
        )

    elif hospital_status == "WARNING":

        st.warning(
            "Hospital capacity is approaching high utilization."
        )

    else:

        st.error(
            "Hospital capacity is under critical pressure."
        )


# ============================================================
# CAPACITY
# ============================================================

with tab_capacity:

    st.header(
        "Hospital Capacity"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Hospital Beds",
        total_beds
    )

    c2.metric(
        "Beds In Use",
        current_occupied
    )

    c3.metric(
        "Beds Available",
        available_beds
    )

    c4.metric(
        "Utilization",
        f"{occupancy_rate:.1f}%"
    )

    c5, c6, c7, c8 = st.columns(4)

    c5.metric(
        "ICU Capacity",
        icu_beds
    )

    c6.metric(
        "ICU Used",
        icu_used
    )

    c7.metric(
        "ICU Available",
        icu_available
    )

    c8.metric(
        "ICU Utilization",
        f"{icu_occupancy:.1f}%"
    )


# ============================================================
# PATIENT FLOW
# ============================================================

with tab_flow:

    st.header(
        "Patient Flow"
    )

    st.write(
        """
        Patient Arrival → Registration →
        Diagnosis → Admission → Treatment → Discharge
        """
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Patients / Day",
        adjusted_patients
    )

    c2.metric(
        "Total Arrivals",
        total_arrivals
    )

    c3.metric(
        "Patients Served",
        total_served
    )

    c4.metric(
        "Total Discharged",
        total_discharge
    )

    st.subheader(
        "Patient Demand vs Served"
    )

    st.line_chart(

        df.set_index("Day")[

            [
                "Patient Arrival",
                "Patients Served"
            ]
        ]
    )


# ============================================================
# QUEUE
# ============================================================

with tab_queue:

    st.header(
        "Hospital Queue"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Current Queue",
        current_queue
    )

    c2.metric(
        "Average Queue",
        f"{average_queue:.1f}"
    )

    c3.metric(
        "Maximum Queue",
        maximum_queue
    )

    c4.metric(
        "Average Waiting",
        f"{average_waiting_time:.1f} min"
    )

    st.subheader(
        "Queue Development"
    )

    st.line_chart(

        df.set_index("Day")[

            ["Queue"]
        ]
    )

    st.subheader(
        "Waiting Time"
    )

    st.line_chart(

        df.set_index("Day")[

            ["Waiting Time (Min)"]
        ]
    )


# ============================================================
# SIMULATION
# ============================================================

with tab_simulation:

    st.header(
        "Hospital Simulation"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Simulation Days",
        simulation_days
    )

    c2.metric(
        "Patients / Day",
        adjusted_patients
    )

    c3.metric(
        "Doctor Utilization",
        f"{doctor_utilization:.1f}%"
    )

    c4.metric(
        "Nurse Utilization",
        f"{nurse_utilization:.1f}%"
    )

    st.subheader(
        "Simulation Timeline"
    )

    st.line_chart(

        df.set_index("Day")[

            [
                "Patient Arrival",
                "Patients Served",
                "Occupied Beds",
                "Queue"
            ]
        ]
    )

    st.subheader(
        "Simulation Data"
    )

    st.dataframe(

        df.round(2),

        use_container_width=True,

        hide_index=True
    )


# ============================================================
# FORECAST
# ============================================================

with tab_forecast:

    st.header(
        "Patient Surge Forecast"
    )


    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Forecast Horizon",
        f"{forecast_days} days"
    )

    c2.metric(
        "Average Forecast",
        f"{forecast_average} patients/day"
    )

    c3.metric(
        "Expected Peak",
        f"{peak_patients} patients"
    )

    c4.metric(
        "Forecast Risk",
        forecast_risk
    )

    st.subheader(
        "Expected Peak Demand"
    )

    p1, p2, p3, p4 = st.columns(4)

    p1.metric(
        "Peak Day",
        f"Day {peak_day}"
    )

    p2.metric(
        "Peak Date",
        peak_date.strftime(
            "%d %b %Y"
        )
    )

    p3.metric(
        "Peak Increase",
        f"{peak_increase:+.1f}%"
    )

    p4.metric(
        "Detected Surge Days",
        surge_day_count
    )

    if first_surge_date:

        st.error(
            "High-demand period detected between "
            f"{first_surge_date.strftime('%d %b %Y')} "
            "and "
            f"{last_surge_date.strftime('%d %b %Y')}."
        )

    else:

        st.success(
            "No surge period crosses the current threshold."
        )

    st.subheader(
        "Projected Patient Demand"
    )

    forecast_chart = (
        forecast_df[
            [
                "Date",
                "Predicted Patients"
            ]
        ]
        .set_index("Date")
    )

    st.line_chart(
        forecast_chart
    )

    st.subheader(
        "Surge Capacity Pressure"
    )

    s1, s2 = st.columns(2)

    s1.metric(
        "Doctor Load at Peak",
        f"{peak_doctor_load:.1f}%"
    )

    s2.metric(
        "Nurse Load at Peak",
        f"{peak_nurse_load:.1f}%"
    )

    if peak_doctor_load > 100:

        st.error(
            "Projected peak demand exceeds the current "
            "calculated doctor service capacity."
        )

    if peak_nurse_load > 100:

        st.error(
            "Projected peak demand exceeds the current "
            "calculated nurse service capacity."
        )

    st.subheader(
        "Forecast Details"
    )

    forecast_display = (
        forecast_df.copy()
    )

    forecast_display[
        "Date"
    ] = (

        pd.to_datetime(
            forecast_display["Date"]
        )

        .dt.strftime(
            "%d-%m-%Y"
        )
    )

    forecast_display[
        "Increase (%)"
    ] = (

        forecast_display[
            "Increase (%)"
        ]

        .round(1)
    )

    st.dataframe(

        forecast_display,

        use_container_width=True,

        hide_index=True
    )


# ============================================================
# SCENARIO
# ============================================================

with tab_scenario:

    st.header(
        "Hospital What-If Scenario"
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Available Budget",
        rupiah(
            monthly_budget
        )
    )

    c2.metric(
        "Target Staff Utilization",
        "70%"
    )

    c3.metric(
        "Patients Served",
        total_served
    )

    display_scenario = (
        scenario_data.copy()
    )

    display_scenario[
        "Additional Cost"
    ] = (

        display_scenario[
            "Additional Cost"
        ]

        .apply(rupiah)
    )

    display_scenario[
        "Budget Remaining"
    ] = (

        display_scenario[
            "Budget Remaining"
        ]

        .apply(rupiah)
    )

    numeric_round_columns = [

        "Occupancy (%)",
        "Waiting Time",
        "Doctor Utilization (%)",
        "Nurse Utilization (%)"
    ]

    for column in numeric_round_columns:

        display_scenario[column] = (

            display_scenario[column]
            .round(1)
        )

    st.dataframe(

        display_scenario,

        use_container_width=True,

        hide_index=True
    )

    st.subheader(
        "Patients Served Comparison"
    )

    st.bar_chart(

        scenario_data
        .set_index("Scenario")[

            ["Patients Served"]
        ]
    )

    st.subheader(
        "Queue Comparison"
    )

    st.bar_chart(

        scenario_data
        .set_index("Scenario")[

            ["Final Queue"]
        ]
    )


# ============================================================
# ============================================================
# STAFF UTILIZATION POLICY
# ============================================================

TARGET_STAFF_UTILIZATION = 70.0

# Dokter dan perawat ditargetkan sedekat mungkin dengan 70%.
# Jika utilization < 70%, optimizer mencoba mengurangi tenaga kerja.
# Jika utilization > 70%, optimizer mencoba menambah tenaga kerja.
# Karena jumlah staf berupa bilangan bulat, tepat 70.00% tidak selalu
# mungkin. Dalam kondisi tersebut dipilih konfigurasi aman yang
# paling dekat dengan 70% dengan tetap mempertimbangkan biaya.


# ============================================================
# AI PLANNER
# ============================================================

with tab_ai:

    st.header(
        "AI Hospital Planner"
    )


    # ========================================================
    # CURRENT SITUATION
    # ========================================================

    st.subheader(
        "Current Situation"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Hospital Status",
        hospital_status
    )

    c2.metric(
        "Occupancy",
        f"{occupancy_rate:.1f}%"
    )

    c3.metric(
        "Queue",
        current_queue
    )

    c4.metric(
        "Budget",
        rupiah(
            monthly_budget
        )
    )


    c5, c6, c7, c8 = st.columns(4)

    c5.metric(
        "Doctor Load",
        f"{doctor_utilization:.1f}%"
    )

    c6.metric(
        "Nurse Load",
        f"{nurse_utilization:.1f}%"
    )

    c7.metric(
        "Forecast Peak",
        peak_patients
    )

    c8.metric(
        "Surge Risk",
        forecast_risk
    )

    st.subheader(
        "Staff Utilization Target"
    )

    u1, u2, u3 = st.columns(3)

    u1.metric(
        "Target Utilization",
        "70%"
    )

    u2.metric(
        "Doctor Utilization",
        f"{doctor_utilization:.1f}%"
    )

    u3.metric(
        "Nurse Utilization",
        f"{nurse_utilization:.1f}%"
    )

    if doctor_utilization < TARGET_STAFF_UTILIZATION:

        st.info(
            "Doctor utilization berada di bawah 70%. "
            "Resource Optimizer akan mengevaluasi pengurangan dokter "
            "agar utilisasi mendekati 70% dengan tetap menjaga pelayanan."
        )

    elif doctor_utilization > TARGET_STAFF_UTILIZATION:

        st.warning(
            "Doctor utilization berada di atas 70%. "
            "Resource Optimizer akan mengevaluasi penambahan dokter "
            "agar utilisasi mendekati 70% dengan mempertimbangkan budget."
        )

    else:

        st.success(
            "Doctor utilization berada pada target 70%."
        )

    if nurse_utilization < TARGET_STAFF_UTILIZATION:

        st.info(
            "Nurse utilization berada di bawah 70%. "
            "Resource Optimizer akan mengevaluasi pengurangan perawat "
            "agar utilisasi mendekati 70% dengan tetap menjaga pelayanan."
        )

    elif nurse_utilization > TARGET_STAFF_UTILIZATION:

        st.warning(
            "Nurse utilization berada di atas 70%. "
            "Resource Optimizer akan mengevaluasi penambahan perawat "
            "agar utilisasi mendekati 70% dengan mempertimbangkan budget."
        )

    else:

        st.success(
            "Nurse utilization berada pada target 70%."
        )


    # ========================================================
    # DETECTED BOTTLENECKS
    # ========================================================

    st.subheader(
        "Detected Bottlenecks"
    )

    for item in bottlenecks:

        st.write(
            f"• {item}"
        )


    # ========================================================
    # PLANNING COST ASSUMPTIONS
    # ========================================================

    st.subheader(
        "Planning Cost Assumptions"
    )

    cost_table = pd.DataFrame(
        {
            "Resource": [
                "Doctor / Month",
                "Nurse / Month",
                "Additional Bed"
            ],

            "Cost / Value": [

                rupiah(
                    doctor_monthly_cost
                ),

                rupiah(
                    nurse_monthly_cost
                ),

                rupiah(
                    bed_addition_cost
                )
            ]
        }
    )

    st.dataframe(
        cost_table,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Nilai biaya default adalah asumsi prototype. "
        "Untuk implementasi rumah sakit, gunakan data biaya internal."
    )


    # ========================================================
    # RESOURCE OPTIMIZATION ENGINE
    # ========================================================

    def evaluate_resource_configuration(
        test_doctors,
        test_nurses,
        test_beds
    ):

        test_doctors = max(
            1,
            int(test_doctors)
        )

        test_nurses = max(
            1,
            int(test_nurses)
        )

        test_beds = max(
            1,
            int(test_beds)
        )


        # ----------------------------------------------------
        # RUN SIMULATION
        # ----------------------------------------------------

        test_df = hospital_simulation(

            test_beds,
            test_doctors,
            test_nurses,

            seed=10
        )


        result = summarize_simulation(
            test_df
        )


        # ----------------------------------------------------
        # RESOURCE CHANGE
        # ----------------------------------------------------

        doctor_change = (
            test_doctors -
            doctors
        )

        nurse_change = (
            test_nurses -
            nurses
        )

        bed_change = (
            test_beds -
            total_beds
        )


        # ----------------------------------------------------
        # COST OF ADDITION
        # ----------------------------------------------------

        doctor_addition_cost = (

            max(
                0,
                doctor_change
            )

            *

            doctor_monthly_cost
        )


        nurse_addition_cost = (

            max(
                0,
                nurse_change
            )

            *

            nurse_monthly_cost
        )


        bed_addition_total_cost = (

            max(
                0,
                bed_change
            )

            *

            bed_addition_cost
        )


        additional_cost = (

            doctor_addition_cost

            +

            nurse_addition_cost

            +

            bed_addition_total_cost
        )


        # ----------------------------------------------------
        # SAVING FROM RESOURCE REDUCTION
        # ----------------------------------------------------

        doctor_saving = (

            max(
                0,
                -doctor_change
            )

            *

            doctor_monthly_cost
        )


        nurse_saving = (

            max(
                0,
                -nurse_change
            )

            *

            nurse_monthly_cost
        )


        monthly_saving = (

            doctor_saving

            +

            nurse_saving
        )


        # ----------------------------------------------------
        # NET BUDGET IMPACT
        # ----------------------------------------------------

        net_budget_impact = (

            additional_cost

            -

            monthly_saving
        )


        # ----------------------------------------------------
        # AVAILABLE BUDGET
        # ----------------------------------------------------

        effective_budget = (

            monthly_budget

            +

            monthly_saving
        )


        budget_ok = (

            additional_cost

            <=

            effective_budget
        )


        # ----------------------------------------------------
        # SERVICE LEVEL
        # ----------------------------------------------------

        service_ratio = safe_divide(

            result["served"],

            max(
                1,
                base["served"]
            )
        )


        # ----------------------------------------------------
        # QUEUE CHANGE
        # ----------------------------------------------------

        queue_change = (

            result["avg_queue"]

            -

            base["avg_queue"]
        )


        # ----------------------------------------------------
        # WAITING CHANGE
        # ----------------------------------------------------

        waiting_change = (

            result["waiting"]

            -

            base["waiting"]
        )


        # ----------------------------------------------------
        # SAFE OPERATIONAL LIMIT
        # ----------------------------------------------------

        doctor_safe = (

            result["doctor_util"]

            <= 90
        )


        nurse_safe = (

            result["nurse_util"]

            <= 90
        )


        occupancy_safe = (

            result["occupancy"]

            <= 95
        )


        service_safe = (

            service_ratio

            >= 0.98
        )


        queue_safe = (

            result["avg_queue"]

            <=

            max(
                5,
                base["avg_queue"] * 1.10
            )
        )


        operational_safe = (

            doctor_safe

            and

            nurse_safe

            and

            occupancy_safe

            and

            service_safe

            and

            queue_safe
        )


        return {

            "Doctors":
                test_doctors,

            "Nurses":
                test_nurses,

            "Beds":
                test_beds,

            "Doctor Change":
                doctor_change,

            "Nurse Change":
                nurse_change,

            "Bed Change":
                bed_change,

            "Doctor Utilization":
                result["doctor_util"],

            "Nurse Utilization":
                result["nurse_util"],

            "Bed Occupancy":
                result["occupancy"],

            "Average Queue":
                result["avg_queue"],

            "Waiting Time":
                result["waiting"],

            "Patients Served":
                result["served"],

            "Service Ratio":
                service_ratio,

            "Queue Change":
                queue_change,

            "Waiting Change":
                waiting_change,

            "Additional Cost":
                additional_cost,

            "Doctor Saving":
                doctor_saving,

            "Nurse Saving":
                nurse_saving,

            "Monthly Saving":
                monthly_saving,

            "Net Budget Impact":
                net_budget_impact,

            "Effective Budget":
                effective_budget,

            "Budget OK":
                budget_ok,

            "Operational Safe":
                operational_safe
        }


    # ========================================================
    # CREATE RESOURCE CANDIDATES
    # ========================================================

    resource_options = []


    # --------------------------------------------------------
    # CURRENT CONFIGURATION
    # --------------------------------------------------------

    resource_options.append(

        evaluate_resource_configuration(

            doctors,
            nurses,
            total_beds
        )
    )


    # ========================================================
    # STAFF CANDIDATES FOR 70% UTILIZATION
    # ========================================================

    average_daily_served = max(
        1,
        safe_divide(
            base["served"],
            simulation_days
        )
    )

    ideal_doctors = max(
        1,
        int(
            round(
                safe_divide(
                    average_daily_served,
                    doctor_capacity_per_day *
                    (TARGET_STAFF_UTILIZATION / 100)
                )
            )
        )
    )

    ideal_nurses = max(
        1,
        int(
            round(
                safe_divide(
                    average_daily_served,
                    nurse_capacity_per_day *
                    (TARGET_STAFF_UTILIZATION / 100)
                )
            )
        )
    )

    doctor_candidates = sorted(
        set(
            [doctors]
            +
            list(
                range(
                    max(1, ideal_doctors - 10),
                    ideal_doctors + 11
                )
            )
        )
    )

    nurse_candidates = sorted(
        set(
            [nurses]
            +
            list(
                range(
                    max(1, ideal_nurses - 20),
                    ideal_nurses + 21
                )
            )
        )
    )

    # Uji perubahan dokter saja.
    for test_doctors in doctor_candidates:

        resource_options.append(

            evaluate_resource_configuration(

                test_doctors,
                nurses,
                total_beds
            )
        )

    # Uji perubahan perawat saja.
    for test_nurses in nurse_candidates:

        resource_options.append(

            evaluate_resource_configuration(

                doctors,
                test_nurses,
                total_beds
            )
        )

    # Uji perubahan dokter dan perawat secara bersamaan.
    for test_doctors in doctor_candidates:

        for test_nurses in nurse_candidates:

            resource_options.append(

                evaluate_resource_configuration(

                    test_doctors,
                    test_nurses,
                    total_beds
                )
            )


    # ========================================================
    # ADD BEDS
    # ========================================================

    for addition in [

        1,
        5,
        10,
        20,
        30

    ]:

        resource_options.append(

            evaluate_resource_configuration(

                doctors,
                nurses,
                total_beds + addition
            )
        )


    # ========================================================
    # MIXED RESOURCE CHANGES
    # ========================================================

    mixed_doctor_values = doctor_candidates

    mixed_nurse_values = nurse_candidates


    bed_values = [

        total_beds,

        total_beds + 5,

        total_beds + 10
    ]


    for test_doctors in mixed_doctor_values:

        for test_nurses in mixed_nurse_values:

            for test_beds in bed_values:

                resource_options.append(

                    evaluate_resource_configuration(

                        test_doctors,
                        test_nurses,
                        test_beds
                    )
                )


    # ========================================================
    # RESOURCE DATAFRAME
    # ========================================================

    resource_optimizer_df = pd.DataFrame(
        resource_options
    )


    resource_optimizer_df = (

        resource_optimizer_df

        .drop_duplicates(

            subset=[
                "Doctors",
                "Nurses",
                "Beds"
            ]

        )

        .reset_index(
            drop=True
        )
    )


    # ========================================================
    # SCORE RESOURCE PLAN
    # ========================================================

    def calculate_resource_score(row):

        score = 0.0


        doctor_util = float(
            row[
                "Doctor Utilization"
            ]
        )


        nurse_util = float(
            row[
                "Nurse Utilization"
            ]
        )


        occupancy = float(
            row[
                "Bed Occupancy"
            ]
        )


        avg_queue = float(
            row[
                "Average Queue"
            ]
        )


        waiting = float(
            row[
                "Waiting Time"
            ]
        )


        service_ratio = float(
            row[
                "Service Ratio"
            ]
        )


        monthly_saving = float(
            row[
                "Monthly Saving"
            ]
        )


        additional_cost = float(
            row[
                "Additional Cost"
            ]
        )


        # ----------------------------------------------------
        # DOCTOR UTILIZATION TARGET
        # ----------------------------------------------------

        doctor_distance = abs(
            doctor_util -
            TARGET_STAFF_UTILIZATION
        )

        # 70% adalah target utama.
        # Semakin jauh dari 70%, semakin besar penalti.
        score -= doctor_distance * 25

        if doctor_distance <= 0.5:

            score += 500


        # ----------------------------------------------------
        # NURSE UTILIZATION TARGET
        # ----------------------------------------------------

        nurse_distance = abs(
            nurse_util -
            TARGET_STAFF_UTILIZATION
        )

        # 70% adalah target utama.
        # Semakin jauh dari 70%, semakin besar penalti.
        score -= nurse_distance * 25

        if nurse_distance <= 0.5:

            score += 500


        # ----------------------------------------------------
        # BED OCCUPANCY
        # ----------------------------------------------------

        if 65 <= occupancy <= 85:

            score += 25

        elif 50 <= occupancy < 65:

            score += 15

        elif 85 < occupancy <= 90:

            score += 15

        elif 40 <= occupancy < 50:

            score += 5

        elif occupancy > 95:

            score -= 70

        elif occupancy < 30:

            score -= 15


        # ----------------------------------------------------
        # QUEUE
        # ----------------------------------------------------

        if avg_queue <= 1:

            score += 30

        elif avg_queue <= 5:

            score += 25

        elif avg_queue <= 10:

            score += 10

        elif avg_queue <= 20:

            score -= 10

        else:

            score -= 50


        # ----------------------------------------------------
        # WAITING TIME
        # ----------------------------------------------------

        if waiting <= 5:

            score += 20

        elif waiting <= 15:

            score += 15

        elif waiting <= 30:

            score += 5

        else:

            score -= 40


        # ----------------------------------------------------
        # PATIENT SERVICE
        # ----------------------------------------------------

        if service_ratio >= 1.0:

            score += 35

        elif service_ratio >= 0.99:

            score += 30

        elif service_ratio >= 0.98:

            score += 20

        elif service_ratio >= 0.95:

            score -= 30

        else:

            score -= 150


        # ----------------------------------------------------
        # SAVING REWARD
        # ----------------------------------------------------

        if monthly_saving > 0:

            saving_unit = max(

                1,

                min(
                    doctor_monthly_cost,
                    nurse_monthly_cost
                )
            )


            saving_score = min(

                35,

                safe_divide(
                    monthly_saving,
                    saving_unit
                )

                * 4
            )


            score += saving_score


        # ----------------------------------------------------
        # COST PENALTY
        # ----------------------------------------------------

        if additional_cost > 0:

            if monthly_budget > 0:

                cost_ratio = (

                    additional_cost /

                    monthly_budget
                )

                score -= (

                    cost_ratio * 25
                )

            else:

                score -= 100


        # ----------------------------------------------------
        # HARD CONSTRAINT
        # ----------------------------------------------------

        if not bool(
            row["Budget OK"]
        ):

            score -= 1000


        if not bool(
            row["Operational Safe"]
        ):

            score -= 1000


        return score


    resource_optimizer_df[
        "Score"
    ] = (

        resource_optimizer_df.apply(

            calculate_resource_score,

            axis=1
        )
    )


    # ========================================================
    # FILTER SAFE PLANS
    # ========================================================

    safe_resource_plans = (

        resource_optimizer_df[

            (
                resource_optimizer_df[
                    "Budget OK"
                ]
            )

            &

            (
                resource_optimizer_df[
                    "Operational Safe"
                ]
            )

        ]

        .copy()
    )


    # ========================================================
    # UTILIZATION DISTANCE TO 70%
    # ========================================================

    safe_resource_plans[
        "Doctor Distance to 70"
    ] = abs(
        safe_resource_plans[
            "Doctor Utilization"
        ] - TARGET_STAFF_UTILIZATION
    )

    safe_resource_plans[
        "Nurse Distance to 70"
    ] = abs(
        safe_resource_plans[
            "Nurse Utilization"
        ] - TARGET_STAFF_UTILIZATION
    )

    safe_resource_plans[
        "Max Utilization Distance"
    ] = safe_resource_plans[
        [
            "Doctor Distance to 70",
            "Nurse Distance to 70"
        ]
    ].max(axis=1)

    safe_resource_plans[
        "Total Utilization Distance"
    ] = (
        safe_resource_plans[
            "Doctor Distance to 70"
        ]
        +
        safe_resource_plans[
            "Nurse Distance to 70"
        ]
    )


    # ========================================================
    # SELECT PLAN
    # ========================================================

    if len(
        safe_resource_plans
    ) > 0:

        safe_resource_plans = (

            safe_resource_plans

            .sort_values(

                by=[
                    "Max Utilization Distance",
                    "Total Utilization Distance",
                    "Net Budget Impact",
                    "Additional Cost",
                    "Score"
                ],

                ascending=[
                    True,
                    True,
                    True,
                    True,
                    False
                ]
            )

            .reset_index(
                drop=True
            )
        )


        best_resource_plan = (

            safe_resource_plans.iloc[0]
        )

    else:

        fallback_plans = (

            resource_optimizer_df

            .sort_values(

                by=[
                    "Score",
                    "Patients Served"
                ],

                ascending=[
                    False,
                    False
                ]
            )

            .reset_index(
                drop=True
            )
        )


        best_resource_plan = (

            fallback_plans.iloc[0]
        )


    # ========================================================
    # SELECTED RESOURCE PLAN
    # ========================================================

    selected_doctors = int(
        best_resource_plan[
            "Doctors"
        ]
    )


    selected_nurses = int(
        best_resource_plan[
            "Nurses"
        ]
    )


    selected_beds = int(
        best_resource_plan[
            "Beds"
        ]
    )


    selected_doctor_change = int(
        best_resource_plan[
            "Doctor Change"
        ]
    )


    selected_nurse_change = int(
        best_resource_plan[
            "Nurse Change"
        ]
    )


    selected_bed_change = int(
        best_resource_plan[
            "Bed Change"
        ]
    )


    selected_saving = float(
        best_resource_plan[
            "Monthly Saving"
        ]
    )


    selected_cost = float(
        best_resource_plan[
            "Additional Cost"
        ]
    )


    selected_net_budget = float(
        best_resource_plan[
            "Net Budget Impact"
        ]
    )


    # ========================================================
    # RESOURCE STATUS
    # ========================================================

    underutilized_resources = []


    if doctor_utilization < 50:

        underutilized_resources.append(
            "Doctor"
        )


    if nurse_utilization < 50:

        underutilized_resources.append(
            "Nurse"
        )


    if occupancy_rate < 50:

        underutilized_resources.append(
            "Bed"
        )


    overloaded_resources = []


    if doctor_utilization > 90:

        overloaded_resources.append(
            "Doctor"
        )


    if nurse_utilization > 90:

        overloaded_resources.append(
            "Nurse"
        )


    if occupancy_rate > 90:

        overloaded_resources.append(
            "Bed"
        )


    # ========================================================
    # AI INSIGHT
    # ========================================================

    st.divider()

    st.subheader(
        "AI Resource Insight"
    )


    insight_col1, insight_col2 = st.columns(2)


    with insight_col1:

        st.markdown(
            "**Underutilized Resource**"
        )

        if underutilized_resources:

            for resource in underutilized_resources:

                st.write(
                    f"• {resource}"
                )

        else:

            st.write(
                "Tidak ada resource dengan utilisasi sangat rendah."
            )


    with insight_col2:

        st.markdown(
            "**Overloaded Resource**"
        )

        if overloaded_resources:

            for resource in overloaded_resources:

                st.write(
                    f"• {resource}"
                )

        else:

            st.write(
                "Tidak ada resource dengan utilisasi >90%."
            )


    # ========================================================
    # SELECTED RESOURCE PLAN UI
    # ========================================================

    st.subheader(
        "Selected Resource Plan"
    )


    r1, r2, r3 = st.columns(3)


    r1.metric(

        "Doctors",

        selected_doctors,

        delta=(
            f"{selected_doctor_change:+d}"
        )
    )


    r2.metric(

        "Nurses",

        selected_nurses,

        delta=(
            f"{selected_nurse_change:+d}"
        )
    )


    r3.metric(

        "Beds",

        selected_beds,

        delta=(
            f"{selected_bed_change:+d}"
        )
    )


    # ========================================================
    # FINANCIAL IMPACT
    # ========================================================

    f1, f2, f3 = st.columns(3)


    f1.metric(

        "Additional Cost",

        rupiah(
            selected_cost
        )
    )


    f2.metric(

        "Monthly Saving",

        rupiah(
            selected_saving
        )
    )


    if selected_net_budget > 0:

        net_label = (
            "Additional Spending"
        )

        net_value = rupiah(
            selected_net_budget
        )

    elif selected_net_budget < 0:

        net_label = (
            "Net Saving"
        )

        net_value = rupiah(
            abs(
                selected_net_budget
            )
        )

    else:

        net_label = (
            "Net Budget Impact"
        )

        net_value = rupiah(0)


    f3.metric(

        net_label,

        net_value
    )


    # ========================================================
    # EXPECTED SIMULATION IMPACT
    # ========================================================

    st.subheader(
        "Expected Simulation Impact"
    )


    impact_table = pd.DataFrame(

        {

            "Indicator": [

                "Doctor Utilization",

                "Nurse Utilization",

                "Bed Occupancy",

                "Average Queue",

                "Waiting Time",

                "Patients Served"
            ],


            "Current": [

                f"{doctor_utilization:.1f}%",

                f"{nurse_utilization:.1f}%",

                f"{occupancy_rate:.1f}%",

                f"{average_queue:.1f}",

                f"{average_waiting_time:.1f} min",

                f"{total_served:,}"
            ],


            "Proposed": [

                (
                    f"{best_resource_plan['Doctor Utilization']:.1f}%"
                ),

                (
                    f"{best_resource_plan['Nurse Utilization']:.1f}%"
                ),

                (
                    f"{best_resource_plan['Bed Occupancy']:.1f}%"
                ),

                (
                    f"{best_resource_plan['Average Queue']:.1f}"
                ),

                (
                    f"{best_resource_plan['Waiting Time']:.1f} min"
                ),

                (
                    f"{int(best_resource_plan['Patients Served']):,}"
                )
            ]
        }
    )


    st.dataframe(

        impact_table,

        use_container_width=True,

        hide_index=True
    )


    # ========================================================
    # STAFFING PLAN
    # ========================================================

    st.subheader(
        "Staffing Plan"
    )


    staffing_messages = []


    # --------------------------------------------------------
    # DOCTOR PLAN
    # --------------------------------------------------------

    if selected_doctor_change < 0:

        doctor_reduction = abs(
            selected_doctor_change
        )

        doctor_saving_value = (

            doctor_reduction

            *

            doctor_monthly_cost
        )


        staffing_messages.append(

            f"Dokter: {doctors} → {selected_doctors}. "
            f"Potensi penghematan {rupiah(doctor_saving_value)}/bulan. "
            f"Utilisasi diproyeksikan menjadi "
            f"{best_resource_plan['Doctor Utilization']:.1f}%."
        )


    elif selected_doctor_change > 0:

        doctor_addition = (
            selected_doctor_change
        )

        doctor_cost_value = (

            doctor_addition

            *

            doctor_monthly_cost
        )


        staffing_messages.append(

            f"Dokter: {doctors} → {selected_doctors}. "
            f"Tambahan biaya {rupiah(doctor_cost_value)}/bulan. "
            f"Utilisasi diproyeksikan menjadi "
            f"{best_resource_plan['Doctor Utilization']:.1f}%."
        )


    else:

        staffing_messages.append(

            f"Dokter tetap {doctors}. "
            "Simulasi tidak menunjukkan kebutuhan perubahan jumlah dokter."
        )


    # --------------------------------------------------------
    # NURSE PLAN
    # --------------------------------------------------------

    if selected_nurse_change < 0:

        nurse_reduction = abs(
            selected_nurse_change
        )

        nurse_saving_value = (

            nurse_reduction

            *

            nurse_monthly_cost
        )


        staffing_messages.append(

            f"Perawat: {nurses} → {selected_nurses}. "
            f"Potensi penghematan {rupiah(nurse_saving_value)}/bulan. "
            f"Utilisasi diproyeksikan menjadi "
            f"{best_resource_plan['Nurse Utilization']:.1f}%."
        )


    elif selected_nurse_change > 0:

        nurse_addition = (
            selected_nurse_change
        )

        nurse_cost_value = (

            nurse_addition

            *

            nurse_monthly_cost
        )


        staffing_messages.append(

            f"Perawat: {nurses} → {selected_nurses}. "
            f"Tambahan biaya {rupiah(nurse_cost_value)}/bulan. "
            f"Utilisasi diproyeksikan menjadi "
            f"{best_resource_plan['Nurse Utilization']:.1f}%."
        )


    else:

        staffing_messages.append(

            f"Perawat tetap {nurses}. "
            "Simulasi tidak menunjukkan kebutuhan perubahan jumlah perawat."
        )


    # --------------------------------------------------------
    # BED PLAN
    # --------------------------------------------------------

    if selected_bed_change > 0:

        bed_cost_value = (

            selected_bed_change

            *

            bed_addition_cost
        )


        staffing_messages.append(

            f"Bed: {total_beds} → {selected_beds}. "
            f"Tambahan biaya {rupiah(bed_cost_value)}. "
            f"Occupancy diproyeksikan "
            f"{best_resource_plan['Bed Occupancy']:.1f}%."
        )


    else:

        staffing_messages.append(

            f"Bed tetap {total_beds}. "
            "Tidak ada penambahan bed yang memberikan "
            "manfaat operasional cukup besar dalam simulasi."
        )


    for message in staffing_messages:

        st.write(
            f"• {message}"
        )


    # ========================================================
    # STAFF REDUCTION WARNING
    # ========================================================

    if (

        selected_doctor_change < 0

        or

        selected_nurse_change < 0

    ):

        st.warning(
            "Pengurangan pada planner adalah rekomendasi kapasitas "
            "berdasarkan simulasi."
        )


    # ========================================================
    # BUDGET CONSTRAINT INSIGHT
    # ========================================================

    st.subheader(
        "Budget Insight"
    )


    cheapest_new_staff = min(

        doctor_monthly_cost,

        nurse_monthly_cost
    )


    if monthly_budget < cheapest_new_staff:

        st.warning(

            f"Budget {rupiah(monthly_budget)} tidak cukup "
            "untuk menambah 1 dokter atau 1 perawat "
            "berdasarkan cost assumption saat ini. "
            "Planner memprioritaskan optimasi resource existing."
        )


    elif selected_cost > monthly_budget:

        st.warning(

            "Plan penambahan resource melebihi budget langsung. "
            "Penghematan dari resource underutilized diperlukan "
            "sebelum realokasi."
        )


    else:

        st.success(

            "Resource plan berada dalam batas budget model."
        )


    # ========================================================
    # GENERATE AI PLAN
    # ========================================================

    generate_plan = st.button(

        "GENERATE MANAGEMENT PLAN",

        use_container_width=True
    )


    if generate_plan:


        if not OPENROUTER_API_KEY:

            st.error(
                "OPENROUTER_API_KEY belum tersedia."
            )


        else:


            # =================================================
            # ACTION DESCRIPTION
            # =================================================

            if selected_doctor_change < 0:

                doctor_action = (

                    f"Kurangi kapasitas ekuivalen "
                    f"{abs(selected_doctor_change)} dokter"
                )


            elif selected_doctor_change > 0:

                doctor_action = (

                    f"Tambah "
                    f"{selected_doctor_change} dokter"
                )


            else:

                doctor_action = (

                    "Pertahankan jumlah dokter"
                )


            if selected_nurse_change < 0:

                nurse_action = (

                    f"Kurangi kapasitas ekuivalen "
                    f"{abs(selected_nurse_change)} perawat"
                )


            elif selected_nurse_change > 0:

                nurse_action = (

                    f"Tambah "
                    f"{selected_nurse_change} perawat"
                )


            else:

                nurse_action = (

                    "Pertahankan jumlah perawat"
                )


            if selected_bed_change > 0:

                bed_action = (

                    f"Tambah "
                    f"{selected_bed_change} bed"
                )


            else:

                bed_action = (

                    "Pertahankan jumlah bed"
                )


            # =================================================
            # AI PROMPT
            # =================================================

            ai_prompt = f"""
Anda adalah Hospital Resource Planning Assistant.

Anda BUKAN chatbot umum.

Tugas Anda hanya membuat insight manajemen yang SINGKAT,
NUMERIK, dan langsung berdasarkan hasil simulasi Python.

Jangan membuat angka baru.

Jangan mengubah angka hasil optimizer.

Jangan otomatis menyarankan tambah dokter,
perawat, atau bed.

Jika resource terlalu banyak,
jelaskan resource mana yang dapat dikurangi.

Pengurangan staf TIDAK boleh langsung disebut PHK.

Gunakan istilah:
- redistribusi
- penyesuaian shift
- pengurangan overtime
- natural attrition
- evaluasi kontrak
- pengurangan kapasitas ekuivalen

jika relevan.

PHK hanya boleh disebut sebagai opsi terakhir
dan bukan keputusan otomatis.

==================================================
CURRENT HOSPITAL
==================================================

Patients/day:
{adjusted_patients}

Doctors:
{doctors}

Nurses:
{nurses}

Beds:
{total_beds}

Doctor utilization:
{doctor_utilization:.2f}%

Nurse utilization:
{nurse_utilization:.2f}%

Bed occupancy:
{occupancy_rate:.2f}%

Average queue:
{average_queue:.2f}

Waiting time:
{average_waiting_time:.2f} minutes

Patients served:
{total_served}

==================================================
BUDGET
==================================================

Available budget:
{rupiah(monthly_budget)}

Doctor cost:
{rupiah(doctor_monthly_cost)} / month

Nurse cost:
{rupiah(nurse_monthly_cost)} / month

Bed cost:
{rupiah(bed_addition_cost)}

==================================================
PYTHON OPTIMIZER RESULT
==================================================

Doctor:
{doctors} -> {selected_doctors}

Doctor action:
{doctor_action}

Nurse:
{nurses} -> {selected_nurses}

Nurse action:
{nurse_action}

Bed:
{total_beds} -> {selected_beds}

Bed action:
{bed_action}

Additional cost:
{rupiah(selected_cost)}

Monthly saving:
{rupiah(selected_saving)}

Net budget impact:
{rupiah(selected_net_budget)}

==================================================
EXPECTED IMPACT
==================================================

Doctor utilization:
{doctor_utilization:.2f}%
->
{best_resource_plan["Doctor Utilization"]:.2f}%

Nurse utilization:
{nurse_utilization:.2f}%
->
{best_resource_plan["Nurse Utilization"]:.2f}%

Bed occupancy:
{occupancy_rate:.2f}%
->
{best_resource_plan["Bed Occupancy"]:.2f}%

Average queue:
{average_queue:.2f}
->
{best_resource_plan["Average Queue"]:.2f}

Waiting:
{average_waiting_time:.2f} minutes
->
{best_resource_plan["Waiting Time"]:.2f} minutes

Patients served:
{total_served}
->
{int(best_resource_plan["Patients Served"])}

==================================================
FORECAST
==================================================

Peak demand:
{peak_patients} patients

Peak date:
{peak_date.strftime("%d %B %Y")}

Doctor peak load:
{peak_doctor_load:.2f}%

Nurse peak load:
{peak_nurse_load:.2f}%

Surge risk:
{forecast_risk}

==================================================
INSTRUCTIONS
==================================================

Jawab HANYA dengan format berikut.

## 1. Bottleneck

Maksimal 3 bullet.

Sebutkan resource yang overload atau underutilized.
Gunakan angka utilisasi.

## 2. Resource Plan

Tulis tepat 3 bullet:

- Doctor:
- Nurse:
- Bed:

Gunakan hasil optimizer Python.

## 3. Budget Impact

Maksimal 3 bullet.

Sebutkan:
- additional cost
- monthly saving
- net budget impact

## 4. Operational Impact

Maksimal 4 bullet.

Bandingkan sebelum dan sesudah:
- utilization
- queue
- waiting
- patients served

## 5. Staffing Plan

Maksimal 4 bullet.

Jika dokter/perawat berlebih,
jelaskan pengurangan kapasitas dengan urutan:

1. redistribusi unit
2. penyesuaian shift
3. kurangi overtime
4. natural attrition / evaluasi kontrak

Jangan langsung menyarankan PHK.

Jika resource perlu ditambah,
sebutkan jumlah dan biaya.

## 6. Management Action

Maksimal 3 bullet.

Berikan langkah implementasi praktis.

Jangan menulis pembukaan.

Jangan menulis kesimpulan panjang.

Jangan memberikan teori.

Jangan memberikan disclaimer umum.

Jangan mengulang semua data.

Gunakan Bahasa Indonesia.

Jawaban harus ringkas seperti
decision-support dashboard,
bukan seperti percakapan ChatGPT.
"""


            # =================================================
            # CALL AI
            # =================================================

            try:

                with st.spinner(
                    "AI sedang menyusun management plan..."
                ):


                    response = requests.post(

                        "https://openrouter.ai/api/v1/chat/completions",

                        headers={

                            "Authorization":
                                f"Bearer {OPENROUTER_API_KEY}",

                            "Content-Type":
                                "application/json"
                        },


                        json={

                            "model":
                                "openrouter/free",

                            "messages": [

                                {

                                    "role":
                                        "system",

                                    "content":
                                        (
                                            "You are a concise hospital "
                                            "resource planning engine. "
                                            "Never invent numbers. "
                                            "Use only simulation results "
                                            "provided by the application."
                                        )
                                },

                                {

                                    "role":
                                        "user",

                                    "content":
                                        ai_prompt
                                }
                            ],

                            "temperature":
                                0.2
                        },


                        timeout=90
                    )


                if response.status_code == 200:


                    result = response.json()


                    ai_text = (

                        result[
                            "choices"
                        ][0][
                            "message"
                        ][
                            "content"
                        ]
                    )


                    st.session_state[
                        "ai_plan"
                    ] = ai_text


                else:


                    st.error(
                        "AI gagal membuat management plan."
                    )


                    st.code(
                        response.text
                    )


            except Exception as error:


                st.error(
                    "Terjadi kesalahan pada AI Planner."
                )


                st.code(
                    str(error)
                )


    # ========================================================
    # DISPLAY AI PLAN
    # ========================================================

    if st.session_state.ai_plan:


        st.divider()


        st.subheader(
            "AI Management Plan"
        )


        st.markdown(
            st.session_state.ai_plan
        )


# ============================================================
# REPORT
# ============================================================

with tab_report:

    st.header(
        "Hospital Planning Report"
    )

    report_data = pd.DataFrame(
        {
            "Indicator": [

                "Simulation Days",
                "Patients / Day",

                "Total Beds",
                "Occupied Beds",
                "Available Beds",

                "Occupancy Rate",

                "Doctors",
                "Nurses",

                "Doctor Utilization",
                "Nurse Utilization",

                "Current Queue",
                "Average Queue",
                "Maximum Queue",

                "Average Waiting",

                "Patients Served",

                "ICU Capacity",
                "ICU Used",

                "Available Budget",

                "Target Staff Utilization",

                "Forecast Average",
                "Forecast Peak",
                "Peak Date",
                "Surge Risk",

                "Hospital Status"
            ],

            "Result": [

                simulation_days,

                adjusted_patients,

                total_beds,

                current_occupied,

                available_beds,

                f"{occupancy_rate:.1f}%",

                doctors,

                nurses,

                f"{doctor_utilization:.1f}%",

                f"{nurse_utilization:.1f}%",

                current_queue,

                f"{average_queue:.1f}",

                maximum_queue,

                f"{average_waiting_time:.1f} min",

                total_served,

                icu_beds,

                icu_used,

                rupiah(
                    monthly_budget
                ),

                "70%",

                forecast_average,

                peak_patients,

                peak_date.strftime(
                    "%d %b %Y"
                ),

                forecast_risk,

                hospital_status
            ]
        }
    )

    st.subheader(
        "Simulation Summary"
    )

    st.dataframe(

        report_data,

        use_container_width=True,

        hide_index=True
    )

    st.subheader(
        "Forecast Summary"
    )

    st.line_chart(

        forecast_df
        .set_index("Date")[

            ["Predicted Patients"]
        ]
    )

    st.subheader(
        "Scenario Summary"
    )

    st.dataframe(

        display_scenario,

        use_container_width=True,

        hide_index=True
    )

    if st.session_state.ai_plan:

        st.subheader(
            "AI Management Plan"
        )

        st.markdown(
            st.session_state.ai_plan
        )

    st.subheader(
        "Download Simulation Data"
    )

    csv = (

        df.to_csv(
            index=False
        )

        .encode(
            "utf-8"
        )
    )

    st.download_button(

        "DOWNLOAD SIMULATION CSV",

        data=csv,

        file_name=
            "hospital_simulation.csv",

        mime=
            "text/csv",

        use_container_width=True
    )

    forecast_csv = (

        forecast_df.to_csv(
            index=False
        )

        .encode(
            "utf-8"
        )
    )

    st.download_button(

        "DOWNLOAD FORECAST CSV",

        data=forecast_csv,

        file_name=
            "patient_demand_forecast.csv",

        mime=
            "text/csv",

        use_container_width=True
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI-Assisted Hospital Capacity Simulation | "
    "Python + Streamlit + OpenRouter | "
    "Planning Prototype"
)