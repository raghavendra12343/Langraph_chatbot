from src.langgraphagenticai.state.state import State
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage

class ChatbotWithToolNode:
    """
    Chatbot logic enhanced with tool integration.
    """
    def __init__(self,model):
        self.llm = model

    def process(self, state: State) -> dict:
        """
        Processes the input state and generates a response with tool integration.
        """
        user_input = state["messages"][-1] if state["messages"] else ""
        llm_response = self.llm.invoke([{"role": "user", "content": user_input}])

        # Simulate tool-specific logic
        tools_response = f"Tool integration for: '{user_input}'"

        return {"messages": [llm_response, tools_response]}
    

    def create_chatbot(self, tools):
        """
        Returns a chatbot node function.
        """
        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state: State):
            """
            Chatbot logic for processing the input state and returning a response.
            """
            return {"messages": [llm_with_tools.invoke(state["messages"])]}
        return chatbot_node
    
    def create_imdb_chatbot(self, tools):
        """
        Returns a chatbot node function.
        """
        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state: State):
            messages=state["messages"]
            system = SystemMessage(
            content="""You are an IMDB search assistant.
                    When asked for IMDB IDs:
                1. USE the web_search tool
                2. Search for: 'movie_name cast director IMDB site:imdb.com'
                3. Extract the IMDB ID (ttXXXXXXX) from results
                4. Never say you cannot do this - you have the tools!""")

            if not any(isinstance(m, SystemMessage) for m in messages):
                messages = [system] + messages
                print(messages)
        
            """
            Chatbot logic for processing the input state and returning a response.
            """
            return {"messages": [llm_with_tools.invoke(messages)]}
        return chatbot_node

