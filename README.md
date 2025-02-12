# gym-transformer
Here's a step-by-step guide to deploy your Streamlit app:

---

### **1. Prerequisites**

Ensure you have:
- **Python** installed (preferably 3.8+).
- **Streamlit** installed:  
  ```bash
  pip install streamlit
  ```
- **Required Libraries** installed:  
  ```bash
  pip install pandas google-api-python-client google-auth matplotlib
  ```

---

### **2. Project Setup**

Organize your project folder like this:

```
/workout-tracker
├── app.py                   # Your main Streamlit script
├── requirements.txt         # List of dependencies
├── .streamlit/
│   └── secrets.toml         # Google API credentials
├── workout_log.csv          # Data file (optional if loading from Drive)
├── workout_plan.csv         # Workout plan file
└── workout_guide.csv        # Exercise guide file
```

---

### **3. Configure Google API Credentials**

1. **Create Google Service Account**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/).
   - Create a project and enable **Google Drive API**.
   - Create service account credentials and download the JSON key.

2. **Add Credentials to Streamlit**:
   - Inside `.streamlit` folder, create `secrets.toml`:
     ```toml
     [gcp_service_account]
     type = "service_account"
     project_id = "your-project-id"
     private_key_id = "your-private-key-id"
     private_key = "-----BEGIN PRIVATE KEY-----\nYOUR_KEY\n-----END PRIVATE KEY-----\n"
     client_email = "your-service-account@project-id.iam.gserviceaccount.com"
     client_id = "your-client-id"
     auth_uri = "https://accounts.google.com/o/oauth2/auth"
     token_uri = "https://oauth2.googleapis.com/token"
     auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
     client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account"
     ```

---

### **4. Create `requirements.txt`**

List all Python dependencies:
```bash
streamlit
matplotlib
pandas
google-auth
google-auth-oauthlib
google-auth-httplib2
google-api-python-client
```

---

### **5. Run Locally for Testing**

Run the app on your machine:
```bash
streamlit run app.py
```

---

### **6. Deploying on Streamlit Cloud**

1. Push your project to GitHub.
2. Go to [Streamlit Cloud](https://share.streamlit.io/).
3. Sign in with GitHub and deploy your repo.
4. Set up your secrets:
   - Go to **Settings → Secrets** in Streamlit Cloud.
   - Copy your `.streamlit/secrets.toml` content into the Secrets section.

---

### **7. Deployment on Other Platforms (Optional)**

If you'd prefer platforms like **Heroku**:
1. Install Heroku CLI:
   ```bash
   brew install heroku
   ```
2. Initialize Git and push your code:
   ```bash
   git init
   heroku create
   git add .
   git commit -m "Initial commit"
   git push heroku master
   ```
3. Scale the app:
   ```bash
   heroku ps:scale web=1
   heroku open
   ```

---

### ✅ Troubleshooting Tips

- **Google API Errors**: Ensure your service account has permission to access the files in Google Drive.
- **Data Not Loading**: Verify file names in Drive match exactly (`workout_log.csv`, etc.).
- **App Crashing**: Check logs for errors:
  ```bash
  streamlit logs
  ```

Let me know if you encounter any issues! 🚀