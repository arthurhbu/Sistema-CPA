import styles from './GerarPdf.module.css';
import { useState, useEffect, useMemo } from 'react';
import { useDropzone } from 'react-dropzone';
import zip_upload_logo from '../img/zip_upload_logo.png';
import UploadButtonZip from '../components/uploadButtonZip';
import { RiFileZipFill } from "react-icons/ri";

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


function GerarPdf(){ 
    const [compressArchive, setCompressArchive] = useState([]);

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

    return (
        <div className={styles.containerGerarPdfs}>
            <div className={styles.intro}>
                <p className={styles.intro_titulo}>Gerar PDFs dos relatórios</p>
                <p className={styles.intro_infos}>
                    Envie o arquivo zip contendo os relatórios markdowns e as figuras do mesmo para que possa ser gerado os PDFs para serem entregues. O arquivo será entregue via email.
                </p>
            </div>
            <div className={styles.mainSession}>
                <div {...getRootProps({style})}>
                    <input {...getInputProps()}/>
                    <img src={zip_upload_logo} alt='zip_upload_logo' className={styles.responsiveLogo} />
                    <p className={styles.procurarArquivos__text}>Arraste e solte o arquivo ou</p>
                    <UploadButtonZip/>
                    <p className={styles.procurarArquivos_arqSuportados}>Apenas arquivos compactados</p>  
                </div>
                <div className={styles.display_flex_session}>
                    <div className={styles.session_filebox}>
                        <p className={styles.arquivosImportados_text}> Arquivo Escolhido:</p>
                        <p>{thumbs}</p>
                    </div>
                    <button className={styles.gerarPDFButton}>Gerar PDFs</button>
                </div>
            </div>
        </div>
    );
}

export default GerarPdf