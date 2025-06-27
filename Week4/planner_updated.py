from typing import List, TypedDict, Dict
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
    current_index: int

class DeveloperState(TypedDict):
    changes: List[str]
    logs: List[str]
    code_files: Dict[str, str]

class OverallState(TypedDict):
    planner: PlannerState
    developer: DeveloperState

# Tools
class InternalWriteTool:
    def __init__(self):
        self.storage: Dict[str, str] = {}
    
    def write(self, filename: str, content: str):
        self.storage[filename] = content

class ScraperTool:
    def scrape(self, url: str) -> str:
        return f"Full text content extracted from {url}"

# Planner Agent
class PlannerAgent:
    def __init__(self):
        self.logs: List[str] = []
        self.scraper = ScraperTool()
    
    def plan(self, task: str) -> List[str]:
        self.logs.append(f"🧠 Thinking about task: {task}")
        
        # Research phase
        internal_results = ["Internal: Analyze requirements", "Internal: Design solution"]
        external_results = [self.scraper.scrape("https://example.com/article")]
        
        # Generate steps with Gemini
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""Based on research:
        Internal: {internal_results}
        External: {external_results}
        
        Break this task into 2-3 actionable steps. Return ONLY steps as a bullet list.
        Task: {task}"""
        
        response = model.generate_content(prompt)
        steps_text = response.text.strip()
        steps = [line.strip('-* ').strip() for line in steps_text.split('\n') if line.strip()][:3]
        
        self.logs.append(f"Generated steps: {steps}")
        return steps

# Developer Agent
class DeveloperAgent:
    def __init__(self, writer: InternalWriteTool):
        self.logs: List[str] = []
        self.writer = writer
    
    def apply_change(self, step: str, filename: str) -> str:
        self.logs.append(f"⚙️ Implementing: {step}")
        
        # Generate code with Gemini
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            f"""You are a developer. Write code to implement this step.
            Return ONLY the code. No explanations.
            Step: {step}"""
        )
        
        code = response.text.strip()
        self.writer.write(filename, code)
        self.logs.append(f"✅ Completed: {step}")
        return code

def main():
    internal_writer = InternalWriteTool()
    planner = PlannerAgent()
    developer = DeveloperAgent(internal_writer)

    state: OverallState = {
        "planner": {"tasks": ["Create Gemini agents with state management"], "current_index": 0},
        "developer": {"changes": [], "logs": [], "code_files": {}}
    }

    # Generate and process steps
    steps = planner.plan(state["planner"]["tasks"][0])
    for i, step in enumerate(steps):
        state["planner"]["current_index"] = i
        filename = "module.py"
        code = developer.apply_change(step, filename)
        state["developer"]["changes"].append(code)
        state["developer"]["code_files"][filename] = internal_writer.storage.get(filename, "")
        
        # Aggregate logs
        state["developer"]["logs"].extend(planner.logs + developer.logs)
        planner.logs.clear()
        developer.logs.clear()

    # Output results
    print("\nFINAL STATE:")
    print(f"Steps: {steps}")
    print(f"Changes: {state['developer']['changes']}")
    print(f"Code files: {state['developer']['code_files']}")
    print("\nLOGS:")
    for log in state["developer"]["logs"]:
        print(f"- {log}")

if __name__ == "__main__":
    main()
