import styles from './StyledInput.module.css';

function StyledInput({value, onChange}) { 
    return (
        <div className={styles.form_group}>
            <input type="input" className={styles.form_field} placeholder="" name="ano" id='ano' required value={value} onChange={onChange}/>
            <label htmlFor="ano" className={styles.form_label}>Ano</label>
        </div>
    );
}

export default StyledInput;