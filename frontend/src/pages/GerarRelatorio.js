import styles from './GerarRelatorio.module.css';
import StyledInput from '../components/StyledInput';
import { useEffect, useState } from 'react';
import SelectAutoWidth from '../components/selectAutoWidth';
import delete_icon from '../img/trash.png'

function GerarRelatorio(){
    const [ano, setAno] = useState('');
    const [introConcl, setIntroConcl] = useState('');
    const [databases, setDatabases] = useState([]);
    const [instrumento, setInstrumento] = useState('');
    const [response, setResponse] = useState('');
    const [popupVisible, setPopupVisible] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');
    const [isProcessing, setIsProcessing] = useState(false);
    const [idInstrumento, setIdInstrumento] = useState('');
    const [isLoadingZips, setIsLoadingZips] = useState(false);
    const [avaliableZips, setAvaliableZips] = useState([]);

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

    const fetchZipsDisponiveis = async () => {
        setIsLoadingZips(true);

        try {

            const response = await fetch(`${process.env.REACT_APP_BACKEND}/api/relatorios/zips`, {
                method: 'GET',
            })

            if(!response.ok) {
                throw new Error('Erro na resposta do servidor')
            }

            const resData = await response.json();

            if(resData.error) {
                throw new Error(resData.error)
            }
            
            setAvaliableZips(resData.zips || []);
        } catch(e){
            throw new Error('Erro ao tentar fazer requisição', e)
        } finally { 
            setIsLoadingZips(false);
        }
    }

    useEffect(() => {
        fetchZipsDisponiveis();
    }, [isProcessing]);

    const handleGenerate = async (ano, introConcl, instrumento) => { 
        const formData = new FormData();

        formData.append('ano', ano);
        formData.append('introConcl', introConcl);
        formData.append('instrumento', instrumento);

        try { 
            setIsProcessing(true);
            const response = await fetch(`${process.env.REACT_APP_BACKEND}/api/gerarRelatorios`, {
                method: 'POST',
                body: formData
            })

            const resData = await response.json();

            if(!response.ok) { 
                throw new Error('Erro na resposta do servidor')
            }

            if(resData.error) {
                setResponse(resData.error);
                setPopupVisible(true);
                throw new Error(resData.error);
            }
            
            setPopupVisible(true);
            setIdInstrumento(resData.id_instrumento);
            setResponse('Relatórios gerados com sucesso!');

        } catch(e) { 
            console.log('Não foi possível realizar a requisição', e)
        } finally { 
            setIsProcessing(false);
        }
    }

    const downloadZip = (idInstrumento) => { 
        if (!idInstrumento) { 
            return;
        }

        const link = document.createElement('a');
        link.href = `${process.env.REACT_APP_BACKEND}/api/relatorios/${idInstrumento}/download`;
        link.setAttribute('download', `relatorio_${idInstrumento}.zip`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    const deleteZip = async (idInstrumento) => {

        if (!idInstrumento) {
            console.error('ID do instrumento não foi passado');
            return;
        }
        try {
            const response = await fetch(`${process.env.REACT_APP_BACKEND}/api/relatorios/delete/${idInstrumento}`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                console.error('Erro ao tentar deletar o ZIP');
                return;
            }

            const resData = await response.json();

            if (resData.error) {
                setPopupVisible(true);
                setResponse(resData.error);
                return;
            }

            setPopupVisible(true);
            setResponse('ZIP deletado com sucesso!');
        } catch (e) {
            console.error('Erro ao tentar deletar o ZIP', e);
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
            <div className={styles.containerRelatoriosZip}>
                <div className={styles.downloaded_zip_box}>
                    <div style={{display: 'flex', justifyContent: 'space-between'}}>    
                        <div style={{marginBottom: '20px'}}>             
                            <p className={styles.downloaded_zip_box_title}>Relatórios Gerados</p>
                            <p className={styles.downloaded_zip_box_text}>Arquivos ZIPs dos relatórios disponíveis para download: </p>
                        </div>   
                        <div style={{marginLeft: '20px', display: 'flex', alignItems: 'center'}}>
                        <p className={styles.downloaded_zip_box_text}>Atualizar lista de ZIPs</p>
                        <button 
                            onClick={fetchZipsDisponiveis}
                            className={styles.button_refresh}
                            title='Atualizar lista de ZIPs'
                        >
                            
                            <svg style={{width:'2vw', color: '#fff'}} xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                            </svg>
                        </button>
                        </div>
                    </div>


                {isLoadingZips ? (
                    <p className="text-gray-500">Carregando lista de ZIPs...</p>
                    ) : (
                    <div>
                        <table className={styles.downloaded_zip_table}>
                        <thead>
                            <tr style={{width: '100%', display: 'flex', justifyContent: 'space-between'}}>
                            <th className={styles.header_table}>Nome</th>
                            <th className={styles.header_table}>Tamanho</th>
                            <th className={styles.header_table}>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {avaliableZips.map((zip) => (
                            <tr key={zip.id} className={styles.table_body}>
                                <td className={styles.tuple_table}>{zip.filename}</td>
                                <td className={styles.tuple_table}>{formatFileSize(zip.size)}</td>
                                <td className={styles.tuple_table}>
                                    <div style={{display: 'flex'}}>
                                        <button
                                            onClick={() => downloadZip(zip.id)}
                                            className={styles.button_download}
                                        >
                                            Baixar
                                        </button>
                                        <button 
                                            className={styles.button_delete}
                                            onClick={() => {deleteZip(zip.id)}}
                                        >
                                            <img style={{width: '1.5rem'}} src={delete_icon} alt='delete_icon'></img>
                                        </button>
                                    </div>
                                </td>
                            </tr>
                            ))}
                        </tbody>
                        </table>
                    </div>
                    )}
                </div>
            </div>

            {popupVisible && <div className={styles.overlay}/>}

            {popupVisible && (
                <div className={styles.popup}>
                    <button className={styles.popup_buttonExit} onClick={() => {
                        setPopupVisible(false)
                        setResponse('')
                        }}>
                        <p style={{color: 'currentColor', fontSize: '1.6rem', padding: '0', margin:'0'}}>X</p>
                    </button>
                    <p className={styles.popup_message}>{response}</p>
                </div>
            )}
        </div>

    );
}

const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

export default GerarRelatorio
