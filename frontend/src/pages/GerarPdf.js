import styles from './GerarPdf.module.css';
import { useState, useMemo, useEffect} from 'react';
import { useDropzone } from 'react-dropzone';
import zip_upload_logo from '../img/zip_upload_logo.png';
import UploadButtonZip from '../components/uploadButtonZip';
import { RiFileZipFill } from "react-icons/ri";
import { formatFileSize } from './GerarRelatorio';
import delete_icon from '../img/trash.png';
import pdf_icon from '../img/pdf.png';


const iconStyle = { 
    color: '#41ADFF',
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
    maxHeight: '60%',
    padding: '2.5em',
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


export default function GerarPdf(){ 
    const [popupVisible, setPopupVisible] = useState(false);
    const [popupMessage, setPopupMessage] = useState('');
    const [compressArchive, setCompressArchive] = useState([]);
    const [error, setError] = useState('');
    const [idInstrumentoPdf, setIdInstrumentoPdf] = useState('');
    const [avaliablePdfs, setAvaliablePdfs] = useState([]);
    const [isLoadingZips, setIsLoadingZips] = useState(false);

    //Dropzone
    const {
        getRootProps,
        getInputProps,
        isFocused,
        isDragAccept,
        isDragReject,
    } = useDropzone({
        maxFiles: 1,
        accept: {
            'application/zip': ['.zip'],
            'application/x-rar-compressed': ['.rar'],
            'application/x-7z-compressed': ['.7z'],
            'application/gzip': ['.gz'],
            'application/x-tar': ['.tar'],
            'application/x-bzip2': ['.bz2'],
            'application/x-xz': ['.xz'],
        },
        onDrop: acceptedFiles => { 
            console.log(acceptedFiles[0])
            setCompressArchive(acceptedFiles.map(compressArchive => Object.assign(compressArchive, {
                preview: compressArchive.name
            })))
            }
        });

    const thumbs = compressArchive.map(compressArchive => ( 
        <div key={compressArchive.name} style={listElementStyle}>
            <RiFileZipFill style={iconStyle}/>
            <p style={filenameStyle}>{compressArchive.name}</p>
        </div>
    ));

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

    useEffect(() => {
        fetchPdfsAvaliable();
    }, []);


    const deletePdfZip = async (idInstrumento) => { 
        if (!idInstrumento) { 
            throw new Error('Id do instrumento está faltando');
        }

        try { 
            const response = await fetch(`${process.env.REACT_APP_BACKEND}/api/pdf/${idInstrumento}/delete`, { 
                method: 'DELETE'
            });

            if (!response.ok) { 
                throw new Error('Erro ao tentar deletar arquivo zip.');
            }

            const resData = await response.json()

            if(resData.error) { 
                console.log('error: ', resData.error + resData.details)
                setPopupMessage(resData.error)
                setPopupVisible(true);
                return;
            }

            setPopupMessage('Arquivo zip deletado com sucesso.');
            setPopupVisible(true);
            fetchPdfsAvaliable();
        } catch(e) { 
            throw new Error('Erro ao tentar se conectar com o banco.', e)
        }
    }

    const downloadPdfZip = (idInstrumento) => { 

        if(!idInstrumento){
            throw new Error('Id do instrumento está faltando');
        }

        try { 
            const link = document.createElement('a');
            link.href = `${process.env.REACT_APP_BACKEND}/api/pdf/${idInstrumento}/download`;
            link.setAttribute('download', `relatorio_${idInstrumento}.zip`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
        catch(e) { 
            setPopupMessage('Ocorreu um erro ao tentar realizar o download');
            setPopupVisible(true);
        }
    }


    const fetchPdfsAvaliable = async () => {
        setIsLoadingZips(true);
        try {
            const response = await fetch(`${process.env.REACT_APP_BACKEND}/api/pdf/listar`, {
                method: 'GET',
            });

            if (!response.ok) {
                setPopupMessage('Erro ao buscar PDFs: Internal Server Error (Unknown Error)');
                setPopupVisible(true);
                throw new Error('Erro ao buscar PDFs');
            }

            const resData = await response.json();

            if(resData.error) { 
                console.log('error: ', resData.error + resData.details)
                setPopupMessage(resData.error)
                setPopupVisible(true);
            }

            setAvaliablePdfs(resData.pdfs || []);
        } 
        catch(e) { 
            setPopupMessage('Erro ao tentar conectar com o backend');
            setPopupVisible(true);
        } finally { 
            setIsLoadingZips(false);
        }
    }

    const generatePDFRequest = async (compressArchive) => {

        const formData = new FormData();
        formData.append('compressArchive', compressArchive[0]);
        console.log(formData)
        try { 
            const response = await fetch(`${process.env.REACT_APP_BACKEND}/api/pdf/gerar`, {
                method: 'POST',
                body: formData
            });

            
            if (!response.ok) {
                setPopupMessage('Erro ao gerar PDFs: Internal Server Error (Unknown Error)');
                setPopupVisible(true);
                throw new Error('Erro ao gerar PDFs');
            }

            const resData = await response.json()
            
            setCompressArchive([]);
            setPopupMessage(resData.message);
            setPopupVisible(true);

            setIdInstrumentoPdf(resData.id_instrumento_pdf);
            
        } catch (error) {
            setPopupMessage('Ocorreu um erro ao tentar se conectar com o backend');
            setPopupVisible(true);
        }
    } 

    const handleGeneratePDF = async () => {
        if(!compressArchive.length){
            setError('Arquivo Zip não foi selecionado');
            console.error('Arquivo Zip não foi selecionado');
            return
        }

        try {
            setError('')
            await generatePDFRequest(compressArchive);
        } catch (error) {  
            setError('Erro ao gerar PDFs');
            console.error('Erro ao gerar PDFs', error);
        }
    }

    return (
        <div className={styles.containerGerarPdfs}>
            {/* Container contendo introdução da página */}
            <div className={styles.intro}>
                <p className={styles.intro_titulo}>Gerar PDFs dos relatórios</p>
                <p className={styles.intro_infos}>
                    Envie o arquivo zip contendo os relatórios markdowns e as figuras do mesmo para que possa ser gerado os PDFs para serem entregues. Um aviso sobre a finalização da geração dos PDFs será enviada via email. Completada a geração dos PDFs confira na aba de arquivos gerados para baixá-los. Assim que não for mais utilizar o arquivo dos PDFs por favor exclua o mesmo, para poupar armazenamento do nosso servidor.
                </p>
            </div>
            {/* Sessão principal da página */}
            <div className={styles.mainSession}>

                {/* Área do Dropzone para inserir arquivos */}
                <div {...getRootProps({style})}>
                    <input {...getInputProps()}/>
                    <img src={zip_upload_logo} alt='zip_upload_logo' className={styles.responsiveLogo} />
                    <p className={styles.procurarArquivos__text}>Arraste e solte o arquivo ou</p>
                    <UploadButtonZip/>
                    <p className={styles.procurarArquivos_arqSuportados}>Apenas arquivos compactados</p>  
                </div>

                <div className={styles.display_flex_session}>
                    {/* Área onde o arquivo escolhido será mostrado ao usuário */}
                    <div className={styles.session_filebox}>
                        <p className={styles.arquivosImportados_text}> Arquivo Escolhido:</p>
                        <p>{thumbs}</p>
                    </div>
                    {/* Botão para gerar os relatórios PDFs */}
                    <div className={styles.containerButton}>
                        <button onClick={handleGeneratePDF} className={styles.gerarPDFButton}>Gerar PDFs</button>
                        {error && <p className={styles.errorMessage}>{error}</p>}
                    </div>
                </div>
            </div>

            {/* Container onde os arquivos PDFs gerados ficarão */}
            <div className={styles.containerRelatoriosZip}>
                <div className={styles.downloaded_zip_box}>

                    {/* Parte superior desse Container onde tem infos e botão para atualizar os PDFs */}
                    <div className={styles.zip_box_header}>
                        <div>             
                            <p className={styles.downloaded_zip_box_title}>Relatórios Gerados</p>
                            <p className={styles.downloaded_zip_box_text}>Arquivos ZIPs dos relatórios disponíveis para download: </p>
                        </div>   
                        <div className={styles.zip_box_refresh}>
                        <p className={styles.downloaded_zip_box_text}>Atualizar lista de ZIPs</p>
                        <button 
                            onClick={fetchPdfsAvaliable}
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
                    ) : avaliablePdfs.length === 0 ? (
                    <div className={styles.empty_state}>
                        <p className={styles.empty_state_text}>Nenhum PDF gerado ainda.</p>
                        <p className={styles.empty_state_subtext}>Gere PDFs usando o formulário acima.</p>
                    </div>
                    ) : (
                    <div className={styles.zip_cards_container}>
                        {avaliablePdfs.map((zip) => (
                            <div key={zip.id} className={styles.zip_card}>
                                <div className={styles.zip_card_info}>
                                    <div className={styles.zip_card_icon}>
                                        <img src={pdf_icon} alt="PDF icon" style={{width: '40px', height: '40px'}} />
                                    </div>
                                    <div className={styles.zip_card_details}>
                                        <p className={styles.zip_card_filename}>{zip.filename}</p>
                                        <p className={styles.zip_card_size}>{formatFileSize(zip.size)}</p>
                                    </div>
                                </div>
                                <div className={styles.zip_card_actions}>
                                    <button
                                        onClick={() => downloadPdfZip(zip.id)}
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
                                                deletePdfZip(zip.id);
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
            
            {/* Popups para mostrar logs para o usuário */}
            {popupVisible &&  <div className={styles.overlay}/>}

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
        </div>
    );
}
