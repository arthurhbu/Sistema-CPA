import styles from './uploadButtonZip.module.css';
import { PiFileZipDuotone } from "react-icons/pi";

function UploadButtonZip() { 
    return (
        <button className={styles.container_btn_file}>
            <PiFileZipDuotone style={{fontSize: '1.7em'}} />
            Upload Zip File
        {/* <input class="file" name="text" type="file" /> */}
        </button>
    );
}

export default UploadButtonZip