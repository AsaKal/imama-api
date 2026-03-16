# IMaMa Chatbot API Documentation

Base URL (after deployment): `https://<your-render-service>.onrender.com`

---

## Endpoints

### 1. Health Check

Check if the API is running.

```
GET /health
```

**Response** `200 OK`
```json
{
  "status": "ok"
}
```

---

### 2. Create New Session

Call this when a user opens the app or starts a new conversation. Store the returned `session_id` on the device and send it with every chat request.

```
POST /session/new
```

**Request body:** none

**Response** `200 OK`
```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

**Android (Kotlin) example:**
```kotlin
val response = client.post("$BASE_URL/session/new")
val sessionId = response.body<SessionResponse>().session_id
// Save sessionId in SharedPreferences or ViewModel
```

---

### 3. Send Message (Chat)

Send a user message and get the bot's reply. The bot maintains conversation context using the session_id.

```
POST /chat
```

**Request headers:**
```
Content-Type: application/json
```

**Request body:**
```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "message": "Habari, nina miezi 6 ya ujauzito"
}
```

| Field        | Type   | Required | Description                              |
|-------------|--------|----------|------------------------------------------|
| session_id  | string | Yes      | The session ID from `/session/new`       |
| message     | string | Yes      | The user's message text (in Swahili)     |

**Response** `200 OK`
```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "response": "Habari! Pole kwa usumbufu. Hebu niulize maswali machache...",
  "timestamp": "2026-03-16T10:30:00.000000+00:00"
}
```

| Field       | Type   | Description                                |
|------------|--------|--------------------------------------------|
| session_id | string | Echo of the session ID                     |
| response   | string | The bot's reply (in Swahili)               |
| timestamp  | string | ISO 8601 UTC timestamp of the response     |

**Error** `500`
```json
{
  "detail": "error description"
}
```

**Android (Kotlin) example:**
```kotlin
val response = client.post("$BASE_URL/chat") {
    contentType(ContentType.Application.Json)
    setBody(ChatRequest(session_id = sessionId, message = userMessage))
}
val botReply = response.body<ChatResponse>().response
```

---

### 4. Delete Session

Call this when the user logs out or wants to clear conversation history.

```
DELETE /session/{session_id}
```

**Response** `200 OK`
```json
{
  "status": "deleted"
}
```

---

## Typical Flow

```
App opens
   │
   ▼
POST /session/new  ──►  save session_id locally
   │
   ▼
User types message
   │
   ▼
POST /chat { session_id, message }  ──►  display response
   │
   ▼
(repeat for each message)
   │
   ▼
User closes app / logs out
   │
   ▼
DELETE /session/{session_id}  (optional, sessions expire after 24h)
```

---

## Notes for Android Developer

1. **Session persistence**: Store `session_id` in `SharedPreferences` so the conversation survives app restarts. Sessions expire after 24 hours of inactivity on the server.

2. **Timeout**: Bot responses may take 5-15 seconds depending on the complexity of the query. Set your HTTP client timeout to at least **30 seconds**.

3. **Error handling**: On `500` errors, show a generic error message to the user. On network errors, allow retry.

4. **Language**: The bot speaks Swahili. Send messages in Swahili for best results.

5. **New conversation**: To start a fresh conversation (e.g., "New Chat" button), call `POST /session/new` to get a new `session_id`.

6. **Interactive docs**: After deployment, visit `https://<your-service>.onrender.com/docs` for Swagger UI where you can test all endpoints interactively.

---

## Data Models (for Kotlin/Java)

```kotlin
// Request
data class ChatRequest(
    val session_id: String,
    val message: String
)

// Response
data class ChatResponse(
    val session_id: String,
    val response: String,
    val timestamp: String
)

// Session
data class SessionResponse(
    val session_id: String
)
```
