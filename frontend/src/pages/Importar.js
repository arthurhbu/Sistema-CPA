import styles from './Importar.module.css';
import upload_logo from '../img/upload_logo.png';
import { useDropzone } from 'react-dropzone';
import {useEffect, useMemo} from 'react';
import { useState } from 'react';
import { FaFileCsv } from "react-icons/fa6";
import StyledInput from '../components/StyledInput';
import UploadButton from '../components/uploadButton';
import { Link } from 'react-router-dom';
import { io } from 'socket.io-client'
import SelectAutoWidth from '../components/selectAutoWidth';
import HeaderPopup from '../components/PopupHeader';


console.log(process.env);

console.log("API URL:", process.env.REACT_APP_BACKEND); // Debugging line to check the BACKEND variable

// const socket = io(process.env.REACT_APP_BACKEND, {
//     transports: [ 'websocket', 'polling'],
//     withCredentials: true,
// })

const iconStyle = { 
    color: '#2ef092',
    marginTop: '1.5vh',
    fontSize: '3.5em'
}

const listElementStyle = { 
    display: 'flex',
    justifyContent:'center'
}

const filenameStyle = {
    paddingLeft:'1em',
    fontSize:'1.5rem',
    fontWeight:'600',
    fontFamily:'Inter'
}

const baseStyle = {
    display:'flex',
    flexDirection:'column',
    flexWrap: 'nowrap',
    backgroundColor: 'white',
    alignItems: 'center',
    textAlign: 'center',
    maxWidth: '50%',
    padding: '5em',
    borderWidth: '2px',
    borderRadius: '10px',
    borderColor: '#c5c4c4',
    borderStyle: 'dashed',
    transition: 'border .24s ease-in-out'
  };
  
const focusedStyle = {
    borderColor: '#2196f3'  
};

const acceptStyle = {
    borderColor: '#00e676'
};

const rejectStyle = {
    borderColor: '#ff1744'
};


