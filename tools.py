from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime

def save_to_txt(data: str, filename: str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)

    
    return f"Data successfully saved to {filename}"

save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Saves structured research data to a text file.",
)

search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search",
    func=search.run,
    description="Search the web for information",
)

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=200)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

def detect_language(code: str) -> str:
    if "def " in code or "import" in code:
        return "Python"
    elif "function " in code or "console.log" in code:
        return "JavaScript"
    elif "cin" in code or "cout" in code:
        return "C++"
    elif "printf" in code:
        return "C"
    elif "System.out.println" in code:
        return "Java"
    return "Unknown"

from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    groq_api_key=os.getenv("API_KEY"),
)

def explain_code(code: str) -> str:
    prompt =f"""
                You are a Code interpreter. Your job is to explain what this code is supposed to do:\n\n{code}
            """
    return llm.invoke(prompt)

def analyze_errors(code: str) -> str:
    prompt = f"""
                You are a bug fixer. Your job is to find out if this code might has errors. Analyze it and explain any bugs or mistakes. 
                Suggest corrections.
                Code:
                {code}
            """
    return llm.invoke(prompt)

def fix_code(code: str) -> str:
    prompt = f"""
                Your job is to fix this buggy code and return the corrected version only:\n\n{code}
            """
    return llm.invoke(prompt)

language_tool = Tool(name="detect_language", func=detect_language, description="Detects the programming language.")
explain_tool = Tool(name="explain_code", func=explain_code, description="Explains what the code does.")
analyze_tool = Tool(name="analyze_errors", func=analyze_errors, description="Finds and explains bugs.")
fix_tool = Tool(name="fix_code", func=fix_code, description="Fixes the provided code.")