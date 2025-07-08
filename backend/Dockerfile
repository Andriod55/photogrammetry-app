FROM node:18-bullseye

WORKDIR /app
COPY ../package.json ../package-lock.json* ./
RUN npm install --production

# Install Python deps
RUN apt-get update && apt-get install -y python3 python3-pip unzip && rm -rf /var/lib/apt/lists/*
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY . ../backend
CMD ["node", "app.js"]
