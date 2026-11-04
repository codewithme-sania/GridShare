
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------
# GRIDSHARE - SOLAR EV CHARGING SIMULATION
# Initial dashboard with illustrative demo data
# --------------------------------------------------

st.set_page_config(
    page_title="GridShare | Smart EV Charging",
    page_icon="⚡",
    layout="wide"
)

# Professional styling
st.markdown("""
<style>
    .main {
        background-color: #f5f8fc;
    }
    .block-container {
        padding-top: 1.5rem;
    }
    .metric-card {
        background: white;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #e5eaf0;
    }
    h1, h2, h3 {
        color: #12304a;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# DEMO DATA
# Replace this section with Member 1's actual output
# --------------------------------------------------

@st.cache_data
def create_demo_data():

    rng = np.random.default_rng(42)

    days = pd.date_range("2026-10-20", periods=10)

    stations = ["Station 1", "Station 2", "Station 3"]

    scenarios = [
        "Normal Demand",
        "High Demand",
        "Low Solar",
        "High Solar"
    ]

    records = []

    for scenario in scenarios:
        for day_number, day in enumerate(days):

            for station in stations:

                demand = rng.uniform(100, 180)

                solar_factor = {
                    "Normal Demand": 0.65,
                    "High Demand": 0.50,
                    "Low Solar": 0.30,
                    "High Solar": 0.90
                }[scenario]

                solar = demand * solar_factor * rng.uniform(0.8, 1.2)

                solar_used = min(demand, solar)

                grid = max(0, demand - solar_used)

                records.append({
                    "Date": day,
                    "Day": day_number + 1,
                    "Scenario": scenario,
                    "Station": station,
                    "Demand_kWh": round(demand, 2),
                    "Solar_kWh": round(solar, 2),
                    "Solar_Used_kWh": round(solar_used, 2),
                    "Grid_kWh": round(grid, 2)
                })

    return pd.DataFrame(records)


df = create_demo_data()


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("⚡ GridShare")
st.subheader("Intelligent Solar Energy Sharing for EV Charging")

st.markdown(
    "A software-based simulation of solar-powered EV charging "
    "across three interconnected charging stations."
)

st.warning(
    "DEMO MODE: These are illustrative sample values, "
    "not validated hackathon simulation results."
)

st.divider()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("⚡ GridShare")
st.sidebar.caption("Smart Solar EV Charging")

selected_scenario = st.sidebar.selectbox(
    "Select Simulation Scenario",
    [
        "Normal Demand",
        "High Demand",
        "Low Solar",
        "High Solar"
    ]
)

scenario_df = df[df["Scenario"] == selected_scenario].copy()

st.sidebar.divider()
st.sidebar.info("3 Charging Stations | 10 Simulation Days")
st.sidebar.caption("PS-09 Hackathon Project")


# --------------------------------------------------
# TABS
# --------------------------------------------------

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 Overview",
    "🔌 Stations",
    "☀️ Solar Sharing",
    "📊 Baselines",
    "📅 10-Day Analysis",
    "🧪 Scenarios"
])


# --------------------------------------------------
# TAB 1: OVERVIEW
# --------------------------------------------------

with tab1:

    st.header("Dashboard Overview")

    total_demand = scenario_df["Demand_kWh"].sum()
    total_solar = scenario_df["Solar_Used_kWh"].sum()
    total_grid = scenario_df["Grid_kWh"].sum()

    solar_share = (
        total_solar / total_demand * 100
        if total_demand > 0 else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total EV Demand",
        f"{total_demand:,.1f} kWh"
    )

    col2.metric(
        "Solar Energy Used",
        f"{total_solar:,.1f} kWh"
    )

    col3.metric(
        "Grid Energy",
        f"{total_grid:,.1f} kWh"
    )

    col4.metric(
        "Solar Share",
        f"{solar_share:.1f}%"
    )

    st.divider()

    st.subheader("Energy Distribution")

    energy_df = pd.DataFrame({
        "Energy Source": ["Solar Energy Used", "Grid Energy"],
        "Energy (kWh)": [total_solar, total_grid]
    })

    fig = px.pie(
        energy_df,
        names="Energy Source",
        values="Energy (kWh)",
        hole=0.55,
        title="Solar vs Grid Energy"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Station-wise Charging Demand")

    station_demand = (
        scenario_df.groupby("Station")["Demand_kWh"]
        .sum()
        .reset_index()
    )

    fig2 = px.bar(
        station_demand,
        x="Station",
        y="Demand_kWh",
        color="Station",
        title="Total EV Charging Demand by Station",
        labels={"Demand_kWh": "Demand (kWh)"}
    )

    st.plotly_chart(fig2, use_container_width=True)


# --------------------------------------------------
# TAB 2: STATIONS
# --------------------------------------------------

with tab2:

    st.header("Three Charging Stations")

    cols = st.columns(3)

    for i, station in enumerate(
        ["Station 1", "Station 2", "Station 3"]
    ):

        station_data = scenario_df[
            scenario_df["Station"] == station
        ]

        demand = station_data["Demand_kWh"].sum()
        solar = station_data["Solar_Used_kWh"].sum()
        grid = station_data["Grid_kWh"].sum()

        with cols[i]:

            st.subheader(f"🔌 {station}")

            st.metric("Charging Demand", f"{demand:.1f} kWh")

            st.metric("Solar Used", f"{solar:.1f} kWh")

            st.metric("Grid Used", f"{grid:.1f} kWh")

            share = solar / demand * 100 if demand else 0

            st.progress(int(min(100, share)))

            st.caption(f"Solar contribution: {share:.1f}%")

    st.divider()

    st.subheader("Station Energy Comparison")

    fig = px.bar(
        scenario_df,
        x="Station",
        y=["Solar_Used_kWh", "Grid_kWh"],
        barmode="stack",
        title="Solar and Grid Energy by Station"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Station Data")

    st.dataframe(
        scenario_df[
            [
                "Date",
                "Station",
                "Demand_kWh",
                "Solar_Used_kWh",
                "Grid_kWh"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# TAB 3: SOLAR SHARING
# --------------------------------------------------

with tab3:

    st.header("☀️ Solar Energy Sharing")

    st.write(
        "This section shows how available solar energy "
        "contributes to EV charging demand across all stations."
    )

    total_demand = scenario_df["Demand_kWh"].sum()
    solar_used = scenario_df["Solar_Used_kWh"].sum()

    solar_share = (
        solar_used / total_demand * 100
        if total_demand else 0
    )

    col1, col2 = st.columns(2)

    col1.metric("Solar Energy Utilization", f"{solar_used:.1f} kWh")

    col2.metric("Solar Share of EV Demand", f"{solar_share:.2f}%")

    daily_solar = (
        scenario_df.groupby("Day")[
            ["Solar_Used_kWh", "Grid_kWh"]
        ]
        .sum()
        .reset_index()
    )

    fig = px.area(
        daily_solar,
        x="Day",
        y=["Solar_Used_kWh", "Grid_kWh"],
        title="Daily Solar and Grid Energy Usage",
        labels={
            "Day": "Simulation Day",
            "value": "Energy (kWh)"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Solar Share by Station")

    station_share = (
        scenario_df.groupby("Station")[
            ["Demand_kWh", "Solar_Used_kWh"]
        ]
        .sum()
        .reset_index()
    )

    station_share["Solar Share (%)"] = (
        station_share["Solar_Used_kWh"]
        / station_share["Demand_kWh"] * 100
    )

    fig = px.bar(
        station_share,
        x="Station",
        y="Solar Share (%)",
        color="Station",
        title="Solar Contribution at Each Station"
    )

    st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------
# TAB 4: BASELINE COMPARISON
# --------------------------------------------------

with tab4:

    st.header("📊 Baseline Comparison")

    st.write(
        "Compare GridShare with three illustrative energy "
        "management approaches. Confirm these definitions "
        "with Member 1 before using the final results."
    )

    demand = scenario_df["Demand_kWh"].sum()
    solar = scenario_df["Solar_Used_kWh"].sum()

    # Illustrative comparison only
    comparison = pd.DataFrame({
        "Method": [
            "Grid Only",
            "Independent Solar",
            "GridShare"
        ],
        "Solar Used (kWh)": [
            0,
            solar * 0.65,
            solar
        ],
        "Grid Used (kWh)": [
            demand,
            demand - solar * 0.65,
            demand - solar
        ]
    })

    st.dataframe(
        comparison.round(2),
        use_container_width=True,
        hide_index=True
    )

    fig = px.bar(
        comparison,
        x="Method",
        y=["Solar Used (kWh)", "Grid Used (kWh)"],
        barmode="stack",
        title="Energy Source Comparison"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "Baseline values are placeholders. Replace them with "
        "the actual two additional baseline calculations "
        "from Member 1's simulation."
    )


# --------------------------------------------------
# TAB 5: 10-DAY ANALYSIS
# --------------------------------------------------

with tab5:

    st.header("📅 Ten-Day Performance Analysis")

    daily = (
        scenario_df.groupby("Day")[
            [
                "Demand_kWh",
                "Solar_Used_kWh",
                "Grid_kWh"
            ]
        ]
        .sum()
        .reset_index()
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average Daily Demand",
        f"{daily['Demand_kWh'].mean():.2f} kWh"
    )

    col2.metric(
        "Average Daily Solar",
        f"{daily['Solar_Used_kWh'].mean():.2f} kWh"
    )

    col3.metric(
        "Average Daily Grid",
        f"{daily['Grid_kWh'].mean():.2f} kWh"
    )

    st.divider()

    fig = px.line(
        daily,
        x="Day",
        y=[
            "Demand_kWh",
            "Solar_Used_kWh",
            "Grid_kWh"
        ],
        markers=True,
        title="10-Day Energy Performance",
        labels={
            "Day": "Simulation Day",
            "value": "Energy (kWh)"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Daily Results Table")

    st.dataframe(
        daily.round(2),
        use_container_width=True,
        hide_index=True
    )

    st.subheader("10-Day Average Results")

    averages = daily[
        ["Demand_kWh", "Solar_Used_kWh", "Grid_kWh"]
    ].mean().to_frame("Daily Average (kWh)")

    st.dataframe(
        averages.round(2),
        use_container_width=True
    )

    csv = daily.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download 10-Day Results",
        data=csv,
        file_name="gridshare_10_day_results.csv",
        mime="text/csv"
    )


# --------------------------------------------------
# TAB 6: SCENARIO TESTING
# --------------------------------------------------

with tab6:

    st.header("🧪 Simulation Scenario Testing")

    st.write("Explore the four simulation scenarios.")

    scenario_results = (
        df.groupby("Scenario")[
            [
                "Demand_kWh",
                "Solar_Used_kWh",
                "Grid_kWh"
            ]
        ]
        .sum()
        .reset_index()
    )

    scenario_results["Solar Share (%)"] = (
        scenario_results["Solar_Used_kWh"]
        / scenario_results["Demand_kWh"] * 100
    )

    fig = px.bar(
        scenario_results,
        x="Scenario",
        y="Solar Share (%)",
        color="Scenario",
        title="Solar Share Across Four Scenarios"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Scenario Results")

    st.dataframe(
        scenario_results.round(2),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("Selected Scenario Details")

    selected_data = df[
        df["Scenario"] == selected_scenario
    ]

    st.write(f"Current scenario: **{selected_scenario}**")

    st.dataframe(
        selected_data,
        use_container_width=True,
        hide_index=True
    )

    csv = scenario_results.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download Scenario Results",
        data=csv,
        file_name="gridshare_scenario_results.csv",
        mime="text/csv"
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown("""
<center>
    <b>GRIDSHARE | PS-09 HACKATHON</b><br>
    Intelligent Solar Energy Sharing for EV Charging<br>
    <small>Initial Simulation Dashboard</small>
</center>
""", unsafe_allow_html=True)
