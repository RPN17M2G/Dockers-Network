# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN  apt-get update && apt-get install -y iputils-ping
RUN python -m pip install -r requirements.txt

WORKDIR /code
RUN python3 -m pip install psutil \
&&  pip install speedtest-cli \ 
&& pip install --no-cache-dir --upgrade fastapi uvicorn
COPY ./node /code/node

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /code
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python","-u", "-m", "node.main"]
