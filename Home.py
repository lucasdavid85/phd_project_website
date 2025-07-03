import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import os

st.set_page_config(page_title="Thesis Portal", layout="wide")

st.title("🎓 Welcome to the Thesis Data Portal")
st.markdown("### 🔍 Explore a Topic:")

# Helper function to build image path
def get_image_path(filename):
    return os.path.join("Videos", filename)

# Helper to display tile
def clickable_tile(image_filename, label, description, page_name, color):
    st.image(get_image_path(image_filename))
    st.markdown(f"<div style='text-align:center; color:{color}; font-weight:bold'>{label}</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; font-size:14px'>{description}</p>", unsafe_allow_html=True)
    if st.button(f"Go to {label}", key=label, help=description):
        switch_page(page_name)

# ---- TOPIC REDIRECTION SECTION ----
col1, col2, col3 = st.columns(3)

with col1:
    clickable_tile(
        image_filename="DFR_alone.png",
        label="🧬 Organisms & Network",
        description="Explore how proteins interact across organisms.",
        page_name="Organism_Network.py",
        color="#1f77b4"
    )

with col2:
    clickable_tile(
        image_filename="test1.png",
        label="🔬 ANS DFR Interaction",
        description="Investigate substrate specificity in enzymes.",
        page_name="pages/ANS_DFR_Substrate/py",
        color="#e76f51"
    )

with col3:
    clickable_tile(
        image_filename="test.00013.png",
        label="🧪 Metabolite Influence",
        description="Study how metabolites affect protein activity.",
        page_name="Metabolite_Influence",
        color="#2a9d8f"
    )

# ---- CONTACT FORM ----
st.header("📬 Contact")

with st.form("contact_form"):
    st.write("You can contact me via email using the form below.")
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    subject = st.text_input("Subject")
    message = st.text_area("Message")

    submitted = st.form_submit_button("Send Email")

    if submitted:
        mailto_link = f"mailto:lucas.david@univ-cotedazur.fr?subject={subject}&body=From: {name} ({email})%0A%0A{message}"
        st.markdown(f"[📨 Click here to send via your email client]({mailto_link})", unsafe_allow_html=True)
