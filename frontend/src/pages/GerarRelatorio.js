import styles from './GerarRelatorio.module.css';
import StyledInput from '../components/StyledInput';
import { useEffect, useState } from 'react';
import SelectAutoWidth from '../components/selectAutoWidth';

function GerarRelatorio(){
    const [ano, setAno] = useState('');
    const [introConcl, setIntroConcl] = useState('');
    const [databases, setDatabases] = useState([]);
    const [instrumento, setInstrumento] = useState('');
    const [response, setResponse] = useState('')
    const [popupVisible, setPopupVisible] = useState(false)
    const [errorMessage, setErrorMessage] = useState('');

    const handleSelectIntroConlcChange = (value) => { 
        setIntroConcl(value);
    }

    const handleSelectDatabaseChange = (value) => { 
        setInstrumento(value)
    } 

    const handleAnoChange = (e) => { 
        setAno(e.target.value);
    }

    const tipoIntroConlc = [
        {label: 'Nenhum', value: ''},
        {label: 'Discente', value: 'Discente'},
        {label: 'Egresso', value: 'Egresso'},
        {label: 'EAD', value: 'EAD'},
        {label: 'Docente', value: 'Docente'},
        {label: 'Agente', value: 'Agente'},
        {label: 'Pos', value: 'Pos'},
    ];

    const listDatabases = []
    {databases.map((database) => { 
        listDatabases.push({
            label: database, value: database
        })
    }
    )}

    const handleGenerate = async (ano, introConcl, instrumento) => { 
        const formData = new FormData();

        formData.append('ano', ano);
        formData.append('introConcl', introConcl);
        formData.append('instrumento', instrumento);

        try { 
            const res = await fetch(`${process.env.REACT_APP_BACKEND}/api/gerarRelatorios`, {

                method: 'POST',
                body: formData
            })

            if(!res.ok) { 
                throw new Error('Erro na resposta do servidor')
            }

            const data = await res.json()
            setResponse(data.message)
            console.log(response)
            setPopupVisible(true)

        } catch(e) { 
            console.log('Não foi possível realizar a requisição', e)
        }
    }

    const handleSubmit = async () => { 
        if(!ano || !instrumento || !introConcl) { 
            setErrorMessage('Por Favor, preencha todos os campos antes de gerar o relatório!!!!')
            return;
        }

        setErrorMessage('');

        await handleGenerate(ano, introConcl, instrumento);
    }

    useEffect(() => {
        const fetchDatabase = async () => { 
            try { 
                const res = await fetch(`${process.env.REACT_APP_BACKEND}/api/instrumentos`);

                const instrumentosDisponiveis = await res.json();
                setDatabases(instrumentosDisponiveis)

            }catch(error) { 
                console.error('Erro ao tentar fazer requisição', error)
            }
        };
        
        fetchDatabase();
    }, []);


    return(
        <div className={styles.containerGerarRelatorio}>
            <div className={styles.containerIntro}>
                <p className={styles.containerIntro_tituloPagina}>Gerar relatório</p>
                <p className={styles.containerIntro_infos}>
                    Os relatórios gerados do instrumento serão enviados para o email da secretaria da CPA, será uma arquivo ZIP contendo todos os relatórios em PDF, Markdown e as figuras dos relatórios. Para gerar os relatórios, primeiramente o instrumento precisa ter passado pelo processamento de dados. Outro ponto, quando for gerar os relatórios, conferir se nenhum outro instrumento está sendo processado, para que não haja problemas.
                </p>
            </div>
            <div className={styles.containerInstrumento}>
                {/* <p style={{fontSize: '1.3rem', fontFamily: 'Inter', fontWeight: '600', marginTop:'40px', backgroundColor: '#80dfff', padding: '15px', borderRadius: '5px', border: '2px solid #000'}}>Instrumento</p> */}
                <SelectAutoWidth
                    onSelectChange={handleSelectDatabaseChange}
                    label='Instrumento'
                    options={listDatabases}
                    >
                </SelectAutoWidth>
            </div>
            <div className={styles.containerRelatorioEsp}>
                <div className={styles.containerRelatorioEsp_escolhaComponentesRelatorio_IntroConcl}>
                    <p style={{fontSize: '1.6rem', fontFamily: 'Inter', fontWeight: '600', marginTop:'0'}}> Escolha a Introdução e Conclusão </p>
                    <p>Escolha a introdução e conclusão para ser inserida no relatório, de acordo com o instrumento</p>
                    <SelectAutoWidth 
                        onSelectChange={handleSelectIntroConlcChange} 
                        label='Tipo'
                        options={tipoIntroConlc}  
                    />
                </div>
                <div className={styles.containerRelatorioEsp_escolhaComponentesRelatorio_Ano}>
                    <p style={{fontSize: '1.6rem', fontFamily: 'Inter', fontWeight: '600', marginTop:'0', marginBottom: '50px'}}>Escolha o Ano para ser inserido no relatório</p>
                    <StyledInput type='number' value={ano} onChange={handleAnoChange}></StyledInput>
                </div>
            </div>
            <div className={styles.containerButton}>
                <button onClick={handleSubmit} className={styles.buttonGerarRelatorio}> Gerar relatórios </button>
                {errorMessage && <p className={styles.errorMessage}>{errorMessage}</p>}
            </div>

            {popupVisible && <div className={styles.overlay}/>}

            {popupVisible && (
                <div className={styles.popup}>
                    <button className={styles.popup_buttonExit} onClick={() => setPopupVisible(false)}>X</button>
                    <p className={styles.popup_message}>{response}</p>
                </div>
            )}
        </div>


    );
}

export default GerarRelatorio
