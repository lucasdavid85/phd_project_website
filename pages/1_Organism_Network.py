import streamlit as st
import py3Dmol
import os

st.set_page_config(page_title="Organism Network", layout="wide")
st.title("Catalytic site of Vitis vinifera DFRs")

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

# === Display 3 Viewers in Columns ===
col1, col2, col3 = st.columns(3)

with col1:
    render_protein_viewer(
        pdb_path="Videos/Vitis_DHK.pdb",
        focus_resns=["DHK","NPH"],
        highlight_residues=[123, 124, 128, 133, 158, 162, 222],
        rotate_angles=(-220, -40, -160),
        title="Vitis vinifera DHK"
    )

with col2:
    render_protein_viewer(
        pdb_path="Videos/Vitis_DHQ.pdb",
        focus_resns=["DQH", "NPH"],
        highlight_residues=[123, 124, 128, 133, 158, 162, 222],
        rotate_angles=(90,-90, 20),
        title="Vitis vinifera DHQ"
    )

with col3:
    render_protein_viewer(
        pdb_path="Videos/Vitis_DHM.pdb",
        focus_resns=["DHM", "NPH"],
        highlight_residues=[125, 126, 130, 135, 160, 164, 224],
        rotate_angles=(90, 20, -130),
        title="Vitis vinifera DHM"
    )

st.markdown(""" 
### The three Vitis vinifera DFRs (DHK, DHQ, DHM) are shown in the 3D viewer.
- **DHK**: Dihydrokaempferol
- **DHQ**: Dihydroquercetin
- **DHM**: Dihydromyricetin
""")

st.markdown("""Molecular dynamics simulations were performed to study the interactions of these DFRs with the substrate NPH (Naringenin).
            
         """)
st.image("Videos/TIGHT_resMDVvZm_PUBLICATION.png", caption="DFR Organism MD simulation",)








# Optional video section
st.header("Video")
st.video("Videos/graph_evolution.mp4", autoplay=True)
