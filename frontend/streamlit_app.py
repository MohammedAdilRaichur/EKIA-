import streamlit as st
import sys
import os
from langchain_core.messages import HumanMessage, AIMessage

# Add the parent directory to sys.path to import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import config
from app.agent.graph import app_graph

st.set_page_config(
    page_title="Enterprise Knowledge Intelligence Agent (EKIA)",
    page_icon="🤖",
    layout="wide"
)

def main():
    st.title("NovaTech Solutions - EKIA 🤖")
    
    st.markdown("""
    Welcome to the **NovaTech Solutions** Enterprise Knowledge Intelligence Agent.
    You can ask questions about HR policies, IT guidelines, financial rules, or look up employee and department data.
    """)
    
    with st.sidebar:
        st.header("Admin / Evaluation")
        st.write("Configuration:")
        st.write(f"- LLM: {config.LLM_PROVIDER}")
        st.write(f"- Embeddings: {config.EMBEDDING_MODEL}")
        st.write(f"- Top K: {config.TOP_K}")
        
        if st.button("Clear Conversation"):
            st.session_state.messages = []
            st.rerun()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Ask a question about NovaTech policies..."):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Prepare LangGraph state
        langchain_messages = []
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                langchain_messages.append(AIMessage(content=msg["content"]))
        
        # Run agent
        with st.spinner("Thinking... (Searching knowledge base / Executing tools)"):
            try:
                response = app_graph.invoke({"messages": langchain_messages})
                final_ai_msg = response["messages"][-1]
                response_content = final_ai_msg.content
                
                # Gemini often returns content as a list of blocks instead of a plain string
                if isinstance(response_content, list):
                    extracted_text = ""
                    for block in response_content:
                        if isinstance(block, dict) and 'text' in block:
                            extracted_text += block['text']
                        elif isinstance(block, str):
                            extracted_text += block
                    response_content = extracted_text
                    
            except Exception as e:
                response_content = f"An error occurred: {str(e)}\n\nMake sure your GOOGLE_API_KEY is set in the `.env` file."

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response_content)
            
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response_content})

if __name__ == "__main__":
    main()
