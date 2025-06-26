import { useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import Styles from './Progresso.module.css';
import { ring2, waveform, hatch } from 'ldrs'

ring2.register()
waveform.register()
hatch.register()

const Processo = () => {
    const navigate = useNavigate();
    const [processing, setProcessing] = useState(false);
    const [filename, setFilename] = useState('');
    const [progresso, setProgresso] = useState({});
    const [finishedProcessing, setFinishedProcessing] = useState(false);
    const [lastProcessedFile, setLastProcessedFile] = useState('');
    const [lastProcessedProgress, setLastProcessedProgress] = useState({});
    const [processingResult, setProcessingResult] = useState(null); // 'success', 'error', null

    const checkStatus = useCallback(async () => { 
        try {
            const response = await fetch(`${process.env.REACT_APP_BACKEND}/api/csv/importacao/progresso`);
            if (!response.ok) {
                throw new Error('Erro ao buscar o status do processo');
            }
            const status = await response.json();
            
            // Se estava processando e agora não está mais, significa que finalizou
            if (processing && !status.processing) {
                setFinishedProcessing(true);
                setLastProcessedFile(filename);
                setLastProcessedProgress(progresso);
                
                // Verificar se houve erro no processamento
                const hasErrors = Object.values(progresso).some(value => 
                    value !== 'Finalizado' && value !== 'Pendente'
                );
                setProcessingResult(hasErrors ? 'error' : 'success');
            }
            
            // Se não estava processando e agora está, significa que um novo processo começou
            if (!processing && status.processing) {
                setFinishedProcessing(false);
                setProcessingResult(null);
                setLastProcessedFile('');
                setLastProcessedProgress({});
            }
            
            setProcessing(status.processing);
            setFilename(status.file);
            setProgresso(status.progresso);
        } catch (error) {
            console.error('Erro na requisição:', error);
        }
    }, [processing, filename, progresso]);

    useEffect(() => { 
        checkStatus();
    }, [])

    useEffect(() => { 
        const interval = setInterval(checkStatus, 5000); 
        return () => {
            clearInterval(interval);
        };
    }, [checkStatus]);

    const handleBackToDefault = () => {
        setFinishedProcessing(false);
        setProcessingResult(null);
        setLastProcessedFile('');
        setLastProcessedProgress({});
    };

    const getErrorMessages = () => {
        return Object.entries(lastProcessedProgress)
            .filter(([key, value]) => value !== 'Finalizado' && value !== 'Pendente')
            .map(([key, value]) => `${key}: ${value}`);
    };

    return(
        <div className={Styles.containerProgresso}>

            {/* Container para infos e introdução da página */}
            <div className={Styles.containerIntroducao}>
                <p className={Styles.containerIntroducao_tituloPagina}>Progresso do Instrumento</p>
                <p className={Styles.containerIntroducao_textoIntro}>Pagina dedicada à ilustrar se um instrumento está sendo processado. Ao final do processamento de um instrumento, um email será enviado como aviso. É necessário apontar: enquanto um Instrumento estiver em processo não tente inserir outro arquivo para que não haja problemas.</p>
            </div>
            
            {/* Área que apresenta se um instrumento está processando ou não*/}
            {processing ? (
                <>
                    {/* Loading animation */}
                    <div className={Styles.containerProcessando}>
                        <p className={Styles.containerProcessando_titulo}>Um instrumento está sendo processado</p>
                        <div className={Styles.containerAnimation}>
                            <div className={Styles.circleAnimation}>                        
                                <l-ring-2
                                    size="500"
                                    stroke="20"
                                    stroke-length="0.25"
                                    bg-opacity="0.1"
                                    speed="3" 
                                    color="#3dff94" 
                                ></l-ring-2>

                                <div className={Styles.waveAnimation}>
                                    <l-waveform
                                        size="150"
                                        stroke="10"
                                        speed="1" 
                                        color="black" 
                                    ></l-waveform>
                                </div>
                            </div>
                        </div>

                        {/* Infos de progresso da importação */}
                        <p className={Styles.containerProcessando_nomeInstrumento}>Instrumento: {filename}</p>
                        <p style={{fontSize: '1.8rem', fontWeight: '500', marginBottom: '0', marginTop:'60px'}}>Etapas</p>
                        <ul className={Styles.checkList}>
                            {Object.keys(progresso).length > 0 ? ( 
                                Object.keys(progresso)
                                .filter(key => key !== 'Importado' && key !== 'Gerado')
                                .reverse() 
                                .map((key) => (
                                    progresso[key] === 'Finalizado' ? (
                                        <li className={Styles.itemCheckList_finalizado} key={key}>
                                            {key}: {"Finalizada ✅"}
                                        </li>
                                    ) : progresso[key] === 'Pendente' ? (
                                        <li className={Styles.itemCheckList_pendente} key={key}>
                                            {key}: {"Pendente ⌛"}
                                        </li>
                                    ) : (
                                        <li className={Styles.itemCheckList_erro} key={key}>
                                            {key}: {progresso[key]}
                                        </li>
                                    )
                                ))
                            ) : (
                                <li>Nenhum progresso encontrado.</li>
                            )}
                        </ul>
                    </div>
                </>
            ) : finishedProcessing ? (
                // Tela de resultado da importação finalizada
                <div className={Styles.containerProcessando}>
                    <p className={Styles.containerProcessando_titulo}>
                        {processingResult === 'success' ? 'Importação Concluída com Sucesso!' : 'Erro na Importação'}
                    </p>
                    
                    <div className={Styles.containerAnimation}>
                        {processingResult === 'success' ? (
                            <div style={{fontSize: '8rem', color: '#3dff94', marginBottom: '2rem'}}>✅</div>
                        ) : (
                            <div style={{fontSize: '8rem', color: '#ff3d3d', marginBottom: '2rem'}}>❌</div>
                        )}
                    </div>

                    <p className={Styles.containerProcessando_nomeInstrumento}>Instrumento: {lastProcessedFile}</p>
                    
                    {processingResult === 'success' ? (
                        <div style={{textAlign: 'center', marginTop: '2rem'}}>
                            <p style={{fontSize: '1.5rem', color: '#3dff94', marginBottom: '1rem'}}>
                                Todas as etapas foram concluídas com sucesso!
                            </p>
                            <p style={{fontSize: '1.2rem', color: '#666', marginBottom: '2rem'}}>
                                O instrumento foi processado e está pronto para geração de relatórios.
                            </p>
                        </div>
                    ) : (
                        <div style={{textAlign: 'center', marginTop: '2rem'}}>
                            <p style={{fontSize: '1.5rem', color: '#ff3d3d', marginBottom: '1rem'}}>
                                Ocorreram erros durante o processamento:
                            </p>
                            <div style={{marginBottom: '2rem'}}>
                                {getErrorMessages().map((error, index) => (
                                    <p key={index} style={{fontSize: '1.1rem', color: '#ff3d3d', marginBottom: '0.5rem'}}>
                                        {error}
                                    </p>
                                ))}
                            </div>
                        </div>
                    )}

                    <div style={{textAlign: 'center', marginTop: '3rem'}}>
                        <button 
                            onClick={handleBackToDefault}
                            style={{
                                padding: '1rem 2rem',
                                fontSize: '1.2rem',
                                backgroundColor: '#3dff94',
                                color: '#000',
                                border: 'none',
                                borderRadius: '8px',
                                cursor: 'pointer',
                                fontWeight: '600',
                                transition: 'all 0.3s ease'
                            }}
                            onMouseOver={(e) => e.target.style.backgroundColor = '#2dd884'}
                            onMouseOut={(e) => e.target.style.backgroundColor = '#3dff94'}
                        >
                            Voltar à Tela Principal
                        </button>
                    </div>
                </div>
            ) : (
                // Tela default - nenhum instrumento sendo processado
                <div className={Styles.containerProcessando}>
                    <p className={Styles.containerProcessando_titulo}>Nenhum Instrumento está sendo processado</p>
                    <div className={Styles.containerAnimation}>
                        <l-hatch
                            size="250"
                            stroke="28"
                            speed="5.5" 
                            color="#3dff94" 
                        ></l-hatch>
                    </div>
                </div>
            )}
        </div>
    );
}

export default Processo;
