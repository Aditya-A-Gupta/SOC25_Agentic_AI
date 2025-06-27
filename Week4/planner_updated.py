from typing import List, TypedDict, Dict, Any
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

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

class InternalWriteTool:
    def __init__(self):
        self.storage: Dict[str, str] = {}
        self.logs: List[str] = []

    def write(self, filename: str, content: str):
        self.logs.append(f"Writing to {filename}")
        before = self.storage.get(filename, "")
        self.logs.append(f"Before content:\n{before}")
        self.storage[filename] = content
        self.logs.append(f"After content:\n{content}")

class ScraperTool:
    def __init__(self):
        self.logs: List[str] = []

    def scrape(self, url: str) -> str:
        self.logs.append(f"Scraping URL: {url}")
        return f"Full text content extracted from {url}"

class PlannerAgent:
    def __init__(self):
        self.generated_steps: List[str] = []
        self.logs: List[str] = []
        self.internal_search_results: List[str] = []
        self.external_search_results: List[str] = []
        self.scraper = ScraperTool()

    def search_internal(self, query: str) -> List[str]:
        self.logs.append(f"🔍 Internal search: {query}")
        results = ["Internal docs: Analyze requirements", "Internal docs: Design solution"]
        self.internal_search_results = results
        return results

    def search_external(self, query: str) -> List[str]:
        self.logs.append(f"🌐 External search: {query}")
        url = "https://example.com/article"
        result = self.scraper.scrape(url)
        self.external_search_results = [result]
        return self.external_search_results

    def plan(self, task: str) -> List[str]:
        if not self.generated_steps:
            self.logs.append(f"🧠 Thinking about how to break down the task: {task}")
            explanation = f"The task '{task}' can be broken down by first searching internal docs, then external resources, and finally planning actionable steps."
            self.logs.append(f"💡 Explanation: {explanation}")
            self.search_internal(task)
            self.search_external(task)
            self.logs.extend(self.scraper.logs)
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
            self.generated_steps = steps
            self.logs.append(f"Generated steps: {self.generated_steps}")
        return self.generated_steps

class DeveloperAgent:
    def __init__(self, writer: InternalWriteTool):
        self.logs: List[str] = []
        self.writer = writer

    def apply_change(self, step: str, filename: str) -> str:
        self.logs.append(f"🧠 Reflecting on the step: {step}")
        rationale = f"To implement '{step}', I will write code that addresses this specific part of the project."
        self.logs.append(f"💡 Rationale: {rationale}")
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a developer. Write code to implement the following step. Return only the code."},
                {"role": "user", "content": f"Step: {step}"}
            ],
            max_tokens=300
        )
        code = response.choices[0].message.content.strip()
        self.writer.write(filename, code)
        self.logs.extend(self.writer.logs)
        self.writer.logs.clear()
        self.logs.append(f"✅ Completed: {step}")
        return code

def main():
    internal_writer = InternalWriteTool()
    planner_agent = PlannerAgent()
    developer_agent = DeveloperAgent(internal_writer)

    state: OverallState = {
        "planner": {"tasks": ["Create LangGraph agents with OpenAI integration"], "current_index": 0},
        "developer": {"changes": [], "logs": [], "code_files": {}}
    }

    steps = planner_agent.plan(state["planner"]["tasks"][0])

    for i, step in enumerate(steps):
        state["planner"]["current_index"] = i
        filename = "module.py"
        code = developer_agent.apply_change(step, filename)
        state["developer"]["changes"].append(code)
        state["developer"]["code_files"][filename] = internal_writer.storage[filename]
        state["developer"]["logs"].extend(planner_agent.logs + developer_agent.logs)
        planner_agent.logs.clear()
        developer_agent.logs.clear()

    print("\nFINAL STATE:")
    print(f"Planner tasks: {steps}")
    print(f"Developer changes: {state['developer']['changes']}")
    print(f"Code files: {state['developer']['code_files']}")
    print("\nEXECUTION LOGS:")
    for log in state["developer"]["logs"]:
        print(f"- {log}")

if __name__ == "__main__":
    main()
