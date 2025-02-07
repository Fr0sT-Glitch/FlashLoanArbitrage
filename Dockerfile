# Use a stable Python image
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    WORKDIR=/app

# Set a fixed working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js & Hardhat dependencies
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g hardhat

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install JavaScript dependencies for frontend
RUN cd frontend && npm install && npm run build

# Make sure Solidity contracts are compiled
RUN cd contracts && npx hardhat compile

# Expose necessary ports
EXPOSE 8545 3000

# Set default command to start the bot
CMD ["python", "scripts/start_arbitrage.py"]
