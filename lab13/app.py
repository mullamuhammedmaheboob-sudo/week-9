
import streamlit as st
import pandas as pd

from db import (
    init_db, create_user, get_user_by_username,
    get_all_users, user_exists, update_password
)

from auth import (
    hash_password, verify_password,
    validate_username, validate_email,
    validate_password
)

st.set_page_config(page_title="Auth App", page_icon="A")

@st.cache_resource
def setup_database():
    init_db()
    return True

setup_database()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

def signup_page():
    st.title("Create Account")

    with st.form("signup_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Sign Up")

    if submit:
        for ok, msg in [
            validate_username(username),
            validate_email(email),
            validate_password(password)
        ]:
            if not ok:
                st.error(msg)
                return

        if password != confirm:
            st.error("Passwords do not match.")
            return

        if user_exists(username=username):
            st.error("Username already taken.")
            return

        if user_exists(email=email):
            st.error("Email already registered.")
            return

        if create_user(username, email, hash_password(password)):
            st.success("Account created! Please log in.")
        else:
            st.error("Something went wrong.")

def login_page():
    st.title("Login")

    if st.session_state.attempts >= 3:
        st.error("Too many failed attempts. Try again later.")
        return

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        user = get_user_by_username(username)

        if user and verify_password(password, user["password_hash"]):
            st.session_state.attempts = 0
            st.session_state.logged_in = True

            st.session_state.user = {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
                "created_at": user["created_at"],
                "role": user["role"]
            }

            st.rerun()

        else:
            st.session_state.attempts += 1

            if st.session_state.attempts >= 3:
                st.error("Too many failed attempts. Try again later.")
                st.stop()
            else:
                st.error(
                    f"Invalid credentials. Attempt {st.session_state.attempts}/3"
                )

def reset_password_page():
    st.title("Change Password")

    with st.form("reset_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        current_password = st.text_input(
            "Current Password", type="password"
        )
        new_password = st.text_input(
            "New Password", type="password"
        )
        submit = st.form_submit_button("Reset")

    if submit:
        user = get_user_by_username(username)

        if (
            user
            and user["email"] == email
            and verify_password(
                current_password,
                user["password_hash"]
            )
        ):
            ok, msg = validate_password(new_password)

            if not ok:
                st.error(msg)
                return

            update_password(
                username,
                hash_password(new_password)
            )

            st.success("Password updated. Please log in.")

        else:
            st.error("Invalid account details or current password.")

def dashboard_page():
    user = st.session_state.user

    st.title(f"Welcome, {user['username']}!")

    c1, c2 = st.columns(2)

    c1.metric("User ID", user["id"])
    c2.metric("Username", user["username"])

    st.write("Email:", user["email"])

    st.write(
        "Joined:",
        user["created_at"].strftime("%Y-%m-%d %H:%M")
    )

    st.write("Role:", user["role"])

    st.markdown("---")

    if st.session_state.user["role"] == "admin":
        st.subheader("Admin Panel")
        st.subheader("Registered Users")

        users = get_all_users()

        if users:
            df = pd.DataFrame(users)

            df["created_at"] = pd.to_datetime(
                df["created_at"]
            ).dt.strftime("%Y-%m-%d %H:%M")

            st.dataframe(df)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

if st.session_state.logged_in:
    dashboard_page()

else:
    tab_login, tab_signup, tab_reset = st.tabs(
        ["Login", "Sign Up", "Forgot Password"]
    )

    with tab_login:
        login_page()

    with tab_signup:
        signup_page()

    with tab_reset:
        reset_password_page()
