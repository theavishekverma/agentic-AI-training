import random
from datetime import datetime, timedelta

# Generate 1000 synthetic web server error log lines
errors = []
start_date = datetime(2026, 1, 1)

status_codes = [400, 401, 403, 404, 408, 500, 502, 503, 504]
messages = {
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    408: "Request Timeout",
    500: "Internal Server Error",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout"
}

for i in range(1000):
    # Random date within 100 days
    log_date = start_date + timedelta(days=random.randint(0, 100),
                                      seconds=random.randint(0, 86400))
    status = random.choice(status_codes)
    msg = messages[status]
    ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
    line = f"{log_date.strftime('%Y-%m-%d %H:%M:%S')} ERROR {status} {msg} from {ip}"
    errors.append(line)

# Save to a /home/avishek/Avishek/Python
with open("/home/avishek/Avishek/Python/webserver_errors.log", "w") as f:
    for line in errors:
        f.write(line + "\n")

print("Generated 1000 error log lines in webserver_errors.log")