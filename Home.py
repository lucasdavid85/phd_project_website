import streamlit as st
import os

st.set_page_config(page_title="Thesis Portal", layout="wide")

st.title("🎓 Welcome to the Thesis Data Portal")
st.markdown("### 🔍 Explore a Topic:")

# Helper function to build image path
def get_image_path(filename):
    return os.path.join("images", filename)

# Helper to display tile (non-clickable image, text only)
def topic_tile(image_filename, label, description, color):
    st.image(get_image_path(image_filename))
    st.markdown(f"<div style='text-align:center; color:{color}; font-weight:bold'>{label}</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; font-size:14px'>{description}</p>", unsafe_allow_html=True)
    st.markdown("---")

# ---- TOPIC REDIRECTION SECTION ----
col1, col2, col3 = st.columns(3)

with col1:
    topic_tile(
        image_filename="DFR_alone.png",
        label="🧬 Organisms & Network",
        description="Go to the sidebar and click 'Organism Network' to explore this topic.",
        color="#1f77b4"
    )

with col2:
    topic_tile(
        image_filename="test1.png",
        label="🔬 ANS DFR Interaction",
        description="Go to the sidebar and click 'ANS DFR Substrate' to explore this topic.",
        color="#e76f51"
    )

with col3:
    topic_tile(
        image_filename="test.00013.png",
        label="🧪 Metabolite Influence",
        description="Go to the sidebar and click 'Metabolite Influence' to explore this topic.",
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
