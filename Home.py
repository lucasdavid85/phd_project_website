import streamlit as st

st.set_page_config(page_title="Thesis Portal", layout="wide")

st.title("Welcome to the Thesis Data Portal")

st.markdown("### Select a topic:")
st.page_link("pages/1_Organism_Network.py", label="1. Organisms and network protein interaction", icon="🧬")
st.page_link("pages/2_ANS_DFR_Substrate.py", label="2. ANS DFR protein interaction in substrate specificity", icon="🔬")
# if st.button("Go to ANS DFR Interaction"):
#     st.switch_page("2_ANS_DFR_Substrate.py")

st.page_link("pages/3_Metabolite_Influence.py", label="3. Presence of metabolites can perturb substrate specificity", icon="🧪")



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
