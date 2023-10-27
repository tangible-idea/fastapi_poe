from fastapi_poe.types import ProtocolMessage
from fastapi_poe.client import get_bot_response
import asyncio
from fastapi import FastAPI, APIRouter
import uvicorn

app = FastAPI()
concated= ""

# router = APIRouter()
# router.add_api_route('/api/v2/hello-world', 
# endpoint = HelloWorld().read_hello, methods=["GET"])
# app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/gpt3")
async def call_gpt3(request: str, apikey: str):
    global concated # 전역변수 사용

    await concat_message(apikey, request, "GPT-3.5-Turbo")
    return {"message": concated}

@app.get("/gpt4/{request}")
async def call_gpt4(request: str, apikey: str):
    global concated # 전역변수 사용

    await concat_message(apikey, request, "GPT-4.0")
    return {"message": concated}

@app.get("/bot/{botname}")
async def call_bot(botname: str, request: str, apikey: str):
    global concated # use global variable

    await concat_message(apikey, request, botname)
    return {"message": concated}

async def concat_message(apikey, request, botname):
    global concated # use global variable
    concated= "" # 초기화

    message = ProtocolMessage(role="user", content=request)
    async for partial in get_bot_response(messages=[message], bot_name=botname, api_key=apikey): 
        #print(partial.text, end='')
        concated = concated + partial.text

if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)