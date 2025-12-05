from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode

def get_tools():
    """
    Return the list of tools to be used in the chatbot
    """
    tools=[TavilySearchResults(max_results=5)]
    return tools
def get_imdb_tools():
    """
    Return the list of tools to be used in the chatbot
    """
    tools=[ TavilySearchResults(
    max_results=5,
    topic="general",
    include_images=True,
    search_depth="advanced",
     description="""
    A search tool for retrieving IMDB IDs and movie/show details.
    Always start the query with the exact content name if available.
    If the content name may not match perfectly (due to dubbing, alternate titles, 
    or spelling variations), expand the search by including the director and cast.
    Focus only on results from site:imdb.com and always extract the IMDB ID (ttXXXXXXX).
    """ ) ]
    return tools

def create_tool_node(tools):
    """
    creates and returns a tool node for the graph
    """
    return ToolNode(tools=tools)

