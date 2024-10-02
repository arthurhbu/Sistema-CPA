import styles from './Footer.module.css';
import { FaInstagram, FaFacebook, FaLinkedin } from 'react-icons/fa';

function Footer() { 
    return(
        <footer className={styles.footer}>
            <ul className={styles.social_list}>
                <li>
                    <FaInstagram/>
                </li>
                <li>
                    <FaFacebook/>
                </li>
                <li>
                    <FaLinkedin/>
                </li>
            </ul>
            <p className={styles.copy_right}>
                <span>CPA</span> &copy; 2024 
            </p>
        </footer>
    );
}

export default Footer