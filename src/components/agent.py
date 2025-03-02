import os
from dotenv import load_dotenv
from src.utils.llm_manager import get_ollama_llm, get_gemini_llm
from src.utils.vector_db_manager import initialize_vector_store, get_retriever_from_vector_store, add_documents_to_vector_store
from src.components.planner import generate_plan
from src.components.memory import Memory
from src.components.refiner import refine_response
from src.components.create_tools import create_tools
from langchain.agents import initialize_agent, AgentType, AgentExecutor
from src.logger import logging
from src.utils.config import get_config

load_dotenv()

class Agent:
    def __init__(self):
        """Initializes the AI Banking Assistant Agent."""
        try:
            logging.info("🔹 Initializing Memory...")
            self.memory = Memory()
            logging.info("✅ Memory Initialized Successfully!")

            self.overall_goal = get_config("AGENT_OVERALL_GOAL")
            self.agent_ollama_prompt = get_config("AGENT_OLLAMA_PROMPT")
            self.agent_gemini_prompt = get_config("AGENT_GEMINI_PROMPT")
            if not self.overall_goal:
                raise ValueError("❌ Error: AGENT_OVERALL_GOAL environment variable not set.")

            logging.info("🔹 Initializing LLMs...")
            self.ollama_llm = get_ollama_llm(system_prompt=self.agent_ollama_prompt)
            self.gemini_llm = get_gemini_llm(system_prompt=self.agent_gemini_prompt)
            logging.info("✅ LLMs Initialized.")

            logging.info("🔹 Initializing Vector Store...")
            self.vectordb = initialize_vector_store()
            if not self.vectordb:
                logging.info("⚠️ Warning: Vector store could not be initialized.")

            self.retriever = get_retriever_from_vector_store(self.vectordb) if self.vectordb else None

            logging.info("🔹 Creating Tools...")
            self.tools = create_tools(self.retriever, self.ollama_llm, self.gemini_llm) if self.retriever else []
            if self.tools:
                logging.info("✅ Tools Created Successfully!")

            if self.tools:
                self.agent = initialize_agent(self.tools, self.ollama_llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, handle_parsing_errors=True)
                self.agent_executor = AgentExecutor.from_agent_and_tools(
                    agent=self.agent,
                    tools=self.tools,
                    verbose=True,
                    max_execution_time=600,  # Set timeout to 120 seconds (adjust as needed)
                    handle_parsing_errors=True
                )
            else:
                logging.info("⚠️ Warning: Agent not initialized (Missing Tools).")
                self.agent_executor = None

        except Exception as e:
            logging.info(f"❌ Error initializing Agent: {e}")
            self.agent_executor = None

    def run(self, user_query, user_id):
        """Processes user queries and generates responses."""
        try:
            self.memory.add_memory(f"User: {user_query}")
            plan = generate_plan(user_query)
            logging.info("Generated Plan: ",plan)
            self.memory.add_memory(f"Plan: {plan}")

            final_result = ""  # Initialize the final result variable
            if self.agent:
                response = self.agent.run(user_query)
                final_result += response  # Append the response
                logging.info("After running successfully Agent Executor appending the final result: ",response)
            else:
                final_result = "⚠️ Agent not initialized or missing tools."

            refined_response = refine_response(final_result, user_query)  # Pass the final result
            logging.info("Refining the response and summarizing it: ",refined_response)
            self.memory.add_memory(f"Assistant: {refined_response}")
            self.memory.summarize_memory()
            logging.info("Refining the response and summarizing it: ",refined_response)
            return refined_response

        except Exception as e:
            return f"❌ Error processing request: {e}"

    def add_document(self, document_path):
        """Adds a new document to the vector database."""
        try:
            if not self.vectordb:
                logging.info("❌ Error: Vector store not initialized.")
                return False

            if not self.retriever:
                logging.info("ℹ️ Reinitializing retriever...")
                self.retriever = get_retriever_from_vector_store(self.vectordb)
                self.tools = create_tools(self.retriever, self.ollama_llm, self.gemini_llm)
                if self.tools:
                    self.agent = initialize_agent(self.tools, self.ollama_llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, handle_parsing_errors=True)
                    self.agent_executor = AgentExecutor.from_agent_and_tools(
                        agent=self.agent.agent,
                        tools=self.tools,
                        verbose=True,
                        max_execution_time=600,
                        handle_parsing_errors=True
                    )
                else:
                    self.agent_executor=None

            return add_documents_to_vector_store(self.vectordb, document_path)

        except Exception as e:
            logging.info(f"❌ Error adding document: {e}")
            return False