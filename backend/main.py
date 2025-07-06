from fastapi import FastAPI, Request
from agent import agent

app = FastAPI()

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message", "")
    print(f"📩 User input: {user_input}")

    try:
        response = agent.invoke(user_input)
        print(f"🤖 Bot response: {response}")
        return {"response": response}
    except Exception as e:
        print(f"❌ Error during agent response: {e}")
        return {"response": f"❌ Error processing request: {str(e)}"}


@app.get("/")
def read_root():
    return {"message": "🤖 AI Appointment Bot is running!"}

