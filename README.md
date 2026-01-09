# Amplitude Project

A Python script designed to export data from the **Amplitude Analytics** platform. This tool automates the process of requesting data, handling authentication, and managing binary file (.zip) storage.

## 🌟 Key Features

* **Automated Data Export:** Retrieves amplitude event data for a specific date range.
* **Resilient Retry Logic:** Implements a `while` loop with 10s delay to handle server-side errors (5xx) up to 3 times.
* **Security First:** Utilizes `python-dotenv` to manage sensitive API credentials via environment variables.
* **Binary File Management:** Handles raw binary streams to save exports as compressed `.zip` files within a structured data directory.
* **Logging:** Creates log files on every run to document the success or errors created.

---

## 🏗 Project Architecture

### Steps

1. **Authentication:** Loads `AMP_API_KEY` and `AMP_SECRET_KEY`.
2. **API Request:** Calls the Amplitude API with a defined start and end datetime.
3. **Validation:** If the API call was successful (200): Creates a `data/` folder and saves the response as a timestamped `.zip`.
    * **Server Error (5xx):** Triggers the retry mechanism, with up to 3 attempts to account for server outages. A warning will be logged for this error code.
    * **Client Error (4xx):** Prevents unnecessary API calls on user error. An error will be logged for this error code. 

---

## 🛠 How to use

1. **Clone the project:**
```bash
git clone https://github.com/yourusername/amplitude-export.git
cd amplitude-export

```


2. **Install requirements:**
```bash
pip install requests python-dotenv

```


3. **Configure Environment:**
Create a `.env` file in the root directory:
```env
AMP_API_KEY=your_api_key_here
AMP_SECRET_KEY=your_secret_key_here

```

---

## 📊 More Details

### Error Handling & Retries

The script distinguishes between different types of failure to optimize performance:

* **Retryable:** If the status code is >=500, the script assumes a temporary system outage and waits 10 seconds before trying again.
* **Fatal:** If the status code is in the 400 range (e.g., `403 Forbidden`), the script logs the reason and terminates immediately to allow for manual fixes.

### File Naming Convention

Files are saved using a precise timestamp format to prevent overwriting previous exports:
`data/YYYY-MM-DD_HH-MM-SS.zip`
An error will be logged if the .zip file cannot be saved in the data directory.

