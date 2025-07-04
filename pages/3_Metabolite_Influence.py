import streamlit as st
import py3Dmol
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import defaultdict

st.set_page_config(page_title="DFR metabolites Interaction", layout="wide")
st.title("Influence of Flavonoid Metabolite Concentration on DFR Substrate Specificity")

# Section: Overview
st.markdown("""
**Study Aim:**  
Does a high concentration of metabolites influence DFR substrate specificity?
""")

# Section: Video
st.header("DFR and metabolites Overview")
st.video("Videos/DFR_metabolites.mp4",  start_time=0)

# Section: Heatmap Image
st.header("Residue Interaction Heatmap (Precomputed)")
st.image("Videos/Residence_time.png", caption="DFR–Metabolite Interaction")

# Section: Dynamic Heatmap from CSV
# st.header("Residue Total Residency Time Heatmap (CSV-Based)")
# csv_heatmap_path = "Videos/protein_interaction_summary.csv"

# if os.path.exists(csv_heatmap_path):
#     df_heatmap = pd.read_csv(csv_heatmap_path)
#     df_heatmap["Residency Time (ns)"] = df_heatmap["Total Residency Time"] // 100

#     df_sorted = df_heatmap.sort_values(by="Residency Time (ns)", ascending=False)
#     heatmap_data = df_sorted.set_index("Protein Residue")[["Residency Time (ns)"]]
#     normalized_data = (heatmap_data - heatmap_data.min()) / (heatmap_data.max() - heatmap_data.min())

#     fig, ax = plt.subplots(figsize=(6, min(20, len(normalized_data) * 0.10)))
#     sns.heatmap(normalized_data, cmap="viridis", linewidths=0.3, ax=ax,
#                 cbar_kws={'label': 'Residency Time (ns, normalized)'})
#     ax.set_title("Residue Residency Time in Nanoseconds")
#     st.pyplot(fig)
# else:
#     st.error(f"CSV file not found at: {csv_heatmap_path}")

# # Section: 3D Structure Viewer
# st.header("Top 20 Interacting Residues on 3D Structure")


# Custom Atom and Molecule parser
class Atom:
    def __init__(self, line):
        self.type = line[0:6].strip()
        self.resid = int(line[22:26])
        self.resname = line[17:20].strip()
        self.x = float(line[30:38])
        self.y = float(line[38:46])
        self.z = float(line[46:54])

class Molecule:
    def __init__(self, pdb_lines):
        self.residues = defaultdict(list)
        for line in pdb_lines:
            if line.startswith(("ATOM", "HETATM")):
                atom = Atom(line)
                self.residues[atom.resid].append(atom)

    def get_residue_com(self, resid):
        atoms = self.residues.get(resid, [])
        if not atoms:
            return None
        x = sum(atom.x for atom in atoms) / len(atoms)
        y = sum(atom.y for atom in atoms) / len(atoms)
        z = sum(atom.z for atom in atoms) / len(atoms)
        return {"x": x, "y": y, "z": z}

# === Streamlit Setup ===
st.set_page_config(page_title="3D Residue Labeling", layout="wide")
st.title("Top Interacting Residues with Properly Positioned Labels")

# === File Paths ===
pdb_path = "Videos/Vitis_DHK.pdb"
csv_path = "Videos/top20_combined_binding_residues.csv"

# === Load PDB file ===
try:
    with open(pdb_path, "r") as f:
        pdb_lines = f.readlines()
        pdb_data = "".join(pdb_lines)
except FileNotFoundError:
    st.error(f"PDB file not found at: {pdb_path}")
    st.stop()

# === Parse molecule ===
mol = Molecule(pdb_lines)

# === Load top residue CSV ===
try:
    df = pd.read_csv(csv_path)
    top_residues = df["Residue_ID"].tolist()
    residue_labels = dict(zip(df["Residue_ID"], df["Residue"]))
except FileNotFoundError:
    st.error(f"CSV file not found at: {csv_path}")
    st.stop()

# === Initialize 3D viewer ===
view = py3Dmol.view(width=900, height=700)
view.addModel(pdb_data, "pdb")
view.setStyle({"cartoon": {"color": "white"}})

# === Style and label residues ===
for resid in top_residues:
    resid_str = str(resid)
    label = residue_labels[resid]

    # Highlight the residue
    view.setStyle({"resi": resid_str}, {"stick": {"color": "yellow"}})

    # Get position of the residue
    pos = mol.get_residue_com(resid)
    if pos:
        view.addLabel(label, {
            "position": pos,
            "fontColor": "black",
            "backgroundColor": "white",
            "fontSize": 12
        })

view.zoomTo()
st.components.v1.html(view._make_html(), height=750, scrolling=True)
