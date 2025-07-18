#!/usr/bin/env python3
"""
Script para validar se todas as dependências do requirements.txt estão sendo utilizadas no código.
"""

import os
import re
import sys
from pathlib import Path

def read_requirements(file_path):
    """Lê o arquivo requirements.txt e retorna as dependências."""
    dependencies = []
    
    # Tenta diferentes codificações
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '==' in line:
                        package = line.split('==')[0].lower()
                        dependencies.append(package)
            break  # Se conseguiu ler, sai do loop
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Erro ao ler arquivo com encoding {encoding}: {e}")
            continue
    
    return dependencies

def find_python_files(directory):
    """Encontra todos os arquivos Python no diretório."""
    python_files = []
    for root, dirs, files in os.walk(directory):
        # Ignora diretórios de ambiente virtual e cache
        dirs[:] = [d for d in dirs if d not in ['venv', '__pycache__', 'Lib', 'Scripts']]
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

def extract_imports_from_file(file_path):
    """Extrai todas as importações de um arquivo Python."""
    imports = set()
    
    # Tenta diferentes codificações
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
                
            # Padrões para importações
            patterns = [
                r'^import\s+([a-zA-Z_][a-zA-Z0-9_]*)',
                r'^from\s+([a-zA-Z_][a-zA-Z0-9_]*)',
                r'^import\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+as',
                r'^from\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+import'
            ]
            
            for line in content.split('\n'):
                line = line.strip()
                for pattern in patterns:
                    match = re.match(pattern, line)
                    if match:
                        package = match.group(1).lower()
                        # Ignora importações internas do projeto
                        if not package.startswith(('src.', 'api.', 'database.', 'app')):
                            imports.add(package)
            break  # Se conseguiu ler, sai do loop
                        
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Erro ao ler arquivo {file_path} com encoding {encoding}: {e}")
            continue
    
    return imports

def validate_dependencies():
    """Valida se todas as dependências estão sendo utilizadas."""
    backend_dir = Path(__file__).parent
    requirements_file = backend_dir / 'requirements.txt'
    
    if not requirements_file.exists():
        print("❌ Arquivo requirements.txt não encontrado!")
        return False
    
    # Lê as dependências do requirements.txt
    requirements = read_requirements(requirements_file)
    print(f"📦 Dependências encontradas no requirements.txt: {len(requirements)}")
    
    # Encontra todos os arquivos Python
    python_files = find_python_files(backend_dir)
    print(f"🐍 Arquivos Python encontrados: {len(python_files)}")
    
    # Extrai todas as importações
    all_imports = set()
    for file_path in python_files:
        imports = extract_imports_from_file(file_path)
        all_imports.update(imports)
    
    print(f"📚 Importações únicas encontradas: {len(all_imports)}")
    
    # Verifica quais dependências não estão sendo usadas
    unused_dependencies = []
    for dep in requirements:
        if dep not in all_imports:
            unused_dependencies.append(dep)
    
    # Verifica quais importações não estão no requirements.txt
    missing_dependencies = []
    for imp in all_imports:
        if imp not in requirements:
            missing_dependencies.append(imp)
    
    # Relatório
    print("\n" + "="*50)
    print("RELATÓRIO DE VALIDAÇÃO")
    print("="*50)
    
    if unused_dependencies:
        print(f"\n❌ Dependências não utilizadas ({len(unused_dependencies)}):")
        for dep in unused_dependencies:
            print(f"   - {dep}")
    else:
        print("\n✅ Todas as dependências estão sendo utilizadas!")
    
    if missing_dependencies:
        print(f"\n⚠️  Importações não listadas no requirements.txt ({len(missing_dependencies)}):")
        for imp in missing_dependencies:
            print(f"   - {imp}")
        print("\n💡 Nota: Algumas dessas podem ser bibliotecas padrão do Python")
    else:
        print("\n✅ Todas as importações estão cobertas!")
    
    # Lista de bibliotecas padrão do Python para referência
    stdlib_modules = {
        'os', 'sys', 're', 'json', 'csv', 'zipfile', 'smtplib', 'email', 
        'threading', 'time', 'shutil', 'logging', 'datetime', 'random',
        'pathlib', 'configparser', 'base64', 'typing', 'collections',
        'functools', 'itertools', 'urllib', 'http', 'ssl', 'socket',
        'subprocess', 'tempfile', 'pickle', 'copy', 'math', 'statistics'
    }
    
    print(f"\n📋 Bibliotecas padrão do Python encontradas:")
    stdlib_found = [imp for imp in all_imports if imp in stdlib_modules]
    for imp in sorted(stdlib_found):
        print(f"   - {imp}")
    
    return len(unused_dependencies) == 0

if __name__ == "__main__":
    print("🔍 Validando dependências do Sistema CPA Backend...")
    success = validate_dependencies()
    
    if success:
        print("\n🎉 Validação concluída com sucesso!")
        sys.exit(0)
    else:
        print("\n⚠️  Validação encontrou problemas. Verifique o relatório acima.")
        sys.exit(1) 