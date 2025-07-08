# 📊 Cobertura de Código - Guia Completo

## 🔍 O que é Cobertura de Código?

**Cobertura de código** é uma métrica que mede **qual porcentagem do seu código fonte é executada** durante os testes automatizados. É essencial para garantir qualidade e confiabilidade do software.

## 📈 Resultado Atual do Projeto

```
📊 COBERTURA ATUAL: 53%
```

### 📋 Detalhamento por App:

| App | Cobertura | Status | Prioridade |
|-----|-----------|--------|------------|
| **Models** | 93-95% | 🟢 Excelente | ✅ Mantida |
| **URLs** | 100% | 🟢 Perfeito | ✅ Completa |
| **Views** | 21-82% | 🟡 Variável | 🎯 Melhorar |
| **Serializers** | 33-100% | 🔴 Baixa | ⚠️ Crítico |
| **Authentication** | 0% | 🔴 Zero | 🚨 Urgente |

## 🎯 Interpretação dos Níveis

- **🟢 90-100%**: Excelente cobertura
- **🟡 80-89%**: Boa cobertura  
- **🟠 70-79%**: Cobertura aceitável
- **🟡 60-69%**: Cobertura baixa
- **🔴 <60%**: Cobertura insuficiente

## 🚀 Como Executar Análise de Cobertura

### Método Automatizado (Recomendado)
```bash
python run_coverage.py
```

### Método Manual
```bash
# Instalar coverage
pip install coverage

# Executar testes com cobertura
coverage run --source=app manage.py test

# Ver relatório no terminal
coverage report --show-missing

# Gerar relatório HTML
coverage html
```

## 📊 Áreas que Precisam de Melhoria

### 🚨 **Críticas (0-50% cobertura):**

1. **Authentication (0%)**
   ```python
   # app/usuarios/authentication.py - SEM TESTES
   # Precisa de testes para login, logout, tokens
   ```

2. **Serializers (33-47%)**
   ```python
   # Faltam testes para validações e campos customizados
   ```

3. **UserManager (23%)**
   ```python
   # app/usuarios/usermanager.py - Lógica de criação de usuários
   ```

### 🟡 **Moderadas (50-80% cobertura):**

1. **Views de Rotas (21%)**
   ```python
   # app/rotas/views.py - Lógica complexa de otimização
   ```

2. **Views de Usuários (49%)**
   ```python
   # app/usuarios/views.py - Endpoints da API
   ```

## 🛠️ Plano de Melhoria

### Fase 1: Críticas (Meta: 70%+)
```python
# 1. Testes de Authentication
def test_login_success(self):
    # Teste de login válido
    
def test_login_invalid(self):
    # Teste de login inválido
    
def test_token_generation(self):
    # Teste de geração de tokens
```

### Fase 2: Serializers (Meta: 80%+)
```python
# 2. Testes de Serializers
def test_serializer_validation(self):
    # Testes de validação de campos
    
def test_serializer_create(self):
    # Testes de criação via serializer
```

### Fase 3: Views Complexas (Meta: 75%+)
```python
# 3. Testes de Views
def test_api_endpoints(self):
    # Testes de endpoints REST
    
def test_error_handling(self):
    # Testes de tratamento de erros
```

## 📈 Scripts Disponíveis

### 1. **run_coverage.py** - Análise Completa
- ✅ Instala dependências automaticamente
- ✅ Executa todos os testes
- ✅ Gera relatórios terminal + HTML
- ✅ Análise e interpretação

### 2. **run_tests.py** - Testes Rápidos
- ✅ Execução rápida de testes
- ✅ Validação de funcionalidades
- ✅ Relatório de sucessos/falhas

## 🎯 Metas de Cobertura

| Prazo | Meta | Foco |
|-------|------|------|
| **Curto** | 70% | Authentication + Serializers |
| **Médio** | 85% | Views complexas + Validações |
| **Longo** | 90%+ | Edge cases + Integrações |

## 📂 Arquivos Gerados

```
htmlcov/
├── index.html          # Página principal do relatório
├── app_alojamentos_models_py.html
├── app_funcionarios_views_py.html
└── ...                 # Um arquivo por módulo
```

### 🌐 Como Ver Relatório HTML
```bash
# Abrir no navegador padrão (Windows)
start htmlcov/index.html

# Ou navegar manualmente até a pasta htmlcov/
```

## 💡 Dicas Importantes

### ✅ **Boas Práticas:**
- Foque primeiro nas áreas com **0% de cobertura**
- **80% de cobertura** é geralmente suficiente
- Teste **casos de erro** e **edge cases**
- Ignore arquivos de configuração (`migrations`, `settings`)

### ❌ **Evite:**
- Obsessão por 100% (nem sempre necessário)
- Testes apenas para "aumentar números"
- Ignorar lógica complexa não testada

## 🔄 Integração com CI/CD

```yaml
# Exemplo para GitHub Actions
- name: Run Tests with Coverage
  run: python run_coverage.py
  
- name: Upload Coverage Reports
  uses: codecov/codecov-action@v1
```

## 📊 Próximos Passos

1. **📥 Execute**: `python run_coverage.py`
2. **📖 Analise**: Abra `htmlcov/index.html`
3. **🎯 Foque**: Áreas com menor cobertura
4. **✅ Teste**: Adicione testes específicos
5. **🔄 Repita**: Execute novamente para ver progresso

---

**Meta: Elevar cobertura de 53% para 80%+ através de testes estratégicos! 🎯**
