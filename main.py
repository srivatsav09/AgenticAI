from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent,AgentExecutor
from tools import search_tool,wiki_tool,save_tool
import os

load_dotenv()

class ResearchResponse(BaseModel):
    topic:str
    summary:str
    sources:list[str]
    tools_used:list[str]


llm = ChatGroq(
    model="Llama3-70b-8192",
    temperature=0,
    groq_api_key = os.getenv("API_KEY"),

    # other params...
)

parser = PydanticOutputParser(pydantic_object=ResearchResponse)
prompt_extract = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that helps generate structured research reports.
            Answer the user query and return only a JSON object with the following keys:
            - topic: the topic of the query
            - summary: a concise summary of the answer
            - sources: a list of credible sources
            - tools_used: any tools you used to generate this answer
            Wrap the entire output in a JSON object and provide no extra text.
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [search_tool,wiki_tool,save_tool]

agent = create_tool_calling_agent(
    llm = llm,
    prompt = prompt_extract,
    tools = tools,
)

agent_executor = AgentExecutor(agent=agent,tools=tools,verbose=True)
query = input("what can i help u find?")
raw_res = agent_executor.invoke({"query":query})
print(raw_res)

try:
    struct_resp = parser.parse(raw_res['output'])
    print(struct_resp)
except Exception as e:
    print(e)

# response = llm.invoke("Who was the first indian to step on the moon?")
# print(response)
