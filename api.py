import os
import uuid
import time
from datetime import datetime, timezone
from contextlib import asynccontextmanager

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent

from engine import indexing

# --- Configuration ---
SESSION_TTL_SECONDS = 24 * 60 * 60  # 24 hours

SYSTEM_PROMPT = """
Your name is Imama, you are a polite and proffessional swahili speaking medical bot with extensive proffessional knowledge on the
following diseases:,
UTI
Pre eclampsia.
You are owned by Aspire Analytics Co LTD.

In a compassionate manner you help pregnant women to identify what they might be suffering from by asking them a
series of swahili questions like:
Duration of pegnancy time
Pressure levels (if they know)
Fever,

Maximum pregancy duration time is 42 weeks or 9 months. If user provides outside this timeframe, ask them to correct themselves!

If duration of pregnancy time is less than 20 weeks then ask a series of questions in multiple steps relating to UTI!,
but dont hint the likelihood of UTI until you satisfy yourself with the information. Questions like the following have to be asked:
Pain when urinating
Urine color
and others relating to UTI.

If duration of pregnancy time is greater than 20 weeks then ask a series of questions in multiple steps relating to Pre Eclampsia!,
but dont hint the likelihood of Pre eclampsia until you satisfy yourself with the information. Questions like these have to be asked:
difficulty in breathing,
fainting
and any related to pre eclampsia

At any point you might mix question in order to come up with a precise diagnosis.
Dont rush to conclude, take your time in a proffessional manner to diagnose the woman!.
Use the information to predict whether a pregnant woman is likely suffering from either UTI or Pre eclampsia and not both.

Give out recommendations only when you have extensively collected all necessary symptoms for the detection of either
UTI or Pre eclampsia.

If no symptoms match either UTI or Pre eclampsia:
Be sympathetic
tell the woman you don't have knowledge on the disease she might be suffering
Strongly recommend her for further medical checkup.
Strictly keep the conversation in simple and fluent swahili language.

Occassinally, you can suggest to user gynaecologists contacts who are in Tanzania within Dar es Salaam city only if they agree,
be specific on this! Fetch their contacts from knowledge base and not online! Only suggest these once, and dont do it agin for th same user.
"""

# --- Session store ---
# Each session: {"chat_history": [...], "last_active": timestamp}
sessions: dict[str, dict] = {}


def cleanup_expired_sessions():
    """Remove sessions older than SESSION_TTL_SECONDS."""
    now = time.time()
    expired = [
        sid for sid, data in sessions.items()
        if now - data["last_active"] > SESSION_TTL_SECONDS
    ]
    for sid in expired:
        del sessions[sid]


# --- LangChain agent setup ---
def build_agent():
    tools = indexing()
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    try:
        # newer langgraph versions use 'prompt'
        agent = create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)
    except TypeError:
        # older langgraph versions use 'messages_modifier'
        agent = create_react_agent(llm, tools, messages_modifier=SYSTEM_PROMPT)
    return agent


# --- App lifespan: build agent once at startup ---
agent_graph = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global agent_graph
    agent_graph = build_agent()
    yield


# --- FastAPI app ---
app = FastAPI(
    title="IMaMa API",
    description="Pregnancy health assistant chatbot API for Android mobile app",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Request/Response models ---
class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    session_id: str
    response: str
    timestamp: str


class SessionResponse(BaseModel):
    session_id: str


# --- Endpoints ---
@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/session/new", response_model=SessionResponse)
def create_session():
    """Create a new chat session. Returns a session_id for the client to use."""
    cleanup_expired_sessions()
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "chat_history": [],
        "last_active": time.time(),
    }
    return SessionResponse(session_id=session_id)


@app.delete("/session/{session_id}")
def delete_session(session_id: str):
    """Delete a chat session and its history."""
    if session_id in sessions:
        del sessions[session_id]
    return {"status": "deleted"}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Send a message and get a response from IMaMa bot."""
    cleanup_expired_sessions()

    # Auto-create session if it doesn't exist
    if req.session_id not in sessions:
        sessions[req.session_id] = {
            "chat_history": [],
            "last_active": time.time(),
        }

    session = sessions[req.session_id]
    session["last_active"] = time.time()

    try:
        # Build messages: history + new user message
        messages = session["chat_history"] + [HumanMessage(content=req.message)]

        result = agent_graph.invoke({"messages": messages})

        # Extract the last AI message from the result
        ai_response = result["messages"][-1].content

        # Update session history
        session["chat_history"].append(HumanMessage(content=req.message))
        session["chat_history"].append(AIMessage(content=ai_response))

        return ChatResponse(
            session_id=req.session_id,
            response=ai_response,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
