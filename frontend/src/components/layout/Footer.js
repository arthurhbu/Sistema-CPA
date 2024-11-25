import styles from './Footer.module.css';
import { FaInstagram, FaFacebook, FaLinkedin } from 'react-icons/fa';
import cpa_symbol from '../../img/cpa_symbol_white.png'


function Footer() { 
    return(
        <footer className={styles.footer}>
            {/* <ul className={styles.social_list}>
                <li>
                    <FaInstagram/>
                </li>
                <li>
                    <FaFacebook/>
                </li>
                <li>
                    <FaLinkedin/>
                </li>
            </ul> */}
            <div className={styles.copy_right}>
                <img style={{width:'10%'}} src={cpa_symbol}></img>
                <span>Sistema CPA</span>&copy; 2024 
                {/* <div style={{marginLeft:'45px'}}>
                    <p style={{margin:'0', fontSize:'20px'}}>Envie uma mensagem </p>
                    <p style={{margin: '0'}}>sec-cpa@uem.br</p>
                </div> */}
            </div>
        </footer>
    );
}

export default Footer