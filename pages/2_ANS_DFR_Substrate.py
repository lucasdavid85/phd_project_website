import streamlit as st
import py3Dmol
import os
from PIL import Image

# === Protein viewer function ===
def render_protein_viewer(pdb_path, focus_resns, highlight_residues, rotate_angles, title,
                          width=1200, height=800):
    if not os.path.exists(pdb_path):
        st.error(f"PDB file not found: {pdb_path}")
        return

    with open(pdb_path, "r") as f:
        pdb_data = f.read()

    st.subheader(title)
    view = py3Dmol.view(width=width, height=height)
    view.addModel(pdb_data, "pdb")

    # Base white cartoon style
    view.setStyle({'cartoon': {'color': 'white'}})

    # ✅ Color chain F in lightgreen (DFR)
    view.setStyle({'chain': 'F'}, {'cartoon': {'color': 'lightgreen'}})

    # ✅ Color chain D in skyblue (ANS)
    view.setStyle({'chain': 'D'}, {'cartoon': {'color': 'skyblue'}})

    # Optional: Highlight specific residues
    for resid in highlight_residues:
        view.setStyle({'resi': str(resid)}, {'stick': {'colorscheme': 'default'}})

    # Rotate orientation
    view.rotate(rotate_angles[0], 'x')
    view.rotate(rotate_angles[1], 'y')
    view.rotate(rotate_angles[2], 'z')

    # Optional: zoom to specific regions
    view.zoomTo({'or': [{'resi': list(range(1, 351))}, {'resi': list(range(351, 371))}]})
    view.zoom(0.8)
    view.setBackgroundColor('white')

    # Render the viewer
    st.components.v1.html(view._make_html(), height=height + 100, scrolling=True)

# === Streamlit app layout ===
st.set_page_config(page_title="ANS DFR Interaction", layout="wide")
st.title("ANS DFR Protein Interaction in Substrate Specificity")

st.markdown("""
**Aim of the study**: Does the protein–protein interaction influence the substrate specificity of DFR?
""")

st.markdown("""
Anthocyanidin synthase (ANS) is the enzyme that follows dihydroflavonol reductase (DFR) in the flavonoid biosynthetic pathway.  
ANS converts the products of DFR — leucoanthocyanidins — into anthocyanins, which contribute to red, purple, and blue pigmentation in plants.
""")

st.image("Videos/ANS.png", caption="ANS enzyme")

st.markdown("""
The catalytic site of ANS includes an iron atom coordinated by two histidines (HIS), an aspartate (ASP), and a 2-oxoglutarate (2OG) cofactor.  
Below is a structural visualization of the ANS catalytic site.
""")

st.image("Videos/ANS_cata.png", caption="ANS catalytic site")

# === Section: ANS–DFR Interaction ===
st.header("ANS–DFR Interaction")

st.image("Videos/compressed.gif", caption="ANS DFR interaction")

# === 3D View: ANS catalytic site ===
render_protein_viewer(
    pdb_path="Videos/AF_model.pdb",
    focus_resns=["AP1", "FE1"],
    highlight_residues=[289, 233, 235, 353],
    rotate_angles=(-220, -40, -160),
    title="ANS catalytic site"
)

# === 3D View: ANS–DFR complex (LZerD model) ===
render_protein_viewer(
    pdb_path="Videos/LZerD_Model.pdb",
    focus_resns=["HIS"],  # Optional
    highlight_residues=[289, 233, 235, 353],  # Optional
    rotate_angles=(-220, -40, -160),
    title="ANS DFR interaction using LZerD model",
    width=1400,
    height=800
)
