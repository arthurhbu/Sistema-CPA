import {Link} from 'react-router-dom';
import styles from './NavBar.module.css';

import CPA_logo from '../../img/cpa_logo_white.png';
import UEM_logo from '../../img/uem_logo_white.png';

function NavBar() {
    return(
        <div>
            <nav className={styles.navbar}>
                

                    <img alt='cpa_logo' src={CPA_logo} style={{maxWidth:'10vw'}}></img>
                    <ul className={styles.list}>
                        <li className={styles.item}>
                            <Link to="/">Home</Link>
                        </li>
                        <li className={styles.item}>
                            <Link to="/importar">Importar</Link>
                        </li>
                        <li className={styles.item}>
                            <Link to="/progresso">Progresso</Link>
                        </li>
                        <li className={styles.item}>
                            <Link to="/gerar_relatorio">Gerar Relatório</Link>
                        </li>
                        <li className={styles.item}>
                            <Link to='/gerar_pdfs'>Gerar PDFs</Link>
                        </li>
                    </ul>
                    <img alt='uem_logo' src={UEM_logo} style={{maxWidth:'10vw'}}></img>
            </nav>
        </div>
    );
}

export default NavBar