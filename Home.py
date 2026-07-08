import base64
import os

import streamlit as st

st.set_page_config(page_title="Thesis Portal", layout="wide")

st.title("🎓 Welcome to the Thesis Data Portal")
st.markdown("### 🔍 Explore a Topic:")

# Uniform image display size
IMAGE_HEIGHT = 250

# ---- Styling for the clickable tiles ----
st.markdown(
    f"""
    <style>
    .tile-link {{
        display: block;
        text-decoration: none;
        color: inherit;
    }}
    .tile-link img {{
        width: 100%;
        height: {IMAGE_HEIGHT}px;
        object-fit: cover;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .tile-link:hover img {{
        transform: scale(1.03);
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.3);
    }}
    .tile-label {{
        display: block;
        text-align: center;
        margin-top: 12px;
        font-size: 1.1rem;
        font-weight: 600;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


def _img_to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def display_tile(image_path, page_slug, label):
    """Render an image that navigates to `page_slug` when clicked anywhere."""
    if not os.path.exists(image_path):
        st.error(f"Image not found: {image_path}")
        return

    ext = os.path.splitext(image_path)[1].lstrip(".").lower() or "png"
    encoded = _img_to_base64(image_path)
    st.markdown(
        f"""
        <a class="tile-link" href="{page_slug}" target="_self">
            <img src="data:image/{ext};base64,{encoded}" alt="{label}">
            <span class="tile-label">{label}</span>
        </a>
        """,
        unsafe_allow_html=True,
    )


# ---- Tile Layout ----
col1, col2, col3 = st.columns(3)

with col1:
    display_tile("Videos/DFR_alone.png", "Organism_Network", "🧬 Organisms & Network")

with col2:
    display_tile("Videos/test1.png", "ANS_DFR_Substrate", "🔬 ANS DFR Interaction")

with col3:
    display_tile("Videos/test.00013.png", "Metabolite_Influence", "🧪 Metabolite Influence")

# ---- Contact Section ----
st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
st.header("📬 Contact")
st.markdown("Questions about this work? Get in touch:")
st.link_button("📧 Email lucas.david@univ-cotedazur.fr", "mailto:lucas.david@univ-cotedazur.fr")
