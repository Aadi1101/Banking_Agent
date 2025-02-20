# src.components/agent.py
from src.utils.llm_manager import get_ollama_llm, get_gemini_llm
from src.utils.vector_db_manager import initialize_vector_store, get_retriever_from_vector_store
from src.components.planner import generate_plan
from src.components.memory import Memory
from src.components.refiner import refine_response
from src.components.goal_manager import GoalManager
# from src.components.tools import create_tools
from langchain.agents import initialize_agent, AgentType

class Agent:
    def __init__(self):
        self.memory = Memory()
        self.goal_manager = GoalManager()
        self.ollama_llm = get_ollama_llm(system_prompt="You are a helpful banking assistant.")
        self.gemini_llm = get_gemini_llm(system_prompt="You are a skilled financial analyst.")  # Initialize Gemini LLM (if available)
        self.vectordb = initialize_vector_store()  # Initialize vector database
        self.retriever = None
        self.tools = None
        self.agent = None

        if self.vectordb:
            self.retriever = get_retriever_from_vector_store(self.vectordb)
            self.tools = create_tools(self.retriever, self.ollama_llm, self.gemini_llm)  # Create tools with retriever.
            if self.tools: # check if tools were created successfully
                self.agent = initialize_agent(self.tools, self.ollama_llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
            else:
                print("Error: Tools could not be initialized.")
        else:
            print("Error: Vector database could not be initialized.")

    def run(self, user_query, user_id):
        self.memory.add_memory(f"User: {user_query}")  # Store user query in memory
        plan = generate_plan(user_query)  # Generate a plan
        self.memory.add_memory(f"Plan: {plan}")  # Store the plan.
        response = ""
        if self.agent:
            try:
                response = self.agent.run(user_query)  # Run the agent.
            except Exception as e:
                response = f"Error running agent: {e}" # handle agent errors.
                print(response)
        else:
            response = "Agent is not initialized. Please check the logs."

        refined_response = refine_response(response, user_query)  # Refine the response
        self.memory.add_memory(f"Assistant: {refined_response}")  # Store refined response
        self.memory.summarize_memory()  # Summarize memory (optional)
        return refined_response

    def set_goal(self, user_id, goal):
        self.goal_manager.set_goal(user_id, goal)
        self.memory.add_memory(f"User {user_id} set goal: {goal}") # add goal to memory.

    def get_goal_status(self, user_id):
        return self.goal_manager.get_goal_status(user_id)

    def update_goal_progress(self, user_id, progress):
        self.goal_manager.update_progress(user_id, progress)
        self.memory.add_memory(f"User {user_id} updated goal progress to: {progress}") # add progress to memory.

    def get_memory(self, query):
        return self.memory.retrieve_memory(query)

    def clear_memory(self):
        self.memory.summarize_memory() #Summarize before clearing.
        self.memory = Memory() #Reinitialize the memory object.

    def add_document(self, document_path):
        if self.vectordb:
            if not self.retriever: # if no retriever exists, create one.
                self.retriever = get_retriever_from_vector_store(self.vectordb)
                self.tools = create_tools(self.retriever, self.ollama_llm, self.gemini_llm)  # Create tools with retriever.
                if self.tools:
                    self.agent = initialize_agent(self.tools, self.ollama_llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
                else:
                    print("Error: Tools could not be initialized.")
            return add_documents_to_vector_store(self.vectordb, document_path)
        return False