import streamlit as st
from winning_wdc import get_drivers_standings
import fastf1

# Activer le cache FastF1 pour Streamlit
fastf1.Cache.enable_cache('/tmp/fastf1_cache')

st.title("🏎️ F1 Championship Title Checker")

year = st.number_input("Enter season year:", min_value=1950, max_value=2025, value=2023)
round_number = st.number_input("Enter round number:", min_value=1, max_value=25, value=1)

if st.button("Check Standings"):
    with st.spinner("Loading data, please wait... ⏳"):
        results = get_drivers_standings(year, round_number)
    st.success("Done! ✅")
    st.write(results)
