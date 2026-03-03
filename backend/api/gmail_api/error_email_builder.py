"""
Módulo para construção de emails de erro estruturados e informativos
"""

from datetime import datetime
from typing import Dict, Any, Optional

class ErrorEmailBuilder:
    """Classe para construir emails de erro estruturados"""
    
    @staticmethod
    def build_collections_error(instrumento: str, modalidade: str, ano: int, error_details: str, 
                               context: Dict[str, Any] = None) -> Dict[str, str]:
        """
        Constrói email de erro para problemas na criação de collections de apoio
        
        Args:
            instrumento: Nome do instrumento
            modalidade: Tipo do instrumento (EAD, Discente, etc.)
            ano: Ano de referência
            error_details: Detalhes técnicos do erro
            context: Informações adicionais de contexto
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        subject = f"ERRO SISTEMA CPA - Collections de Apoio - {instrumento}"
        
        # Informações básicas
        body_parts = [
            "SISTEMA CPA - RELATORIO DE ERRO",
            "",
            "INFORMACOES GERAIS:",
            f"- Data/Hora: {timestamp}",
            f"- Instrumento: {instrumento}",
            f"- Modalidade: {modalidade}",
            f"- Ano de Referencia: {ano}",
            f"- Etapa: Criacao de Collections de Apoio",
            ""
        ]
        
        # Adicionar contexto se disponível
        if context:
            body_parts.extend([
                "DETALHES DO PROCESSAMENTO:",
                f"- Funcao: prepare_side_dataframes()",
            ])
            
            if 'centros' in context:
                centros_str = ", ".join(context['centros']) if context['centros'] else "Nenhum"
                body_parts.append(f"- Centros encontrados: {centros_str}")
            
            if 'centro_atual' in context:
                body_parts.append(f"- Centro sendo processado: {context['centro_atual']}")
                
            if 'count_instrumento' in context:
                body_parts.append(f"- Documentos em instrumento: {context['count_instrumento']}")
                
            if 'count_cursos_centros' in context:
                body_parts.append(f"- Documentos em cursos_e_centros: {context['count_cursos_centros']}")
                
            if 'count_cursos_ano' in context:
                body_parts.append(f"- Documentos para ano {ano}: {context['count_cursos_ano']}")
                
            if 'codigos_comum' in context:
                body_parts.append(f"- Codigos de curso em comum: {context['codigos_comum']}")
            
            body_parts.append("")
        
        # Erro técnico
        body_parts.extend([
            "ERRO TECNICO:",
            f"{error_details}",
            ""
        ])
        
        # Próximos passos
        body_parts.extend([
            "ACOES RECOMENDADAS:",
            "1. Verificar se os arquivos cursos_e_centros.csv e centros_e_diretores.csv existem",
            "2. Confirmar compatibilidade entre codigos de curso",
            "3. Validar se o ano de referencia esta correto",
            "4. Verificar logs do container para mais detalhes",
            "",
            "---",
            "Sistema CPA - Universidade Estadual de Maringa"
        ])
        
        return {
            'subject': subject,
            'body': '\n'.join(body_parts)
        }
    
    @staticmethod
    def build_csv_import_error(instrumento: str, modalidade: str, etapa: str, error_details: str,
                              context: Dict[str, Any] = None) -> Dict[str, str]:
        """
        Constrói email de erro para problemas na importação de CSV
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        subject = f"ERRO SISTEMA CPA - Importacao CSV - {instrumento}"
        
        body_parts = [
            "SISTEMA CPA - RELATORIO DE ERRO",
            "",
            "INFORMACOES GERAIS:",
            f"- Data/Hora: {timestamp}",
            f"- Instrumento: {instrumento}",
            f"- Modalidade: {modalidade}",
            f"- Etapa: {etapa}",
            ""
        ]
        
        if context:
            body_parts.extend([
                "DETALHES DO PROCESSAMENTO:",
            ])
            
            if 'arquivo_csv' in context:
                body_parts.append(f"- Arquivo CSV: {context['arquivo_csv']}")
                
            if 'linhas_processadas' in context:
                body_parts.append(f"- Linhas processadas: {context['linhas_processadas']}")
                
            if 'colunas_esperadas' in context:
                body_parts.append(f"- Colunas esperadas: {context['colunas_esperadas']}")
                
            if 'colunas_encontradas' in context:
                body_parts.append(f"- Colunas encontradas: {context['colunas_encontradas']}")
            
            body_parts.append("")
        
        body_parts.extend([
            "ERRO TECNICO:",
            f"{error_details}",
            "",
            "ACOES RECOMENDADAS:",
            "1. Verificar formato e estrutura do arquivo CSV",
            "2. Confirmar se todas as colunas obrigatorias estao presentes",
            "3. Validar encoding do arquivo (UTF-8)",
            "4. Verificar se nao ha caracteres especiais problematicos",
            "",
            "---",
            "Sistema CPA - Universidade Estadual de Maringa"
        ])
        
        return {
            'subject': subject,
            'body': '\n'.join(body_parts)
        }
    
    @staticmethod
    def build_report_generation_error(instrumento: str, error_details: str,
                                    context: Dict[str, Any] = None) -> Dict[str, str]:
        """
        Constrói email de erro para problemas na geração de relatórios
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        subject = f"ERRO SISTEMA CPA - Geracao Relatorios - {instrumento}"
        
        body_parts = [
            "SISTEMA CPA - RELATORIO DE ERRO",
            "",
            "INFORMACOES GERAIS:",
            f"- Data/Hora: {timestamp}",
            f"- Instrumento: {instrumento}",
            f"- Etapa: Geracao de Relatorios",
            ""
        ]
        
        if context:
            body_parts.extend([
                "DETALHES DO PROCESSAMENTO:",
            ])
            
            if 'centro' in context:
                body_parts.append(f"- Centro: {context['centro']}")
                
            if 'curso' in context:
                body_parts.append(f"- Curso: {context['curso']}")
                
            if 'template' in context:
                body_parts.append(f"- Template: {context['template']}")
            
            body_parts.append("")
        
        body_parts.extend([
            "ERRO TECNICO:",
            f"{error_details}",
            "",
            "ACOES RECOMENDADAS:",
            "1. Verificar se as collections centro_por_ano e cursos_por_centro foram criadas",
            "2. Confirmar se os templates de introducao e conclusao existem",
            "3. Validar dados nas collections de apoio",
            "",
            "---",
            "Sistema CPA - Universidade Estadual de Maringa"
        ])
        
        return {
            'subject': subject,
            'body': '\n'.join(body_parts)
        }
    
    @staticmethod
    def build_pdf_generation_error(instrumento: str, error_details: str,
                                 context: Dict[str, Any] = None) -> Dict[str, str]:
        """
        Constrói email de erro para problemas na geração de PDFs
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        subject = f"ERRO SISTEMA CPA - Geracao PDFs - {instrumento}"
        
        body_parts = [
            "SISTEMA CPA - RELATORIO DE ERRO",
            "",
            "INFORMACOES GERAIS:",
            f"- Data/Hora: {timestamp}",
            f"- Instrumento: {instrumento}",
            f"- Etapa: Geracao de PDFs",
            ""
        ]
        
        if context:
            body_parts.extend([
                "DETALHES DO PROCESSAMENTO:",
            ])
            
            if 'total_relatorios' in context:
                body_parts.append(f"- Total de relatorios: {context['total_relatorios']}")
                
            if 'status_code' in context:
                body_parts.append(f"- Status HTTP: {context['status_code']}")
                
            if 'timeout' in context:
                body_parts.append(f"- Timeout: {context['timeout']}s")
            
            body_parts.append("")
        
        body_parts.extend([
            "ERRO TECNICO:",
            f"{error_details}",
            "",
            "ACOES RECOMENDADAS:",
            "1. Verificar se o servico conversor-pdf-backend esta rodando",
            "2. Confirmar conectividade de rede entre containers",
            "3. Validar se os arquivos markdown foram gerados corretamente",
            "4. Verificar logs do container conversor-pdf-backend",
            "",
            "---",
            "Sistema CPA - Universidade Estadual de Maringa"
        ])
        
        return {
            'subject': subject,
            'body': '\n'.join(body_parts)
        }
    
    @staticmethod
    def build_success_notification(instrumento: str, operation: str, 
                                 context: Dict[str, Any] = None) -> Dict[str, str]:
        """
        Constrói notificação de sucesso estruturada
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        subject = f"SUCESSO SISTEMA CPA - {operation} - {instrumento}"
        
        body_parts = [
            "SISTEMA CPA - NOTIFICACAO DE SUCESSO",
            "",
            "INFORMACOES GERAIS:",
            f"- Data/Hora: {timestamp}",
            f"- Instrumento: {instrumento}",
            f"- Operacao: {operation}",
            f"- Status: Concluido com sucesso",
            ""
        ]
        
        if context:
            body_parts.extend([
                "DETALHES:",
            ])
            
            for key, value in context.items():
                body_parts.append(f"- {key}: {value}")
            
            body_parts.append("")
        
        body_parts.extend([
            "PROXIMOS PASSOS:",
            "- O instrumento esta disponivel para as proximas etapas",
            "",
            "---",
            "Sistema CPA - Universidade Estadual de Maringa"
        ])
        
        return {
            'subject': subject,
            'body': '\n'.join(body_parts)
        }