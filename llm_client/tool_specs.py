TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "query_sales_data",
            "description": "Fetch sales data between two dates",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_date": {"type": "string"},
                    "end_date": {"type": "string"}
                },
                "required": ["start_date", "end_date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "train_model",
            "description": "Train a churn prediction model",
            "parameters": {
                "type": "object",
                "properties": {
                   
                },
               
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "predict_churn",
            "description": "Predict customer churn using trained model",
            "parameters": {
            "type": "object",
            "properties": {}
    }
  }
}
]
