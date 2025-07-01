import streamlit as st
import py3Dmol
import os


def render_protein_viewer(pdb_path, focus_resns, highlight_residues, rotate_angles, title):
    if not os.path.exists(pdb_path):
        st.error(f"PDB file not found: {pdb_path}")
        return

    with open(pdb_path, "r") as f:
        pdb_data = f.read()

    st.subheader(title)
    view = py3Dmol.view(width=350, height=500)
    view.addModel(pdb_data, "pdb")
    view.setStyle({'cartoon': {'color': 'white'}})

    # Highlight resn-specific regions
    for resn, color in zip(focus_resns, ['greenCarbon', 'blueCarbon']):
        view.setStyle({'resn': resn}, {'stick': {'colorscheme': color}})
        view.addLabel(resn, {
            'position': {'resn': resn},
            'backgroundColor': 'white',
            'fontColor': 'black',
            'fontSize': 12
        })

    # Highlight residues
    for resid in highlight_residues:
        view.setStyle({'resi': str(resid)}, {'stick': {'colorscheme': 'default'}})
        view.addLabel(f"{resid}", {
            'position': {'resi': str(resid)},
            'backgroundColor': 'white',
            'fontColor': 'red',
            'fontSize': 10
        })

    # Orientation
    view.rotate(rotate_angles[0], 'x')
    view.rotate(rotate_angles[1], 'y')
    view.rotate(rotate_angles[2], 'z')
    view.zoomTo({'or': [{'resn': r} for r in focus_resns] })
    view.zoom(0.6)
    view.setBackgroundColor('white')
    st.components.v1.html(view._make_html(), height=700, scrolling=True)




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



render_protein_viewer(
    pdb_path="Videos/AF_model.pdb",
    focus_resns=["FE"],
    highlight_residues=[289,233,235],
    rotate_angles=(-220, -40, -160),
    title="ANS cataytic site")
    

st.image("Videos/ANS_DFR_interaction.png", caption="ANS DFR interaction")

render_protein_viewer(
    pdb_path="Videos/LZerD_Model.pdb",
    # focus_resns=["FE"],
    # highlight_residues=[289,233,235],
    rotate_angles=(-220, -40, -160),
    title="ANS DFR interaction using LZerD model")
    


# st.title("Protein protein docking protocols")



# st.title("Substrate channelling from DFR to ANS")
