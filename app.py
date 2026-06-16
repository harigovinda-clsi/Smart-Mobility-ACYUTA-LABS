# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="OneJourney AI - Mobility Equity",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional aesthetic and visible metrics
st.markdown("""
<style>
    :root {
        --primary-color: #0a2463;    /* Deep Navy */
        --secondary-color: #247ba0;  /* Teal */
        --success-color: #06d6a0;    /* Green */
        --warning-color: #f18f01;    /* Orange */
        --danger-color: #c1121f;     /* Red */
        --bg-light: #f5f5f5;         /* Light Gray */
    }
    
    .main {
        background-color: white;
    }
    
    /* Base card container styling */
    .stMetric {
        background-color: var(--bg-light) !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        border-left: 4px solid var(--secondary-color) !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    }

    /* FIX: Force labels (e.g., "Collapse Risk") to be visible dark charcoal */
    [data-testid="stMetricLabel"] p {
        color: #1A1A1A !important;
        font-weight: 500 !important;
    }

    /* FIX: Force metric values (numbers) to be solid black */
    [data-testid="stMetricValue"] > div {
        color: #000000 !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if "city" not in st.session_state:
    st.session_state.city = SyntheticCity(num_zones=12)
