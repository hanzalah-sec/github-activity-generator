FROM python:3.11-slim

WORKDIR /app

# Copy repository files
COPY activity_generator.py config.json ./

# Create initial log file
RUN touch activity_log.txt

# Run in daemon mode with 1-hour interval by default
CMD ["python", "activity_generator.py", "--daemon", "--interval", "3600"]
