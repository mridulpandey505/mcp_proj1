class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name, description, handler, input_schema):
        self.tools[name] = {
            "description": description,
            "handler": handler,
            "input_schema": input_schema
        }

    def get(self, name):
        return self.tools.get(name)

    def list_tools(self):
        return list(self.tools.keys())
