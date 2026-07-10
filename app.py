import streamlit as st
from database import Research

from database import (
    Session,
    User,
    verify_password,
    create_default_admin
)

create_default_admin()

st.set_page_config(
    page_title="iRATco Research Monitoring",
    page_icon="🧬",
    layout="centered"
)

if "login" not in st.session_state:
    st.session_state.login = False

if "user" not in st.session_state:
    st.session_state.user = None


def login_page():

    st.title("🧬 iRATco Research Monitoring")

    st.write("Please login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        session = Session()

        user = session.query(User).filter_by(
            username=username
        ).first()

        if user:

            if verify_password(password, user.password):

                st.session_state.login = True
                st.session_state.user = user

                st.success("Login Success")

                st.rerun()

            else:

                st.error("Wrong Password")

        else:

            st.error("User not found")

        session.close()


def dashboard():

    session = Session()

    research = session.query(Research).filter_by(
        owner=st.session_state.user.username
    ).first()

    st.title("🧬 iRATco Research Monitoring")

    if research is None:

        st.warning("Belum ada research untuk user ini.")

    else:

        st.subheader("Principal Investigator")
        st.info(research.principal_investigator)

        st.subheader("Research Code")
        st.code(research.code)

        st.subheader("Research Title")
        st.success(research.title)

        st.subheader("Research Design")

        st.link_button(
            "📄 Open Research Design",
            research.design_link
        )

        st.progress(research.progress/100)

        st.write(f"{research.progress}%")

    session.close()

    if st.button("Logout"):
        st.session_state.login=False
        st.session_state.user=None
        st.rerun()
