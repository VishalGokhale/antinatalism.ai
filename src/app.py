# this is main fastapi app
# generate a skeleton for this app
# this app should have 1 endpoint /chat-with-david that accepts a json payload with following keys
# query-for-david: string
# chat-history: list of strings

# this app should have a function that takes the query-for-david and chat-history and returns a response


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn

from core_functions import generate_david_response


class ChatWithDavidRequest(BaseModel):
    query_for_david: str
    chat_history: List[str]


class ChatWithDavidResponse(BaseModel):
    response: str


def chat_with_david(request: ChatWithDavidRequest) -> ChatWithDavidResponse:
    david_benatar_response = generate_david_response(request.query_for_david, request.chat_history)
    return ChatWithDavidResponse(response=david_benatar_response)


if __name__ == '__main__':
    app = FastAPI()

    from dotenv import load_dotenv
    load_dotenv()

    @app.post("/chat-with-david")
    def chat_with_david_endpoint(request: ChatWithDavidRequest):
        try:
            response = chat_with_david(request)
            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


    uvicorn.run(app, host="localhost", port=9000)
