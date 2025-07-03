import streamlit as st

st.set_page_config(page_title="Thesis Portal", layout="wide")

st.title("🎓 Welcome to the Thesis Data Portal")
st.markdown("### 🔍 Explore a Topic:")

# ---- TOPIC REDIRECTION SECTION ----
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <a href="pages/1_Organism_Network.py" target="_self">
            <img src="Videos/DFR_alone.png" width="100%" style="border-radius:12px; box-shadow:0 4px 8px rgba(0,0,0,0.1); margin-bottom:10px;" />
            <div style="text-align:center">
                <h3 style="color:#1f77b4;">🧬 Organisms & Network</h3>
                <p style="font-size:14px;">Explore how proteins interact across organisms.</p>
            </div>
        </a>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <a href="pages/2_ANS_DFR_Substrate.py" target="_self">
            <img src="Videos/test1.png" width="100%" style="border-radius:12px; box-shadow:0 4px 8px rgba(0,0,0,0.1); margin-bottom:10px;" />
            <div style="text-align:center">
                <h3 style="color:#e76f51;">🔬 ANS DFR Interaction</h3>
                <p style="font-size:14px;">Investigate substrate specificity in enzymes.</p>
            </div>
        </a>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <a href="pages/3_Metabolite_Influence.py" target="_self">
            <img src="Videos/test.0003.png" width="100%" style="border-radius:12px; box-shadow:0 4px 8px rgba(0,0,0,0.1); margin-bottom:10px;" />
            <div style="text-align:center">
                <h3 style="color:#2a9d8f;">🧪 Metabolite Influence</h3>
                <p style="font-size:14px;">Study how metabolites affect protein activity.</p>
            </div>
        </a>
    """, unsafe_allow_html=True)

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
