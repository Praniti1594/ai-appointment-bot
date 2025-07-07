import streamlit as st
import requests

st.set_page_config(page_title="AI Appointment Booking", page_icon="📅")
st.title("🤖📅 AI Appointment Booking Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("💬 Ask me to book an appointment (e.g., 'Book a meeting for tomorrow at 5 PM')")

if st.button("Send"):
    if user_input.strip():
        # Append user input to chat
        st.session_state.chat_history.append(("You", user_input))

        # Call FastAPI backend
        try:
            response = requests.post("https://ai-appointment-bot-3.onrender.com/chat", json={"message": user_input}, timeout=30)

            response.raise_for_status()
            bot_reply = response.json().get("response", "🤖 No response from bot.")
        except requests.exceptions.RequestException as e:
            bot_reply = f"⚠️ Network error: {e}"
        except ValueError:
            bot_reply = "⚠️ Error: Received invalid JSON from backend."

        # Append bot response to chat
        st.session_state.chat_history.append(("Bot", bot_reply))

# Show chat history
for speaker, message in st.session_state.chat_history:
    st.write(f"**{speaker}:** {message}")
