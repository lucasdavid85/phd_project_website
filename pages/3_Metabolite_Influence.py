import streamlit as st
import py3Dmol
import os

st.set_page_config(page_title="ANS DFR Interaction", layout="wide")
st.title("Influence of flavonoid metabolite high concentration on DFR substrate specificity")
st.markdown("""
            Aim of the study : Does a high concentration of metabolites may have an influence the substrate specificity of DFR?
            """)
st.title("Protein protein docking methods")

st.video("Videos/DFR_metabolites.mp4", autoplay=True)