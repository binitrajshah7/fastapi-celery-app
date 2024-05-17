import time
from fastapi import FastAPI, HTTPException
import uvicorn
from dotenv import load_dotenv
import redis
from celery import Celery
import uuid
from lib.utils import init_logging

load_dotenv()


app = FastAPI()
logger = init_logging(__name__)

redis_client = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)

celery = Celery(
    'tasks',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)


@app.get("/api/v1/health-check")
async def health_check():
    logger.info(f"========> /api/v1/health-check")
    return {"status": "OK"}


@celery.task
def generate_primes_task(request_id, n):
    time.sleep(5)
    primes = [2]
    num = 3
    while len(primes) < n:
        is_prime = True
        for i in range(len(primes)):
            if num % primes[i] == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
        num += 2
    redis_client.set(request_id, str(primes))
    return primes


@app.post("/api/v1/generate_primes/")
async def generate_primes(request_data: dict):
    #TODO: user_id to be derived from token
    user_id = 5
    n = request_data["number"]
    cache_key = f"{user_id}:{n}"

    request_id = redis_client.get(cache_key)
    if request_id:
        result = redis_client.get(request_id)
        if result and result == "processing":
            return {"request_id": request_id, "status": "processing"}
        else:
            return {"request_id": request_id, "status": "completed", "data": result}

    request_id = str(uuid.uuid4())

    redis_client.set(cache_key, request_id)
    redis_client.set(request_id, "processing")
    generate_primes_task.delay(request_id, n)
    return {"request_id": request_id, "status": "processing"}


@app.get("/api/v1/check_status/{request_id}")
async def check_status(request_id: str):
    result = redis_client.get(request_id)
    if result:
        if result == "processing":
            return {"request_id": request_id, "status": result}
        return {"request_id": request_id, "status": "completed", "result": result}
    raise HTTPException(status_code=404, detail="Invalid request_id")


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8888)