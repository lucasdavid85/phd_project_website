import streamlit as st
import py3Dmol
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import mdanalysis as mda

st.set_page_config(page_title="ANS DFR Interaction", layout="wide")
st.title("Influence of flavonoid metabolite high concentration on DFR substrate specificity")
st.markdown("""
            Aim of the study : Does a high concentration of metabolites may have an influence the substrate specificity of DFR?
            """)
st.title("Protein protein docking methods")

st.video("Videos/DFR_metabolites.mp4", autoplay=True)


st.header("Residue Interaction Heatmap")

# === Load the CSV File ===

st.header("Residue Total Residency Time Heatmap")

# === Load the CSV File ===
csv_path = "Videos/protein_interaction_summary.csv"  # Adjust path as needed
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)

    # Convert to nanoseconds using integer division
    df["Residency Time (ns)"] = df["Total Residency Time"] // 100

    # Sort and prepare heatmap data
    df_sorted = df.sort_values(by="Residency Time (ns)", ascending=False)
    heatmap_data = df_sorted.set_index("Protein Residue")[["Residency Time (ns)"]]

    # Normalize for color intensity
    normalized_data = (heatmap_data - heatmap_data.min()) / (heatmap_data.max() - heatmap_data.min())

    # Create a smaller heatmap figure
    fig, ax = plt.subplots(figsize=(6, min(20, len(normalized_data) * 0.10)))
    sns.heatmap(normalized_data, cmap="viridis", linewidths=0.3, ax=ax,
                cbar_kws={'label': 'Residency Time (ns, normalized)'})
    ax.set_title("Residue Residency Time in Nanoseconds")
    st.pyplot(fig)
else:
    st.error(f"CSV file not found at: {csv_path}")



def plot_top_interacting_residues(pdb_file, matrix_file, top_n=15):
    # Load interaction matrix data
    data = np.load(matrix_file, allow_pickle=True)
    interaction_matrix = data["interaction_matrix"]
    protein_resnames = data["protein_resnames"]
    protein_resids = data["protein_resids"]

    # Aggregate interactions over all frames
    interaction_counts = np.sum(interaction_matrix, axis=2)

    # Map residue → total interaction count
    residue_interactions = {resid: 0 for resid in protein_resids}
    for i, resid in enumerate(protein_resids):
        residue_interactions[resid] = np.sum(interaction_counts[:, i])

    # Select top N residues
    top_resids = sorted(residue_interactions, key=residue_interactions.get, reverse=True)[:top_n]

    # Load PDB and compute residue center of mass
    u = mda.Universe(pdb_file)
    protein = u.select_atoms("protein")

    with open(pdb_file, "r") as f:
        pdb_data = f.read()

    view = py3Dmol.view(width=900, height=700)
    view.addModel(pdb_data, "pdb")
    view.setStyle({"cartoon": {"color": "white"}})

    # Highlight and label top interacting residues
    for res in protein.residues:
        if res.resid in top_resids:
            resname = res.resname
            resid = str(res.resid)

            view.setStyle({"resi": resid}, {"stick": {"color": "yellow"}})

            com = res.atoms.center_of_mass()
            view.addLabel(f"{resname}-{resid}", {
                "position": {"x": float(com[0]), "y": float(com[1]), "z": float(com[2])},
                "fontColor": "black",
                "backgroundColor": "white",
                "fontSize": 12
            })

    view.zoomTo()
    return view

# === Streamlit Integration ===
st.header("Top Protein-Ligand Interacting Residues (3D View)")

# File paths
pdb_path = "Videos/your_model.pdb"
matrix_path = "Videos/your_interaction_matrix.npz"

if st.button("Render Top Interactions"):
    view = plot_top_interacting_residues(pdb_path, matrix_path, top_n=15)
    st.components.v1.html(view._make_html(), height=750, scrolling=True)



st.image("Videos/Residence_time.png", caption="DFR metabolite interaction")
