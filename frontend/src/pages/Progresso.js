import { useEffect, useState, useCallback } from 'react';
import { DotLottieReact } from '@lottiefiles/dotlottie-react';
import Styles from './Progresso.module.css';

import { ring2, waveform, hatch } from 'ldrs'

ring2.register()
waveform.register()
hatch.register()

const Processo = () => {
    const [processing, setProcessing] = useState(false);
    const [filename, setFilename] = useState('');

    const checkStatus = useCallback(async () => { 
        try {
            const response = await fetch('http://localhost:5000/progresso');
            if (!response.ok) {
                throw new Error('Erro ao buscar o status do processo');
            }
            const status = await response.json();
            setProcessing(status.processing);
            console.log(processing)
            setFilename(status.file);
            console.log(filename)
        } catch (error) {
            console.error('Erro na requisição:', error);
        }
    }, [processing, filename]);

    useEffect(() => { 
        const interval = setInterval(checkStatus, 5000);
        return () => {
            clearInterval(interval);
        };
    }, [checkStatus]);

    return(
        <div className={Styles.containerProgresso}>
            <div className={Styles.containerIntroducao}>
                <p className={Styles.containerIntroducao_tituloPagina}>Progresso do Instrumento</p>
                <p className={Styles.containerIntroducao_textoIntro}>Pagina dedicada à ilustrar se um instrumento está sendo processado. Ao final do processamento de um instrumento, um email será enviado como aviso. É necessário apontar: enquanto um Instrumento estiver em processo não tente inserir outro arquivo para que não haja problemas.</p>
            </div>
            {processing ? (
                <>
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
                        <p className={Styles.containerProcessando_nomeInstrumento}>Instrumento: {filename}</p>
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
