# 🛠️ Setup Guide for AWS Glue De-Identifier Project

This document guides you through the setup and deployment of the **AWS Glue De-Identifier** project.

---

## 📦 Prerequisites

Before you begin:

- ✅ AWS account
- ✅ IAM permissions for S3, Glue, and Glue Studio
- ✅ Python 3.8+ installed locally
- ✅ Streamlit installed
- ✅ Basic understanding of S3, IAM, and Glue jobs

---

## 1️⃣ S3 Bucket Setup

Create two buckets in your AWS account:

| Bucket Name          | Purpose                  |
|----------------------|---------------------------|
| `healthcare-upload`  | Stores raw uploaded CSVs  |
| `healthcare-output`  | Stores de-identified data |

> 📍Make sure bucket names are globally unique (e.g., `yourname-healthcare-upload`)

---

## 2️⃣ Create the AWS Glue Job

### A. Go to AWS Glue Studio → **Jobs**
1. Click **Create job**
2. Use **Visual with a source and target**
3. Source → S3 (CSV) → `s3://healthcare-upload/`
4. Target → S3 → `s3://healthcare-output/`

### B. Add Custom Transform
1. Add a **Transform node**
2. Choose **Custom transform**
3. Paste the script from `glue_jobs/deidentify_job_script.py`

### C. Job Parameters
Add two job arguments so the frontend can dynamically pass them:
```text
--input_path
--output_path

```

Then in the source node:

Change data location to: Dynamic path: ${input_path}

And in the target node:

Set output location to: ${output_path}

✅ This makes your Glue job reusable for each file upload

---

## 3️⃣ Configure IAM Role
### Create or use an IAM role for Glue with:

* AmazonS3FullAccess

* AWSGlueServiceRole

Also grant the same or limited permissions to the credentials used in your Streamlit app:

* glue:StartJobRun, glue:GetJobRun

* s3:PutObject, s3:GetObject

---

## 4️⃣ Launch the Streamlit Frontend

### A. Navigate to the frontend folder

``
cd streamlit_app
``
### B. Install dependencies
``
pip install -r requirements.txt
``
### C. Run the web app
``
streamlit run app.py
``
### D. Upload Sample File
Upload a file like sample_input.csv, then wait for Glue job completion and download the cleaned file.

---

## 5️⃣ Optional: AWS Athena Setup (for Querying Output)
If you want to query the results:

1. Go to AWS Glue → Crawlers

2. Create a crawler for s3://healthcare-output/

3. Create a database (e.g., healthcare_db)

4. Run the crawler

5. Go to Athena → Select database → Run:

``
SELECT * FROM patient_deid LIMIT 10;
``
---
## ✅ Final Checklist
```
| Task                           | Status |
| ------------------------------ | ------ |
| Create 2 S3 buckets            | ✅      |
| Build and test Glue job        | ✅      |
| Add dynamic input/output paths | ✅      |
| Set up Streamlit frontend      | ✅      |
| Trigger job and verify results | ✅      |
| (Optional) Add Athena access   | ✅      |
```
---
## 🤝 Support
For help, contact:
Ahmed Elbashier
[LinkedIn](https://www.linkedin.com/in/ahmed-elbashier) | [GitHub](https://github.com/AhmedElbashier)



