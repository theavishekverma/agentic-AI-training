# Logging Documentation

## Overview
The Employee Management API uses a comprehensive logging system to track application behavior, errors, and user actions.

## Logging Configuration

### Logger Setup (`config/logger.py`)
- **Log Level**: DEBUG (file), INFO (console)
- **Log File**: `logs/app_YYYYMMDD_HHMMSS.log`
- **Rotating File Handler**: Automatically creates new log files when size exceeds 10MB
- **Max Backup Logs**: 5 backup log files

### Log Format
```
YYYY-MM-DD HH:MM:SS,mmm - logger_name - LEVEL - message
```

## Log Levels

- **DEBUG**: Detailed information (used for development/troubleshooting)
- **INFO**: General informational messages (normal operation)
- **WARNING**: Warning messages (potentially problematic situations)
- **ERROR**: Error messages (serious problems)

## What Gets Logged

### Main Application (main.py)
- Application initialization
- CORS configuration
- HTTP middleware logs:
  - Request method, path, and client IP
  - Response status code
  - Processing duration

### Employee Routes (app/employee.py)
- **GET /employees/**: Fetches all employees, logs count
- **GET /employees/{id}**: Fetches specific employee, logs employee ID
- **POST /employees/**: Creates new employee, logs employee details and assigned ID
- **DELETE /employees/{id}**: Deletes employee, logs deletion event

### Employee Service (services/employee_service.py)
- File read/write operations
- JSON parsing errors
- File existence checks
- Data load/save confirmations

## Log File Location
```
Day19_Project_Employee_Mgmt/
└── logs/
    └── app_20260613_120000.log
```

## Example Log Output

```
2026-06-13 12:00:01,234 - employee_api.main - INFO - FastAPI application initialized
2026-06-13 12:00:01,240 - employee_api.main - INFO - CORS enabled for origins: ['http://localhost:3000']
2026-06-13 12:00:05,123 - employee_api.main - DEBUG - → POST /employees/ from 127.0.0.1
2026-06-13 12:00:05,234 - employee_api.employee - INFO - Creating new employee: John Doe
2026-06-13 12:00:05,240 - employee_api.employee_service - INFO - Successfully wrote 1 employees to file
2026-06-13 12:00:05,300 - employee_api.main - INFO - ← POST /employees/ | Status: 201 | Duration: 0.177s
```

## Monitoring Logs

### Real-time Monitoring (Console)
Logs at INFO level and above appear in the console during development.

### Historical Review (File)
- Check `logs/` directory for archived logs
- Each log file is timestamped with creation time
- Use text editors or log viewers to analyze

## Best Practices

1. **Check logs when**: API returns unexpected errors, operations fail, or behavior is unusual
2. **Monitor duration**: Pay attention to processing times, especially for POST/DELETE operations
3. **Review warnings**: Warning messages indicate potential issues that may need attention
4. **Archive logs**: Old logs are automatically rotated to prevent disk space issues

## Troubleshooting with Logs

### Employee Creation Fails
```
employee_api.employee - ERROR - Error creating employee: ...
```
Check the error message and logs above for details.

### File I/O Errors
```
employee_api.employee_service - ERROR - IO error writing to db/employee.json: ...
```
Check file permissions and disk space.

### CORS Issues
```
employee_api.main - WARNING - Request from unauthorized origin
```
Check CORS configuration in `main.py` and update allowed origins if needed.
