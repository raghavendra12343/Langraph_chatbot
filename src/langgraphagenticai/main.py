import streamlit as st
import uuid 
from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI ## taking and loading theui 
# {'selected_llm': 'Groq', 'selected_groq_model': 'openai/gpt-oss-120b',
#  'GROQ_API_KEY': '',
#  'selected_usecase': 'Basic Chatbot'}
from src.langgraphagenticai.LLMS.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlitui.display_result import DisplayResultStreamlit
from langgraph.checkpoint.memory import MemorySaver


def load_langgraph_agenticai_app():
    """
    Loads and runs the LangGraph AgenticAI application with Streamlit UI.
    This function initializes the UI, handles user input, configures the LLM model,
    sets up the graph based on the selected use case, and displays the output while 
    implementing exception handling for robustness.

    """

    ## loading ui and the user input we can track here llm and api keys
    ui=LoadStreamlitUI()
    user_input=ui.load_streamlit_ui()
    usecase=user_input.get("selected_usecase")
    # thread_id=f"{usecase}_{str(uuid.uuid4())}"
    # thread level funtionality

    if "thread_id" not in st.session_state:
       st.session_state.thread_id = f"{usecase}_{uuid.uuid4()}"
    thread_id = st.session_state.thread_id

    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return
    
    # Text input for user message
    if st.session_state.IsFetchButtonClicked:
        user_message = st.session_state.timeframe 
    else :
        user_message = st.chat_input("Enter your message:")

    if user_message:
        try:
            ## Configure The LLM's
            obj_llm_config=GroqLLM(user_contols_input=user_input)
            model=obj_llm_config.get_llm_model()
            ## getting the model based on user inputs which are selected from the console
            if not model:
                st.error("Error: LLM model could not be initialized")
                return
            
            # Initialize and set up the graph based on use case
            usecase=user_input.get("selected_usecase")

            if not usecase:
                    st.error("Error: No use case selected.")
                    return
            
            ## Graph Builder
            ## here model is used to pass to  graph intial check 
            if "memory" not in st.session_state: 
                st.session_state.memory = MemorySaver()
            memory = st.session_state.memory
            graph_builder=GraphBuilder(model,thread_id,memory)
            
            try:
                 graph=graph_builder.setup_graph(usecase)
                 print(user_message)
                 DisplayResultStreamlit(usecase,graph,user_message,thread_id).display_result_on_ui()
            except Exception as e:
                 print(f"Error: Graph set up failed- {e}")
                 st.error(f"Error: Graph set up failed- {e}")
                 return

        except Exception as e:
             print(f"Error: Graph set up failed- {e}")
             st.error(f"Error: Graph set up failed- {e}")
             return   
