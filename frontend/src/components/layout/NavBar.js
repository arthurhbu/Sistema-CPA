import {Link} from 'react-router-dom';
import styles from './NavBar.module.css';

import CPA_logo_full from '../../img/CPA_logo_full.png';
import UEM_logo from '../../img/uem_logo.png';
import GRE_logo from '../../img/gre_logo.png';

function NavBar() {
    return(
        <div>
            <nav className={styles.navbar}>
                
                    {/* <img src={logo} alt='cpa'/> */}
                    <p className={styles.p}>Comissão Própria de Avaliação - UEM</p>
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
                    </ul>
            </nav>
            <div className={styles.header}>
                <img src={GRE_logo} alt='header' className={styles.responsive}></img> 
                <img src={CPA_logo_full} alt='header' className={styles.responsiveCpaLogo}></img>
                <img src={UEM_logo} alt='header' className={styles.responsive}></img>
            </div>
        </div>
    );
}

export default NavBar