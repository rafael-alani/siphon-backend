FROM nikolaik/python-nodejs:python3.11-nodejs22

# Install system dependencies, Rust, and Cargo
RUN apt-get update && apt-get install -y --no-install-recommends \
	build-essential \
	curl \
	&& curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
	&& export PATH="$HOME/.cargo/bin:$PATH" \
	&& echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> /etc/environment \
	&& apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy application files
COPY . .

# Install Python dependencies
RUN . /etc/environment && pip install --no-cache-dir --debug -r requirements.txt


# Install Node.js dependencies
RUN npm install

# Expose the port Cloud Run will use
ENV PORT="8000"
EXPOSE 8000

CMD [ "npm", "run", "dev"]