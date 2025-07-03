import streamlit as st
import base64

st.set_page_config(page_title="Thesis Portal", layout="wide")

st.title("🎓 Welcome to the Thesis Data Portal")
st.markdown("### 🔍 Explore a Topic:")

# Helper to simulate a clickable image+text block
def clickable_tile(image_path, label, description, page_file, color):
    if st.button(f"{label}", key=label, help=description):
        st.switch_page(page_file)
    st.image(image_path, use_column_width=True)
    st.markdown(f"<div style='text-align:center; color:{color}; font-weight:bold'>{label}</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; font-size:14px'>{description}</p>", unsafe_allow_html=True)

# ---- TOPIC REDIRECTION SECTION ----
col1, col2, col3 = st.columns(3)

with col1:
    clickable_tile(
        image_path="Videos/DFR_alone.png",
        label="🧬 Organisms & Network",
        description="Explore how proteins interact across organisms.",
        page_file="pages/1_Organism_Network.py",
        color="#1f77b4"
    )

with col2:
    clickable_tile(
        image_path="Videos/test1.png",
        label="🔬 ANS DFR Interaction",
        description="Investigate substrate specificity in enzymes.",
        page_file="pages/2_ANS_DFR_Substrate.py",
        color="#e76f51"
    )

with col3:
    clickable_tile(
        image_path="Videos/test.0003.png",
        label="🧪 Metabolite Influence",
        description="Study how metabolites affect protein activity.",
        page_file="pages/3_Metabolite_Influence.py",
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
        st.markdown(f"[Click here to send via your email client]({mailto_link})", unsafe_allow_html=True)
