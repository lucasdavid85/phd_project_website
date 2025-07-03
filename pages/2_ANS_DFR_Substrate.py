import streamlit as st
import py3Dmol
import os
from PIL import Image
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

    # Default white cartoon
    view.setStyle({'cartoon': {'color': 'white'}})

    # 🟦 Color ANS residues 1–350 in blue
    view.setStyle({'resi': list(range(1, 351))}, {'cartoon': {'color': 'skyblue'}})

    # 🟥 Color DFR residues 351–370 in red
    view.setStyle({'resi': list(range(351, 371))}, {'cartoon': {'color': 'lightcoral'}})

    # Highlight specific residues (optional)
    for resid in highlight_residues:
        view.setStyle({'resi': str(resid)}, {'stick': {'colorscheme': 'default'}})

    # Orientation
    view.rotate(rotate_angles[0], 'x')
    view.rotate(rotate_angles[1], 'y')
    view.rotate(rotate_angles[2], 'z')

    # Zoom on both regions: ANS and DFR
    view.zoomTo({'or': [{'resi': list(range(1, 351))}, {'resi': list(range(351, 371))}]})
    view.zoom(0.8)
    view.setBackgroundColor('white')

    st.components.v1.html(view._make_html(), height=height + 100, scrolling=True)



st.set_page_config(page_title="ANS DFR Interaction", layout="wide")
st.title("ANS DFR Protein Interaction in Substrate Specificity")
st.markdown("""
            Aim of the study : Does the protein protein interaction influence the substrate specificity of DFR?
            """)

st.markdown("""
  Anthocyanidin synthase (ANS) is the following enzyme in the flavonoid biosynthetic pathway after dihydroflavonol reductase (DFR).
            ANS transforms the DFR product, leucoanthocyanidins, into anthocyanins, leucopelargonidins and leucodelphinidins into anthocyanins,
             which are responsible for the red, purple, and blue colors in many plants.
            """)

st.image("Videos/ANS.png", caption="ANS enzyme")


st.markdown("""
            The catalytic site of ANS is composed with an iron atom with two histidine residues (HIS) with an aspartate residue (ASP) and a cofactor 2-oxoglutarate (2OG).
            Here is a visualization of the ANS catalytic site with the iron atom and the 2OG cofactor.
            """)
st.image("Videos/ANS_cata.png", caption="ANS catalytic site")

# === Display 3 Viewers in Columns ===

st.header("ANS DFR Interaction")
st.image("Videos/compressed.gif", caption="ANS DFR interaction")


image = Image.open("Videos/compressed.gif")
resized = image.resize((800, 600))  # Width x Height in pixels
st.image(resized, caption="ANS DFR interaction")

render_protein_viewer(
    pdb_path="Videos/AF_model.pdb",
    focus_resns=["AP1"],
    highlight_residues=[289,233,235],
    rotate_angles=(-220, -40, -160),
    title="ANS cataytic site")
    

# st.image("Videos/ANS_DFR_interaction.png", caption="ANS DFR interaction")

render_protein_viewer(
    pdb_path="Videos/LZerD_Model.pdb",
    focus_resns=["HIS"],  # Not needed here
    highlight_residues=[289, 233, 235],  # Optional
    rotate_angles=(-220, -40, -160),
    title="ANS DFR interaction using LZerD model",
    width=1400,
    height=800
)


# st.title("Protein protein docking protocols")



# st.title("Substrate channelling from DFR to ANS")
