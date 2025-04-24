import streamlit as st
from main import run_debug_agent

st.set_page_config(page_title="Debugging AI Assistant", layout="wide")
st.title("🛠️ AI Code Debugging & Explanation Assistant")

st.markdown("""
Paste your buggy code below, and this AI agent will:
1. Detect the language
2. Explain the code
3. Identify bugs
4. Provide a fixed version
5. (Optionally) run it and return output

⚠️ *Python-only execution is supported currently.*
""")

code_input = st.text_area("Paste your code here:", height=300)

if st.button("🔍 Analyze & Fix"):
    if not code_input.strip():
        st.warning("Please paste some code to debug.")
    else:
        with st.spinner("Running debugging agent..."):
            result = run_debug_agent(code_input)
            print(result)
        if isinstance(result, dict) or "error" not in result:
            st.subheader("📌 Detected Language")
            st.code(result.language or "Unknown")

            st.subheader("🧠 Code Explanation")
            st.write(result.explanation or "No explanation found.")

            st.subheader("🐞 Bug Report")
            st.write(result.bugs or "No bugs found.")

            st.subheader("✅ Fixed Code")
            st.code(result.fixed_code or "No fix generated.", language="python")

            # if result.get("optional_output"):
            #     st.subheader("⚙️ Execution Output")
            #     st.code(result["optional_output"])
        else:
            st.error("Something went wrong: \n" + str(result))