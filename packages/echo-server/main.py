from fastapi import FastAPI, Query
from pydantic import BaseModel
import json

app = FastAPI()

class EchoResponse(BaseModel):
    data: dict

@app.get("/echo", response_model=EchoResponse)
async def echo(data: str = Query(...)):
    try:
        json_data = json.loads(data)
        return {"data": json_data}
    except json.JSONDecodeError:
        return {"data": {"error": "Invalid JSON"}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
