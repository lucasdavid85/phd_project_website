import streamlit as st

st.set_page_config(page_title="Thesis Portal", layout="wide")

st.title("🎓 Welcome to the Thesis Data Portal")
st.markdown("### 🔍 Explore a Topic:")

# Uniform image display size (e.g., 250px height)
IMAGE_HEIGHT = 250

# Helper to make consistent tile layout
def display_tile(image_path, link_path, label, height=IMAGE_HEIGHT):
    st.image(image_path,  output_format="auto", caption="", clamp=True)
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)  # vertical spacing
    st.page_link(link_path, label=label)

# ---- Tile Layout ----
col1, col2, col3 = st.columns(3)

with col1:
    display_tile("Videos/DFR_alone.png", "pages/1_Organism_Network.py", "🧬 Organisms & Network")

with col2:
    display_tile("Videos/test1.png", "pages/2_ANS_DFR_Substrate.py", "🔬 ANS DFR Interaction")

with col3:
    display_tile("Videos/test.00013.png", "pages/3_Metabolite_Influence.py", "🧪 Metabolite Influence")

# ---- Contact Section ----
st.header("📬 Contact")

with st.form("contact_form"):
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    subject = st.text_input("Subject")
    message = st.text_area("Message")

    submitted = st.form_submit_button("Send Email")

    if submitted:
        mailto_link = f"mailto:lucas.david@univ-cotedazur.fr?subject={subject}&body=From: {name} ({email})%0A%0A{message}"
        st.markdown(f"[📨 Click here to send via your email client]({mailto_link})", unsafe_allow_html=True)
