import streamlit as st
import mysql.connector


def create_connection():
    con=mysql.connector.connect(
        host="localhost",
        user="root",
        password="sql@123",
        database="samdb"
    )
    return con

def new_user(username, email,password):
    con=create_connection()
    cursor=con.cursor()
    query="insert into classroom_user (user_name, email, password) values (%s,%s,%s)"
    cursor.execute(query,(username,email,password))
    con.commit()
    con.close()

def auth_user(username,password):
    con=create_connection()
    cursor=con.cursor()
    query="select * from classroom_user where user_name=%s and password=%s"
    cursor.execute(query,(username,password))
    data=cursor.fetchone()
    con.close()
    return data

def myProfile(username):
    con=create_connection()
    cursor=con.cursor()
    query="select id, user_name,email,password,profile_pic,about_us from classroom_user where user_name=%s"
    cursor.execute(query,(username,))
    data=cursor.fetchone()
    con.close()
    return data


def registration_form():
    st.subheader("Registration")
    username=st.text_input("username")
    email=st.text_input("email")
    password=st.text_input("password",type="password")
    bt=st.button("Register")
    if bt:
        new_user(username,email,password)
        st.success("User Registered Successfully!")
    
def login_form():
    st.subheader("Login")
    username=st.text_input("username")
    password=st.text_input("password",type="password")
    bt=st.button("Login")
    if bt:
        d=auth_user(username,password)
        if d:
            st.session_state["Logged_In"]=True
            st.session_state["username"]=username
            st.success(f"Welcome {username}!")
        else:
            st.error("Invalid User!")

def update_profile(username, new_email=None,new_password=None,about=None,profile_pic=None):
    con=create_connection()
    cursor=con.cursor()
    if new_email:
        query="update classroom_user set email=%s where user_name=%s"
        cursor.execute(query,(new_email,username))
    if new_password:
        query="update classroom_user set password=%s where user_name=%s"
        cursor.execute(query,(new_password,username))
    if about:
        query="update classroom_user set about_us=%s where user_name=%s"
        cursor.execute(query,(about,username))
    if profile_pic:
        profile_pic_data=profile_pic.read()
        query="update classroom_user set profile_pic=%s where user_name=%s"
        cursor.execute(query,(profile_pic_data,username))
    con.commit()
    con.close()



def update_profile_form():
    st.subheader("Update Profile")
    username=st.session_state["username"]
    st.write(f"username: {username}")
    profile_pic=st.file_uploader("browse profile pic",type=["jpg","png","jpeg"])
    if profile_pic:
        st.image(profile_pic,width=150, use_column_width=False)
        st.markdown(
            """
            <style>
            .profile_pic {
                border-radius:50%;
                border:block;
                margin-left:auto;
                margin-right:auto;
            }
            </style>          
            """,
            
        unsafe_allow_html=True
        )        

    new_email=st.text_input("New Email")
    new_password=st.text_input("New Password",type="password")
    about=st.text_area("About Us")
    bt=st.button("Update profile")
    if bt:
        update_profile(username,new_email=new_email,new_password=new_password,about=about,profile_pic=profile_pic)
        st.success(f"{username} Profile updated successfully!")

def myprofile_form():
    st.subheader("My Profile")
    username=st.session_state["username"]
    user_data=myProfile(username)
    if user_data:
        id, user_name,email,password,profile_pic,about_us=user_data
        if profile_pic:
            st.image(profile_pic,width=150, use_column_width=False)
        st.markdown(
            """
            <style>
            .profile_pic {
                border-radius:50%;
                border:block;
                margin-left:auto;
                margin-right:auto;
            }
            </style>          
            """,
            
        unsafe_allow_html=True
        )
    st.write(f"**ID**: {id}") 
    st.write(f"**User Name**: {user_name}") 
    st.write(f"**Email**: {email}") 
    st.write(f"**Password**: {password}") 
    st.write(f"**About**: {about_us}")          
    
def logout():
    st.session_state["username"] = None
    st.session_state["logged_in"] = False
    st.success("User Logged Out Successfully!")

def menu():
    st.title("Welcome to Samarthya Classes!")
    menu=["Login", "Register","Update Profile","My Profile", "Logout"]
    select=st.sidebar.selectbox("MENU",menu)
    if select=="Login":
        login_form()
    elif select=="Register":
        registration_form()
    elif select=="My Profile":
        if "Logged_In" in st.session_state and st.session_state["Logged_In"]:
            myprofile_form()
        else:
            st.error("Data not found")

    elif select=="Update Profile":
        if "Logged_In" in st.session_state and st.session_state["Logged_In"]:
            update_profile_form()
        else:
            st.error("Please login first!")

    elif select=="Logout":
        if "Logged_In" in st.session_state and st.session_state["Logged_In"]:
            logout()
    


if __name__ == "__main__":
    menu() 



