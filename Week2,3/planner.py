from langgraph.graph import StateGraph, END
from typing import List, TypedDict, Annotated
import operator
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class PlannerState(TypedDict):
    tasks: List[str]

class DeveloperState(TypedDict):
    changes: List[str]
    logs: List[str]

class OverallState(TypedDict):
    planner: Annotated[PlannerState, operator.add]
    developer: Annotated[DeveloperState, operator.add]

# Planner Agent Implementation
class PlannerAgent:
    def __init__(self):
        self.logs = []
    
    def internal_search(self, query: str) -> List[str]:
        """Mock internal knowledge base search"""
        self.logs.append(f"🔍 Internal search: {query}")
        return ["Analyze requirements", "Design solution", "Implement core logic"]
    
    def web_search(self, query: str) -> List[str]:
        """Mock web search tool"""
        self.logs.append(f"🌐 Web search: {query}")
        return ["Best practices: LangGraph documentation", "Relevant examples: GitHub repos"]
    
    def plan(self, task: str) -> List[str]:
        """Generate 2-3 actionable steps using OpenAI"""
        self.logs.append(f"📝 Planning task: {task}")
        
        # Generate steps with OpenAI
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a task planner. Break the task into 2-3 actionable steps. Return only the steps as a bullet list."},
                {"role": "user", "content": f"Task: {task}"}
            ],
            max_tokens=150
        )
        
        steps_text = response.choices[0].message.content.strip()
        steps = [line.strip('- ').strip() for line in steps_text.split('\n') if line.strip()]
        self.logs.append(f"Generated steps: {steps}")
        return steps[:3]

# Developer Agent Implementation
class DeveloperAgent:
    def __init__(self):
        self.logs = []
    
    def apply_changes(self, steps: List[str]) -> List[str]:
        """Apply code changes using OpenAI"""
        changes = []
        for step in steps:
            self.logs.append(f"⚙️ Applying: {step}")
            
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a developer. Write code to implement the following step. Return only the code."},
                    {"role": "user", "content": f"Step: {step}"}
                ],
                max_tokens=300
            )
            
            code = response.choices[0].message.content.strip()
            changes.append(code)
            self.logs.append(f"✅ Completed: {step}\nCode:\n{code}")
        return changes

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

graph = StateGraph(OverallState)
graph.add_node("planner", planner_node)
graph.add_node("developer", developer_node)
graph.set_entry_point("planner")
graph.add_edge("planner", "developer")
graph.add_edge("developer", END)
app = graph.compile()

initial_state = OverallState(
    planner={"tasks": ["Create LangGraph agents with OpenAI integration"]},
    developer={"changes": [], "logs": []}
)
result = app.invoke(initial_state)

print("\n" + "="*50)
print("FINAL STATE:")
print(f"Planner tasks: {result['planner']['tasks']}")
print(f"Developer changes: {result['developer']['changes']}")
print("\nEXECUTION LOGS:")
for log in result['logs']:
    print(f"- {log}")
