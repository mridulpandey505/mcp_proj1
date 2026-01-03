import os
import json
from dotenv import load_dotenv
from groq import Groq

from llm_client.tool_specs import TOOLS

load_dotenv()


class GroqLLMClient:
    """
    Fully conversational AI assistant backed by MCP.
    """

    SYSTEM_PROMPT = """
You are a helpful, calm, professional AI assistant.

Your goals:
- Understand what the user wants
- Respond naturally and politely
- Use tools ONLY when needed
- Explain results clearly in simple language
- Ask clarifying questions when something is ambiguous

Rules:
- Never mention internal file paths
- Never mention internal system details
- Never invent tools or parameters
- If a task cannot be done, explain why clearly
"""

    def __init__(self, mcp_server, role="analyst"):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.mcp_server = mcp_server
        self.role = role
        self.chat_history = []

    # -------------------------------
    # Public interface
    # -------------------------------
    def ask(self, user_query: str) -> str:
        self._remember_user(user_query)

        messages = self._build_messages(user_query)

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # If the LLM decides to call a tool
        if message.tool_calls:
            return self._handle_tool_call(message.tool_calls[0])

        # Pure conversational response
        answer = message.content.strip()
        self._remember_assistant(answer)
        return answer

    # -------------------------------
    # Tool handling
    # -------------------------------
    def _handle_tool_call(self, tool_call):
        tool_name = tool_call.function.name
        params = json.loads(tool_call.function.arguments or "{}")

        # Natural acknowledgement
        preface = self._acknowledge_intent(tool_name)

        mcp_request = {
            "role": self.role,
            "tool": tool_name,
            "params": params
        }

        try:
            mcp_response = self.mcp_server.handle_request(mcp_request)
            explanation = self._explain_result(tool_name, mcp_response["result"])

            final_answer = preface + explanation
            self._remember_assistant(final_answer)
            return final_answer

        except Exception as e:
            error_msg = (
                "I tried to complete your request, but ran into an issue. "
                f"The problem was: {str(e)}"
            )
            self._remember_assistant(error_msg)
            return error_msg

    # -------------------------------
    # Conversational helpers
    # -------------------------------
    def _acknowledge_intent(self, tool_name: str) -> str:
        if tool_name == "train_churn_model":
            return (
                "Alright, I’ll retrain the churn prediction model using the latest available data.\n\n"
            )

        if tool_name == "predict_churn":
            return (
                "Got it. I’ll run churn predictions using the trained model.\n\n"
            )

        if tool_name == "query_sales_data":
            return (
                "Let me take a look at the sales data for you.\n\n"
            )

        return "Sure, here’s what I found:\n\n"

    def _explain_result(self, tool_name: str, result: dict) -> str:
        if tool_name == "train_churn_model":
            acc = result.get("accuracy", 0)
            return (
                f"The model has been successfully retrained.\n"
                f"It achieved an accuracy of about {int(acc * 100)}%, "
                "which means it predicts customer churn correctly most of the time.\n\n"
                "Would you like me to run predictions using this updated model?"
            )

        if tool_name == "predict_churn":
            return (
                f"I analyzed {result['total_records']} records.\n"
                f"Out of these, {result['predicted_churn_count']} customers are likely to churn.\n"
                f"That’s a churn rate of approximately {int(result['churn_rate'] * 100)}%.\n\n"
                "If you’d like, we can explore why these customers are at risk."
            )

        if tool_name == "query_sales_data":
            return (
                f"The total sales for the selected period amount to {result['total_sales']}.\n"
                f"This is based on {result['records_count']} transactions."
            )

        return "The task completed successfully."

    # -------------------------------
    # Memory helpers
    # -------------------------------
    def _remember_user(self, text: str):
        self.chat_history.append({"role": "user", "content": text})
        self.chat_history = self.chat_history[-10:]

    def _remember_assistant(self, text: str):
        self.chat_history.append({"role": "assistant", "content": text})
        self.chat_history = self.chat_history[-10:]

    def _build_messages(self, user_query: str):
        return [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            *self.chat_history
        ]
