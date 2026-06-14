# Employee Management System - React Client

A simple React application to test CORS with the FastAPI Employee Management API.

## Features

- **Fetch All Employees**: View a table of all employees
- **Create Employee**: Add a new employee with name, age, and department
- **View Single Employee**: Get details of a specific employee
- **CORS Testing**: Test cross-origin requests with the backend API

## Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- FastAPI backend running on `http://localhost:8000`

## Setup

1. Install dependencies:

```bash
cd client
npm install
```

2. Start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## API Endpoints Being Tested

- `GET /employees/` - Fetch all employees
- `POST /employees/` - Create a new employee
- `GET /employees/{id}` - Get a specific employee

## CORS Configuration

The FastAPI backend is configured to accept requests from:
- `http://localhost:3000`
- `http://localhost:5173`
- `http://127.0.0.1:3000`
- `http://127.0.0.1:5173`
- `http://127.0.0.1:8001`

## Build for Production

```bash
npm run build
npm run preview
```

## Notes

- Make sure the FastAPI backend is running before testing
- The application uses Vite for fast development and optimized builds
- CORS headers are properly configured in the backend
