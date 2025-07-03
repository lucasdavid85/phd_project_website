import streamlit as st
import py3Dmol
import os
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network



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
st.image("Videos/MD_comparison.png", caption="DFR Organism MD simulation",)



# Load and display the SVG
svg_path = "Videos/V2.svg"

try:
    with open(svg_path, "r") as f:
        svg_content = f.read()

    # Embed SVG with scrollable container if it's large
    st.markdown("""
    <div style='overflow-x: auto; border:1px solid #ccc; padding:10px'>
    """ + svg_content + """
    </div>
    """, unsafe_allow_html=True)

except FileNotFoundError:
    st.error(f"SVG file not found at path: {svg_path}")

# Optional video section
st.header("Molecular dynamic simulation of Vitis vinifera DFR with DHQ substrate")
st.video("Videos/DFR_DHQ.mp4", start_time=0)


##################################################################################

# Graph to print 
st.set_page_config(layout="wide")
st.title("Interactive Network Viewer")

# Load GraphML file
graphml_path = "Videos/DHK_bounded_dhk_nph_neighborhood.graphml"
G = nx.read_graphml(graphml_path)

# Create PyVis Network
net = Network(height="750px", width="100%", bgcolor="#ffffff", font_color="black")
net.from_nx(G)

# Customize node: change DHK color
for node in net.nodes:
    if node["id"] == "DHK":
        node["color"] = "red"
        node["size"] = 30
        node["title"] = "Target Node: DHK"

# Enable physics and layout options
net.toggle_physics(True)
net.set_options("""
{
  "nodes": {
    "shape": "dot",
    "size": 15
  },
  "physics": {
    "enabled": true,
    "stabilization": { "iterations": 100 }
  }
}
""")


# Save and render
html_path = "/tmp/pyvis_graph.html"
net.write_html(html_path, notebook=False)

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

st.components.v1.html(html_content, height=750, scrolling=True)
##################################################################################
# Optional video section
st.header("Graph evolution across simulation")
st.video("Videos/graph_evolution.mp4", autoplay=True)
