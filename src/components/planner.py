from src.utils.llm_manager import get_ollama_llm

def generate_plan(user_query):
    print("USER QUERY: ",user_query)
    planner_llm = get_ollama_llm(system_prompt="""
    You are a task planner. Break down complex user queries into a sequence of actionable sub-tasks.
    Provide the output in a numbered list.
    """)
    prompt = f"User query: {user_query}\nTask breakdown:"
    plan = planner_llm.invoke(prompt)
    print("PLAN: ",plan)
    return plan.split("\n")