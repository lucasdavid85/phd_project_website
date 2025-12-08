import streamlit as st
import py3Dmol
import os
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
from io import StringIO


import pandas as pd
import imageio.v2 as imageio
from io import BytesIO

from io import StringIO, BytesIO


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



col4, col5, col6 = st.columns(3)

with col4:
    st.image("Videos/ligand_animation_DHK.gif", caption="ORCA quantum calculation of DHK ligand cycle B rotation")

with col5:
    st.image("Videos/ligand_animation_DHQ.gif", caption="ORCA quantum calculation of DHQ ligand cycle B rotation")

with col6:
    st.image("Videos/ligand_animation_DHM.gif", caption="ORCA quantum calculation of DHM ligand cycle B rotation")


##################################################################################

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import imageio.v2 as imageio
from io import StringIO, BytesIO

# ---------- RAW DATA ----------
DATA = """Angle DHK DHQ DHM
-180 1,144716292 1,167752184 1,722496125
-170 1,038353347 1,108414839 1,609782779
-160 0,9508596278 1,065323727 1,464351061
-150 0.8067205809 0,9784826181 0,9814130899
-140 0,6138051816 0,8102471872 0,9876819148
-130 0,3897715613 0,5995042288 0,687060699
-120 0,2053149968 0,4186244713 0,4107743212
-110 0,1053903044 0,2767695606 0,1862073174
-100 0,09393197186 0,2365398946 0,04681224604
-90 0,1659889452 0,3118975704 0
-80 0,361075529 0,4998242652 0,06858056801
-70 0,7046435292 0,8463478375 0,2618975736
-60 1,193674622 1,291980339 0,5726907264
-50 1,680936137 1,750922328 0,9035579241
-40 1,939727536 2,001882402 1,083320714
-30 1,945506904 2,017250122 1,111564939
-20 1,768825188 1,916773221 1,053790093
-10 1,555114107 1,757467257 0,9942456694
0 1,359845545 1,600119125 0,9716113836
10 1,219622161 1,449792829 0,9826618347
20 1,103294357 1,288227829 1,003965799
30 0,9469251402 1,094270763 0,940888494
40 0,7022276157 0,7934550195 0,802955521
50 0,4091616204 0,4688378215 0,6266816868
60 0,1537838756 0,1953689634 0,4473895297
70 0,008778864802 0,02084588219 0,2825489278
80 0 0 0,2545808071
90 0,09864457192 0,1027673127 0,3687499764
100 0,3195531924 0,3145833132 0,600778074
110 0,6405559329 0,6213102013 0,9259788565
120 1,048795113 1,002591552 1,318712265
130 1,468498902 1,394458997 1,712430864
140 1,746573683 1,641396732 1,998801328
150 1,74761535 1,666409281 2,080233301
160 1,557561396 1,503721038 1,983521459
170 1,319565679 1,307843792 1,84393186
180 1,144716292 1,167752184 1,722496125
"""

# ---------- LOAD DATA ----------
@st.cache_data
def load_data():
    # Convert commas to dots so pandas can parse floats
    text = DATA.replace(",", ".")
    df = pd.read_csv(StringIO(text), sep=r"\s+")
    return df

# ---------- BUILD GIF ----------
@st.cache_data
def make_curve_gif(df, duration=5, extra_final_frames=8):
    frames = []

    angles = df["Angle"]
    dhk = df["DHK"]
    dhq = df["DHQ"]
    dhm = df["DHM"]

    # Fix axis limits so points don't move between frames
    x_min, x_max = angles.min(), angles.max()
    y_min = min(dhk.min(), dhq.min(), dhm.min())
    y_max = max(dhk.max(), dhq.max(), dhm.max())
    # Small margin
    y_margin = 0.05 * (y_max - y_min)
    y_min -= y_margin
    y_max += y_margin

    for i in range(1, len(df) + 1):
        fig, ax = plt.subplots(figsize=(5, 4))

        # Plot curves up to step i (progressive drawing)
        ax.plot(angles[:i], dhk[:i], label="DHK")
        ax.plot(angles[:i], dhq[:i], label="DHQ")
        ax.plot(angles[:i], dhm[:i], label="DHM")

        # Fixed axes
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)

        # Show axes + labels
        ax.set_xlabel("Angle (°)")
        ax.set_ylabel("Energy (kcal/mol)")
        ax.set_title("Energy vs Angle")
        ax.legend()
        ax.grid(True)

        buf = BytesIO()
        fig.savefig(
            buf,
            format="png",
            bbox_inches="tight",
            pad_inches=0.1,
        )
        plt.close(fig)
        buf.seek(0)
        frames.append(imageio.imread(buf))

    # Hold the final frame for a bit longer (pause at end)
    for _ in range(extra_final_frames):
        frames.append(frames[-1])

    gif_bytes = BytesIO()
    imageio.mimsave(gif_bytes, frames, format="GIF", duration=duration, loop=0)
    gif_bytes.seek(0)
    return gif_bytes

# ---------- STREAMLIT APP ----------
st.title("Energy vs Angle – automatic curve drawing")

df = load_data()
gif = make_curve_gif(df, duration=3, extra_final_frames=8)

# Center the figure on the page
left, center, right = st.columns([1, 2, 1])
with center:
    st.image(gif, use_column_width=True)







######################################################################################
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
st.video("Videos/graph_evolution.mp4",start_time=0)
