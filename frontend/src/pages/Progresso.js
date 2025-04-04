import { useEffect, useState, useCallback } from 'react';
import Styles from './Progresso.module.css';
import { ring2, waveform, hatch } from 'ldrs'

ring2.register()
waveform.register()
hatch.register()

const Processo = () => {
    const [processing, setProcessing] = useState(false);
    const [filename, setFilename] = useState('');
    const [progresso, setProgresso] = useState({});

    const checkStatus = useCallback(async () => { 
        try {
            const response = await fetch(`${process.env.REACT_APP_BACKEND}/api/csv/importacao/progresso`);
            if (!response.ok) {
                throw new Error('Erro ao buscar o status do processo');
            }
            const status = await response.json();
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
            ) : (
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
