from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import ToolMessage, SystemMessage
from app.agent.state import AgentState
from app.tools.knowledge_search import knowledge_search
from app.tools.sql_tool import query_database
from app.tools.calculator import calculate

tools = [knowledge_search, query_database, calculate]

def call_model(state: AgentState):
    messages = state['messages']
    
    model = ChatGoogleGenerativeAI(temperature=0, model="gemini-3.6-flash")
    model_with_tools = model.bind_tools(tools)
    
    system_prompt = """You are NovaTech Solutions' Enterprise Knowledge Agent.
You answer employee queries based on internal knowledge.
When asked about policies, ALWAYS use the knowledge_search tool.
When asked about employees, departments, projects, or expenses, ALWAYS use the query_database tool.
When asked to perform math, use the calculate tool.
Always cite your sources clearly based on tool outputs. If you don't know the answer or the tools yield no results, explicitly state that there is insufficient information. Do not fabricate answers or citations."""

    # Inject system prompt
    current_messages = list(messages)
    if not current_messages or not isinstance(current_messages[0], SystemMessage):
        current_messages.insert(0, SystemMessage(content=system_prompt))

    response = model_with_tools.invoke(current_messages)
    return {"messages": [response]}

def call_tools(state: AgentState):
    messages = state['messages']
    last_message = messages[-1]
    
    tool_map = {t.name: t for t in tools}
    tool_responses = []
    
    for tool_call in last_message.tool_calls:
        tool_name = tool_call['name']
        tool_args = tool_call['args']
        tool_instance = tool_map.get(tool_name)
        if tool_instance:
            try:
                result = tool_instance.invoke(tool_args)
            except Exception as e:
                result = f"Error: {str(e)}"
            tool_responses.append(ToolMessage(
                tool_call_id=tool_call['id'],
                name=tool_name,
                content=str(result)
            ))
            
    return {"messages": tool_responses}

def should_continue(state: AgentState):
    messages = state['messages']
    last_message = messages[-1]
    
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "continue"
    return "end"

workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("action", call_tools)
workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "action",
        "end": END
    }
)
workflow.add_edge("action", "agent")
app_graph = workflow.compile()
