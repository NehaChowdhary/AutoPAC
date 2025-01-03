# Fetching python 3.10 image
FROM python:3.10

# Basic setup of environment and apt
RUN apt-get update -y && apt-get upgrade -y
RUN mkdir -p /root/privateGPT/server

# Workdir setup
WORKDIR /root/privateGPT/server

# Copying requirements.txt file and downloading dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copying build distro
# COPY dist/* .
# RUN pip install privateGPT_server-1.0.0-py3-none-any.whl

# Copying entrypoint file and making it executable
# COPY entrypoint.sh .
# RUN chmod +x entrypoint.sh

# Copying the main files
COPY privateGPT_server.py .
COPY t5model.py .
COPY t5dataset.py .

# Exposing port 5000 for production server
EXPOSE 5000

# Starting the production server with serve -s build in entrypoint.sh
CMD ["python", "privateGPT_server.py"]