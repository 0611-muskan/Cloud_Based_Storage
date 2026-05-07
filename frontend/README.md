# File Manager - Streamlit Frontend

A modern Python-based file management UI built with Streamlit and AWS integration.

## Features

✅ **AWS Cognito Authentication**
- Sign up with email verification
- OTP confirmation
- Secure login/logout
- JWT token-based sessions

✅ **File Management**
- Upload files to AWS S3
- List user-specific files
- Delete files
- Generate shareable links (60-second expiry)
- Download files

✅ **Modern UI**
- Clean, responsive Streamlit interface
- Real-time file listing
- Status messages and notifications

## Requirements

- Python 3.8+
- Backend server running on `http://localhost:5000`

## Installation

Install dependencies from the **global requirements.txt** in the root directory:

```bash
# From root directory
pip install -r requirements.txt
```

This installs both backend and frontend dependencies at once.

## Running the App

```bash
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`

## Architecture

```
Frontend (Streamlit)
    ↓
Flask Backend
    ↓
AWS Services (S3 + Cognito)
```

## Project Structure

```
frontend/
├── streamlit_app.py       # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── config.toml       # Streamlit configuration
└── README.md             # This file
```

## How It Works

1. **Authentication**: Uses AWS Cognito for secure user management
2. **File Upload**: Files are uploaded to Flask backend, then to S3
3. **File Storage**: Files are stored in S3 with user email as prefix (user-isolation)
4. **File Sharing**: Generates presigned URLs with 60-second expiration
5. **Session Management**: Uses Streamlit session state to track authentication

## API Endpoints (Backend)

- `POST /files/upload` - Upload file
- `GET /files?email=user@example.com` - List user files
- `DELETE /files/<key>` - Delete file
- `GET /files/share/<key>` - Get signed URL

## Troubleshooting

### "Connection refused" error
- Make sure Flask backend is running: `python app.py`

### "Invalid email or password"
- Ensure email is confirmed (check confirmation OTP)
- Verify AWS Cognito credentials in backend `.env`

### Files not showing up
- Check that email matches the one you signed up with
- Verify AWS credentials and S3 permissions

## Security Notes

- Tokens are stored in Streamlit session state (not persisted)
- Signed URLs expire after 60 seconds
- Files are isolated by user email
- All API calls include email parameter for verification
