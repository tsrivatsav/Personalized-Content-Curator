# Use a base Python image
FROM python:3.9-slim-buster

# Create app directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt ./

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port for Streamlit app
EXPOSE 8501

# Command to run the app
CMD ["streamlit", "run", "pdf_upload.py", "--server.enableXsrfProtection", "false"]
