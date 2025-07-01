import streamlit as st
import py3Dmol
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

    # Convert residency time to nanoseconds (ps / 100)
    df["Residency Time (ns)"] = df["Total Residency Time"] / 100

    # Sort and prepare heatmap data
    df_sorted = df.sort_values(by="Residency Time (ns)", ascending=False)
    heatmap_data = df_sorted.set_index("Protein Residue")[["Residency Time (ns)"]]

    # Normalize values for color contrast
    heatmap_normalized = (heatmap_data - heatmap_data.min()) / (heatmap_data.max() - heatmap_data.min())

    # Plot the heatmap
    fig, ax = plt.subplots(figsize=(8, max(10, len(heatmap_normalized) * 0.15)))
    sns.heatmap(heatmap_normalized, cmap="viridis", linewidths=0.5, ax=ax,
                cbar_kws={'label': 'Residency Time (ns, normalized)'})
    ax.set_title("Total Residency Time per Residue (in ns)")
    st.pyplot(fig)
else:
    st.error(f"CSV file not found at path: {csv_path}")


