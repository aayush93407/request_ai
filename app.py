import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"  # FastAPI URL

def upload_pdf():
    """Upload PDF and extract URLs."""
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded_file is not None:
        # Send the file to FastAPI for processing
        try:
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            response = requests.post(f"{API_BASE}/upload-pdf", files=files)

            if response.status_code == 200:
                # Show extracted URLs
                urls = response.json().get("urls", [])
                if urls:
                    st.write("Extracted URLs:")
                    for url in urls:
                        st.write(url)
                else:
                    st.error("No URLs found in the PDF.")
            else:
                st.error(f"Error: {response.json().get('message')}")
        except Exception as e:
            st.error(f"Error while uploading: {e}")

upload_pdf()
