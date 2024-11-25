import styles from './GerarPdf.module.css';
import backgroundAnimation from '../components/BackgroundAnimation';

function GerarPdf(){ 
    return (
        <div className={styles.containerGerarPdfs}>
            <p> area para Colocar arquivos Markdown</p>
            <p>Escolher o intrumento para poder gerar os PDFS</p>
            <p></p>
        </div>
    );
}

export default GerarPdf