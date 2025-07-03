import streamlit as st

st.set_page_config(page_title="Thesis Portal", layout="wide")

st.title("🎓 Welcome to the Thesis Data Portal")
st.markdown("### 🔍 Explore a Topic:")

col1, col2, col3 = st.columns(3)

with col1:
    st.image("Videos/DFR_alone.png", use_column_width=True)
    st.page_link("pages/1_Organism_Network.py", label="🧬 Organisms & Network")

with col2:
    st.image("Videos/test1.png", use_column_width=True)
    st.page_link("pages/2_ANS_DFR_Substrate.py", label="🔬 ANS DFR Interaction")

with col3:
    st.image("Videos/test.00013.png", use_column_width=True)
    st.page_link("pages/3_Metabolite_Influence.py", label="🧪 Metabolite Influence")

# Contact section
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
