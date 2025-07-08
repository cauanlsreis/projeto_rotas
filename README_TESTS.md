# 🧪 Guia de Testes Automatizados - Projeto Rotas

## 📋 Estrutura de Testes Criada

Cada app possui uma pasta `tests/` com os seguintes arquivos:

```
app/
├── alojamentos/tests/
│   ├── __init__.py
│   ├── test_models.py      # Testes dos modelos
│   ├── test_views.py       # Testes das views
│   └── test_serializers.py # Testes dos serializers
├── funcionarios/tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_views.py
│   └── test_serializers.py
├── obras/tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_views.py
│   └── test_serializers.py
├── rotas/tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_views.py
│   └── test_serializers.py
├── usuarios/tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_views.py
│   └── test_serializers.py
└── veiculos/tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_views.py
    └── test_serializers.py
```

## 🚀 Como Executar os Testes

### 1. Executar Todos os Testes (Método Recomendado)

```bash
python run_tests.py
```

Este script executa todos os testes de forma organizada e mostra um resumo no final.

### 2. Executar Testes por App

```bash
# Testes de alojamentos
python manage.py test app.alojamentos.tests.test_models
python manage.py test app.alojamentos.tests.test_views
python manage.py test app.alojamentos.tests.test_serializers

# Testes de funcionários
python manage.py test app.funcionarios.tests.test_models
python manage.py test app.funcionarios.tests.test_views
python manage.py test app.funcionarios.tests.test_serializers

# Testes de obras
python manage.py test app.obras.tests.test_models
python manage.py test app.obras.tests.test_views
python manage.py test app.obras.tests.test_serializers

# Testes de rotas
python manage.py test app.rotas.tests.test_models
python manage.py test app.rotas.tests.test_views
python manage.py test app.rotas.tests.test_serializers

# Testes de usuários
python manage.py test app.usuarios.tests.test_models
python manage.py test app.usuarios.tests.test_views
python manage.py test app.usuarios.tests.test_serializers

# Testes de veículos
python manage.py test app.veiculos.tests.test_models
python manage.py test app.veiculos.tests.test_views
python manage.py test app.veiculos.tests.test_serializers
```

### 3. Executar um Teste Específico

```bash
# Exemplo: testar apenas a criação de alojamentos
python manage.py test app.alojamentos.tests.test_models.TestAlojamentosModel.test_criacao_alojamento
```

### 4. Executar com Verbosidade Alta

```bash
python manage.py test app.alojamentos.tests.test_models --verbosity=2
```

## 📝 Tipos de Testes Implementados

### 🏗️ Testes de Modelos (`test_models.py`)
- ✅ Criação de objetos com campos obrigatórios
- ✅ Validação de relacionamentos (ForeignKey)
- ✅ Teste de campos únicos (unique)
- ✅ Validação de defaults

### 🌐 Testes de Views (`test_views.py`)
- ✅ Testes básicos de criação e funcionamento
- ✅ Validação de métodos `__str__`
- ✅ Testes de campos únicos e validações
- ✅ Testes de relacionamentos entre modelos

### 📄 Testes de Serializers (`test_serializers.py`)
- ✅ Testes básicos de funcionamento
- ✅ Validação de criação de objetos

## 🔧 Exemplos de Testes

### Teste de Modelo (Alojamento)
```python
def test_criacao_alojamento(self):
    aloj = Alojamentos.objects.create(
        nome="Teste Alojamento",
        endereco="Rua Teste",
        numero="123",
        cidade="São Paulo",
        estado="SP",
        latitude=-23.550520,
        longitude=-46.633309
    )
    self.assertEqual(aloj.nome, "Teste Alojamento")
    self.assertEqual(aloj.cidade, "São Paulo")
```

### Teste de Relacionamento (Funcionário)
```python
def test_criacao_funcionario(self):
    # Primeiro criar um alojamento (necessário para o funcionário)
    alojamento = Alojamentos.objects.create(...)
    
    funcionario = Funcionarios.objects.create(
        nome_completo="João Silva",
        cpf="123.456.789-00",
        alojamento=alojamento
    )
    self.assertEqual(funcionario.nome_completo, "João Silva")
```

## 📊 Cobertura de Testes

Cada app possui testes para:
- ✅ **Modelos**: Criação, validação, relacionamentos
- ✅ **Views**: Funcionalidades básicas (adaptáveis para APIs)
- ✅ **Serializers**: Estrutura básica

## 🛠️ Personalização

### Adicionando Novos Testes

1. **Para um novo modelo**: Adicione em `test_models.py`
2. **Para uma nova view**: Adicione em `test_views.py`
3. **Para um novo serializer**: Adicione em `test_serializers.py`

### Exemplo de Teste Personalizado
```python
class TestNovoRecurso(TestCase):
    def setUp(self):
        # Configuração inicial
        pass
    
    def test_nova_funcionalidade(self):
        # Seu teste aqui
        self.assertEqual(resultado_esperado, resultado_obtido)
```

## 🔍 Debugging de Testes

### Testes que Falham
Se um teste falhar, o Django mostrará:
- ❌ Qual teste falhou
- 📍 Linha exata do erro
- 📝 Descrição do erro

### Teste com Dados de Debug
```python
def test_debug_example(self):
    obj = MinhaModel.objects.create(...)
    print(f"Objeto criado: {obj}")  # Para debug
    self.assertEqual(obj.campo, "valor_esperado")
```

## 📈 Boas Práticas

1. **Execute os testes regularmente** durante o desenvolvimento
2. **Adicione novos testes** sempre que criar novas funcionalidades
3. **Use nomes descritivos** para os métodos de teste
4. **Mantenha os testes simples** e focados em uma funcionalidade
5. **Use setUp()** para dados que são usados em múltiplos testes

## 🎯 Próximos Passos

Para expandir os testes, considere adicionar:
- 🔐 Testes de autenticação e autorização
- 🌐 Testes de API completos (com requisições HTTP)
- 📊 Testes de performance
- 🧪 Testes de integração
- 📋 Testes de validação de formulários
- 🔄 Testes de migrations

---

**Agora você possui uma base sólida de testes automatizados! 🚀**
