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
