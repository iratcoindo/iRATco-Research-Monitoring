import streamlit as st

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

    st.title("Dashboard")

    st.success(
        f"Welcome {st.session_state.user.fullname}"
    )

    st.write("Role :", st.session_state.user.role)

    st.divider()

    st.write("Versi 0.1")

    st.info("Login berhasil.")

    if st.button("Logout"):

        st.session_state.login = False
        st.session_state.user = None

        st.rerun()


if st.session_state.login:

    dashboard()

else:

    login_page()
