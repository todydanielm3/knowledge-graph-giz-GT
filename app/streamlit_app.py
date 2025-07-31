
# app/streamlit_app.py
import streamlit as st
from neo4j import GraphDatabase
from pyvis.network import Network
import pandas as pd
import os

@st.cache_resource
def get_driver():
    bolt_url = st.secrets.get("bolt_url") or os.getenv("BOLT_URL") or "bolt://localhost:7687"
    user     = st.secrets.get("user")     or os.getenv("NEO4J_USER") or "neo4j"
    pwd      = st.secrets.get("password") or os.getenv("NEO4J_PASS") or "test12345"
    return GraphDatabase.driver(bolt_url, auth=(user, pwd))

def run_cypher(query, **kwargs):
    with get_driver().session() as sess:
        result = sess.run(query, kwargs)
        return [r.data() for r in result]

def create_sample_relationships():
    """Cria relações de exemplo se não existirem"""
    with get_driver().session() as sess:
        # Verifica se já existem relações
        result = sess.run("MATCH ()-[r]-() RETURN count(r) as count")
        count = result.single()["count"]
        
        if count == 0:
            # Criar algumas relações de exemplo
            sess.run("""
            MATCH (p1:Project {name: 'AdaptaInfra'}), (p2:Project {name: 'Gênero&Infra'})
            CREATE (p1)-[:RELACIONADO_COM {motivo: 'Infraestrutura compartilhada'}]->(p2)
            """)
            
            sess.run("""
            MATCH (p1:Project {name: 'Clima-Amazônia'}), (p2:Project {name: 'AdaptaInfra'})
            CREATE (p1)-[:INFLUENCIA {tipo: 'Mudanças climáticas'}]->(p2)
            """)
            
            # Criar entidades adicionais
            sess.run("""
            CREATE (o1:Organizacao {name: 'GIZ Brasil', tipo: 'Cooperação'})
            CREATE (o2:Organizacao {name: 'Ministério da Infraestrutura', tipo: 'Governo'})
            CREATE (t1:Tema {name: 'Sustentabilidade', area: 'Meio Ambiente'})
            CREATE (t2:Tema {name: 'Igualdade de Gênero', area: 'Social'})
            """)
            
            # Conectar projetos às organizações e temas
            sess.run("""
            MATCH (p:Project), (o:Organizacao {name: 'GIZ Brasil'})
            CREATE (p)-[:EXECUTADO_POR]->(o)
            """)
            
            sess.run("""
            MATCH (p:Project {name: 'AdaptaInfra'}), (t:Tema {name: 'Sustentabilidade'})
            CREATE (p)-[:ABORDA]->(t)
            """)
            
            sess.run("""
            MATCH (p:Project {name: 'Gênero&Infra'}), (t:Tema {name: 'Igualdade de Gênero'})
            CREATE (p)-[:ABORDA]->(t)
            """)

st.title("📈 Knowledge Graph – Produtos Digitais GIZ-BR")

# Inicializar relações se necessário
create_sample_relationships()

# Buscar projetos únicos
projects_data = run_cypher("MATCH (p:Project) RETURN DISTINCT p.name as name ORDER BY p.name")
project_names = [p["name"] for p in projects_data]

if not project_names:
    st.error("Nenhum projeto encontrado no banco de dados!")
    st.stop()

proj = st.selectbox("Escolha um projeto", project_names)

