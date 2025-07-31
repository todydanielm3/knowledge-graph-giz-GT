# Contribuindo para o Knowledge Graph GIZ-BR

Obrigado pelo seu interesse em contribuir para este projeto! 🎉

## Como Contribuir

### 1. Fork do Projeto
- Faça um fork do repositório
- Clone o seu fork localmente
- Configure o upstream para o repositório original

### 2. Configuração do Ambiente
```bash
git clone https://github.com/seu-usuario/knowledge-graph-giz-GT.git
cd knowledge-graph-giz-GT
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Criando uma Branch
```bash
git checkout -b feature/sua-nova-funcionalidade
# ou
git checkout -b fix/correcao-de-bug
```

### 4. Fazendo Mudanças
- Faça suas mudanças seguindo os padrões do projeto
- Adicione testes se necessário
- Documente mudanças significativas

### 5. Testando
```bash
# Iniciar o ambiente
docker compose up -d
python etl/load_metadata.py
streamlit run app/streamlit_app.py

# Testar funcionalidades
```

### 6. Commit e Push
```bash
git add .
git commit -m "feat: adiciona nova funcionalidade X"
git push origin feature/sua-nova-funcionalidade
```

### 7. Pull Request
- Abra um Pull Request no GitHub
- Descreva claramente as mudanças
- Referencie issues relacionadas se houver

## Padrões de Código

### Python
- Use PEP 8 para formatação
- Adicione docstrings para funções públicas
- Use type hints quando possível

### Commits
Siga o padrão [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` para novas funcionalidades
- `fix:` para correções de bugs
- `docs:` para mudanças na documentação
- `style:` para formatação de código
- `refactor:` para refatoração
- `test:` para adição de testes

## Tipos de Contribuições

### 🐛 Reportar Bugs
- Use o template de issue para bugs
- Inclua passos para reproduzir
- Adicione screenshots se relevante

### 💡 Sugerir Funcionalidades
- Use o template de issue para features
- Explique o caso de uso
- Descreva a solução proposta

### 📖 Melhorar Documentação
- Corrija erros de digitação
- Adicione exemplos
- Melhore explicações

### 🚀 Implementar Funcionalidades
- Verifique as issues abertas
- Comente na issue antes de começar
- Siga os padrões estabelecidos

## Diretrizes

### Code Review
- Seja respeitoso e construtivo
- Explique o "porquê" dos comentários
- Teste as mudanças localmente

### Documentação
- Mantenha o README atualizado
- Documente novas funcionalidades
- Inclua exemplos quando necessário

### Testes
- Adicione testes para novas funcionalidades
- Mantenha a cobertura de testes alta
- Teste edge cases importantes

## Precisa de Ajuda?

- Abra uma issue com label "question"
- Entre em contato com os maintainers
- Consulte a documentação no README

Obrigado por contribuir! 🙏
