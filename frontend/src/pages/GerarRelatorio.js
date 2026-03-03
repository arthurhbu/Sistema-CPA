import { CiImport } from "react-icons/ci";
import styles from './GerarRelatorio.module.css';
import StyledInput from '../components/StyledInput';
import { useEffect, useState, useRef } from 'react';
import SelectAutoWidth from '../components/selectAutoWidth';
import delete_icon from '../img/trash.png';

function GerarRelatorio(){

    /*
        FALTA CRIAR LÓGICA PARA INSERIR NOVA INTRODUÇÃO E NOVA CONCLUSÃO, ALÉM DE CRIAR ALGUNS BLOQUEIOS PARA QUE PESSOA NÃO POSSA TENTAR ENVIAR COISAS SEM TER PREENCHIDO OU ALGO DO GENERO. 
    */

    const introducaoInputRef = useRef(null);
    const conclusaoInputRef = useRef(null);

    const [introducaoFile, setIntroducaoFile] = useState([]);
    const [conclusaoFile, setConclusaoFile] = useState([]);
    const [ano, setAno] = useState('');
    const [introConcl, setIntroConcl] = useState('');
    const [databases, setDatabases] = useState([]);
    const [instrumento, setInstrumento] = useState('');
    const [popupConfirmReplaceIntroVisible, setPopupConfirmReplaceIntroVisible] = useState(false);
    const [popupConfirmReplaceConclVisible, setPopupConfirmReplaceConclVisible] = useState(false);
    const [popupVisible, setPopupVisible] = useState(false);
    const [popupMessage, setPopupMessage] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [isProcessing, setIsProcessing] = useState(false);
    const [idInstrumento, setIdInstrumento] = useState('');
    const [isLoadingZips, setIsLoadingZips] = useState(false);
    const [avaliableZips, setAvaliableZips] = useState([]);

    const triggerIntroducaoInput = () => introducaoInputRef.current.click();
    const triggerConclusaoInput = () => conclusaoInputRef.current.click();

    const tipoIntroConlc = [
        {label: 'Nenhum', value: ''},
        {label: 'Discente', value: 'discente'},
        {label: 'Egresso', value: 'egresso'},
        {label: 'EAD', value: 'ead'},
        {label: 'Docente', value: 'docente'},
        {label: 'Agente', value: 'agente'},
        {label: 'Pos', value: 'pos'},
    ];

    const handleSelectIntroConlcChange = (value) => { 
        setIntroConcl(value);
    }

    const handleSelectDatabaseChange = (value) => { 
        setInstrumento(value)
    } 

    const handleAnoChange = (e) => { 
        setAno(e.target.value);
    }

    const handleIntroducaoChange = (e) => { 
        if (e.target.files.length > 0) { 
            setIntroducaoFile(Array.from(e.target.files));
        }
    }

    const handleConclusaoChange = (e) => { 
        if (e.target.files.length > 0) { 
            setConclusaoFile(Array.from(e.target.files));
        }
    }

    const renderFileList = (files) => { 
        return files.map((file, index) => (
            <p style={{margin: '0', fontSize: '1.3rem', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', width: '70%', marginLeft: '15px', alignSelf: 'center'}}>{file.name}</p>
        ))
    }

    const listDatabases = []
    {databases.map((database) => { 
        listDatabases.push({
            label: database, value: database
        })
    }
    )}
    
    const fetchZipsDisponiveis = async () => {
        setIsLoadingZips(true);

        try {
            const response = await fetch(`${process.env.REACT_APP_BACKEND}/api/relatorios/zips`, {
                method: 'GET',
            })

            if(!response.ok) {
                throw new Error('Erro na resposta do servidor')
            }

            const resData = await response.json();

            if(resData.error) {
                console.log(resData.error)
            }
            
            setAvaliableZips(resData.zips || []);
        } catch(e){
            console.error('Erro ao tentar fazer requisição', e);
        } finally { 
            setIsLoadingZips(false);
        }
    }

    useEffect(() => {
        fetchZipsDisponiveis();
    }, [isProcessing]);

    const handleConfirmationReplaceArchive = (type) => { 
        if (type === 'introducao') {
            if (!introducaoFile || introducaoFile.length === 0) {
                setErrorMessage('Selecione um arquivo para substituir a introdução!');
                return;
            }
            if(!instrumento) {
                setPopupMessage('Primeiro escolha o instrumento!');
                setPopupVisible(true);
                return;
            }
            setErrorMessage('');
            setPopupMessage('Você tem certeza que deseja substituir a introdução?'); 
            setPopupConfirmReplaceIntroVisible(true);
        } else if (type === 'conclusao') { 
            if (!conclusaoFile || conclusaoFile.length === 0) {
                setErrorMessage('Selecione um arquivo para substituir a conclusão!');
                return;
            }
            if(!instrumento) {
                setPopupMessage('Primeiro escolha o instrumento!');
                setPopupVisible(true);
                return;
            }
            setErrorMessage('');
            setPopupMessage('Você tem certeza que deseja substituir a conclusão?'); 
            setPopupConfirmReplaceConclVisible(true);
        }
    }

    const handleConfirmReplaceIntroduction = async (arquivo) => {
        try { 
            const formData = new FormData();
            formData.append('arquivo_introducao', arquivo[0]);
            const response = await fetch(`${process.env.REACT_APP_BACKEND}/api/instrumento/${instrumento}/introducao/substituir`, {
                method: 'POST',
                body: formData,
            })

            if(!response.ok) {
                setPopupMessage('Erro na resposta do servidor');
                setPopupVisible(true);
                return;
            }

            const resData = await response.json();

            if(resData.error) {
                setPopupMessage(resData.error + resData.details);
                setPopupVisible(true);
                return;
            }

            setPopupMessage(resData.message)
            setPopupVisible(true);
            setIntroducaoFile([]);

        } catch(e) { 
            console.log('Não foi possível realizar a requisição', e)
        }
    }

    const handleConfirmReplaceConclusion = async (arquivo) => {
        try { 
            const formData = new FormData();
            formData.append('arquivo_conclusao', arquivo[0]);
            console.log(arquivo[0])
            const response = await fetch(`${process.env.REACT_APP_BACKEND}/api/instrumento/${instrumento}/conclusao/substituir`, {
                method: 'POST',
                body: formData,
            })

            if(!response.ok) {
                setPopupMessage('Erro na resposta do servidor');
                setPopupVisible(true);
                return;
            }
            
            const resData = await response.json();

            if(resData.error) {
                setPopupMessage(resData.error + resData.details);
                setPopupVisible(true);
                return;
            }

            setPopupMessage(resData.message)
            setPopupVisible(true);
            setIntroducaoFile([]);

        } catch(e) { 
            console.log('Não foi possível realizar a requisição', e)
        }
    }

    const handleDownloadIntroducao = () => { 
        if (!instrumento) { 
            setErrorMessage('Primeiro escolha o instrumento!');
            return;
        }
        setErrorMessage('');
        const link = document.createElement('a');
        link.href = `${process.env.REACT_APP_BACKEND}/api/instrumento/${instrumento}/introducao/download`;
        link.setAttribute('download', `introducao_${instrumento}.md`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    const handleDownloadConclusao = () => { 
        if (!instrumento) { 
            setErrorMessage('Primeiro escolha o instrumento!');
            return;
        }
        setErrorMessage('');
        const link = document.createElement('a');
        link.href = `${process.env.REACT_APP_BACKEND}/api/instrumento/${instrumento}/conclusao/download`;
        link.setAttribute('download', `introducao_${instrumento}.md`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    const handleGenerate = async (ano, introConcl, instrumento) => { 
        const formData = new FormData();

        formData.append('ano', ano);
        formData.append('introConcl', introConcl);
        formData.append('instrumento', instrumento);

        try { 
            setIsProcessing(true);
            const response = await fetch(`${process.env.REACT_APP_BACKEND}/api/relatorios/gerar`, {
                method: 'POST',
                body: formData
            })

            const resData = await response.json();

            if(!response.ok) { 
                throw new Error('Erro na resposta do servidor')
            }

            if(resData.error) {
                setPopupMessage(resData.error);
                setPopupVisible(true);
                throw new Error(resData.error);
            }
            
            setPopupVisible(true);
            setIdInstrumento(resData.id_instrumento);
            setPopupMessage('Relatórios gerados com sucesso!');
            setPopupVisible(true);

        } catch(e) { 
            console.log('Não foi possível realizar a requisição', e)
        } finally { 
            setIsProcessing(false);
        }
    }

    const downloadZip = (idInstrumento) => { 
        if (!idInstrumento) { 
            return;
        }

        const link = document.createElement('a');
        link.href = `${process.env.REACT_APP_BACKEND}/api/relatorios/${idInstrumento}/download`;
        link.setAttribute('download', `relatorio_${idInstrumento}.zip`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    const deleteZip = async (idInstrumento) => {

        if (!idInstrumento) {
            console.error('ID do instrumento não foi passado');
            return;
        }
        try {
            const response = await fetch(`${process.env.REACT_APP_BACKEND}/api/relatorios/${idInstrumento}/delete`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                console.error('Erro ao tentar deletar o ZIP');
                return;
            }

            const resData = await response.json();

            if (resData.error) {
                setPopupMessage(resData.error);
                setPopupVisible(true);
                return;
            }

            setPopupMessage('ZIP deletado com sucesso!');
            setPopupVisible(true);
            fetchZipsDisponiveis();
        } catch (e) {
            console.error('Erro ao tentar deletar o ZIP', e);
            setPopupMessage('Erro ao deletar o ZIP');
            setPopupVisible(true);
        }

    }

    const handleSubmit = async () => { 
        if(!ano || !instrumento || !introConcl) { 
            setErrorMessage('Por Favor, preencha todos os campos antes de gerar o relatório')
            return;
        }

        setErrorMessage('');
        
        await handleGenerate(ano, introConcl, instrumento);
    }

    useEffect(() => {
        const fetchDatabase = async () => { 
            try { 
                const res = await fetch(`${process.env.REACT_APP_BACKEND}/api/instrumento/listar`);
                const instrumentosDisponiveis = await res.json();
                setDatabases(instrumentosDisponiveis)

            }catch(error) { 
                console.error('Erro ao tentar fazer requisição', error)
            }
        };
        
        fetchDatabase();
    }, []);


    return(
        <div className={styles.containerGerarRelatorio}>
            {/* Container contendo infos inicias da página */}
            <div className={styles.containerIntro}>
                <p className={styles.containerIntro_tituloPagina}>Gerar relatório</p>
                <p className={styles.containerIntro_infos}>
                    Para gerar os relatórios sem alterar a introdução e a conclusão do instrumento, apenas preencha os campos e clique para gerar. Os relatórios gerados ficarão temporariamente armazenados em nosso site, podendo baixar a hora que precisar. Delete os arquivos ZIPs antigos para não ocupar tanto o armazenamento do servidor, quando precisar, somente gere os relatórios novamente. Caso queira alterar a introdução ou a conclusão, faça download dos mesmos e altere o que for necessário, apenas os inserindo e substituindo no servidor novamente.
                </p>
            </div>

            {/* Área para escolher o instrumento que será gerado os relatórios */}
            <div className={styles.containerInstrumento}>
                {/* <p style={{fontSize: '1.3rem', fontFamily: 'Inter', fontWeight: '600', marginTop:'40px', backgroundColor: '#80dfff', padding: '15px', borderRadius: '5px', border: '2px solid #000'}}>Instrumento</p> */}

            </div>

            {/* Container para escolher o instrumento e input para inserir ano do instrumento */}
            <div className={styles.containerRelatorioEsp}>
                <div className={styles.containerRelatorioEsp_escolhaComponentesRelatorio_instrumento}>
                    <p style={{fontSize: '1.3rem', fontFamily: 'Inter', fontWeight: '400', marginTop:'0'}}>Selecione o instrumento</p>
                    <SelectAutoWidth
                        onSelectChange={handleSelectDatabaseChange}
                        label='Instrumento'
                        options={listDatabases}
                        >
                    </SelectAutoWidth>
                </div>
                <div className={styles.containerRelatorioEsp_escolhaComponentesRelatorio_Ano}>
                    <p style={{fontSize: '1.3rem', fontFamily: 'Inter', fontWeight: '400', marginTop:'0'}}>Insira o ano do instrumento</p>
                    <StyledInput type='number' value={ano} onChange={handleAnoChange}></StyledInput>
                </div>
                <div className={styles.containerRelatorioEsp_escolhaComponentesRelatorio_instrumento}>
                    <p style={{fontSize: '1.3rem', fontFamily: 'Inter', fontWeight: '400', marginTop:'0'}}>Modal</p>
                    <SelectAutoWidth 
                        onSelectChange={handleSelectIntroConlcChange} 
                        label='Tipo'
                        options={tipoIntroConlc}  
                    />
                </div>
                
            </div>

            {/* Container para conter aba de visualizacao e mudanca de introducao e conclusao daquele instrumento*/}
            <div className={styles.containerTrocaIntroConcl}>
                <div className={styles.containerTrocaIntroConcl_MaxWidth}>
                <p style={{fontSize: '1.6rem', fontFamily: 'Inter', fontWeight: '500', marginLeft: '5vw', marginTop: '3vh', marginBottom: '0'}}>Templates: </p>
                <div style={{display: 'flex', flexDirection: 'column',height: '100%'}}>
                    {/* Container para parte de alterar introducao */}
                    <div className={styles.containerIntroducao}> 
                        <p style={{fontSize: '1.3em', fontFamily: 'Inter', fontWeight: '500', marginTop: '1vh'}}>Introdução do relatório</p>
                        <div className={styles.containerOpcoesIntroEConcl}>
                            <button
                                onClick={handleDownloadIntroducao}
                                className={styles.button_download_introConcl}
                            >
                                Baixar introdução
                            </button>
                            <div className={styles.containerSubstituirIntroducao}>
                                <p>Deseja substituir introdução?</p>
                                <div className={styles.containerImportNewIntroducao}>
                                    <input
                                        type='file'
                                        ref={introducaoInputRef}
                                        onChange={handleIntroducaoChange}
                                        accept='.md'
                                        style={{display: 'none'}}
                                    />
                                    <button 
                                        className={styles.buttonImportArquivoMD}
                                        onClick={triggerIntroducaoInput}
                                        type='button'
                                    >
                                    <CiImport style={{fontSize: '3em'}}/>
                                    </button>
                                    {renderFileList(introducaoFile)}
                                    <button 
                                        className={styles.buttonSubstituir}
                                        onClick={() => handleConfirmationReplaceArchive('introducao')}
                                        type="button"
                                    >
                                        Substituir
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Container para alterar conclusao */}
                    <div className={styles.containerIntroducao}> 
                        <p style={{fontSize: '1.3em', fontFamily: 'Inter', fontWeight: '500', marginTop: '1vh'}}>Conclusão do relatório</p>
                        <div className={styles.containerOpcoesIntroEConcl}>
                            <button
                                onClick={handleDownloadConclusao}
                                className={styles.button_download_introConcl}
                            >
                                Baixar conclusão
                            </button>
                            <div className={styles.containerSubstituirIntroducao}>
                                <p>Deseja substituir conclusão?</p>
                                <div className={styles.containerImportNewIntroducao}>
                                    <input
                                        type='file'
                                        ref={conclusaoInputRef}
                                        onChange={handleConclusaoChange}
                                        accept='.md'
                                        style={{display: 'none'}}
                                    />
                                    <button 
                                        className={styles.buttonImportArquivoMD}
                                        onClick={triggerConclusaoInput}
                                        type='button'
                                    >
                                    <CiImport style={{fontSize: '3em'}}/>
                                    </button>
                                    {renderFileList(conclusaoFile)}
                                    <button 
                                        className={styles.buttonSubstituir}
                                        onClick={() => handleConfirmationReplaceArchive('conclusao')}
                                        type="button"
                                    >
                                        Substituir
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                </div>
            </div>

            <div className={styles.containerButton}>
                <button onClick={handleSubmit} className={styles.buttonGerarRelatorio}> Gerar relatórios </button>
                {errorMessage && <p className={styles.errorMessage}>{errorMessage}</p>}
            </div>

            {/* Área para mostrar os zips dos relatórios que estão disponíveis */}
            <div className={styles.containerRelatoriosZip}>
                <div className={styles.downloaded_zip_box}>
                    {/* Infos iniciais e botão para atualizar os relatórios gerados */}
                    <div className={styles.zip_box_header}>
                        <div>             
                            <p className={styles.downloaded_zip_box_title}>Relatórios Gerados</p>
                            <p className={styles.downloaded_zip_box_text}>Arquivos ZIPs dos relatórios disponíveis para download: </p>
                        </div>   
                        <div className={styles.zip_box_refresh}>
                        <p className={styles.downloaded_zip_box_text}>Atualizar lista de ZIPs</p>
                        <button 
                            onClick={fetchZipsDisponiveis}
                            className={styles.button_refresh}
                            title='Atualizar lista de ZIPs'
                        >
                            
                            <svg style={{width:'2vw', color: '#fff'}} xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                            </svg>
                        </button>
                        </div>
                    </div>

                {/* Lista de cards contendo informações gerais dos relatórios e botões para download e exclusão */}
                {isLoadingZips ? (
                    <div className={styles.loading_container}>
                        <p className={styles.loading_text}>Carregando lista de ZIPs...</p>
                    </div>
                    ) : avaliableZips.length === 0 ? (
                    <div className={styles.empty_state}>
                        <p className={styles.empty_state_text}>Nenhum relatório gerado ainda.</p>
                        <p className={styles.empty_state_subtext}>Gere relatórios usando o formulário acima.</p>
                    </div>
                    ) : (
                    <div className={styles.zip_cards_container}>
                        {avaliableZips.map((zip) => (
                            <div key={zip.id} className={styles.zip_card}>
                                <div className={styles.zip_card_info}>
                                    <div className={styles.zip_card_icon}>
                                        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                            <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                                            <path d="M14 2V8H20" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                                        </svg>
                                    </div>
                                    <div className={styles.zip_card_details}>
                                        <p className={styles.zip_card_filename}>{zip.filename}</p>
                                        <p className={styles.zip_card_size}>{formatFileSize(zip.size)}</p>
                                    </div>
                                </div>
                                <div className={styles.zip_card_actions}>
                                    <button
                                        onClick={() => downloadZip(zip.id)}
                                        className={styles.button_download}
                                        title="Baixar arquivo"
                                    >
                                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                            <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                                            <path d="M7 10L12 15L17 10" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                                            <path d="M12 15V3" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                                        </svg>
                                        Baixar
                                    </button>
                                    <button 
                                        className={styles.button_delete}
                                        onClick={() => {
                                            if (window.confirm(`Tem certeza que deseja deletar ${zip.filename}?`)) {
                                                deleteZip(zip.id);
                                            }
                                        }}
                                        title="Deletar arquivo"
                                    >
                                        <img src={delete_icon} alt='delete_icon'/>
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                    )}
                </div>
            </div>

            {/* Popups de logs das responses para o usuário */}
            {popupVisible && <div className={styles.overlay}/>}

            {popupVisible && (
                <div className={styles.popup}>
                    <button className={styles.popup_buttonExit} onClick={() => {
                        setPopupVisible(false)
                        setPopupMessage('')
                        }}>
                        X
                    </button>
                    <p className={styles.popup_message}>{popupMessage}</p>
                </div>
            )}

            {/* Popup de confirmação de substituição de introducao */}
            {popupConfirmReplaceIntroVisible && <div className={styles.overlay}/>}

            {popupConfirmReplaceIntroVisible && (
                <div className={styles.popup}>
                    <button className={styles.popup_buttonExit} onClick={() => {
                        setPopupConfirmReplaceIntroVisible(false)
                        setPopupMessage('')
                    }}>
                    X
                    </button>
                    <p className={styles.popup_message}>{popupMessage}</p>
                    <div style={{display: 'flex', marginTop: '2vh'}}>
                        <button className={styles.popup_cancel_button} onClick={() => {setPopupConfirmReplaceIntroVisible(false); setPopupMessage('')}}>Cancelar</button>
                        <button 
                            className={styles.popup_confirm_button} 
                            onClick={() => {handleConfirmReplaceIntroduction(introducaoFile); setPopupConfirmReplaceIntroVisible(false); setPopupMessage('')}}
                        >
                            Confirmar
                        </button>
                    </div>
                </div>
            )}

            {/* Popup de confirmação de substituição de conclusao */}
            {popupConfirmReplaceConclVisible && <div className={styles.overlay}/>}

            {popupConfirmReplaceConclVisible && (
                <div className={styles.popup}>
                    <button className={styles.popup_buttonExit} onClick={() => {
                        setPopupConfirmReplaceConclVisible(false)
                        setPopupMessage('')
                    }}>
                    X
                    </button>
                    <p className={styles.popup_message}>{popupMessage}</p>
                    <div style={{display: 'flex', marginTop: '2vh'}}>
                        <button className={styles.popup_cancel_button} onClick={() => {setPopupConfirmReplaceConclVisible(false); setPopupMessage('')}}>Cancelar</button>
                        <button 
                            className={styles.popup_confirm_button} 
                            onClick={() => {handleConfirmReplaceConclusion(conclusaoFile); setPopupConfirmReplaceConclVisible(false); setPopupMessage('')}}
                        >
                            Confirmar
                        </button>
                    </div>
                </div>
            )}
        </div>

    );
}

export const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

export default GerarRelatorio
