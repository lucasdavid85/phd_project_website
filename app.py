import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import py3Dmol
import pandas as pd
import numpy as np
import os
st.set_page_config(layout="wide")

st.title("Thesis Data Portal: Visualizations and Interactive Elements")

# --- Section 1: Images ---
st.header("Images")
# st.image("/nfs/mathusalem/ldavid/Communications/VISUAL_FOR_PREZ/ligand_movment_prez.png", caption="Example Figure from Results")

# # --- Section 2: Matplotlib Graph ---
# st.header("Matplotlib Graph")
# fig, ax = plt.subplots()
# x = np.linspace(0, 10, 100)
# y = np.sin(x)
# ax.plot(x, y, label="sin(x)")
# ax.set_title("Sine Wave")
# ax.legend()
# st.pyplot(fig)



# # --- Section 4: 3D Protein Viewer ---
# st.header("3D Protein Structure Viewer")
# with st.expander("View Protein in 3D"):
#     # pdb_id = st.text_input("Enter PDB ID (e.g., 1BNA):", "1BNA")
#     pdb_id= "2c29"
#     if pdb_id:
#         view = py3Dmol.view(query='pdb:' + pdb_id)
#         view.setStyle({'cartoon': {'color': 'spectrum'}})
#         view.zoomTo()
#         view.setBackgroundColor('white')
#         st.components.v1.html(view._make_html(), height=500)

# --- Section 4: 3D Protein Viewer (Local File) ---

# --- Section 4: 3D Protein Viewer (Always Visible) ---
st.header("3D Protein Structure Viewer with Custom Style")

# Path to your local PDB file
pdb_path = "/nfs/mathusalem/ldavid/Communications/Videos/Vitis_DHK.pdb"

if os.path.exists(pdb_path):
    with open(pdb_path, "r") as f:
        pdb_data = f.read()

    # Load and visualize the PDB
    view = py3Dmol.view(width=800, height=500)
    view.addModel(pdb_data, "pdb")

    # Show full protein in cartoon
    view.setStyle({'cartoon': {'color': 'white'}})

    # Optional: zoom to whole protein first (you can adjust this)
    view.zoomTo()

    # Zoom to specific resnames (only if they exist)
    view.setStyle({'resn': 'DHK'}, {'stick': {'colorscheme': 'greenCarbon'}})
    view.setStyle({'resn': 'NPH'}, {'stick': {'colorscheme': 'GreenCarbon'}})

    view.addLabel("DHK", {
        'position': {'resn': "DHK"},
        'backgroundColor': 'blue',
        'fontColor': 'black',
        'fontSize': 12
    })

    view.addLabel("NPH", {
        'position': {'resn': 'NPH'},
        'backgroundColor': 'blue',
        'fontColor': 'blue',
        'fontSize': 12
    })
    # view.zoomTo({'resn': ['DHK', 'NPH']})

    # Licorice for specific residue numbers
    highlight_residues = [123, 124, 128, 158, 162, 222]
    for resid in highlight_residues:
        view.setStyle({'resi': str(resid)}, {'stick': {'colorscheme': 'BlueCarbon'}})
        view.addLabel(f"Resid {resid}", {
            'position': {'resi': str(resid)},
            'backgroundColor': 'white',
            'fontColor': 'red',
            'fontSize': 10
        })





    # Set orientation manually (rotation in degrees)
    view.rotate(-220, 'x')
    view.rotate(-40, 'y')
    view.rotate(-160, 'z') 
    view.zoomTo({'or': [
        {'resn': 'DHK'},
        {'resn': 'NPH'},
        {'resi': [str(r) for r in highlight_residues]}
    ]})

    view.setBackgroundColor('white')
    st.components.v1.html(view._make_html(), height=500)


else:
    st.error(f"PDB file not found at: {pdb_path}")





# --- Section 5: Video ---
st.header("Video")
st.video("/nfs/mathusalem/ldavid/Communications/Videos/graph_evolution.mp4",autoplay=True)  # Supports local or URL path

# --- Section 6: Markdown and Uploads ---
# st.header("Upload & Notes")
# uploaded_file = st.file_uploader("Upload a CSV file")
# if uploaded_file:
#     df_uploaded = pd.read_csv(uploaded_file)
#     st.write("Uploaded Data Preview:")
#     st.dataframe(df_uploaded)

# st.markdown("""
# ### Notes
# - You can use this portal to showcase results dynamically.
# - Combine static images with interactive elements.
# - Perfect for defending or sharing complex bioinformatics visualizations.
# """)
