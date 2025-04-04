import styles from './GerarPdf.module.css';
import { useState, useMemo, useEffect} from 'react';
import { useDropzone } from 'react-dropzone';
import zip_upload_logo from '../img/zip_upload_logo.png';
import UploadButtonZip from '../components/uploadButtonZip';
import { RiFileZipFill } from "react-icons/ri";
import { formatFileSize } from './GerarRelatorio';
import delete_icon from '../img/trash.png';


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

            const resData = response.json()

            if(resData.error) { 
                console.log('error: ', resData.error + resData.details)
                setPopupMessage(resData.error)
                setPopupVisible(true);
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
            const response = await fetch(`${process.env.REACT_APP_BACKEND}/api/pdfs`, {
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
                    Envie o arquivo zip contendo os relatórios markdowns e as figuras do mesmo para que possa ser gerado os PDFs para serem entregues. O arquivo será entregue via email.
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
                    <div style={{display: 'flex', justifyContent: 'space-between'}}>    
                        <div style={{marginBottom: '20px'}}>             
                            <p className={styles.downloaded_zip_box_title}>Relatórios Gerados</p>
                            <p className={styles.downloaded_zip_box_text}>Arquivos ZIPs dos relatórios disponíveis para download: </p>
                        </div>   
                        <div style={{marginLeft: '20px', display: 'flex', alignItems: 'center'}}>
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

                {/* Área de tabela dos arquivos gerados */}
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
                            {avaliablePdfs.map((zip) => (
                            <tr key={zip.id} className={styles.table_body}>
                                <td className={styles.tuple_table}>{zip.filename}</td>
                                <td className={styles.tuple_table}>{formatFileSize(zip.size)}</td>
                                <td className={styles.tuple_table}>
                                    <div style={{display: 'flex'}}>
                                        <button
                                            onClick={() => downloadPdfZip(zip.id)}
                                            className={styles.button_download}
                                        >
                                            Baixar
                                        </button>
                                        <button 
                                            className={styles.button_delete}
                                            onClick={() => {deletePdfZip(zip.id)}}
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
            
            {/* Popups para mostrar logs para o usuário */}
            {popupVisible &&  <div className={styles.overlay}/>}

            {popupVisible && (
                <div className={styles.popup}>
                    <button className={styles.popup_buttonExit} onClick={() => {
                        setPopupVisible(false)
                        setPopupMessage('')
                        }}>
                        <p style={{color: 'currentColor', fontSize: '1.6rem', padding: '0', margin:'0'}}>X</p>
                    </button>
                    <p className={styles.popup_message}>{popupMessage}</p>
                </div>
            )}
        </div>
    );
}
