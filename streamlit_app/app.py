import streamlit as st
import boto3
import uuid
import time
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os
import pandas as pd
from pathlib import Path
from urllib.parse import quote

# Load env config
load_dotenv()

# Paths
README_PATH = Path("..") / "README.md"
SETUP_PATH = Path("../notes") / "setup_guide.md"
SAMPLE_INPUT_PATH = Path("..") / "data_samples" / "sample_input.csv"
SAMPLE_OUTPUT_PATH = Path("..") / "data_samples" / "expected_output.csv"

# Config
REGION = os.getenv("AWS_REGION", "eu-north-1")
INPUT_BUCKET = os.getenv("INPUT_BUCKET")
OUTPUT_BUCKET = os.getenv("OUTPUT_BUCKET")
GLUE_JOB_NAME = os.getenv("GLUE_JOB_NAME")

# AWS session
session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=REGION
)
s3 = session.client("s3",region_name=REGION)
glue = session.client("glue")

# Page config
st.set_page_config(page_title="Patient De-Identifier", layout="centered")

# Tabs
tab1,tab3, tab4, tab5 = st.tabs([
    "🩺 Run De-Identifier",
    "📥 Sample Input",
    "📤 Sample Output",
    "📄 README",

])
# Try to locate the exact key that matches the uploaded file ID
def find_latest_output_key(bucket):
    response = s3.list_objects_v2(Bucket=bucket)
    all_keys = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].endswith(".csv")]
    if not all_keys:
        return None
    # Sort by timestamp in filename
    sorted_keys = sorted(all_keys, key=lambda k: int(k.split("_")[-1].replace(".csv", "")), reverse=True)
    return sorted_keys[0]


# Tab 1: Main De-ID App
with tab1:
    st.title("🩺 Patient Data De-Identifier")
    uploaded_file = st.file_uploader("📤 Upload Patient CSV File", type="csv")

    if uploaded_file and "job_completed" not in st.session_state:
        file_id = f"{uuid.uuid4()}.csv"
        s3.upload_fileobj(uploaded_file, INPUT_BUCKET, file_id)
        st.success(f"✅ File uploaded to S3: {file_id}")

        # Start Glue job
        try:
            st.info("🚀 Starting AWS Glue job...")
            response = glue.start_job_run(
                JobName=GLUE_JOB_NAME,
                Arguments={
                    "--input_path": f"s3://{INPUT_BUCKET}/{file_id}",
                    "--output_path": f"s3://{OUTPUT_BUCKET}/{file_id}"
                }
            )
            run_id = response["JobRunId"]
            st.success(f"Glue job started: {run_id}")
        except ClientError as e:
            st.error(f"❌ Failed to start job: {e}")
            st.stop()

        # Wait for completion
        with st.spinner("⌛ Waiting for job to finish..."):
            while True:
                status = glue.get_job_run(JobName=GLUE_JOB_NAME, RunId=run_id)
                state = status["JobRun"]["JobRunState"]
                if state in ["SUCCEEDED", "FAILED", "STOPPED"]:
                    break
                time.sleep(10)

        if state == "SUCCEEDED":
            st.session_state["job_completed"] = True
            st.success("🎉 Job completed successfully!")
            matched_key = find_latest_output_key(OUTPUT_BUCKET)

            if matched_key:
                try:
                    url = s3.generate_presigned_url(
                        "get_object",
                        Params={"Bucket": OUTPUT_BUCKET, "Key": matched_key},
                        ExpiresIn=600
                    )
                    st.download_button("⬇️ Download De-identified CSV",
                                       data=s3.get_object(Bucket=OUTPUT_BUCKET, Key=matched_key)['Body'].read(),
                                       file_name="deidentified_output.csv")
                except Exception as e:
                    st.warning(f"✅ File is ready, but failed to generate download link. Error: {e}")
            else:
                st.error("❌ File not found in output bucket. Please check your Glue job output path.")

        if st.button("🔁 Upload New File"):
            st.session_state.clear()
            st.experimental_rerun()

# Tab 2: Setup Guide
# with tab2:
#     st.header("⚙️ Setup Instructions")
#     try:
#         with open(SETUP_PATH, "r", encoding="utf-8") as f:
#             st.markdown(f.read(), unsafe_allow_html=True)
#     except Exception as e:
#         st.error(f"Error loading setup_guide.md: {e}")

# Tab 3: Sample Input
with tab3:
    st.header("📥 Sample Input File")
    try:
        df_input = pd.read_csv(SAMPLE_INPUT_PATH)
        st.dataframe(df_input)
        st.download_button("Download Sample Input", data=df_input.to_csv(index=False), file_name="sample_input.csv")
    except Exception as e:
        st.error(f"Error loading sample input: {e}")

# Tab 4: Sample Output
with tab4:
    st.header("📤 Sample Output (De-Identified)")
    try:
        df_output = pd.read_csv(SAMPLE_OUTPUT_PATH)
        st.dataframe(df_output)
        st.download_button("Download Sample Output", data=df_output.to_csv(index=False), file_name="sample_output.csv")
    except Exception as e:
        st.error(f"Error loading sample output: {e}")

# Tab 5: README
with tab5:
    st.header("📄 Project Overview (README)")
    try:
        with open(README_PATH, "r", encoding="utf-8") as f:
            st.markdown(f.read(), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading README.md: {e}")

