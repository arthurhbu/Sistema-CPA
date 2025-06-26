import styles from './Importar.module.css';
import {useEffect, useRef} from 'react';
import { useState } from 'react';
import StyledInput from '../components/StyledInput';
import { CiImport } from "react-icons/ci";
import { Link } from 'react-router-dom';
import SelectAutoWidth from '../components/selectAutoWidth';
import HeaderPopup from '../components/PopupHeader';


/*
TAREFAS:

    FINALIZAR BOTAO PARA BAIXAR TEMPLATES, PARA QUE ELE REALMENTE ENVIE UM TEMPLATE PARA DOWNLOAD.

    FINALIZAR A LOGICA DE IMPORTAR OS ARQUIVOS E LIMPAR CÓDIGO. - Finalizado

    ADICIONAR HEADER DA POS GRADUACAO

*/

function Importar(){

    const csvInputRef = useRef(null);
    const introducaoInputRef = useRef(null);
    const conclusaoInputRef = useRef(null);
    const replaceIntroInputRef = useRef(null);
    const replaceTemplateInputRef = useRef(null);

    const [csvFile, setCsvFile] = useState([]);
    const [introducaoFile, setIntroducaoFile] = useState([]);
    const [conclusaoFile, setConclusaoFile] = useState([]);
    const [replaceIntroFile, setReplaceIntroFile] = useState([]);
    const [replaceTemplateFile, setReplaceTemplateFile] = useState([]);
    const [ano, setAno] = useState('');
    const [popupHeaderVisible, setPopupHeaderVisible] = useState(false);
    const [popupImportVisible, setPopupImportVisible] = useState(false);
    const [popupImportMessage, setPopupImportMessage] = useState('Importacao feita com sucesso');
    const [importStatus, setImportStatus] = useState(null);
    const [popupErrorVisible, setPopupErrorVisible] = useState(false);
    const [header, setHeader] = useState([]);
    const [errorMessage, setErrorMessage] = useState('');
    const [popupErrorMessage, setPopupErrorMessage] = useState('');
    const [isProcessing, setIsProcessing] = useState(false);
    const [selectedCsvType, setSelectedCsvType] = useState('');
    const [popupReplaceTemplatesVisible, setPopupReplaceTemplatesVisible] = useState(false);
    const [replaceTemplatesError, setReplaceTemplatesError] = useState('');
    const [replaceTemplatesSuccess, setReplaceTemplatesSuccess] = useState('');

    const headersDisponiveis = {
        "Discente & EAD": ['Nome Instrumento', 'Ano Instrumento', 'Data Inicio', 'Data Fim', 'Codigo Curso', 'Nome Curso', 'Codigo Grupo', 'Nome Grupo', 'Codigo Subgrupo', 'Nome Subgrupo', 'Codigo Disciplina', 'Disciplina', 'Turma', 'Serie', 'Ordem Pergunta', 'Codigo Pergunta', 'Pergunta', 'Ordem Opcoes', 'Opcao', 'Porcentagem', 'Respostas', 'Total do Curso'],
        "Egresso": ['Nome Instrumento', 'Ano Instrumento', 'Data Inicio', 'Data Fim', 'Codigo Curso', 'Nome Curso', 'Codigo Grupo', 'Nome Grupo', 'Codigo Subgrupo', 'Nome Subgrupo', 'Ordem Pergunta', 'Codigo Pergunta', 'Pergunta', 'Ordem Opcoes', 'Opcao', 'Porcentagem', 'Respostas', 'Total do Curso'],
        "Docente & Técnicos": ['Nome Instrumento', 'Ano Instrumento', 'Data Inicio', 'Data Fim', 'Classe', 'Codigo Grupo', 'Nome Grupo', 'Codigo Subgrupo', 'Nome Subgrupo', 'Ordem Pergunta', 'Codigo Pergunta', 'Pergunta', 'Ordem Opcoes', 'Opcao', 'Porcentagem', 'Respostas', 'Total do Curso']
    };

    const importationType = [
        {label: "Nenhum", value: ""},
        {label: "Discente", value: "Discente"},
        {label: "Docente", value: "Docente"},
        {label: "Egresso", value: "Egresso"},
        {label: "EAD", value: "EAD"},
        {label: "Agente", value: "Agente"},
        {label: "Pós Graduação", value: "Pos"}
    ]

    const triggerCsvInput = () => csvInputRef.current.click();
    const triggerIntroducaoInput = () => introducaoInputRef.current.click();
    const triggerConclusaoInput = () => conclusaoInputRef.current.click();
    const triggerReplaceTemplateInput = () => replaceTemplateInputRef.current.click();

    const renderFileList = (files) => { 
        return files.map((file, index) => (
            <p style={{margin: '0', fontSize: '1.3rem', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', width: '70%', marginLeft: '15px'}}>{file.name}</p>
        ))
    }

    //Fetchs, handles e useEffects
    
    useEffect(() => { 
        const interval = setInterval(() => {
            checkProcessingStatus();
        }, 15000);
        
        return () => clearInterval(interval);
    }, []);
    
    useEffect(() => {
        checkProcessingStatus();
    }, []);

    const checkProcessingStatus = async () => { 
        try {
            const response = await fetch(`${process.env.REACT_APP_BACKEND}/api/csv/importacao/progresso`);
            const data = await response.json();
            setIsProcessing(data.processing);
        } catch (error) {
            console.error('Erro ao verificar status de processamento', error);
        }
    };

    const handleDownloadTemplate = async () => {

        const link = document.createElement('a');
        link.href = `${process.env.REACT_APP_BACKEND}/api/relatorios/templates/download`;
        link.setAttribute('download', `templates_intro_e_concl.md`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    const handleCsvChange = (e) => { 
        if (e.target.files.length > 0) { 
            setCsvFile(Array.from(e.target.files));
        }
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

    const handleReplaceIntroChange = (e) => {
        if (e.target.files.length > 0) {
            setReplaceIntroFile(Array.from(e.target.files));
        }
    };

    const handleReplaceTemplateChange = (e) => {
        if (e.target.files.length > 0) {
            setReplaceTemplateFile(Array.from(e.target.files));
        }
    };

    const handleSelectCsvTypeChange = (value) => {
        setSelectedCsvType(value);
        console.log(selectedCsvType)
    }

    const handleAnoChange = (e) => {
        setAno(e.target.value);
    };

    const handleImportSubmit = async () => {
        await confirmImportCSV();
    };

    const handleSubmit = async (e) => { 
        e.preventDefault();
        if(!csvFile.length || !ano || !introducaoFile.length || !conclusaoFile.length || !selectedCsvType) { 
            setErrorMessage('Preencha todos os campos antes de importar!');
            return;
        }
        setErrorMessage('');

        const formData = new FormData();

        formData.append('file', csvFile[0]);
        formData.append('arquivo_introducao', introducaoFile[0]);
        formData.append('arquivo_conclusao', conclusaoFile[0]);

        
        try {
            const res = await fetch(`${process.env.REACT_APP_BACKEND}/api/csv/importar`, {
                method: 'POST',
                body: formData,
            });
            const data = await res.json();

            if (data.error === 'Database already exists') { 
                setPopupErrorMessage(data.message);
                setPopupErrorVisible(true);
            } else if (data.error === '') {
                setHeader(data.header);
                setPopupHeaderVisible(true);
            } else {
                setPopupErrorVisible(true);
                setPopupErrorMessage(data.error);
            }
        } catch (error) {
            console.error('Erro ao tentar fazer requisição', error);
        }
    };

    const handleCancelAndRemoveArchives = async () => { 
        try { 
            const csvUniqueFile = csvFile[0];

            const fileNameWithoutExtension = csvUniqueFile.name.replace('.csv', '');

            const response = await fetch(`${process.env.REACT_APP_BACKEND}/api/csv/cancel/${fileNameWithoutExtension}`, {
                method: 'DELETE'
            });

            setPopupHeaderVisible(false);

            if(!response) { 
                setPopupErrorMessage('Não foi possível estabelecer conexão com o backend.');
                setPopupErrorVisible(true);
            }
            
            const resData = await response.json()
            
            if(resData.error !== '') { 
                setPopupErrorMessage(resData.error);
                setPopupErrorVisible(true);
                return
            }

            setPopupImportMessage('Importação cancelada com sucesso!');
            setPopupImportVisible(true);

        } catch (error) { 
            setPopupErrorMessage('Ocorreu um erro inesperado: ', error);
            setPopupErrorVisible(true);
        }
    }

    const confirmImportCSV = async () => { 

        const dataToSend = { 
            ano: ano,
            modalidade: selectedCsvType
        }

        setIsProcessing(true);
        try { 
            const res = await fetch(`${process.env.REACT_APP_BACKEND}/api/csv/importar/confirmar`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(dataToSend), 
            });
            const result = await res.json();
            if (result.error) { 
                setPopupImportMessage(result.error);
                setPopupImportVisible(true);
                return;
            }

            setPopupHeaderVisible(false);
            setImportStatus(res.status);
            setPopupImportMessage(result.message);
            setPopupImportVisible(true);
        } catch (error) { 
            console.error(error);
        } 
    };

    const handleReplaceTemplatesSubmit = async () => {
        setReplaceTemplatesError('');
        setReplaceTemplatesSuccess('');
        if (!replaceTemplateFile.length) {
            setReplaceTemplatesError('Selecione o arquivo antes de confirmar.');
            return;
        }
        // Placeholder para upload real
        try {
            const formData = new FormData();
            formData.append('arquivo_template', replaceTemplateFile[0]);
            await fetch(`${process.env.REACT_APP_BACKEND}/api/relatorios/templates/upload`, { method: 'POST', body: formData });
            setReplaceTemplatesSuccess('Template substituído com sucesso!');
            setReplaceTemplateFile([]);
        } catch (error) {
            setReplaceTemplatesError('Erro ao substituir template.');
        }
    };

return (
        <div className={styles.importar}>

            {/* Container contendo infos da página */}
            <div className={styles.intro}>
                <p className={styles.titulo}>Inserir Arquivo</p>
                <p className={styles.infos}>
                    A etapa de inserção é feito com o uso de Inteligência Artificial por isso pode demorar um certo tempo para finalizar. Enquanto um instrumento está sendo processado não é possível inserir outro, pois o precesso é feito de maneira unitária. Mas é possível visualizar o progresso aqui:  <Link to='/progresso'>Progresso de inserção</Link>
                </p>
                <div className={styles.tutorial_container}>
                    <p style={{color: 'black'}} className={styles.infos}>
                        <p style={{fontSize:'1.7rem', fontWeight:'700'}}>Tutorial de importação:</p>
                        Para realizar a importação com êxito, siga esses passos: 
                        <ul className={styles.etapas_ul}>
                            <li style={{marginBottom: '1.9vh'}}>Baixe e personalize a Introdução e Conclusão para o instrumento que será processado.</li>
                            <li style={{marginBottom: '1.9vh'}}>Escolha modalidade/tipo do instrumento que será importado, para que não haja incoerências na rotina de importação.</li>
                            <li style={{marginBottom: '1.9vh'}}>Insira o arquivo CSV e os arquivos de introdução e conclusão.</li>
                            <li style={{marginBottom: '1.9vh'}}>Insira o ano referente à quando foi aplicado o formulário do instrumento.</li>
                            <li style={{marginBottom: '1.9vh'}}>Após clicar no botão de importar, confira as colunas do csv que estará importando para ver se ele bate com o padrão que buscamos.</li>
                        </ul>
                    </p>
                    <div className={styles.containerButton}>
                        <button onClick={handleDownloadTemplate} className={styles.button_templates}> Baixar Templates </button>
                        <button onClick={() => setPopupReplaceTemplatesVisible(true)} className={styles.button_templates_replace} style={{}}>Substituir Templates</button>
                    </div>
                </div>
                <div style={{display:'flex', justifyContent:'center'}}>
                    <div style={{backgroundColor:'#E8E8E8', borderRadius:'10px', padding:'3.5vh', marginTop:'5vh', width:'50%',display:'flex', justifyContent:'center', flexDirection: 'column'}} >
                        <p style={{marginTop: '0', fontFamily:'Inter', fontSize:'1.4rem', fontWeight:'500', alignItems: 'center'}}>Primeiro insira a modalidade do instrumento que será processado: </p>
                        <div style={{width: '100%', display:'flex', alignSelf:'center'}}>
                            <SelectAutoWidth 
                                onSelectChange={handleSelectCsvTypeChange} 
                                label='Modal'
                                options={importationType}  
                                textColor={'#6C6C6C'}
                            />
                        </div>
                    </div>
                </div>
            </div>

            {/* Container para inputs e importação do csv */}
            <div className={styles.sessionProcArq}>
                {isProcessing && (
                    <div className={styles.overlay_blocked_section}>
                        <div style={{fontSize: '2rem'}}>Outro instrumento já está sendo processado</div>
                        <div className={styles.spinner}>◠</div>
                    </div>
                )}

                {/* Container para inserir arquivos */}
                    <div className={styles.inputsArquivosImportacao}>
                        <div className={styles.inputArquivoBox}>
                            <div style={{display: 'flex', justifyContent:'space-between'}}>
                                <p style={{color: '#000'}} className={styles.inputArquivoBox_text}> Csv escolhido: </p>
                                <div>
                                    <input
                                        type='file'
                                        ref={csvInputRef}
                                        onChange={handleCsvChange}
                                        accept='.csv'
                                        style={{display: 'none'}}
                                    />
                                    <button 
                                        className={styles.buttonImportArquivoCsv}
                                        onClick={triggerCsvInput}
                                        type='button'
                                    >
                                        <CiImport style={{fontSize: '3em'}}/>
                                    </button>
                                </div>
                            </div>
                            {renderFileList(csvFile)}
                        </div>

                        <div style={{marginTop:'7vh'}} className={styles.inputArquivoBox}>
                            <div style={{display: 'flex', justifyContent:'space-between'}}>
                                <p style={{color: '#000'}} className={styles.inputArquivoBox_text}> Introdução escolhida: </p>
                                <div>
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
                                </div>
                            </div>
                            {renderFileList(introducaoFile)}
                        </div>
                        
                        <div style={{marginTop:'7vh'}} className={styles.inputArquivoBox}>
                            <div style={{display: 'flex', justifyContent:'space-between'}}>
                                <p style={{color: '#000'}} className={styles.inputArquivoBox_text}> Conclusão escolhida: </p>
                                <div>
                                    <input
                                        type='file'
                                        onChange={handleConclusaoChange}
                                        ref={conclusaoInputRef}
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
                                </div>
                            </div>
                            {renderFileList(conclusaoFile)}
                        </div>
                    </div>

                {/* Input de ano e botão para importar csv */}
                <div style={{display: 'flex'}}>
                    <div className={styles.container_inputAno_button}>
                        <div className={styles.session_inputInfos}>
                            <div style={{width:'100%'}}>
                                <p style={{fontFamily:'Inter', fontSize:'1.5rem', fontWeight:'500'}}>Insira o ano do relatório que será gerado: </p>
                                <StyledInput style={{}} type='number' value={ano} onChange={handleAnoChange}></StyledInput>  
                            </div>
                        </div>
                        <button onClick={handleSubmit} className={styles.importarButton}>Importar</button>
                        {errorMessage && <p className={styles.errorMessage}>{errorMessage}</p>}
                    </div>
                </div>
            </div>
            
            {/* Popup para apresentar e comparar o header do csv escolhido com o header modelo */}
            {popupHeaderVisible && <div className={styles.overlay}/>}
            {popupHeaderVisible && (
                <HeaderPopup 
                headerOptions={headersDisponiveis} 
                currentHeader="Discente & EAD"
                onClose={() => setPopupHeaderVisible(false)}
                header={header}
                handleImportSubmit={handleImportSubmit}
                setPopupHeaderVisible={setPopupHeaderVisible}
                handleCancelAndRemove={handleCancelAndRemoveArchives}
                />
            )}

            {/* Popup de Erro quando o fetch para receber o header falhar */}
            {popupErrorVisible && <div className={styles.overlay}/>}

            {popupErrorVisible && (
                <div className={styles.popup}>
                    <p style={{alignSelf: 'center', fontSize:'1.15rem', paddingLeft: '1vw', paddingRight: '1vw'}}>{popupErrorMessage}</p>
                    <button className={styles.popup_buttonExit} onClick={() => {setPopupErrorVisible(false); setPopupErrorMessage('')}}>X</button>
                </div>
            )}

            {/* Popup para Erro ou Mensagem de sucesso quando importação for confirmada  */}
            {popupImportVisible && <div className={styles.overlay}/>}
            {popupImportVisible && importStatus === 200 ? (
                <div className={styles.popup}>
                    <p className={styles.popup_message}>Acompanhe o progesso da inserção</p>
                    <Link to='/progresso'>
                        <button type='button' className={styles.popup_confirm_button}>Progresso da inserção</button>
                    </Link>
                    <button className={styles.popup_buttonExit} onClick={() => setPopupImportVisible(false)}>X</button>
                </div>
            ) : popupImportVisible && importStatus !== 200 ? (
                <div className={styles.popup}>
                    <p className={styles.popup_message}>{popupImportMessage}</p>
                    <button className={styles.popup_buttonExit} onClick={() => setPopupImportVisible(false)}>X</button>
                </div>
            ) : (
                <div></div>
            )}

            {/* Popup para substituir templates */}
            {popupReplaceTemplatesVisible && <div className={styles.overlay}/>} 
            {popupReplaceTemplatesVisible && (
                <div className={styles.popup} style={{minWidth: '350px', maxWidth: '90vw', height: '40vh', display: 'flex', flexDirection: 'column', justifyContent: 'space-between'}}>
                    <div>
                        <p className={styles.popup_message_header}>Substituir Arquivo dos Templates</p>
                        <p style={{fontSize: '1.3rem', color: '#333'}}>Faça upload do novo arquivo contendo os templates de introdução e conclusão (O arquivo deve possuir o nome "templates_intro_e_concl.md"):</p>
                    </div>
                    <div className={styles.inputArquivoBox} style={{margin: '0 auto', width: '80%', minHeight: 'unset', height: 'unset', background: '#E8E8E8'}}>
                        <div style={{display: 'flex', justifyContent:'space-between', color: ''}}>
                            <p style={{color: '#000'}} className={styles.inputArquivoBox_text}> Template escolhido: </p>
                            <div>
                                <input
                                    type='file'
                                    ref={replaceTemplateInputRef}
                                    onChange={handleReplaceTemplateChange}
                                    accept='.md'
                                    style={{display: 'none'}}
                                />
                                <button 
                                    className={styles.buttonImportArquivoMD}
                                    onClick={triggerReplaceTemplateInput}
                                    type='button'
                                >
                                    <CiImport style={{fontSize: '3em'}}/>
                                </button>
                            </div>
                        </div>
                        {replaceTemplateFile.length > 0 && (
                            <p style={{margin: '0', fontSize: '1.3rem', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', width: '70%', marginLeft: '15px'}}>{replaceTemplateFile[0].name}</p>
                        )}
                    </div>
                    {replaceTemplatesError && <p className={styles.errorMessage}>{replaceTemplatesError}</p>}
                    {replaceTemplatesSuccess && <p style={{color: 'green', fontWeight: 500}}>{replaceTemplatesSuccess}</p>}
                    <div style={{display: 'flex', justifyContent: 'flex-end', marginTop: '2vh'}}>
                        <button className={styles.popup_cancel_button} onClick={() => {setPopupReplaceTemplatesVisible(false); setReplaceTemplateFile([]); setReplaceTemplatesError(''); setReplaceTemplatesSuccess('');}}>Cancelar</button>
                        <button className={styles.popup_confirm_button} onClick={handleReplaceTemplatesSubmit}>Confirmar</button>
                    </div>
                </div>
            )}

        </div>
    );
}

export default Importar;
