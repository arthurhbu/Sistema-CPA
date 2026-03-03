import { useState, useEffect } from 'react';
import styles from './Instrumentos.module.css';

function Instrumentos() {
    // Estados para os dados
    const [instrumentos, setInstrumentos] = useState([]);
    const [resumo, setResumo] = useState({
        totalImportados: 0,
        totalSucesso: 0,
        totalErros: 0,
        aguardandoProcessamento: 0,
        emProcessamento: 0
    });
    const [paginaAtual, setPaginaAtual] = useState(1);
    const [totalPaginas, setTotalPaginas] = useState(1);
    const [filtros, setFiltros] = useState({
        status: 'todos',
        dataInicio: '',
        dataFim: '',
        busca: ''
    });
    const [processing, setProcessing] = useState(false);

    const buscarProgresso = async () => { 
        try { 
            const res = await fetch(`${process.env.REACT_APP_BACKEND}/api/csv/importacao/progresso`);

            const data = await res.json();

            if (!res.ok) { 
                throw new Error('Erro ao buscar o status do processo');
            }
            setProcessing(data.processing);
        } catch (error) { 
            console.error('Erro ao buscar o status do processo:', error);
        }
    }

    // Função para buscar os instrumentos
    const buscarInstrumentosStatus = async () => {
        try {
            const response = await fetch(`${process.env.REACT_APP_BACKEND}/api/instrumento/listarComStatus`);
            const data = await response.json();
            
            // Verifica se data é um array, se não for, converte para array
            const instrumentosArray = Array.isArray(data) ? data : Object.values(data);
            console.log(instrumentosArray);
            setInstrumentos(instrumentosArray);
            
            // Atualizar resumo baseado nos dados recebidos
            const novoResumo = {
                totalImportados: instrumentosArray.length,
                totalSucesso: instrumentosArray.filter(i => i.percentual_processados === 100).length,
                totalErros: instrumentosArray.filter(i => !i.importado && !processing).length,
                aguardandoProcessamento: instrumentosArray.filter(i => i.importado && i.percentual_processados !== 100 && !processing).length,
                emProcessamento: instrumentosArray.filter(i => processing && i.percentual_processados !== 100).length
            };
            setResumo(novoResumo);
        } catch (error) {
            console.error('Erro ao buscar instrumentos:', error);
            // Inicializa com arrays vazios em caso de erro
            setInstrumentos([]);
            setResumo({
                totalImportados: 0,
                totalSucesso: 0,
                totalErros: 0,
                aguardandoProcessamento: 0,
                emProcessamento: 0
            });
        }
    };

    // Função para continuar a geração do instrumento
    const continuarGeracao = async (nomeInstrumento) => {
        try {
            console.log('Iniciando continuação da geração do instrumento:', nomeInstrumento);
            
            const response = await fetch(`${process.env.REACT_APP_BACKEND}/api/instrumento/continuarGeracao`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ nome_instrumento: nomeInstrumento })
            });

            const data = await response.json();
            console.log('Resposta do servidor:', data);

            if (!response.ok) {
                throw new Error(data.error || 'Erro ao continuar geração do instrumento');
            }

            console.log('Processamento concluído com sucesso');
            buscarInstrumentosStatus(); // Atualiza a lista após iniciar a geração
        } catch (error) {
            console.error('Erro ao continuar geração do instrumento:', error);
            alert('Erro ao continuar geração do instrumento: ' + error.message);
        }
    };

    // Função para reprocessar um instrumento
    const reprocessarInstrumento = async (id) => {
        try {
            await fetch(`/api/instrumentos/${id}/reprocessar`, {
                method: 'POST'
            });
            buscarInstrumentosStatus(); // Atualiza a lista após reprocessar
        } catch (error) {
            console.error('Erro ao reprocessar instrumento:', error);
        }
    };

    // Função para baixar relatório de erros
    const baixarRelatorioErros = async (id) => {
        try {
            const response = await fetch(`/api/instrumentos/${id}/relatorio-erros`);
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `relatorio-erros-${id}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (error) {
            console.error('Erro ao baixar relatório:', error);
        }
    };

    // Função para filtrar os instrumentos
    const filtrarInstrumentos = (instrumentos) => {
        return instrumentos.filter(instrumento => {
            // Filtro por status
            if (filtros.status !== 'todos') {
                const statusMatch = {
                    'concluido': instrumento.percentual_processados === 100,
                    'processando': processing && instrumento.percentual_processados !== 100,
                    'falha': !instrumento.importado && !processing,
                    'aguardando': instrumento.importado && instrumento.percentual_processados !== 100 && !processing
                };
                if (!statusMatch[filtros.status]) return false;
            }

            // Filtro por data
            if (filtros.dataInicio) {
                const dataInicio = new Date(filtros.dataInicio);
                const dataCriacao = new Date(instrumento.data_criacao);
                if (dataCriacao < dataInicio) return false;
            }
            if (filtros.dataFim) {
                const dataFim = new Date(filtros.dataFim);
                const dataCriacao = new Date(instrumento.data_criacao);
                if (dataCriacao > dataFim) return false;
            }

            // Filtro por busca (nome do arquivo)
            if (filtros.busca) {
                const buscaLower = filtros.busca.toLowerCase();
                const nomeInstrumentoLower = instrumento.nome_instrumento.toLowerCase();
                if (!nomeInstrumentoLower.includes(buscaLower)) return false;
            }

            return true;
        });
    };

    // Efeito para carregar dados iniciais
    useEffect(() => {
        buscarInstrumentosStatus();
        buscarProgresso();
    }, []);

    // Efeito para atualizar o status de processamento periodicamente
    useEffect(() => {
        const interval = setInterval(() => {
            buscarProgresso();
        }, 5000); // Atualiza a cada 5 segundos

        return () => clearInterval(interval);
    }, []);

    // Estado para os instrumentos filtrados
    const [instrumentosFiltrados, setInstrumentosFiltrados] = useState([]);

    // Efeito para aplicar os filtros
    useEffect(() => {
        const filtrados = filtrarInstrumentos(instrumentos);
        setInstrumentosFiltrados(filtrados);
    }, [instrumentos, filtros]);

    // Função para renderizar o status com ícone
    const renderizarStatus = (instrumento) => {
        if (instrumento.percentual_processados === 100) {
            return <span className={styles.statusSucesso}>🟢 Concluído</span>;
        } else if (processing && instrumento.percentual_processados !== 100) {
            return <span className={styles.statusProcessando}>🟡 Em Processamento ({instrumento.percentual_processados}%)</span>;
        } else if (!instrumento.importado && !processing) {
            return <span className={styles.statusErro}>🔴 Falha na Importação</span>;
        } else if (instrumento.importado && instrumento.percentual_processados !== 100 && !processing) {
            return <span className={styles.statusAguardando}>⚪ Aguardando Processamento</span>;
        }
    };

    return (
        <div className={styles.containerInstrumentos}>
            {/* Introdução */}
            <div className={styles.intro}>
                <h1 className={styles.titulo}>Instrumentos</h1>
                <p className={styles.infos}>
                    Nesta página você pode acompanhar o status de todos os instrumentos importados,
                    verificar o progresso do processamento e tomar ações necessárias caso ocorram problemas.
                </p>
            </div>

            {/* Cards de Resumo */}
            <div className={styles.resumoCards}>
                <div className={styles.card}>
                    <h3 className={styles.cardTitulo}>Total de Instrumentos</h3>
                    <p className={styles.cardValor}>{resumo.totalImportados}</p>
                </div>
                <div className={styles.card}>
                    <h3 className={styles.cardTitulo}>Processados com Sucesso</h3>
                    <p className={styles.cardValor}>{resumo.totalSucesso}</p>
                </div>
                <div className={styles.card}>
                    <h3 className={styles.cardTitulo}>Em Processamento</h3>
                    <p className={styles.cardValor}>{resumo.emProcessamento}</p>
                </div>
                <div className={styles.card}>
                    <h3 className={styles.cardTitulo}>Aguardando Processamento</h3>
                    <p className={styles.cardValor}>{resumo.aguardandoProcessamento}</p>
                </div>
                <div className={styles.card}>
                    <h3 className={styles.cardTitulo}>Falha na Importação</h3>
                    <p className={styles.cardValor}>{resumo.totalErros}</p>
                </div>
            </div>

            {/* Filtros e Busca */}
            <div className={styles.filtrosContainer}>
                <div className={styles.busca}>
                    <input
                        type="text"
                        placeholder="Buscar por nome do arquivo..."
                        className={styles.buscaInput}
                        value={filtros.busca}
                        onChange={(e) => setFiltros({...filtros, busca: e.target.value})}
                    />
                </div>
                <div className={styles.filtros}>
                    <select
                        className={styles.filtroSelect}
                        value={filtros.status}
                        onChange={(e) => setFiltros({...filtros, status: e.target.value})}
                    >
                        <option value="todos">Todos os Status</option>
                        <option value="concluido">Concluído (100%)</option>
                        <option value="processando">Em Processamento</option>
                        <option value="falha">Falha na Importação</option>
                        <option value="aguardando">Aguardando Processamento</option>
                    </select>
                    <input
                        type="date"
                        className={styles.filtroSelect}
                        value={filtros.dataInicio}
                        onChange={(e) => setFiltros({...filtros, dataInicio: e.target.value})}
                    />
                    <input
                        type="date"
                        className={styles.filtroSelect}
                        value={filtros.dataFim}
                        onChange={(e) => setFiltros({...filtros, dataFim: e.target.value})}
                    />
                </div>
            </div>

            {/* Lista de Instrumentos */}
            <div className={styles.listaInstrumentos}>
                {instrumentosFiltrados.length === 0 ? (
                    <div className={styles.empty_state}>
                        <p className={styles.empty_state_text}>Nenhum instrumento encontrado.</p>
                        <p className={styles.empty_state_subtext}>
                            {instrumentos.length === 0 
                                ? 'Ainda não há instrumentos importados.' 
                                : 'Tente ajustar os filtros de busca.'}
                        </p>
                    </div>
                ) : (
                    instrumentosFiltrados.map((instrumento) => (
                    <div key={instrumento.nome_instrumento} className={styles.instrumentoCard}>
                        <div className={styles.instrumentoInfo}>
                            <span className={styles.nomeArquivo}>{instrumento.nome_instrumento}</span>
                            <span className={styles.dataUpload}>
                                Criado em: {new Date(instrumento.data_criacao).toLocaleDateString()}
                            </span>
                        </div>
                        <div className={styles.status}>
                            {renderizarStatus(instrumento)}
                        </div>
                        <div className={styles.progresso}>
                            <div>Total de Documentos: {instrumento.total_documentos}</div>
                            <div>Processados: {instrumento.documentos_processados}</div>
                            <div>Não Processados: {instrumento.documentos_nao_processados}</div>
                            <div>Progresso: {instrumento.percentual_processados}%</div>
                        </div>
                        <div className={styles.acoes}>
                            <button
                                className={`${styles.botaoAcao} ${styles.botaoDetalhes}`}
                                onClick={() => window.location.href = `/instrumentos/${instrumento.nome_instrumento}`}
                            >
                                Ver Detalhes
                            </button>
                            {(!instrumento.importado || !instrumento.gerado) && (
                                <button
                                    className={`${styles.botaoAcao} ${styles.botaoContinuar}`}
                                    onClick={() => continuarGeracao(instrumento.nome_instrumento)}
                                >
                                    Continuar Geração
                                </button>
                            )}
                        </div>
                    </div>
                    ))
                )}
            </div>

            {/* Paginação */}
            <div className={styles.paginacao}>
                {Array.from({ length: totalPaginas }, (_, i) => i + 1).map((pagina) => (
                    <button
                        key={pagina}
                        className={`${styles.paginaBotao} ${pagina === paginaAtual ? styles.paginaBotaoAtivo : ''}`}
                        onClick={() => setPaginaAtual(pagina)}
                    >
                        {pagina}
                    </button>
                ))}
            </div>
        </div>
    );
}

export default Instrumentos;