if proj:
    # Mostrar informações do projeto
    project_info = run_cypher("MATCH (p:Project {name: $name}) RETURN p LIMIT 1", name=proj)
    
    if project_info:
        p = project_info[0]["p"]
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(f"📋 Projeto: {proj}")
            st.write(f"**Status:** {p.get('status', 'N/A')}")
            st.write(f"**Data de Início:** {p.get('start_date', 'N/A')}")
            if 'budget' in p:
                st.write(f"**Orçamento:** R$ {p['budget']:,}")
        
        with col2:
            st.subheader("🔗 Estatísticas do Grafo")
            stats = run_cypher("""
            MATCH (p:Project {name: $name})
            OPTIONAL MATCH (p)-[r]-(n)
            RETURN count(DISTINCT r) as relacoes, count(DISTINCT n) as entidades_conectadas
            """, name=proj)
            
            if stats:
                st.metric("Relações", stats[0]["relacoes"])
                st.metric("Entidades Conectadas", stats[0]["entidades_conectadas"])

    # Buscar dados para o grafo
    records = run_cypher("""
    MATCH (p:Project {name: $proj})
    OPTIONAL MATCH (p)-[r]-(n)
    RETURN p, r, n
    """, proj=proj)
    
    # Criar visualização
    st.subheader("🌐 Visualização do Grafo")
    
    g = Network(height="600px", bgcolor="#f8f9fa", directed=True)
    g.set_options("""
    var options = {
      "physics": {
        "enabled": true,
        "stabilization": {"iterations": 100}
      },
      "nodes": {
        "font": {"size": 16}
      },
      "edges": {
        "font": {"size": 14}
      }
    }
    """)
    
    # Adicionar o projeto principal sempre
    project_node = next((rec["p"] for rec in records if rec["p"]), None)
    if project_node:
        g.add_node(
            project_node["id"], 
            label=project_node["name"],
            title=f"Status: {project_node.get('status', 'N/A')}<br>Orçamento: R$ {project_node.get('budget', 'N/A')}",
            color="#e74c3c",
            size=25
        )
    
    # Adicionar nós conectados e relações
    added_nodes = {project_node["id"]} if project_node else set()
    
    for rec in records:
        if rec["r"] and rec["n"]:  # Se há relação e nó conectado
            n = rec["n"]
            node_id = n["id"] if "id" in n else hash(str(n))
            
            if node_id not in added_nodes:
                # Determinar cor baseada no tipo
                if "Project" in n.get("labels", []) or "name" in n:
                    color = "#3498db"
                    size = 20
                elif "Organizacao" in str(n):
                    color = "#2ecc71" 
                    size = 18
                elif "Tema" in str(n):
                    color = "#f39c12"
                    size = 16
                else:
                    color = "#95a5a6"
                    size = 15
                
                label = n.get("name", n.get("tipo", str(node_id)))
                title = "<br>".join([f"{k}: {v}" for k, v in n.items() if k != "id"])
                
                g.add_node(node_id, label=label, title=title, color=color, size=size)
                added_nodes.add(node_id)
            
            # Adicionar aresta
            if project_node:
                edge_label = rec["r"]["type"] if hasattr(rec["r"], "type") else "CONECTADO"
                g.add_edge(project_node["id"], node_id, label=edge_label, arrows="to")
    
    # Se não há relações, mostrar apenas o projeto
    if len(added_nodes) <= 1:
        st.info("⚠️ Este projeto não possui relações cadastradas no grafo. Mostrando apenas o nó do projeto.")
    
    # Gerar e exibir o grafo
    try:
        html = g.generate_html()
        st.components.v1.html(html, height=650, scrolling=True)
    except Exception as e:
        st.error(f"Erro ao gerar o grafo: {e}")
        
    # Mostrar dados em tabela como fallback
    with st.expander("📊 Dados Detalhados"):
        if records and any(rec["r"] for rec in records):
            df_data = []
            for rec in records:
                if rec["r"] and rec["n"]:
                    df_data.append({
                        "Origem": project_node["name"] if project_node else "N/A",
                        "Relação": rec["r"]["type"] if hasattr(rec["r"], "type") else "CONECTADO",
                        "Destino": rec["n"].get("name", "N/A"),
                        "Tipo Destino": str(type(rec["n"]).__name__)
                    })
            
            if df_data:
                df = pd.DataFrame(df_data)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Nenhuma relação encontrada para exibir em tabela.")
        else:
            st.info("Nenhum dado de relação disponível.")

else:
    st.info("Selecione um projeto para visualizar o grafo.")
