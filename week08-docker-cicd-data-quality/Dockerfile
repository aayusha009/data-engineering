# Start from an official Python image (slim = smaller, faster to download)
FROM python:3.11-slim

# All following commands run as if you're inside this folder in the container
WORKDIR /app

# Copy ONLY requirements.txt first
# layer, so it won't reinstall dependencies every time you change your Python code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy everything else (your actual source code) into the image
COPY . .

# Create a non-root user and switch to it — running as root inside a container
# is a security risk best avoided even in a practice project
RUN useradd --create-home appuser
USER appuser

# What actually runs when someone does `docker run` on this image
CMD ["python", "src/pipeline.py"]