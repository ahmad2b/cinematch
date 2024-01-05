import streamlit as st
from database import db_connect, UserManager

engine = db_connect()
user_manager = UserManager(engine)

if "username" not in st.session_state:
    st.session_state["username"] = ""

st.title("🎬 Join Cinematch :popcorn:")
st.markdown("---")
st.write(
    """
    🎉 Welcome to Cinematch! The ultimate movie recommendation system. 🎉 \n Please login or sign up to start discovering awesome movies. 
🎥"""
)
# st.write("Please login or sign up to start discovering awesome movies. 🎥")


tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])

with tab1:
    # st.subheader("Login")
    with st.form(key="login_form"):
        username = st.text_input("👤 Username")
        password = st.text_input("🔒 Password", type="password")
        submit_button = st.form_submit_button("🚀 Login")

        if submit_button:
            response = user_manager.login(username, password)
            if response["status"] == "success":
                st.session_state["username"] = username
                st.success(
                    f"{username} Logged in successfully \n Click here to go to [Home Page](/)"
                )
            else:
                st.error(response["message"])

with tab2:
    # st.subheader("Sign Up")
    with st.form(key="signup_form"):
        new_username = st.text_input("👤 Create a new username")
        new_password = st.text_input("🔒 Set a new password", type="password")
        submit_button = st.form_submit_button("🚀 Sign Up")

        if submit_button:
            response = user_manager.signup(new_username, new_password)
            if response["status"] == "success":
                st.success(
                    f"{new_username} Signed up successfully \n Click here to [Login](/)"
                )
            else:
                st.error(response["message"])
