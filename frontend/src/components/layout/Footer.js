import styles from './Footer.module.css';
import cpa_symbol from '../../img/cpa_symbol_white.png'


function Footer() { 
    return(
        <footer className={styles.footer}>
            <div className={styles.copy_right}>
                <img alt='cpa_symbol' style={{width:'10%'}} src={cpa_symbol}></img>
                <span>Sistema CPA</span>&copy; 2024 
            </div>
        </footer>
    );
}

export default Footer