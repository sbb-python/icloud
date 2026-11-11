# iCloud File Organizer

A Streamlit app for reviewing files that you have already downloaded from iCloud
Drive. It shows the uploaded file names, types, and sizes, and lets you download
individual files or a selected group as a ZIP.

## Important limitations

- The app does not sign in to iCloud, read your iCloud storage quota, sync files,
  or delete files from your Apple account.
- Download files from [iCloud.com](https://www.icloud.com/) before uploading them
  into the app.
- Browser downloads are saved to the device running the browser.
- Uploaded data is handled by the Streamlit server for the current session.
  Avoid uploading sensitive files to a hosted instance. This app does not write
  uploads to its own persistent storage.

## Run locally

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

## Deploy for free on Streamlit Community Cloud

1. Push `app.py`, `storage_utils.py`, and `requirements.txt` to a GitHub repository.
2. Create or sign in to a Streamlit Community Cloud account.
3. Create an app from that repository and set the main file to `app.py`.

The app and its dependencies are installed on Streamlit's hosted server. Uploads
are therefore not processed solely on your laptop. Review Streamlit's current
usage limits before uploading large files.

## Run tests

```powershell
python -m unittest
```
