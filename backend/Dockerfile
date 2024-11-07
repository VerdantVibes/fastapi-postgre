# Use the official Python image  
FROM python:3.10.12  

# Environment variables  
ENV POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PATH="/app/.venv/bin:$PATH"  

# Update and install necessary dependencies  
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    python3-dev \
    libgl1-mesa-glx \
    libpq-dev \
    gcc \
    libpq5 && \
    rm -rf /var/lib/apt/lists/*  

# Install Poetry  
RUN pip install poetry  

# Set work directory  
WORKDIR /app  

# Copy only the dependency files  
COPY pyproject.toml poetry.lock ./  

# Install dependencies  
RUN poetry install --no-root  

# Copy the rest of the application  
COPY . .  

# Expose the port your application will run on (optional)  
EXPOSE 8000  