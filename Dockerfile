FROM nikolaik/python-nodejs:latest

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Node.js dependencies
RUN npm install

# Expose the port Cloud Run will use
ENV PORT 8080
EXPOSE 8080

CMD [ "npm" "run" "dev"]