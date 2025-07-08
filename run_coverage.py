#!/usr/bin/env python
"""
Script para executar testes com cobertura de código
"""
import os
import sys
import subprocess


def install_coverage():
    """Instala a biblioteca coverage se não estiver instalada"""
    print("📦 Verificando se coverage está instalado...")
    try:
        import coverage
        print("✅ Coverage já está instalado!")
        return True
    except ImportError:
        print("📥 Instalando coverage...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'coverage'],
                           check=True, capture_output=True)
            print("✅ Coverage instalado com sucesso!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao instalar coverage: {e}")
            return False


def run_coverage():
    """Executa os testes com cobertura de código"""
    if not install_coverage():
        return False

    print("\n🧪 Executando testes com cobertura de código...")
    print("=" * 60)

    try:
        # Limpa dados de cobertura anteriores
        print("🧹 Limpando dados de cobertura anteriores...")
        subprocess.run([sys.executable, '-m', 'coverage', 'erase'],
                       capture_output=True)

        # Executa os testes com cobertura
        print("🚀 Executando testes com coverage...")
        result = subprocess.run([
            sys.executable, '-m', 'coverage', 'run',
            '--source=app', 'manage.py', 'test'
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print("❌ Erro ao executar testes:")
            print(result.stderr)
            return False

        print("✅ Testes executados com sucesso!")

        # Gera relatório de cobertura
        print("\n📊 Gerando relatório de cobertura...")

        # Relatório resumido no terminal
        coverage_result = subprocess.run([
            sys.executable, '-m', 'coverage', 'report', '--show-missing'
        ], capture_output=True, text=True)

        print("\n" + "=" * 60)
        print("📈 RELATÓRIO DE COBERTURA DE CÓDIGO")
        print("=" * 60)
        print(coverage_result.stdout)

        # Gera relatório HTML
        print("📄 Gerando relatório HTML...")
        subprocess.run([
            sys.executable, '-m', 'coverage', 'html'
        ], capture_output=True)

        print("\n🎉 Relatórios gerados com sucesso!")
        print("📂 Relatório HTML disponível em: htmlcov/index.html")
        print("💡 Abra o arquivo htmlcov/index.html no navegador para ver detalhes")

        return True

    except Exception as e:
        print(f"❌ Erro durante execução: {e}")
        return False


def analyze_coverage():
    """Analisa os resultados da cobertura"""
    print("\n🔍 ANÁLISE DA COBERTURA:")
    print("-" * 40)
    print("📊 Interpretação dos resultados:")
    print("   • 90-100%: Excelente cobertura")
    print("   • 80-89%:  Boa cobertura")
    print("   • 70-79%:  Cobertura aceitável")
    print("   • 60-69%:  Cobertura baixa")
    print("   • <60%:    Cobertura insuficiente")
    print()
    print("💡 Dicas:")
    print("   • Foque nas linhas 'Missing' (não cobertas)")
    print("   • Adicione testes para código não coberto")
    print("   • 100% nem sempre é necessário (código de configuração, etc.)")


if __name__ == "__main__":
    print("🎯 ANÁLISE DE COBERTURA DE CÓDIGO")
    print("=" * 60)

    success = run_coverage()

    if success:
        analyze_coverage()
        print("\n✨ Análise concluída! Use o relatório para melhorar seus testes.")
    else:
        print("\n❌ Falha na análise de cobertura.")
        sys.exit(1)
