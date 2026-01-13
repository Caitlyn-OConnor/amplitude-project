# Amplitude Project

A robust Python-based ETL pipeline designed to extract event data from the **Amplitude Analytics** (EU) platform, process compressed archives, and automate delivery to **AWS S3**.

## 🌟 Key Features

* **Multi-Stage Extraction:** Automatically handles the nested compression used by Amplitude (extracts `.zip` to find `.gz` files, then decompresses those into raw `.json`).
* **S3 Automation with Cleanup:** Uploads processed JSON files to S3 and immediately purges local copies to save disk space.
* **Resilient Networking:** Built-in retry logic for 5xx server errors with a 10-second backoff.
* **Comprehensive Logging:** Tracks every stage of the pipeline—from API connection to file extraction and upload—in timestamped log files.
* **Temporary Workspace Management:** Automatically creates and cleans up intermediate directories (`zipdata`, `extractzip`) during processing.

---

## 🏗 Project Architecture

The pipeline follows a **four-stage** process:

1. **Extraction (API):** Requests data from the Amplitude EU export endpoint.
2. **Decompression (Local):** * Saves the raw binary as a `.zip`.
* Unpacks the `.zip` to reveal dated subfolders containing `.gz` files.
* Decompresses `.gz` files into valid `.json` files in the `/data` directory.


3. **Cloud Sync (AWS):** Scans the `/data` folder and streams all JSON files to the configured S3 bucket using `boto3`.
4. **Housekeeping:** Deletes all local artifacts (Zips, Gzips, and JSONs) upon successful cloud confirmation.

---

## 🛠 Setup & Usage

### 1. Prerequisites

Ensure you have Python 3.x installed and a valid AWS IAM profile named `amplitude_test` configured on your machine.

### 2. Installation

```bash
git clone https://github.com/yourusername/amplitude-export.git
cd amplitude-export
pip install requests python-dotenv boto3

```

### 3. Environment Configuration

Create a `.env` file in the root directory:

```env
# Amplitude Credentials
AMP_API_KEY=your_amplitude_api_key
AMP_SECRET_KEY=your_amplitude_secret_key

# AWS Credentials
AWS_ACCESS_KEY=your_aws_access_key
AWS_SECRET_KEY=your_aws_secret_key
AWS_BUCKET_NAME=your_s3_bucket_name

```

---

## 📊 Technical Details

### Directory Structure

The script manages the following lifecycle for directories:

* `/logs`: Persistent storage for run history.
* `/zipdata`: Temporary storage for the initial API download (Auto-deleted).
* `/extractzip`: Temporary storage for the unzipped contents (Auto-deleted).
* `/data`: Final staging area for JSON files before S3 upload (Auto-cleaned).

### Error Handling & Retries

| Status Code | Action | Logic |
| --- | --- | --- |
| **200 OK** | Proceed | Initiates extraction and upload. |
| **5xx** | Retry | Waits 10s; attempts 3 times before failing. |
| **4xx** | Stop | Logs the specific client error (e.g., Auth failure) and exits. |

### File Cleanup

To prevent data duplication and local storage bloat, the script uses `shutil.rmtree()` for temporary folders and `os.remove()` for individual JSON files only **after** a confirmed successful S3 `put_object` operation.
