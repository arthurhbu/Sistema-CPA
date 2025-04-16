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
        {label: 'Discente', value: 'Discente'},
        {label: 'Egresso', value: 'Egresso'},
        {label: 'EAD', value: 'EAD'},
        {label: 'Docente', value: 'Docente'},
        {label: 'Agente', value: 'Agente'},
        {label: 'Pos', value: 'Pos'},
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
                // throw new Error(resData.error)
                console.log(resData.error)
            }
            
            setAvaliableZips(resData.zips || []);
        } catch(e){
            throw new Error('Erro ao tentar fazer requisição', e)
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
        } catch (e) {
            console.error('Erro ao tentar deletar o ZIP', e);
        }

    }

    const handleSubmit = async () => { 
        if(!ano || !instrumento || !introConcl) { 
            setErrorMessage('Por Favor, preencha todos os campos antes de gerar o relatório!!!!')
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
                                <p style={{width:'15%'}}>Deseja substituir introdução?</p>
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
                                <p style={{width:'15%'}}>Deseja substituir conclusão?</p>
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
                    <div style={{display: 'flex', justifyContent: 'space-between'}}>    
                        <div style={{marginBottom: '20px'}}>             
                            <p className={styles.downloaded_zip_box_title}>Relatórios Gerados</p>
                            <p className={styles.downloaded_zip_box_text}>Arquivos ZIPs dos relatórios disponíveis para download: </p>
                        </div>   
                        <div style={{marginLeft: '20px', display: 'flex', alignItems: 'center'}}>
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

                {/* Tabela contendo informações gerais dos relatórios e botões para download e exclusão */}
                {isLoadingZips ? (
                    <p className="text-gray-500">Carregando lista de ZIPs...</p>
                    ) : (
                    <div>
                        <table className={styles.downloaded_zip_table}>
                        <thead>
                            <tr style={{width: '100%', display: 'flex', justifyContent: 'space-between'}}>
                            <th className={styles.header_table}>Nome</th>
                            <th className={styles.header_table}>Tamanho</th>
                            <th className={styles.header_table}>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {avaliableZips.map((zip) => (
                            <tr key={zip.id} className={styles.table_body}>
                                <td className={styles.tuple_table}>{zip.filename}</td>
                                <td className={styles.tuple_table}>{formatFileSize(zip.size)}</td>
                                <td className={styles.tuple_table}>
                                    <div style={{display: 'flex'}}>
                                        <button
                                            onClick={() => downloadZip(zip.id)}
                                            className={styles.button_download}
                                        >
                                            Baixar
                                        </button>
                                        <button 
                                            className={styles.button_delete}
                                            onClick={() => {deleteZip(zip.id)}}
                                        >
                                            <img style={{width: '1.5rem'}} src={delete_icon} alt='delete_icon'></img>
                                        </button>
                                    </div>
                                </td>
                            </tr>
                            ))}
                        </tbody>
                        </table>
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
