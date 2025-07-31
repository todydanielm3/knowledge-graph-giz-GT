# 📈 Knowledge Graph — Produtos Digitais GIZ-BR

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Neo4j](https://img.shields.io/badge/Neo4j-5.20+-brightgreen.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red.svg)
![Docker](https://img.shields.io/badge/Docker-20.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

</div>

Um protótipo completo que consolida **metadados de projetos da GIZ-Brasil** em um **grafo Neo4j** e exibe tudo em um **app Streamlit** interativo com visualizações dinâmicas.

<img width="826" height="1161" alt="Captura de tela de 2025-07-31 14-05-28" src="https://github.com/user-attachments/assets/fcf1cdb2-f21f-4fbf-a469-1b1138f2c537" />


## 🌟 Características Principais

- **🔍 Visualização Interativa**: Grafos dinâmicos com PyVis
- **📊 Análise de Relações**: Identificação de conexões entre projetos
- **⚡ Performance**: Cache inteligente e consultas otimizadas
- **🐳 Containerização**: Deploy fácil com Docker
- **🔐 Segurança**: Credenciais isoladas e validação de entrada
- **📱 Interface Responsiva**: UI moderna com Streamlit

---

## ✨ Funcionalidades

* **🔧 ETL em Python**: Lê `data/projects.csv`, faz *upsert* dos nós `Project` no Neo4j
* **🗄️ Neo4j (Docker)**: Banco de grafos 5.x Community Edition com plugin APOC
* **🎨 Streamlit + PyVis**: UI interativa para escolher projetos e visualizar conexões
* **🔒 Gestão de Secrets**: Credenciais isoladas em `app/secrets.toml`
* **📈 Métricas em Tempo Real**: Estatísticas de conectividade e análise de grafos
* **🔄 Relacionamentos Automáticos**: Criação inteligente de conexões entre entidades

---

## ⚙️ Requisitos

| Ferramenta                | Versão mínima |
| ------------------------- | ------------- |
| Python                    | 3.10          |
| Docker                    | 20.10         |
| Docker Compose            | v2            |
| (Opcional) `cypher-shell` | Neo4j 5.x CLI |

---

## 🚀 Guia Rápido

### Pré-requisitos
- Python 3.10+
- Docker & Docker Compose
- Git

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/knowledge-graph-giz-GT.git
cd knowledge-graph-giz-GT

# 2. Configure o ambiente Python
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 3. Configure as credenciais
cp app/secrets.toml.example app/secrets.toml
# Edite app/secrets.toml com suas credenciais

# 4. Inicie o Neo4j
docker compose up -d

# 5. Carregue os dados
python etl/load_metadata.py

# 6. Execute a aplicação
streamlit run app/streamlit_app.py
```

🎉 Abra [http://localhost:8501](http://localhost:8501) e explore o grafo!

---

## 🗂️ Estrutura do Projeto

```
knowledge-graph-giz-GT/
├── 📁 app/
│   ├── streamlit_app.py          # 🎨 Interface principal Streamlit
│   ├── secrets.toml.example      # 🔒 Exemplo de configuração
│   └── secrets.toml              # 🔑 Credenciais (não versionado)
├── 📁 data/
│   └── projects.csv              # 📊 Dados de entrada (projetos)
├── 📁 etl/
│   └── load_metadata.py          # ⚙️ Script de ingestão de dados
├── 📁 docs/
│   └── projeto_knowledge_graph_giz.tex  # 📚 Documentação LaTeX
├── docker-compose.yml            # 🐳 Configuração Neo4j
├── requirements.txt              # 📦 Dependências Python
├── LICENSE                       # ⚖️ Licença MIT
├── CONTRIBUTING.md               # 🤝 Guia de contribuição
└── README.md                     # 📖 Esta documentação
```

---

## 🔧 Configuração e Customização

### Adicionando Novos Dados
| Objetivo | Como Fazer |
|----------|------------|
| **Adicionar colunas** ao CSV | Acrescente cabeçalhos em `data/projects.csv` e ajuste `upsert_project()` no ETL |
| **Carregar mais entidades** (`Product`, `Person`…) | Crie funções análogas no ETL e relacione via Cypher |
| **Atualizar em tempo real** | Agende o script no cron ou GitHub Actions |
| **Deploy em nuvem** | Use Neo4j Aura Free + Streamlit Cloud (ajuste `secrets.toml`) |

### Exemplos de Consultas Cypher

```cypher
-- Listar todos os projetos
MATCH (p:Project) RETURN p

-- Encontrar conexões entre projetos
MATCH (p1:Project)-[r]-(p2:Project) 
RETURN p1.name, type(r), p2.name

-- Estatísticas do grafo
MATCH (n) RETURN labels(n), count(n)

-- Projetos por organização
MATCH (p:Project)-[:EXECUTADO_POR]->(o:Organizacao)
RETURN o.name, collect(p.name)
```

---

## 🗺️ Roadmap

### 🎯 Próximas Funcionalidades
- [ ] **Busca Semântica**: Índice vetorial no Neo4j para pesquisa inteligente
- [ ] **APIs REST**: Endpoints para integração com outros sistemas
- [ ] **Dashboard de KPIs**: Métricas avançadas e indicadores de performance
- [ ] **Autenticação SSO**: Integração com Azure AD/OAuth
- [ ] **Machine Learning**: Recomendações baseadas em padrões do grafo
- [ ] **Export/Import**: Backup e restore de dados
- [ ] **Interface Mobile**: App responsivo para dispositivos móveis

### 🔄 Melhorias Técnicas
- [ ] Testes automatizados (pytest)
- [ ] CI/CD com GitHub Actions
- [ ] Monitoramento e logging
- [ ] Performance profiling
- [ ] Documentação API interativa

---

## 🤝 Contribuição

Contribuições são muito bem-vindas! Veja o [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes sobre:

- 🐛 Como reportar bugs
- 💡 Como sugerir funcionalidades
- 🔧 Como configurar o ambiente de desenvolvimento
- 📝 Padrões de código e commit

### Processo Rápido
1. **Fork** o repositório
2. Crie uma branch: `git checkout -b feat/minha-funcionalidade`
3. Commit suas mudanças: `git commit -m "feat: adiciona funcionalidade X"`
4. Push: `git push origin feat/minha-funcionalidade`
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 🙏 Agradecimentos

- **GIZ Brasil** pelo contexto e dados do projeto
- **Neo4j Community** pela excelente documentação
- **Streamlit Team** pela framework intuitiva
- **PyVis** pela biblioteca de visualização

---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela!**

**🔗 [Documentação Completa](docs/projeto_knowledge_graph_giz.tex) | 🐛 [Reportar Bug](../../issues) | 💡 [Sugerir Feature](../../issues)**

</div>

---

*Desenvolvido com ❤️ para facilitar a gestão de conhecimento organizacional*
