FROM python:3.11-slim

# Install PostgreSQL client and server
RUN apt-get update && apt-get install -y \
    postgresql \
    postgresql-contrib \
    && rm -rf /var/lib/apt/lists/*

# Configure PostgreSQL for trust authentication (local development)
RUN sed -i 's/local   all             all                                     peer/local   all             all                                     trust/' /etc/postgresql/17/main/pg_hba.conf && \
    sed -i 's/host    all             all             127.0.0.1\/32            scram-sha-256/host    all             all             127.0.0.1\/32            trust/' /etc/postgresql/17/main/pg_hba.conf && \
    sed -i 's/host    all             all             ::1\/128                 scram-sha-256/host    all             all             ::1\/128                 trust/' /etc/postgresql/17/main/pg_hba.conf

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates/ templates/
COPY static/ static/
COPY boot/ boot/
RUN chmod +x boot/boot.sh boot/seed_data.py

EXPOSE 5000

# Start PostgreSQL and run Flask app
CMD ["./boot/boot.sh"]
