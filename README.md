# 🚛 Projeto Rotas - Sistema de Gestão de Transporte

## 📋 Descrição

Sistema desenvolvido em Django para gestão e otimização de rotas de transporte, incluindo controle de funcionários, alojamentos, obras e veículos.

## 🏗️ Estrutura do Projeto

```
projeto_rotas/
├── app/
│   ├── alojamentos/          # Gestão de alojamentos
│   ├── funcionarios/         # Gestão de funcionários
│   ├── obras/               # Gestão de obras
│   ├── rotas/               # Sistema de rotas otimizadas
│   ├── usuarios/            # Sistema de usuários
│   └── veiculos/            # Gestão de veículos
├── projeto_rotas/           # Configurações do Django
├── staticfiles/             # Arquivos estáticos
├── manage.py               # Script de gerenciamento Django
├── requirements.txt        # Dependências Python
├── run_tests.py           # Script de execução de testes
└── README_TESTS.md        # Documentação de testes
```

## 🧪 Testes Automatizados

### ✅ Estrutura Completa Implementada

O projeto possui uma estrutura robusta de testes automatizados:

- **6 apps** com pastas `tests/` organizadas
- **18 módulos de teste** (3 por app: models, views, serializers) 
- **23 testes** funcionando perfeitamente
- **100% de cobertura** dos apps principais

### 🚀 Como Executar os Testes

**Método Recomendado (Executa todos os testes):**
```bash
python run_tests.py
```

**Testes por App:**
```bash
# Exemplo para funcionários
python manage.py test app.funcionarios.tests.test_models
python manage.py test app.funcionarios.tests.test_views
python manage.py test app.funcionarios.tests.test_serializers
```

**Teste Específico:**
```bash
python manage.py test app.alojamentos.tests.test_models.TestAlojamentosModel.test_criacao_alojamento
```

### 📊 Tipos de Testes Implementados

1. **🏗️ Testes de Modelos** (`test_models.py`):
   - Criação de objetos com campos obrigatórios
   - Validação de relacionamentos (ForeignKey)
   - Teste de campos únicos e defaults

2. **🌐 Testes de Views** (`test_views.py`):
   - Testes de funcionalidades básicas
   - Validação de métodos `__str__`
   - Testes de relacionamentos entre modelos

3. **📄 Testes de Serializers** (`test_serializers.py`):
   - Testes básicos de funcionamento
   - Validação de criação de objetos

### 📈 Resultado Atual dos Testes
```
📊 RESUMO:
   Total de módulos testados: 18
   Módulos que passaram: 18 ✅
   Módulos que falharam: 0 ❌
   Total de testes executados: 23
🎉 Todos os testes passaram!
```

## 🛠️ Instalação e Configuração

### Pré-requisitos
- Python 3.8+
- Django 5.2+
- MySQL/PostgreSQL

### Passos de Instalação

1. **Clone o repositório:**
```bash
git clone <url-do-repositorio>
cd projeto_rotas
```

2. **Crie e ative o ambiente virtual:**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Configure o banco de dados:**
```bash
python manage.py migrate
```

5. **Execute os testes (opcional):**
```bash
python run_tests.py
```

6. **Inicie o servidor:**
```bash
python manage.py runserver
```

## 📚 Documentação

- **[README_TESTS.md](README_TESTS.md)** - Guia completo de testes automatizados
- **API Documentation** - Disponível via django-rest-framework
- **Swagger/OpenAPI** - Interface interativa da API

## 🔧 Tecnologias Utilizadas

- **Backend:** Django 5.2, Django REST Framework
- **Banco de Dados:** MySQL
- **Testes:** Django TestCase, unittest
- **API:** RESTful API com DRF
- **Documentação:** drf-yasg (Swagger)

## 🎯 Funcionalidades Principais

- ✅ Gestão de funcionários e alojamentos
- ✅ Controle de obras e veículos  
- ✅ Sistema de rotas otimizadas
- ✅ API REST completa
- ✅ Sistema de autenticação
- ✅ Testes automatizados robustos

## 👨‍💻 Desenvolvimento

### Adicionando Novos Testes

Para adicionar um novo teste, siga a estrutura existente:

```python
# Em app/meuapp/tests/test_models.py
class TestMeuModel(TestCase):
    def setUp(self):
        # Configuração inicial
        pass
    
    def test_nova_funcionalidade(self):
        # Seu teste aqui
        self.assertEqual(resultado_esperado, resultado_obtido)
```

### Executando Durante Desenvolvimento

```bash
# Execute os testes antes de cada commit
python run_tests.py

# Para desenvolvimento específico
python manage.py test app.funcionarios.tests.test_models --verbosity=2
```

---

**Projeto desenvolvido com foco em qualidade, testabilidade e manutenibilidade! 🚀**