# Knowledge Graph — Produtos Digitais GIZ-BR

Um protótipo completo que consolida **metadados de projetos da GIZ-Brasil** em um **grafo Neo4j** e exibe tudo em um **app Streamlit** interativo.

<p align="center">
  <img src="docs/preview.gif" width="760" alt="GIF da aplicação" />
</p>

---

## ✨ Funcionalidades

* **ETL em Python**: lê `data/projects.csv`, faz *upsert* dos nós `Project` no Neo4j.
* **Neo4j (Docker)**: banco de grafos 5.x Community Edition com plugin APOC.
* **Streamlit + PyVis**: UI para escolher um projeto e visualizar conexões em tempo real.
* **Secrets**: credenciais isoladas em `.streamlit/secrets.toml`.

---

## ⚙️ Requisitos

| Ferramenta                | Versão mínima |
| ------------------------- | ------------- |
| Python                    | 3.10          |
| Docker                    | 20.10         |
| Docker Compose            | v2            |
| (Opcional) `cypher-shell` | Neo4j 5.x CLI |

---

## 🚀 Guia rápido

```bash
git clone https://github.com/<usuario>/knowledge-graph-giz-GT.git
cd knowledge-graph-giz-GT

# 1. Ambiente Python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Subir Neo4j
docker compose up -d          # imagem neo4j:5.20-community

# 3. Configurar segredos
mkdir -p .streamlit
cat > .streamlit/secrets.toml <<'EOF'
bolt_url = "bolt://localhost:7687"
user     = "neo4j"
password = "test12345"
EOF

# 4. Carregar dados mock
python etl/load_metadata.py   # lê data/projects.csv

# 5. Rodar o app
streamlit run app/streamlit_app.py
```

Abra [http://localhost:8501](http://localhost:8501) e selecione um projeto para ver o grafo.

---

## 🗂️ Estrutura de pastas

```
├── app/
│   └── streamlit_app.py   # interface Streamlit
├── data/
│   └── projects.csv       # metadados mock
├── etl/
│   └── load_metadata.py   # script de ingestão
├── docker-compose.yml     # Neo4j 5 + APOC
├── requirements.txt       # dependências Python
└── .streamlit/
    └── secrets.toml       # credenciais (fora do Git)
```

---

## 🔧 Customização

| Deseja…                                            | Faça isto                                                           |
| -------------------------------------------------- | ------------------------------------------------------------------- |
| **Adicionar colunas** no CSV                       | Acrescente cabeçalhos e ajuste `upsert_project()` no ETL.           |
| **Carregar mais entidades** (`Product`, `Person`…) | Crie funções análogas no ETL e relacione via Cypher.                |
| **Atualizar em tempo real**                        | Agende o script no cron ou GitHub Actions.                          |
| **Deploy em nuvem**                                | Use Neo4j Aura Free + Streamlit Cloud (basta mudar `secrets.toml`). |

---

## 🗺️ Roadmap

* [ ] Relacionar `Project → Product → Technology`.
* [ ] Índice vetorial no Neo4j para busca semântica.
* [ ] Dashboard de KPIs (Streamlit Metrics).
* [ ] Autenticação SSO (Azure AD) no app.

---

## 🤝 Contribuição

1. **Fork** o repositório.
2. Crie uma branch: `git checkout -b feat/minha-melhora`.
3. Faça *commit* das mudanças: `git commit -m "feat: …"`.
4. *Push*: `git push origin feat/minha-melhora`.
5. Abra um Pull Request.

---

## 📄 Licença

MIT © 2025 GIZ-AdaptaInfra Team. Veja `LICENSE` para detalhes.

---

Boa exploração — e que seus grafos revelem os melhores insights! 👩‍🔬🕸️
