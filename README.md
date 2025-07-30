# 🔐 AWS Glue De-Identifier

A serverless data pipeline for **automated de-identification of sensitive healthcare data**. Built using **AWS Glue**, **S3**, and a **Streamlit frontend**, this project detects and masks Personally Identifiable Information (PII) / Protected Health Information (PHI) from uploaded patient CSV files.

---

## 📌 Features

- ✅ Upload raw patient CSV data via web interface
- ✅ Automatically triggers AWS Glue job to mask PHI
- ✅ De-identifies fields like `patient_name`, `dob`, `phone`, `address`
- ✅ Stores cleaned output securely in Amazon S3
- ✅ Provides public download link for de-identified file
- ✅ Job status tracking and UI feedback

---

## 🧱 Architecture

![Architecture Diagram](architecture.png)

---

## 🖥️ Tech Stack

- **AWS Glue** – serverless ETL to mask sensitive data
- **Amazon S3** – stores raw and processed data
- **Streamlit** – user-friendly web app for uploads
- **Boto3** – Python SDK to trigger Glue jobs from Streamlit
- **IAM & Glue Catalog** – secure access + metadata

---

## 🚀 How It Works

1. 📤 User uploads a CSV file with raw patient data  
2. ☁️ File is saved to `s3://healthcare-upload/`  
3. 🧠 AWS Glue job is triggered with file path as input  
4. 🔐 Glue job masks sensitive fields and writes output to `s3://healthcare-output/`  
5. 📥 Streamlit shows link to download de-identified file

---

## 📂 Project Structure

```bash
aws-glue-deidentifier/
├── README.md
├── architecture.png
├── streamlit_app/
│ ├── app.py
│ ├── requirements.txt
├── glue_jobs/
│ ├── deidentify_job_script.py
├── data_samples/
│ ├── sample_input.csv
│ ├── expected_output.csv
└── notes/
└── setup_guide.md
```


## 🧪 Sample Input

```csv
patient_id,patient_name,dob,phone,address
1,John Doe,1985-03-12,0551234567,Dubai Marina, Dubai
2,Jane Smith,1990-07-22,0509876543,Abu Dhabi Corniche, Abu Dhabi
```

## ✅ Sample OutPut
```
Output (De-Identified)
patient_id,patient_name,dob,phone,address
1,REDACTED,1985,XXXXXXX,REDACTED
2,REDACTED,1990,XXXXXXX,REDACTED
```

## 📦 Setup & Deployment
You need AWS credentials and access to S3 + Glue

🧱 Configure your AWS credentials in environment or ~/.aws/credentials

🪣 Create 2 S3 buckets: healthcare-upload, healthcare-output

🧠 Create AWS Glue Job with de-identification logic

🖥️ Run Streamlit app:

```
cd streamlit_app
pip install -r requirements.txt
streamlit run app.py
```
## 👨‍💼 Use Cases
Healthcare startups and providers handling sensitive patient data

Privacy-first data pipelines

HIPAA/GDPR anonymization workflows

AI/ML preprocessing for medical datasets


## 🖼️ 2. `architecture.png` – Diagram

Here’s what to include in your **architecture diagram** (I can generate the image if needed):

### 🔁 Architecture Components:

```plaintext
[User / Doctor / Data Analyst]
         |
         ↓
[ Streamlit Frontend App ]
         |
         ↓  (via Boto3)
[ Amazon S3 - Raw Bucket ] --> [ AWS Glue Job ]
                                  |
                                  ↓
                    [ De-Identified Output to S3 ]
                                  |
                                  ↓
             [ Athena / Download Link / API Gateway ]
```
## 👨‍⚕️ Disclaimer
This tool is for educational/demo purposes only and is not approved for clinical diagnosis. Always consult a medical professional for real medical advice.

## 📬 Contact
###  Made with ❤️ by Ahmed Elbashier
[LinkedIn](https://www.linkedin.com/in/ahmed-elbashier) | [GitHub](https://github.com/AhmedElbashier)