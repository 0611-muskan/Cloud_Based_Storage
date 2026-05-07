# Quick Start Guide

## 🚀 Running the Project

### Prerequisites
- Python 3.8+
- AWS Account with S3 and Cognito configured

### Step 1: Install All Dependencies
```bash
# From root directory
pip install -r requirements.txt
```

### Step 2: Configure Backend
```bash
cd backend

# Copy .env.example to .env
copy .env.example .env

# Edit .env with your AWS credentials
```

Example `backend/.env`:
```
AWS_REGION=ap-south-1
AWS_BUCKET_NAME=my-bucket-name
AWS_ACCESS_KEY=AKIAXXXXXXXX
AWS_SECRET_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

### Step 3: Start Backend Server
```bash
cd backend
python app.py
```
✅ Backend runs on `http://localhost:5000`

### Step 4: Start Streamlit Frontend
```bash
cd frontend
streamlit run streamlit_app.py
```
✅ Frontend opens at `http://localhost:8501`

### Step 5: Use the App
1. **Sign Up** with email and password
2. **Confirm** with OTP from email
3. **Login** to dashboard
4. **Upload** files
5. **Share** with generated links
6. **Download** or **Delete** files

---

## 📁 Project Structure

```
Cloud Based App/
├── backend/
│   ├── app.py              # Flask server
│   ├── aws_config.py       # AWS configuration
│   ├── .env.example        # Example env file
│   └── routes/
│       └── file_routes.py  # API routes
│
├── frontend/
│   ├── streamlit_app.py    # Streamlit app
│   ├── README.md           # Frontend docs
│   └── .streamlit/
│       └── config.toml     # Streamlit config
│
├── requirements.txt        # 🌍 Global dependencies
├── CONVERSION_GUIDE.md     # Full conversion docs
└── QUICKSTART.md           # This file
```

---

## 🔧 Troubleshooting

### Backend fails to start
```
Error: Cannot connect to AWS
→ Check AWS credentials in backend/.env
```

### Frontend shows "Connection refused"
```
Error: HTTPConnectionPool
→ Make sure backend is running (python app.py)
→ Check backend is on port 5000
```

### Files not showing up
```
→ Verify email matches signup email
→ Check S3 bucket permissions
```

### Cognito authentication fails
```
→ Verify USER_POOL_ID and CLIENT_ID in streamlit_app.py
→ Check Cognito pool is in ap-south-1 region
```

---

## 📚 Technologies Used

| Component | Technology |
|-----------|-----------|
| Backend | Flask, Python |
| Frontend | Streamlit, Python |
| Database | AWS S3 |
| Auth | AWS Cognito |
| Cloud | AWS |

---

## 💡 Features

✅ User authentication with AWS Cognito  
✅ Secure file upload to S3  
✅ User-isolated file storage  
✅ Shareable links with expiration  
✅ Modern Streamlit UI  
✅ Real-time file listing  
✅ Delete & Download functionality  

---

## 🎓 Next Steps

1. Test file upload with a small file first
2. Try sharing a file with another user
3. Check S3 bucket to see files organized by email
4. Customize Streamlit theme in `.streamlit/config.toml`
5. Deploy to Streamlit Cloud or Heroku

---

For more details, see [CONVERSION_GUIDE.md](CONVERSION_GUIDE.md)
