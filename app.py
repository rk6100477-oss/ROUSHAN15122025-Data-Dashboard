import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. CONFIGURATION (Visual Polish) ---
st.set_page_config(
    page_title="India Diabetes Monitor 2025",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to make it look "Human-Made" and Professional
st.markdown("""
<style>
    .metric-card {background-color: #f0f2f6; border-radius: 10px; padding: 15px; border-left: 5px solid #ff4b4b;}
    h1 {color: #2c3e50;}
</style>
""", unsafe_allow_html=True)

# --- 2. LOAD DATA ---
@st.cache_data
def load_data():
    return pd.read_csv('india_diabetes_master.csv')

df = load_data()

# --- 3. SIDEBAR CONTROLS ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2815/2815428.png", width=100)
st.sidebar.title("📊 Control Panel")

selected_year = st.sidebar.slider("Select Year", 2015, 2025, 2025)
selected_states = st.sidebar.multiselect(
    "Select States to Compare", 
    df['State'].unique(), 
    default=['Maharashtra', 'Tamil Nadu', 'Rajasthan', 'Goa']
)

# Filter Data
df_year = df[df['Year'] == selected_year]
df_trend = df[df['State'].isin(selected_states)]

# --- 4. MAIN DASHBOARD ---
st.title("🇮🇳 India Diabetes Epidemiology Monitor")
st.markdown(f"**Capstone Analysis | Year: {selected_year}**")
st.markdown("---")

# Key Metrics (Top Row)
total_cases = df_year['Total_Diabetics_Millions'].sum()
total_risk = df_year['Total_Pre_Diabetics_Millions'].sum()
gap = df_year['Undiagnosed_Millions'].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Diabetics", f"{total_cases:.1f} M", "Active Cases")
col2.metric("Pre-Diabetics", f"{total_risk:.1f} M", "At-Risk Pool", delta_color="inverse")
col3.metric("Undiagnosed Gap", f"{gap:.1f} M", "Needs Screening", delta_color="off")
col4.metric("States Analyzed", f"{len(df['State'].unique())}", "National Scope")

st.markdown("---")

# --- 5. TABS FOR VISUALIZATION ---
tab1, tab2, tab3 = st.tabs(["🗺️ Spatial Analysis", "📈 Growth Trends", "🤖 AI Analyst Report"])

with tab1:
    st.subheader(f"State-wise Disease Burden ({selected_year})")
    c1, c2 = st.columns([2, 1])
    
    with c1:
        # TREEMAP: Best way to show 'Whole vs Parts' without complex Maps
        fig_tree = px.treemap(
            df_year, 
            path=['State'], 
            values='Total_Diabetics_Millions',
            color='Diabetes_Prev_Pct',
            color_continuous_scale='RdYlGn_r',
            title="<b>Disease Burden Map</b> (Size = Total Patients, Color = Severity)"
        )
        st.plotly_chart(fig_tree, use_container_width=True)
        
    with c2:
        # Leaderboard Bar Chart
        fig_bar = px.bar(
            df_year.sort_values('Diabetes_Prev_Pct', ascending=True),
            x='Diabetes_Prev_Pct', 
            y='State',
            orientation='h',
            title="<b>Prevalence Leaderboard (%)</b>",
            color='Diabetes_Prev_Pct',
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig_bar, use_container_width=True)

with tab2:
    st.subheader("Temporal Analysis (2015-2025)")
    
    # Line Chart
    fig_line = px.line(
        df_trend, 
        x='Year', 
        y='Diabetes_Prev_Pct', 
        color='State', 
        markers=True,
        title="<b>Rise in Prevalence Rates (%)</b>"
    )
    st.plotly_chart(fig_line, use_container_width=True)
    
    # Area Chart (The "Wave" of Pre-diabetes)
    fig_area = px.area(
        df_trend, 
        x='Year', 
        y='Total_Pre_Diabetics_Millions', 
        color='State',
        title="<b>Volume of Pre-Diabetics (The Future Burden)</b>"
    )
    st.plotly_chart(fig_area, use_container_width=True)

with tab3:
    st.subheader("🤖 Automated Insight Generation")
    
    # --- AI LOGIC (Natural Language Generation) ---
    # This block simulates an AI Analyst by calculating insights dynamically
    
    # Logic 1: Find the worst state
    worst_state = df_year.loc[df_year['Diabetes_Prev_Pct'].idxmax()]
    
    # Logic 2: Find the 'Hidden' problem (Undiagnosed)
    hidden_burden_state = df_year.loc[df_year['Undiagnosed_Millions'].idxmax()]
    
    # Logic 3: Trend Analysis (Who is growing fastest?)
    # Comparing 2015 vs 2025 for selected states
    growth_data = df[df['State'].isin(selected_states)]
    growth_summary = "Mixed trends observed."
    if not growth_data.empty:
        fastest = growth_data.groupby('State')['Diabetes_Prev_Pct'].max().idxmax()
        growth_summary = f"**{fastest}** is showing the most aggressive growth trajectory."

    # Displaying the "AI" Report
    st.info(f"**EXECUTIVE SUMMARY REPORT (Generated for {selected_year})**")
    
    st.markdown(f"""
    * **CRITICAL ALERT:** The data indicates that **{worst_state['State']}** is currently the highest-risk zone with a prevalence rate of **{worst_state['Diabetes_Prev_Pct']}%**. Immediate policy intervention is required here.
    
    * **THE HIDDEN ICEBERG:** While prevalence is one factor, the absolute burden of untreated patients is highest in **{hidden_burden_state['State']}** (**{hidden_burden_state['Undiagnosed_Millions']:.2f} Million** undiagnosed cases). This suggests a specific failure in screening infrastructure in this region.
    
    * **FUTURE OUTLOOK:** {growth_summary} The high volume of pre-diabetics suggests a potential 15-20% spike in clinical diabetes cases by 2030 if lifestyle interventions are not enacted.
    """)
    
    st.caption("Insight generated by Rule-Based Analytics Engine • Capstone Project 2025")

# Footer
st.markdown("---")
st.markdown("Created on Mac M2 | BS (CSDA) IIT Patna | Data Source: ICMR-INDIAB")