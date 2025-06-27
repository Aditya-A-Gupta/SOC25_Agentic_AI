from langgraph.graph import StateGraph, END
from typing import List, TypedDict, Annotated, Any
import operator
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# State types
class PlannerState(TypedDict):
    tasks: List[str]

class DeveloperState(TypedDict):
    changes: List[str]
    logs: List[str]

class OverallState(TypedDict):
    planner: Annotated[PlannerState, lambda x, y: {**x, **y}]
    developer: Annotated[DeveloperState, lambda x, y: {**x, **y}]
    logs: Annotated[List[str], operator.add]

# Planner Agent
class PlannerAgent:
    def __init__(self):
        self.logs = []
    
    def plan(self, task: str) -> List[str]:
        self.logs.append(f"📝 Planning task: {task}")
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            f"""You are a task planner. Break this task into 2-3 actionable steps.
            Return ONLY the steps as a bullet list. Do not include any explanations.
            
            Task: {task}"""
        )
        steps_text = response.text.strip()
        steps = [line.strip('-* ').strip() for line in steps_text.split('\n') if line.strip()]
        self.logs.append(f"Generated steps: {steps}")
        return steps[:3]

# Developer Agent
class DeveloperAgent:
    def __init__(self):
        self.logs = []
    
    def apply_changes(self, steps: List[str]) -> List[str]:
        changes = []
        for step in steps:
            self.logs.append(f"⚙️ Applying: {step}")
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(
                f"""You are a developer. Write code to implement this step.
                Return ONLY the code. Do not include explanations.
                
                Step: {step}"""
            )
            code = response.text.strip()
            changes.append(code)
            self.logs.append(f"✅ Completed: {step}\nCode:\n{code}")
        return changes

# Node functions
def planner_node(state: OverallState) -> dict:
    planner = PlannerAgent()
    task = state['planner']['tasks'][0]
    steps = planner.plan(task)
    return {
        "planner": {"tasks": steps},
        "logs": planner.logs
    }

def developer_node(state: OverallState) -> dict:
    developer = DeveloperAgent()
    steps = state['planner']['tasks']
    changes = developer.apply_changes(steps)
    return {
        "developer": {
            "changes": changes,
            "logs": developer.logs
        }
    }

# Build and run the graph
graph = StateGraph(OverallState)
graph.add_node("planner", planner_node)
graph.add_node("developer", developer_node)
graph.set_entry_point("planner")
graph.add_edge("planner", "developer")
graph.add_edge("developer", END)
app = graph.compile()

initial_state = OverallState(
    planner={"tasks": ["Create LangGraph agents with Gemini integration"]},
    developer={"changes": [], "logs": []},
    logs=[]
)
result = app.invoke(initial_state)

print("\n" + "="*50)
print("FINAL STATE:")
print(f"Planner tasks: {result['planner']['tasks']}")
print(f"Developer changes: {result['developer']['changes']}")
print("\nEXECUTION LOGS:")
for log in result['logs']:
    print(f"- {log}")
