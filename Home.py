import streamlit as st

st.set_page_config(page_title="Thesis Portal", layout="wide")

st.title("Welcome to the Thesis Data Portal")

st.markdown("### Select a topic:")
st.page_link("pages/1_Organism_Network.py", label="1. Organisms and network protein interaction", icon="🧬")
st.page_link("pages/2_ANS_DFR_Substrate.py", label="2. ANS DFR protein interaction in substrate specificity", icon="🔬")
# if st.button("Go to ANS DFR Interaction"):
#     st.switch_page("2_ANS_DFR_Substrate.py")

st.page_link("pages/3_Metabolite_Influence.py", label="3. Presence of metabolites can perturb substrate specificity", icon="🧪")
