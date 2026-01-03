from llm_client.groq_client import GroqLLMClient
from core.server import MCPServer
from tools.data_tools import query_sales_data
from tools.ml_tools import train_model, predict_churn
from functools import partial
import json


with open("auth/roles.json") as f:
    permissions = json.load(f)

server = MCPServer(permissions)


server.register_tool(
    name="query_sales_data",
    description="Fetch sales data between two dates",
    handler=query_sales_data,
    input_schema={}
)

server.register_tool(
    name="train_model",
    description="Train churn model on internal dataset",
    handler=partial(
        train_model,
        dataset_path="resources/datasets/churn_data.csv"
    ),
    input_schema={}
)

server.register_tool(
    name="predict_churn",
    description="Predict churn using trained model",
    handler=partial(
        predict_churn,
        dataset_path="resources/datasets/churn_data.csv"
    ),
    input_schema={}
)

assistant = GroqLLMClient(
    mcp_server=server,
    role="ml_engineer"
)


def run_chat():
    print("\nConversational AI Assistant")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() in {"exit", "quit"}:
                print("\nAI: Goodbye!")
                break

            if not user_input:
                continue

            response = assistant.ask(user_input)
            print(f"\nAI: {response}\n")

        except KeyboardInterrupt:
            print("\nAI: Chat ended.")
            break

        except Exception as e:
            print(f"\n Error: {str(e)}\n")


if __name__ == "__main__":
    run_chat()
