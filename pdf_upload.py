import streamlit as st
import PyPDF2
import re
import os
from google.cloud import aiplatform
import smtplib
import json

def load_credentials(file_path):
  with open(file_path, 'r') as f:
    data = json.load(f)
  return data

def store_document(uploaded_file):
  file_path = os.path.join("documents", uploaded_file.name)
  with open(file_path, "wb") as f:
    f.write(uploaded_file.getbuffer())
  return file_path

def send_email(recipient, subject, body):
  credentials = load_credentials('credentials.json')
  sender = credentials['sender']
  password = credentials['password']

  message = f"Subject: {subject}\n\n{body}"

  with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
    smtp.starttls()
    smtp.login(sender, password)
    smtp.sendmail(sender, recipient, message)


def set_up_vertex_ai():
  os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_acct_key.json"
  project = "personalized-content-curator"
  region = "us-central1"  # Replace with your region
  aiplatform.init(project=project, location=region)

# Call this function to set up Vertex AI before using the API
set_up_vertex_ai()

def process_pdf_with_vertex_ai(pdf_file):
  # Extract text using PyPDF2
  text = process_pdf(pdf_file)

  # Create a TextSummarization model
  summarizer = aiplatform.TextSummarization.create(
      display_name="text_summarizer1",
      base_model="google/universal-sentence-encoder-large-512"
  )

  # Generate summary
  summary = summarizer.predict(
      instances=[{"content": text}]
  )

  return summary.predictions[0].summary

def preprocess_text(text):
  # Convert to lowercase
  text = text.lower()
  # Remove punctuation
  text = re.sub(r'[^\w\s]', '', text)
  # Remove extra whitespace
  text = text.strip()
  return text

def process_pdf(uploaded_file):
  try:
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    num_pages = len(pdf_reader.pages)
    text = ""
    for page_num in range(num_pages):
      page = pdf_reader.pages[page_num]
      text += page.extract_text()
    return preprocess_text(text)
  except PyPDF2.errors.PdfReadError as e:
    st.error(f"Error reading PDF: {e}")
    return None

def main():
  st.title("PDF Uploader and Processor")
  uploaded_file = st.file_uploader("Choose a PDF file")
  if uploaded_file is not None:
    pdf_text = process_pdf(uploaded_file)
    if pdf_text:
      st.write("Extracted text:")
      st.text_area("Text", value=pdf_text, height=300)

if __name__ == "__main__":
  main()
