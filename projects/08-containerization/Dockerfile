# 1. Base Image
# Use a slim version of Python to keep image size small
FROM python:3.9-slim

# 2. Working Directory
# This sets the folder inside the container where commands will run
WORKDIR /app

# 3. Copy Requirements
# Copy only the file first to leverage Docker layer caching
COPY requirements.txt .

# 4. Install Dependencies
# --no-cache-dir reduces image size by not saving pip cache
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy Application Code
COPY etl.py .

# 6. Default Command
# This is what runs when you type `docker run`
CMD ["python", "etl.py"]
