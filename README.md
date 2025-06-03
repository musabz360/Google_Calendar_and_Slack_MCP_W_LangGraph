# Google Calendar & Slack MCP Agent (LangGraph)

This project is a starter template for building a custom Reasoning and Action agent using [LangGraph](https://github.com/langchain-ai/langgraph). The agent integrates with Google Calendar and Slack via MCP (Model Context Protocol) for advanced scheduling and communication automation.

---

## Setup Instructions

### 1. Clone the Repository

```powershell
git clone <your-repo-url>
cd Google_Calendar_and_Slack_MCP_W_LangGraph
```

### 2. Create and Activate a Virtual Environment

```powershell
python -m venv .venv
.venv\Scripts\Activate
```

### 3. Install Dependencies

```powershell
pip install -e .
```

---

## Google Cloud Console Setup

1. **Go to [Google Cloud Console](https://console.cloud.google.com/)**
2. **Create a new project** or select an existing one.
3. **Enable the Gmail API and Google Calendar API:**
   - Go to `APIs & Services` > `Library`
   - Search for and enable **Gmail API**
   - Search for and enable **Google Calendar API**
4. **Set up OAuth 2.0 credentials:**
   - Go to `APIs & Services` > `Credentials`
   - Click `Create Credentials` > `OAuth client ID`
   - Choose `Web application`
   - Set `Authorized redirect URIs` to include:  
     `http://localhost:4100/code`
   - Note down the **Client ID** and **Client Secret**

---

## Generating a Refresh Token

1. Add your OAuth credentials to `credentials.json` in the project root:

    ```json
    {
      "web": {
        "client_id": "<YOUR_CLIENT_ID>",
        "client_secret": "<YOUR_CLIENT_SECRET>",
        "redirect_uris": ["http://localhost:4100/code"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token"
      }
    }
    ```

2. Run the refresh token script:

    ```powershell
    node get-refresh-token.js
    ```

   This will create a `token.json` file containing your refresh token.

---

## Integrating with Smithery MCP

1. Go to [Smithery GSuite MCP Server](https://smithery.ai/server/@rishipradeep-think41/gsuite-mcp)
2. In the **Install** section, update the URL with your:
   - `googleClientId`
   - `googleClientSecret`
   - `googleRefreshToken` (from `token.json`)
3. Copy the generated URL.
4. In [`src/base_agent/graph.py`](src/base_agent/graph.py), update the `google_calendar` URL in the `MultiServerMCPClient` config with your new URL.

---

## Running the Agent

You can now use the agent as designed, with full Google Calendar and Slack integration via MCP.

---

## LangGraph Studio (Development UI)

To launch the LangGraph Studio development interface, run the following command in your project directory:

```powershell
langgraph dev --allow-blocking
```

This will start the LangGraph Studio UI, allowing you to visually inspect and interact with your agent's graph and execution flow.

---

## Environment Variables (.env)

This project uses a `.env` file to manage sensitive credentials and configuration. You must create a `.env` file in the project root (or copy from `.env.example`) and provide the following variables:

- `OPENAI_API_KEY` — Your OpenAI API key for LLM access
- `LANGCHAIN_TRACING_V2` — Set to `true` to enable LangSmith tracing
- `LANGCHAIN_API_KEY` — Your LangSmith API key
- `LANGCHAIN_PROJECT` — The LangSmith project name

Optional (for Google/VertexAI):
- `GOOGLE_GENAI_USE_VERTEXAI` — Set to `"True"` to use VertexAI
- `GOOGLE_APPLICATION_CREDENTIALS` — Path to your Google service account JSON
- `GOOGLE_CLOUD_PROJECT` — Your Google Cloud project ID
- `GOOGLE_CLOUD_LOCATION` — Your Google Cloud region

See `.env.example` for a template.

---
