"""
Streamlit UI for StrategyMind
- Query/Response tab: interact with FastAPI /query endpoint
- Neo4j Browser tab: embed Neo4j Browser (localhost:7474)
- Traces tab: embed Jaeger UI (localhost:16686)
"""
import streamlit as st
import requests

st.set_page_config(page_title="StrategyMind Dashboard", layout="wide")

TABS = ["Query & Response", "Neo4j Graph", "Traces"]
tab1, tab2, tab3 = st.tabs(TABS)

API_URL = st.secrets.get("api_url", "http://localhost:8000/query")
NEO4J_URL = st.secrets.get("neo4j_url", "http://localhost:7474")
JAEGER_URL = st.secrets.get("jaeger_url", "http://localhost:16686")

with tab1:
    st.header("Query the StrategyMind Assistant")
    query = st.text_area("Enter your question", height=80)
    if st.button("Submit", type="primary") and query.strip():
        with st.spinner("Querying..."):
            try:
                resp = requests.post(API_URL, json={"query": query})
                resp.raise_for_status()
                answer = resp.json().get("answer", "No answer returned.")
                st.success("Response:")
                st.write(answer)
            except Exception as e:
                st.error(f"Error: {e}")

with tab2:
    st.header("Neo4j Graph Browser")
    st.markdown(f"[Open Neo4j Browser in new tab]({NEO4J_URL})")
    st.components.v1.iframe(NEO4J_URL, height=600)

with tab3:
    st.header("Traces (Jaeger UI)")
    st.markdown(f"[Open Jaeger UI in new tab]({JAEGER_URL})")
    st.components.v1.iframe(JAEGER_URL, height=600)
