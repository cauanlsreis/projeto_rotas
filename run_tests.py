#!/usr/bin/env python
"""
Script para executar todos os testes do projeto
"""
import os
import sys
import subprocess

# Lista de todos os módulos de teste
TEST_MODULES = [
    'app.alojamentos.tests.test_models',
    'app.alojamentos.tests.test_views',
    'app.alojamentos.tests.test_serializers',
    'app.funcionarios.tests.test_models',
    'app.funcionarios.tests.test_views',
    'app.funcionarios.tests.test_serializers',
    'app.obras.tests.test_models',
    'app.obras.tests.test_views',
    'app.obras.tests.test_serializers',
    'app.rotas.tests.test_models',
    'app.rotas.tests.test_views',
    'app.rotas.tests.test_serializers',
    'app.usuarios.tests.test_models',
    'app.usuarios.tests.test_views',
    'app.usuarios.tests.test_serializers',
    'app.veiculos.tests.test_models',
    'app.veiculos.tests.test_views',
    'app.veiculos.tests.test_serializers',
]


def run_tests():
    """Executa todos os testes"""
    print("🚀 Iniciando execução de todos os testes...")
    print("=" * 50)

    total_tests = 0
    failed_tests = 0

    for module in TEST_MODULES:
        print(f"\n📝 Executando: {module}")
        try:
            result = subprocess.run([
                sys.executable, 'manage.py', 'test', module
            ], capture_output=True, text=True)

            if result.returncode == 0:
                print(f"✅ {module} - PASSOU")
                # Conta quantos testes passaram
                if "Ran" in result.stderr:
                    tests_run = result.stderr.split(
                        "Ran ")[1].split(" test")[0]
                    total_tests += int(tests_run)
            else:
                print(f"❌ {module} - FALHOU")
                failed_tests += 1
                print(f"Erro: {result.stderr}")

        except Exception as e:
            print(f"❌ {module} - ERRO: {e}")
            failed_tests += 1

    print("\n" + "=" * 50)
    print(f"📊 RESUMO:")
    print(f"   Total de módulos testados: {len(TEST_MODULES)}")
    print(f"   Módulos que passaram: {len(TEST_MODULES) - failed_tests}")
    print(f"   Módulos que falharam: {failed_tests}")
    print(f"   Total de testes executados: {total_tests}")

    if failed_tests == 0:
        print("🎉 Todos os testes passaram!")
    else:
        print(f"⚠️  {failed_tests} módulo(s) apresentaram falhas")

    return failed_tests == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
