import streamlit as st
import requests
import json
import base64
import jwt
from datetime import datetime
import os
from dotenv import load_dotenv
import boto3

load_dotenv()

# Page config
st.set_page_config(page_title="File Manager", layout="wide", initial_sidebar_state="collapsed")

# AWS Cognito Config
COGNITO_REGION = "ap-south-1"
USER_POOL_ID = "ap-south-1_O5WuVlgnP"
CLIENT_ID = "11kigi99f79mj6lh7v742q70cn"
API_URL = "http://localhost:5000/files"

# Initialize Cognito client with AWS credentials
cognito_client = boto3.client(
    'cognito-idp',
    region_name=COGNITO_REGION,
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_KEY')
)

# Initialize session state
if "token" not in st.session_state:
    st.session_state.token = None
if "email" not in st.session_state:
    st.session_state.email = None

# Helper functions
def get_user_email_from_token(token):
    """Extract email from JWT token"""
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload.get("email")
    except:
        return None

def signup(email, password):
    """Sign up user with Cognito"""
    try:
        response = cognito_client.sign_up(
            ClientId=CLIENT_ID,
            Username=email,
            Password=password,
            UserAttributes=[
                {"Name": "email", "Value": email}
            ]
        )
        return True, "Signup successful! Please confirm with OTP."
    except cognito_client.exceptions.UsernameExistsException:
        return False, "Email already registered."
    except Exception as e:
        return False, str(e)

def confirm_signup(email, otp):
    """Confirm user registration with OTP"""
    try:
        cognito_client.confirm_sign_up(
            ClientId=CLIENT_ID,
            Username=email,
            ConfirmationCode=otp
        )
        return True, "Email confirmed! You can now login."
    except Exception as e:
        return False, str(e)

def login(email, password):
    """Login user with Cognito"""
    try:
        response = cognito_client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password
            }
        )
        token = response['AuthenticationResult']['IdToken']
        st.session_state.token = token
        st.session_state.email = email
        return True, "Login successful!"
    except cognito_client.exceptions.NotAuthorizedException:
        return False, "Invalid email or password."
    except cognito_client.exceptions.UserNotConfirmedException:
        return False, "Please confirm your email first."
    except Exception as e:
        return False, str(e)

def logout():
    """Logout user"""
    st.session_state.token = None
    st.session_state.email = None

# Upload file
def upload_file(file_object, email):
    """Upload file to S3 via Flask backend"""
    try:
        files = {"file": (file_object.name, file_object.getvalue(), file_object.type)}
        data = {"email": email}
        
        response = requests.post(f"{API_URL}/upload", files=files, data=data)
        if response.status_code == 200:
            return True, "File uploaded successfully!"
        else:
            return False, response.json().get("message", "Upload failed")
    except Exception as e:
        return False, str(e)

# Load files
def load_files(email):
    """Get list of user files from backend"""
    try:
        response = requests.get(f"{API_URL}?email={email}")
        if response.status_code == 200:
            return response.json(), None
        else:
            return [], response.json().get("message", "Failed to load files")
    except Exception as e:
        return [], str(e)

# Delete file
def delete_file(key):
    """Delete file from S3 via backend"""
    try:
        response = requests.delete(f"{API_URL}/{key}")
        if response.status_code == 200:
            return True, "File deleted successfully!"
        else:
            return False, response.json().get("message", "Delete failed")
    except Exception as e:
        return False, str(e)

# Get share link
def get_share_link(key):
    """Get signed URL for sharing"""
    try:
        response = requests.get(f"{API_URL}/share/{key}")
        if response.status_code == 200:
            return response.json().get("url"), None
        else:
            return None, response.json().get("message", "Failed to generate link")
    except Exception as e:
        return None, str(e)

# Main App
st.title("☁️ File Manager")

# Check if user is logged in
if not st.session_state.token:
    # Auth page
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.subheader("Login")
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", key="login_btn"):
            if login_email and login_password:
                success, message = login(login_email, login_password)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.warning("Please enter email and password")
    
    with tab2:
        st.subheader("Sign Up")
        signup_email = st.text_input("Email", key="signup_email")
        signup_password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
        
        if st.button("Sign Up", key="signup_btn"):
            if not signup_email or not signup_password:
                st.warning("Please fill all fields")
            elif signup_password != confirm_password:
                st.error("Passwords do not match")
            else:
                success, message = signup(signup_email, signup_password)
                if success:
                    st.success(message)
                    
                    # Ask for OTP
                    st.info("Check your email for OTP")
                    otp = st.text_input("Enter OTP from email")
                    
                    if st.button("Confirm OTP"):
                        confirm_success, confirm_message = confirm_signup(signup_email, otp)
                        if confirm_success:
                            st.success(confirm_message)
                            st.balloons()
                        else:
                            st.error(confirm_message)
                else:
                    st.error(message)

else:
    # Dashboard page
    col1, col2 = st.columns([0.9, 0.1])
    
    with col1:
        st.subheader(f"👋 Welcome, {st.session_state.email}")
    
    with col2:
        if st.button("Logout"):
            logout()
            st.rerun()
    
    st.divider()
    
    # File upload section
    st.subheader("📤 Upload File")
    uploaded_file = st.file_uploader("Choose a file to upload")
    
    if uploaded_file and st.button("Upload"):
        with st.spinner("Uploading..."):
            success, message = upload_file(uploaded_file, st.session_state.email)
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)
    
    st.divider()
    
    # Files list section
    st.subheader("📁 Your Files")
    
    with st.spinner("Loading files..."):
        files, error = load_files(st.session_state.email)
        
        if error:
            st.error(error)
        elif not files:
            st.info("No files uploaded yet")
        else:
            for file in files:
                if not file.get("Key"):
                    continue
                
                # Parse file info
                file_key = file.get("Key")
                file_size = file.get("Size", 0)
                size_mb = round(file_size / (1024 * 1024), 2)
                clean_name = file_key.split("/")[1].split("-", 1)[1] if "-" in file_key else file_key
                
                # Create columns for file display
                col1, col2, col3, col4, col5 = st.columns([0.4, 0.15, 0.15, 0.15, 0.15])
                
                with col1:
                    st.write(f"📄 **{clean_name}**")
                    st.caption(f"{size_mb} MB")
                
                with col2:
                    if st.button("🔗 Share", key=f"share_{file_key}"):
                        url, err = get_share_link(file_key)
                        if url:
                            st.success("Link copied!")
                            st.code(url)
                        else:
                            st.error(err)
                
                with col3:
                    if st.button("⬇️ Download", key=f"download_{file_key}"):
                        url, err = get_share_link(file_key)
                        if url:
                            st.markdown(f"[Click here to download]({url})")
                        else:
                            st.error(err)
                
                with col4:
                    if st.button("🗑️ Delete", key=f"delete_{file_key}"):
                        success, message = delete_file(file_key)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                
                st.divider()
