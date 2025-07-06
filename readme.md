appointment_bot/
│
├── backend/
│   ├── main.py         # FastAPI app
│   └── calendar_tool.py  # Calendar integration
│
├── frontend/
│   └── app.py          # Streamlit chat interface
│
├── agent/
│   └── agent.py        # Langchain or LangGraph agent logic
│
├── service_account.json  # Your Google Calendar key
├── requirements.txt
└── README.md

python -m streamlit run app.py