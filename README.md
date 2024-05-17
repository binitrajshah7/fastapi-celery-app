# FastAPI and Celery Application with Redis

This application is designed to generate prime numbers asynchronously using FastAPI, Celery, and Redis. Users can request the generation of a specified number of prime numbers, and the application processes this request in the background, allowing users to check the status and results of their requests.


## Setup

### 1. Build and Run the Server with Docker
In the fast_api_service directory, you will find two files: **Dockerfile** and **docker-compose.yml**

#### Run below commands to build and run the server:
```bash
  docker-compose build
  docker-compose up
```
 ##### To run in daemon mode
    docker-compose up -d 

## Accessing Endpoints

### 1. Health Check Endpoint
To verify if the server is running, send a GET request to:
```bash
http://0.0.0.0:8888/api/v1/health-check
```

### 2. Generate Primes
Method: `POST`
This endpoint is used to request the generation of a specified number of prime numbers asynchronously. The task is handled in the background by Celery.

```bash
http://0.0.0.0:8888/api/v1/generate_primes/
```

Include the following JSON payload in the request body:
```json
{
    "number": 41
}
```

#### Expected response:

if result not found:
```json
{
    "request_id": "24c8f857-a282-4bdc-936a-55bf61b8acbc",
    "status": "processing"
}
```

If result found:
```json
{
    "request_id": "24c8f857-a282-4bdc-936a-55bf61b8acbc",
    "status": "completed",
    "result": "[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179]"
}
```

Note: Not maintaining any authentication and user master so hardcoded the user_id as of now.
We can derive user_id from token and use it accordingly.



### 3.Check Status
Method: `GET` 
This endpoint is used to check the status of the prime number generation task. It allows users to see whether their request is still being processed or if it has been completed.

```bash
http://0.0.0.0:8888/api/v1/check_status/{request_id}
```

#### Expected response:

if result not found:
```json
{
    "request_id": "24c8f857-a282-4bdc-936a-55bf61b8acbc",
    "status": "processing"
}
```

If result found:
```json
{
    "request_id": "24c8f857-a282-4bdc-936a-55bf61b8acbc",
    "status": "completed",
    "result": "[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179]"
}
```