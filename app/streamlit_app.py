
# app/streamlit_app.py
import streamlit as st
from neo4j import GraphDatabase
from pyvis.network import Network
import json
import os, streamlit as st

@st.cache_resource
def get_driver():
    bolt_url = st.secrets.get("bolt_url") or os.getenv("BOLT_URL")
    user     = st.secrets.get("user")     or os.getenv("NEO4J_USER")
    pwd      = st.secrets.get("password") or os.getenv("NEO4J_PASS")
    return GraphDatabase.driver(bolt_url, auth=(user, pwd))



def run_cypher(query, **kwargs):
    with get_driver().session() as sess:
        result = sess.run(query, kwargs)
        return [r.data() for r in result]

st.title("📈 Knowledge Graph – Produtos Digitais GIZ-BR")

proj = st.selectbox("Escolha um projeto", 
    [d["p"]["name"] for d in run_cypher("MATCH (p:Project) RETURN p")])

records = run_cypher("""
MATCH (p:Project {name:$proj})-[r*1..2]-(n)
RETURN p, r, n
""", proj=proj)

# ── PyVis ───────────────────────────────────────────────────────
g = Network(height="600px", bgcolor="#FFFFFF", directed=True)
for rec in records:
    p = rec["p"]; g.add_node(p.id, p["name"], title=p["status"], color="#1f77b4")
    n = rec["n"]; g.add_node(n.id, n["name"] if "name" in n else n["full_name"])
    for rel in rec["r"]:
        g.add_edge(rel.start_node.id, rel.end_node.id, label=rel.type)

html = g.generate_html()
st.components.v1.html(html, height=600, scrolling=True)
