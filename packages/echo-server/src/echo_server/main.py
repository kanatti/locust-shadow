from fastapi import FastAPI, Query
from pydantic import BaseModel
import json
import asyncio

app = FastAPI()

class EchoResponse(BaseModel):
    data: dict

@app.get("/echo", response_model=EchoResponse)
async def echo(data: str = Query(...), delay_ms: int = Query(0, ge=0, le=60000)):
    try:
        json_data = json.loads(data)
        if delay_ms > 0:
            await asyncio.sleep(delay_ms / 1000)
        return {"data": json_data}
    except json.JSONDecodeError:
        return {"data": {"error": "Invalid JSON"}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)