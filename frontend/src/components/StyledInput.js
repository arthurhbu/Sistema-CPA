import styles from './StyledInput.module.css';

function StyledInput({type, value, onChange}) { 
    return (
        <div className={styles.form_group}>
            <input step='1' min='1900' type={type} className={styles.form_field} placeholder="" name="ano" id='ano' required value={value} onChange={onChange}/>
            <label htmlFor="ano" className={styles.form_label}>Ano</label>
        </div>
    );
}

export default StyledInput;