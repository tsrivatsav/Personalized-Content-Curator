# Personalized-Content-Curator

## Overview
This project aims to develop a web application that assists users in understanding and extracting information from uploaded pdfs. Key features include:
* Document upload and storage
* Text extraction and preprocessing
* Text summarization
* Question answering
* Bite-sized content delivery via email notifications

## Technologies Used
* Python 3.9
* Streamlit
* Google Cloud Platform (Vertex AI, Cloud Storage)
* Docker
* PyPDF2
* smtplib

## Getting Started
**Prerequisites**
* Make sure to have Docker installed
* Create a GCP Service Account with access to the Vertex AI API and download the json file containing the service account key. Rename this file as `service_acct_key.json` and place it in the project's top level working directory.
* Create a json file named `credentials.json` with the following attributes:\
sender: Your email\
password: Your password

**Building the Image:**
1. Navigate to the project's root directory
2. Build the Docker image:
   ```bash
   docker build -t pdf_upload_app .
   ```

**Running the Container:**
1. Run the container with:
   ```bash
   docker run -p 8501:8501 pdf_upload_app
   ```
This will start the container, mapping port 8501 of the container to port 8501 of your host.

**Accessing the Application:**\
Open a web browser and navigate to http://localhost:8501 to access the application.

## Structure
* `pdf_upload.py`: Main application logic
* `Dockerfile`: Dockerfile for building the image
* `requirements.txt`: List of dependencies

## Future Considerations
I will be pushing this container to the Google Container Registry and deploying the app to Google Cloud Run.