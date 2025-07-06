from fastapi import FastAPI, Request
from agent import agent

app = FastAPI()

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message", "")
    response = agent.invoke(user_input)
    return {"response": response}

@app.get("/")
def read_root():
    return {"message": "🤖 AI Appointment Bot is running!"}

