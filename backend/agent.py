import os
import datetime
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from calendar_tool import create_event, check_availability
from dateparser.search import search_dates

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("Missing GOOGLE_API_KEY in environment variables!")

# ✅ Parse natural language to datetime
def parse_datetime(text: str):
    print(f"📥 Input: {text}")
    results = search_dates(
        text,
        settings={
            'PREFER_DATES_FROM': 'future',
            'TIMEZONE': 'Asia/Kolkata',
            'RETURN_AS_TIMEZONE_AWARE': True
        }
    )
    if results:
        parsed = results[0][1]
        print(f"🕒 Parsed: {parsed}")
        return parsed
    print("❌ No date found")
    return None

# ✅ Extract basic event title (like "dinner", "meeting", etc.)
def extract_event_title(text: str):
    keywords = ["meeting", "appointment", "call", "party", "dinner", "lunch", "hangout", "reservation"]
    for keyword in keywords:
        if keyword in text.lower():
            return keyword.capitalize()
    return "AI Booking"  # default title

# ✅ Tool to book appointment with suggestions
def book_appointment_tool(input_text: str) -> str:
    parsed_time = parse_datetime(input_text)
    if not parsed_time:
        return "❌ I couldn't understand the requested time. Please try something like 'Tomorrow at 3 PM'."

    title = extract_event_title(input_text)
    start_time = parsed_time
    end_time = start_time + datetime.timedelta(minutes=30)

    print(f"🔍 Trying to book from {start_time} to {end_time} for: {title}")
    print(f"🔍 Checking availability from {start_time} to {end_time}")

    if check_availability(start_time, end_time):
        link = create_event(title, start_time, end_time)
        return f"✅ Booking confirmed!\n📅 {start_time.strftime('%A, %d %B %Y at %I:%M %p')}\n🔗 {link}"

    # Suggest next 3 available 30-minute slots
    suggestions = []
    for i in range(1, 6):
        alt_start = start_time + datetime.timedelta(minutes=30 * i)
        alt_end = alt_start + datetime.timedelta(minutes=30)
        if check_availability(alt_start, alt_end):
            suggestions.append(alt_start.strftime('%A, %d %B %Y at %I:%M %p'))
        if len(suggestions) == 3:
            break

    print(f"📆 Suggestions: {suggestions}")

    if suggestions:
        return (
            "❌ That time slot is unavailable.\n"
            "✅ Here are the next available options:\n" +
            "\n".join([f"- {s}" for s in suggestions])
        )
    else:
        return "❌ That time is unavailable, and no alternative slots found in the next few hours."


# ✅ Define tools
tools = [
    Tool(
        name="book_appointment",
        func=book_appointment_tool,
        description="Use this tool to book an appointment when the user requests a specific date/time.",
    )
]

# ✅ Gemini LLM setup
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    google_api_key=GOOGLE_API_KEY
)

# ✅ Initialize Agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)
