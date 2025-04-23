# from dotenv import load_dotenv
# from pydantic import BaseModel
# from langchain_groq import ChatGroq
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import PydanticOutputParser
# from langchain.agents import create_tool_calling_agent,AgentExecutor
# from tools import search_tool,wiki_tool,save_tool,language_tool, explain_tool, analyze_tool, fix_tool
# import os

# load_dotenv()

# # class ResearchResponse(BaseModel):
# #     topic:str
# #     summary:str
# #     sources:list[str]
# #     tools_used:list[str]

# class CodeDebugResponse(BaseModel):
#     language: str
#     explanation: str
#     bugs: str
#     fixed_code: str
#     optional_output: str


# llm = ChatGroq(
#     model="Llama3-70b-8192",
#     temperature=0,
#     groq_api_key = os.getenv("API_KEY"),

#     # other params...
# )

# parser = PydanticOutputParser(pydantic_object = CodeDebugResponse)
# # prompt_extract = ChatPromptTemplate.from_messages(
# #     [
# #         (
# #             "system",
# #             """
# #             You are a research assistant that helps generate structured research reports.
# #             Answer the user query and return only a JSON object with the following keys:
# #             - topic: the topic of the query
# #             - summary: a concise summary of the answer
# #             - sources: a list of credible sources
# #             - tools_used: any tools you used to generate this answer
# #             Wrap the entire output in a JSON object and provide no extra text.
# #             """,
# #         ),
# #         ("placeholder", "{chat_history}"),
# #         ("human", "{query}"),
# #         ("placeholder", "{agent_scratchpad}"),
# #     ]
# # ).partial(format_instructions=parser.get_format_instructions())

# prompt_extract = ChatPromptTemplate.from_messages([
#     ("system", 
#         """
#             You are a code debugging and explanation assistant.
#             Your job is to help the user understand and fix buggy code using available tools.
#             Always return a structured JSON format with:
#             - language
#             - explanation
#             - bugs
#             - fixed_code
#         """
#     ),
#     ("human", "{query}"),
#     ("placeholder", "{agent_scratchpad}"),
# ]).partial(format_instructions=parser.get_format_instructions())

# tools = [search_tool,wiki_tool,save_tool,language_tool, explain_tool, analyze_tool, fix_tool]

# agent = create_tool_calling_agent(
#     llm = llm,
#     prompt = prompt_extract,
#     tools = tools,
# )

# agent_executor = AgentExecutor(agent=agent,tools=tools,verbose=True)
# query = input("Enter your code:")
# raw_res = agent_executor.invoke({"query":query})
# print(raw_res)

# try:
#     struct_resp = parser.parse(raw_res['output'])
#     print(struct_resp)
# except Exception as e:
#     print(e)

# # response = llm.invoke("Who was the first indian to step on the moon?")
# # print(response)


from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
import os
from tools import search_tool,wiki_tool,save_tool,language_tool, explain_tool, analyze_tool, fix_tool

load_dotenv()

class DebugResponse(BaseModel):
    language: str
    explanation: str
    bugs: str
    fixed_code: str
    optional_output: str = ""

llm = ChatGroq(
    model="llama-3.1-8b-instant",  # or llama-3-70b-8192
    temperature=0,
    groq_api_key=os.getenv("API_KEY")
)

parser = PydanticOutputParser(pydantic_object=DebugResponse)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", """
        You are a code debugging and explanation agent. Given some code, return a JSON object with:
        - language: Detected programming language
        - explanation: Step-by-step explanation of the code
        - bugs: A list of any bugs found or issues
        - fixed_code: The corrected version of the code
        - optional_output: (Optional) Result after running the fixed code
        If the input is too broken to detect a language or explain, return `"Unknown"` or `"Not Applicable"` for that field.
        Return only a JSON object matching the format.
    """),
    ("human", "{query}"),
    ("placeholder", "{agent_scratchpad}"),
]).partial(format_instructions=parser.get_format_instructions())
tools = [search_tool,wiki_tool,save_tool,language_tool, explain_tool, analyze_tool, fix_tool]
agent = create_tool_calling_agent(llm=llm, prompt=prompt_template, tools=tools)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

def run_debug_agent(code_input: str) -> dict:
    try:
        response = agent_executor.invoke({"query": code_input})
        print("DEBUG RAW RESPONSE:", response)
        print(parser.parse(response["output"]))  # Add this to log raw output
        return parser.parse(response["output"])
    except Exception as e:
        return {"error": str(e)}
