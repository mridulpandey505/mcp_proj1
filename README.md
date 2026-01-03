This project implements a terminal-based conversational AI assistant that can safely interact with real data and machine learning pipelines using Model Context Protocol (MCP) principles.

Unlike typical chatbots, this assistant separates natural language reasoning from execution, ensuring that all real-world actions are performed securely and deterministically.

  🧠 Key Idea

The LLM reasons. The MCP server executes.

The LLM handles conversation, intent understanding, and explanations

The MCP server controls all execution (data access, ML training, prediction)

Sensitive resources (datasets, models) are never exposed to the LLM

This prevents hallucinated actions, unsafe file access, and unintended execution.

✨ Features

💬 Natural, conversational terminal-based assistant

🔒 Secure MCP-based tool execution

🧠 LLM cannot access files, models, or schemas directly

📊 Data querying from CSV datasets

🤖 ML lifecycle support:

Train churn prediction model

Predict churn using trained model

🛑 Hallucination-resistant design

👥 Role-based access control for tools

🛠️ Tech Stack

Python

Groq API (LLaMA-3)

Model Context Protocol (MCP – architectural pattern)

Pandas, Scikit-learn

Terminal-based interface
