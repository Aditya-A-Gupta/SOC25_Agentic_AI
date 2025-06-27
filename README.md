# SOC25_Agentic_AI – Week-wise Learnings

This repository documents the development of an agentic AI system, focusing on modular, state-driven workflows and multi-agent orchestration. Below is a summary of what was learned and implemented each week, according to your target tasks.

## Week 1: IDE Setup & Tech Familiarization

**Goal:**  
Set up a web-based IDE using Monaco Editor with Python execution (via Pyodide), finalize the MVP feature set, and begin exploring multi-agent orchestration.

**What I Learned and Accomplished:**

- **Project Setup:**  
  - Created a new project using React to serve as the foundation for the AgentCode IDE.
  - Installed and integrated Monaco Editor for robust code editing with Python syntax highlighting.
- **Python Execution:**  
  - Enabled in-browser Python code execution using Pyodide.
  - Built an output console to display execution results and errors.
- **UI Design:**  
  - Designed a split-screen layout: code editor on one side, output console on the other.
  - Added a language dropdown (optional) and a toolbar with “Run” and placeholder agent buttons (“Debug”, “Test”, “Explain”).
- **MVP Features:**  
  - Finalized core features for AgentCode v1: editor, execution, output, and basic agent tool buttons.
  - Pushed the initial working codebase to GitHub.
- **Exploration:**  
  - Began exploring multi-agent orchestration frameworks and planning for future agent integrations.

## Week2,3: Agent Scaffolding & State Management

**Goal:**  
Set up LangGraph, scaffold planner and developer agents, manage state, and implement basic agent logic.

**What I Learned and Accomplished:**

- **LangGraph Integration:**  
  - Installed and configured LangGraph for managing agent workflows.
  - Created a shared LangGraph graph to orchestrate planner and developer subgraphs.
- **Agent Scaffolding:**  
  - Developed `plannerAgent` and `developerAgent` scaffolds.
  - Managed three distinct states: `OverallState`, `PlannerState`, and `DeveloperState` for robust context and future parallel processing.
- **Agent Logic:**  
  - Implemented a Planner agent that accepts a task description and outputs 2–3 actionable steps, using internal and optional web search tools for research.
  - Implemented a Developer agent that accepts one or more tasks, applies mock or real code changes, and logs before/after outputs.
- **Logging and Reasoning:**  
  - Logged outputs and reasoning at each node for transparency and debugging.

## Week4: Advanced Workflows, Tool Refinement, and Prompt Engineering

**Goal:**  
Refactor agents for step-by-step execution, refine tool usage, and enhance prompt engineering.

**What I Learned and Accomplished:**

- **Looping Logic:**  
  - Refactored Planner and Developer agents to handle one step at a time, using loops or LangGraph node recurrence.
  - Maintained context between steps via shared or persistent state, preventing repeated steps and infinite loops.
- **Tool Usage:**  
  - Used `search_internal` and `search_external` before generating any plan or edit, ensuring agents consider both internal and external information.
  - Added a scraper tool to extract full-text from external URLs.
  - Implemented `internal_write` for in-place code editing by the Developer agent.
- **Prompt Engineering:**  
  - Wrote Chain-of-Thought prompts to force agents to explain their plan or edit rationale before acting.
  - Logged agent thoughts, tools used, and final outputs for comprehensive traceability and debugging.


---
