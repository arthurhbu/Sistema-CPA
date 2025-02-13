import { useState } from "react";
import styles from "./PopupHeader.module.css"; // Você pode criar um CSS específico para estilizar

function HeaderPopup({ headerOptions, currentHeader, onClose, header, handleImportSubmit, setPopupHeaderVisible }) {
    const [selectedHeader, setSelectedHeader] = useState(currentHeader);

    return (
        <div className={styles.popup_header}>
            {/* Comparação no centro */}
            <div className={styles.popup_headerComparison}>
                <div className={styles.popup_headerColumn}>
                    <p style={{ fontSize: '2.4vh', marginBottom: '1vh', color: '#00DC1D', fontWeight: '700' }}>
                        Correto
                    </p>
                    {headerOptions[selectedHeader]?.map((value, index) => (
                        <p key={index} className={styles.popup_HeaderValues}>{value}</p>
                    ))}
                </div>

                <div className={styles.popup_headerColumn}>
                    <p style={{ fontSize: '2.4vh', marginBottom: '1vh', fontWeight: '700' }}>
                        Do CSV importado
                    </p>
                    {header?.map((col, index) => (
                        <p key={index} className={styles.popup_HeaderValues}>{col}</p>
                    ))}
                </div>
            </div>

            {/* Sidebar no canto direito */}
            <div className={styles.sidebar}>
                {Object.keys(headerOptions).map((key) => (
                    <button
                        key={key}
                        className={selectedHeader === key ? styles.selectedButton : styles.optionButton}
                        onClick={() => setSelectedHeader(key)}
                    >
                        {key}
                    </button>
                ))}
            </div>

            {/* Botões fixos no canto inferior direito */}
            <div className={styles.popup_buttons}>
                <button className={styles.popup_cancel_button} onClick={() => setPopupHeaderVisible(false)}>Cancelar</button>
                <button className={styles.popup_confirm_button} onClick={handleImportSubmit}>Confirmar</button>
            </div>
        </div>
    );
}

export default HeaderPopup;
