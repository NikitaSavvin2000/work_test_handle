import os
import json
import uvicorn
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.config import logger, public_or_local


home_path = os.getcwd()

sem_map_path = f"{home_path}/src/materials/not_and_numeric_year_sem.render.json"
trend_map_path = f"{home_path}/src/materials/not_and_numeric_year_trend.render.json"


if public_or_local == 'LOCAL':
    url = 'http://localhost'
else:
    url = 'http://11.11.11.11'

origins = [
    url
]

app = FastAPI(docs_url="/template_fast_api/v1/", openapi_url='/template_fast_api/v1/openapi.json')
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_json_from_file(file_path: str):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"File not found: {file_path}",
            headers={"X-Error": f"File not found: {file_path}"},
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Error decoding JSON",
            headers={"X-Error": "Error decoding JSON"},
        )


@app.post("/template_fast_api/v1/sem_map")
async def get_sem_map():
    return JSONResponse(content=load_json_from_file(sem_map_path))


@app.post("/template_fast_api/v1/trend_map")
async def get_trend_map():
    return JSONResponse(content=load_json_from_file(trend_map_path))

@app.get("/")
def read_root():
    return {"message": "Welcome to the indicators System API"}


if __name__ == "__main__":
    port = 7070
    uvicorn.run(app, host="0.0.0.0", port=port)
    docs = 'http://0.0.0.0:7070/template_fast_api/v1/'
