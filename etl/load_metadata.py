# etl/load_metadata.py
import pandas as pd
from neo4j import GraphDatabase
from pathlib import Path

# 1) CONFIGS -----------------------------------------------------------
URI      = "bolt://localhost:7687"
USER     = "neo4j"
PASSWORD = "test12345"            # mesma senha do docker-compose
CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "projects.csv"

# 2) DRIVER ------------------------------------------------------------
driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

# 3) FUNÇÃO UPSERT -----------------------------------------------------
def upsert_project(tx, props: dict):
    """
    Garante um nó Project com id único e
    atualiza/insere todas as demais propriedades.
    """
    tx.run(
        """
        MERGE (p:Project {id: $id})
        SET   p += $props
        """,
        id=props["id"],
        props=props
    )

# 4) LOAD --------------------------------------------------------------
def load_projects():
    df = pd.read_csv(CSV_PATH)
    with driver.session() as session:
        # execute_write é o nome novo em vez de write_transaction
        for row in df.to_dict("records"):
            session.execute_write(upsert_project, row)
    print(f"✓ Carregado {len(df)} projetos em Neo4j.")

if __name__ == "__main__":
    load_projects()