function Importar(){
    const [files, setFiles] = useState([]);
    const [ano, setAno] = useState('');
    const [popupHeaderVisible, setPopupHeaderVisible] = useState(false);
    const [popupImportVisible, setPopupImportVisible] = useState(false);
    const [popupImportMessage, setPopupImportMessage] = useState('');
    const [importStatus, setImportStatus] = useState(null);
    const [popupErrorVisible, setPopupErrorVisible] = useState(false);
    const [header, setHeader] = useState([]);
    const [errorMessage, setErrorMessage] = useState('');
    const [isProcessing, setIsProcessing] = useState(false);
    const [selectedCsvType, setSelectedCsvType] = useState('');

    const correctHeaderDiscenteAndEad = ['Nome Instrumento', 'Ano Instrumento', 'Data Inicio', 'Data Fim', 'Codigo Curso', 'Nome Curso', 'Codigo Grupo', 'Nome Grupo', 'Codigo Subgrupo', 'Nome Subgrupo', 'Codigo Disciplina', 'Disciplina', 'Turma', 'Serie', 'Ordem Pergunta', 'Codigo Pergunta', 'Pergunta', 'Ordem Opcoes', 'Opcao', 'Porcentagem', 'Respostas', 'Total do Curso']

    const correctHeaderEgresso = ['Nome Instrumento', 'Ano Instrumento', 'Data Inicio', 'Data Fim', 'Codigo Curso', 'Nome Curso', 'Codigo Grupo', 'Nome Grupo', 'Codigo Subgrupo', 'Nome Subgrupo', 'Ordem Pergunta', 'Codigo Pergunta', 'Pergunta', 'Ordem Opcoes', 'Opcao', 'Porcentagem', 'Respostas', 'Total do Curso']

    const correctHeaderDocenteAndTecnicos = ['Nome Instrumento', 'Ano Instrumento', 'Data Inicio', 'Data Fim', 'Classe', 'Codigo Grupo', 'Nome Grupo', 'Codigo Subgrupo', 'Nome Subgrupo', 'Ordem Pergunta', 'Codigo Pergunta', 'Pergunta', 'Ordem Opcoes', 'Opcao', 'Porcentagem', 'Respostas', 'Total do Curso']

    const headersDisponiveis = {
        "Discente & EAD": ['Nome Instrumento', 'Ano Instrumento', 'Data Inicio', 'Data Fim', 'Codigo Curso', 'Nome Curso', 'Codigo Grupo', 'Nome Grupo', 'Codigo Subgrupo', 'Nome Subgrupo', 'Codigo Disciplina', 'Disciplina', 'Turma', 'Serie', 'Ordem Pergunta', 'Codigo Pergunta', 'Pergunta', 'Ordem Opcoes', 'Opcao', 'Porcentagem', 'Respostas', 'Total do Curso'],
        "Egresso": ['Nome Instrumento', 'Ano Instrumento', 'Data Inicio', 'Data Fim', 'Codigo Curso', 'Nome Curso', 'Codigo Grupo', 'Nome Grupo', 'Codigo Subgrupo', 'Nome Subgrupo', 'Ordem Pergunta', 'Codigo Pergunta', 'Pergunta', 'Ordem Opcoes', 'Opcao', 'Porcentagem', 'Respostas', 'Total do Curso'],
        "Docente & Técnicos": ['Nome Instrumento', 'Ano Instrumento', 'Data Inicio', 'Data Fim', 'Classe', 'Codigo Grupo', 'Nome Grupo', 'Codigo Subgrupo', 'Nome Subgrupo', 'Ordem Pergunta', 'Codigo Pergunta', 'Pergunta', 'Ordem Opcoes', 'Opcao', 'Porcentagem', 'Respostas', 'Total do Curso']
    };

    console.log(process.env);

    console.log("API URL:", process.env.REACT_APP_BACKEND);

    // useEffect(() => {
    //     socket.on("importacao_concluida", (data) => { 
    //         setIsProcessing(false)
    //     }); 

    //     return () => { 
    //         socket.off("importacao_concluida");
    //     };
    // }, []);

    useEffect(() => { 
        const interval = setInterval(() => {
            checkProcessingStatus();
        }, 5000);

        return () => clearInterval(interval);
    }, []);

    const checkProcessingStatus = async () => { 
        try {
            const response = await fetch(`${process.env.REACT_APP_BACKEND}/progresso`);
            const data = await response.json();
            setIsProcessing(data.processing);
        } catch (error) {
            console.error('Erro ao verificar status de processamento', error);
        }
    };

    useEffect(() => {
        checkProcessingStatus();
    }, []);

        const handleSelectCsvTypeChange = (value) => {
            setSelectedCsvType(value);
            console.log(selectedCsvType)
        }

    const {
        getRootProps, 
        getInputProps,
        isFocused, 
        isDragAccept,
        isDragReject,
    } = useDropzone({ 
            maxFiles: 1, 
            accept: {
                'text/csv': ['.csv'],
                // 'application/csv': [],
                // 'text/x-csv': [],
                // 'text/comma-separated-values': [],
                // 'text/x-comma-separated-values': []
            },
            onDrop: acceptedFiles => { 
                console.log(acceptedFiles)

                setFiles(acceptedFiles.map(file => Object.assign(file, {
                    preview: file.name
                })))
            }
        })

    const thumbs = files.map(file => ( 
        <div key={file.name} style={listElementStyle}>
            <FaFileCsv style={iconStyle}/>
            <p style={filenameStyle}>{file.name}</p>
        </div>
    ))
    
    const styleDropzone = useMemo(() => ({
        ...baseStyle,
        ...(isFocused ? focusedStyle : {}),
        ...(isDragAccept ? acceptStyle : {}),
        ...(isDragReject ? rejectStyle : {})
    }), [
        isFocused,
        isDragAccept,
        isDragReject
    ]);

    const handleAnoChange = (e) => {
        setAno(e.target.value);
    };

    const getHeaderCSV = async (file,ano) => { 
        const formData = new FormData();

        formData.append('file', file)
        formData.append('ano', ano)
        try{
            console.log("Fetching from:", `${process.env.REACT_APP_BACKEND}/api/importar`); // Debugging line to check the fetch URL
            const res = await fetch(`${process.env.REACT_APP_BACKEND}/api/importar`, {
                method: 'POST',
                body: formData,
                headers: { 
                },
            });

            const data = await res.json();
            if(data.error === ''){ 
                setHeader(data.header);
                setPopupHeaderVisible(true);    
            }
            else { 
                setPopupErrorVisible(true);
                setErrorMessage(data.error);
            }
            
        } catch(error) {
            console.error('Erro ao tentar fazer requisição', error);
        }
    };

    const handleSubmit = async (e) => { 
        e.preventDefault();
        if(!files.length || !ano) { 
            setErrorMessage('Preencha todos os campos antes de importar!');
            return;
        }
        
        const formData = new FormData();
        formData.append('file', files[0]);
        formData.append('ano', ano);
        
        try {
            const res = await fetch(`${process.env.REACT_APP_BACKEND}/api/importar`, {
                method: 'POST',
                body: formData,
            });
            const data = await res.json();
            if (data.error === '') {
                setHeader(data.header);
                setPopupHeaderVisible(true);
            } else {
                setPopupErrorVisible(true);
                setErrorMessage(data.error);
            }
        } catch (error) {
            console.error('Erro ao tentar fazer requisição', error);
        }
    };


    const importationType = [
        {label: "Nenhum", value: ""},
        {label: "Discente", value: "Discente"},
        {label: "Docente", value: "Docente"},
        {label: "Egresso", value: "Egresso"},
        {label: "EAD", value: "EAD"},
        {label: "Agente", value: "Agente"},
    ]

    const confirmImportCSV = async () => { 
        const data = { 
            ano: ano, 
            modalidade: selectedCsvType,
        };

        setIsProcessing(true);
        try { 
            const res = await fetch(`${process.env.REACT_APP_BACKEND}/api/confirmarImportacao`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data),
            });
            const result = await res.json();
            setPopupHeaderVisible(false);
            setImportStatus(res.status);
            setPopupImportMessage(result.message);
            setPopupImportVisible(true);
        } catch (error) { 
            console.error(error);
        } 
    };


    const handleImportSubmit = async () => {
        // Logic to handle the import submission
        await confirmImportCSV();
    };

