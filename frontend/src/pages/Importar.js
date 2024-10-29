import styles from './Importar.module.css';
import upload_logo from '../img/upload_logo.png';
import { useDropzone } from 'react-dropzone';
import {useMemo} from 'react';
import { useState } from 'react';
import { FaFileCsv } from "react-icons/fa6";
import StyledInput from '../components/StyledInput';
import UploadButton from '../components/uploadButton';

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
    // minHeight: '30em',
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
    const [response, setResponse] = useState('');
    const [popupHeaderVisible, setPopupHeaderVisible] = useState(false);
    const [popupImportVisible, setPopupImportVisible] = useState(false);
    const [popupImportMessage, setPopupImportMessage] = useState('');
    const [popupErrorVisible, setPopupErrorVisible] = useState(false);
    const [popupErrorMessage, setPopupErrorMessage] = useState('');
    const [header, setHeader] = useState([]);
    const [errorMessage, setErrorMessage] = useState('');
    const correctHeader = ['Nome Instrumento', 'Ano Instrumento', 'Data Inicio', 'Data Fim', 'Codigo Curso', 'Nome Curso', 'Codigo Grupo', 'Nome Grupo', 'Codigo Subgrupo', 'Nome Subgrupo', 'Codigo Disciplina', 'Disciplina', 'Turma', 'Serie', 'Ordem Pergunta', 'Codigo Pergunta', 'Pergunta', 'Ordem Opcoes', 'Opcao', 'Porcentagem', 'Respostas', 'Total do Curso']

    const {
        getRootProps, 
        acceptedFiles,
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
    
    const style = useMemo(() => ({
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
            const res = await fetch('http://localhost:5000/api/importar', {
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
        console.log("Arquivo sendo enviado:] ", files[0])


        await getHeaderCSV(files[0], ano)
    };

    const confirmImportCSV = async () => { 
        try { 
            const res = await fetch('http://localhost:5000/api/confirmarImportacao', { 
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ano})
            });
            
            const data = await res.json();
            setPopupHeaderVisible(false);
            setPopupImportMessage(data.response);
            console.log(data.response)
            setPopupImportVisible(true);
        } catch (error) { 
            console.error(error);
        }
    }

    const handleImportSubmit = async (e) => { 
        e.preventDefault();
        if (!ano) { 
            console.error('Está faltando o campo ano');
            return;
        }

        await confirmImportCSV();
    }

    return(
        <div className={styles.importar}>
            <div className={styles.intro}>
                <p className={styles.titulo}>Inserir Arquivo</p>
                <p className={styles.infos}>
                    Inserir arquivo CSV para coletar e gerar novas informações importantes. O arquivo após ser inserido no banco será gerado novas informações utilizando um IA, talvez demore um pouco. A barra de processo será mostrado aqui. Importe um arquivo por vez para não gerar problemas.
                </p>
            </div>
            <div className={styles.sessionProcArq}>
                <div className={styles.session_grid__arqInputBox}>
                    <div className={styles.session_flex_arqInputBox}>
                        <div {...getRootProps({style})}>
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
                            <p style={{fontFamily:'Inter', fontSize:'1.5vw', fontWeight:'500'}}>Insira o ano do relatório que será gerado: </p>
                            <StyledInput type='number' value={ano} onChange={handleAnoChange}></StyledInput>  
                        </div>
                    </div>
                    <button onClick={handleSubmit} className={styles.importarButton}>Importar</button>
                    {errorMessage && <p className={styles.errorMessage}>{errorMessage}</p>}
                </div>
            </div>
            {popupHeaderVisible && <div className={styles.overlay}/>}

            {popupHeaderVisible && (
                <div className={styles.popup_header}>
                    {/* <button className={styles.popup_buttonExit} onClick={() => setPopupVisible(false)}>X</button> */}
                    <p className={styles.popup_message_header}>Confira o cabeçalho do CSV para ver se está dentro dos padrões: </p>
                    <div className={styles.popup_headerComparison}>
                        <div className={styles.popup_headerColumn}>
                            <p style={{fontSize:'2.4vh', marginTop:'1vh', marginBottom:'1vh', textAlign: 'start', color:'#00DC1D', fontWeight: '700'}}>Correto</p>
                            {correctHeader.map((value) => (
                                <p className={styles.popup_HeaderValues}>{value}</p>
                            ))}
                        </div>
                        <div className={styles.popup_headerColumn}>
                            <p style={{fontSize:'2.4vh', marginTop:'1vh', marginBottom:'1vh', textAlign: 'start', fontWeight:'700'}}>Do CSV importado</p>
                            {header?.map((col,index) => (
                                <p className={styles.popup_HeaderValues} key={index}>{col}</p>
                            ))}
                        </div>
                    </div>
                    <button className={styles.popup_cancel_button} onClick={() => setPopupHeaderVisible(false)}>Cancelar</button>
                    <button className={styles.popup_confirm_button} onClick={handleImportSubmit}>Confirmar</button>
                </div>
            )}

            {popupErrorVisible && <div className={styles.overlay}/>}

            {popupErrorVisible && (
                <div className={styles.popup}>
                    <p>{errorMessage}</p>
                </div>

            )}

            {popupImportVisible && <div className={styles.overlay}/>}

            {popupImportVisible && (
                <div className={styles.popup}>
                    <p className={styles.popup_message}>{popupImportMessage}</p>
                    <button className={styles.popup_buttonExit} onClick={() => setPopupImportVisible(false)}>X</button>
                </div>
            )}
        </div>
    );
}

export default Importar
