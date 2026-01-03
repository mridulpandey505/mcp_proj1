import json
from core.server import MCPServer
from tools.data_tools import query_sales_data
from tools.ml_tools import train_model
from llm_client.groq_client import GroqLLMClient
from functools import partial
from tools.ml_tools import predict_churn

# Load permissions
with open("auth/roles.json") as f:
    permissions = json.load(f)

server = MCPServer(permissions)

# Register tools
server.register_tool(
    name="query_sales_data",
    description="Fetch sales data between two dates",
    handler=query_sales_data,
    input_schema={
        "start_date": "string",
        "end_date": "string"
    }
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
    name = "predict_churn",
    description= "Predict churn using the trained model",
    handler= partial(
        predict_churn,
        dataset_path = "resources/datasets/churn_data.csv"
    ),
    input_schema={}
)


llm = GroqLLMClient(
    mcp_server=server,
    role="ml_engineer"
)

print(llm.ask("okay now  show me the sales data for january 2025"))
print("----")
print(llm.ask("train the churn model"))
print("----")
print(llm.ask("give the predictions of the model"))

# response = server.handle_request(request)
# print(response)