return (
        <div className={styles.importar}>
            <div className={styles.intro}>
                <p className={styles.titulo}>Inserir Arquivo</p>
                <p className={styles.infos}>
                    Insira o CSV do instrumento para que comece o processamento dos dados, nessa etapa é feito o uso de Inteligência Artificial por isso pode demorar um certo tempo para finalizar. Enquanto um instrumento está sendo processado não é possível inserir outro, pois o precesso é feito de maneira unitária. Mas é possível visualizar o progresso aqui: Acompanhe o progresso de seu csv.
                </p>
                <div style={{display:'flex', justifyContent:'center'}}>
                    <div style={{backgroundColor:'#E8E8E8', borderRadius:'10px', padding:'3.5vh', marginTop:'5vh', width:'40%',display:'flex', justifyContent:'center', flexDirection: 'column'}} >
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
            <div className={styles.sessionProcArq}>
                {isProcessing && (
                    <div className={styles.overlay_blocked_section}>
                        <div style={{fontSize: '2rem'}}>Outro instrumento já está sendo processado</div>
                        <div className={styles.spinner}>◠</div>
                    </div>
                )}
                <div className={styles.session_grid__arqInputBox}>
                    <div className={styles.session_flex_arqInputBox}>
                        <div {...getRootProps({style: styleDropzone})}>
                            <input {...getInputProps()}/>
                                <img src={upload_logo} alt='upload_logo' className={styles.responsiveLogo} />
                                <p className={styles.procurarArquivos__text}>Arraste e solte o arquivo ou</p>
                                <UploadButton/>
                                <p className={styles.procurarArquivos_arqSuportados}>Arquivos suportados: CSV </p>  
                        </div>
                    </div>
                </div>
                <div className={styles.grid_arqEsc}>
                    <div className={styles.session_arqEscolhido}>
                        <div className={styles.arquivosImportados}>
                            <p className={styles.arquivosImportados_text}> Arquivo Escolhido:</p>
                            <ul>{thumbs}</ul>
                        </div>
                    </div>
                </div>
                <div className={styles.grid_inputInfos}>
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

            {popupHeaderVisible && <div className={styles.overlay}/>}
            {popupHeaderVisible && (
                <HeaderPopup 
                headerOptions={headersDisponiveis} 
                currentHeader="Discente & EAD"
                onClose={() => setPopupHeaderVisible(false)}
                header={header}
                handleImportSubmit={handleImportSubmit}
                setPopupHeaderVisible={setPopupHeaderVisible}
                />
            )}

            {popupErrorVisible && <div className={styles.overlay}/>}

            {popupErrorVisible && (
                <div className={styles.popup}>
                    <p>{errorMessage}</p>
                </div>

            )}

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

        </div>
    );
}

export default Importar;
