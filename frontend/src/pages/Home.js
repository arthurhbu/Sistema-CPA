import styles from './Home.module.css'; 
import {Link} from 'react-router-dom';

function Home(){
    return(
        <div className={styles.home}>
            <div style={{display:'flex', justifyContent:'center', backgroundColor:'#000b1f', width:'100%', paddingBottom:'150px', borderTop:'1px solid #292828'}}>
                <div className={styles.inicio}>
                    {/* <p className={styles.tituloInicio}>Comissão Própria de Avaliação  CPA</p> */}
                    <p>Bem vindo ao nosso sistema Letícia!</p>
                    <p>Relatorios: </p>
                    <p className={styles.intro}>Bem-vindo ao Sistema de Geração de Relatórios da CPA-UEM. Este site foi desenvolvido pela Comissão Própria de Avaliação (CPA) da Universidade Estadual de Maringá (UEM) com o objetivo de facilitar a geração e o acesso a relatórios detalhados e precisos. Nossa plataforma permite a coleta, armazenamento e análise de dados de forma eficiente, oferecendo ferramentas intuitivas e robustas para apoiar decisões estratégicas e melhorar continuamente a qualidade acadêmica e administrativa da UEM.</p>
                </div>
            </div>
            <div className={styles.sessions}>
                <div className={styles.sessionBox}>
                    <p className={styles.tag}>Progresso</p>
                    <p className={styles.resume}>Veja como vai o progresso da inserção dos dados e a geração dos dados necessários.</p>
                    <Link to='/progresso'>
                        <button type='button' className={styles.homeButton}>Ver progresso do csv</button>
                    </Link>
                </div>
                <div className={styles.sessionBox}>
                    <p className={styles.tag}>Inserir Arquivo</p>
                    <p className={styles.resume}>Inserir arquivo CSV para leitura e geração de dados.</p>
                    <Link to='/importar'>
                        <button type='button' className={styles.homeButton}>Inserir Csv</button>
                    </Link>
                </div>
                <div className={styles.sessionBox}>
                    <p className={styles.tag}>Gerar relatório</p>
                    <p className={styles.resume}>Gerar os relatórios após leitura do CSV e ter gerados os dados</p>
                    <Link to='/gerar_relatorio'>
                        <button type='button' className={styles.homeButton}>Gerar Relatório</button>
                    </Link>
                </div>
            </div>
        </div>
    );
}

export default Home
