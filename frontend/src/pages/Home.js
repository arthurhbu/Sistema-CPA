import styles from './Home.module.css'; 
import {Link} from 'react-router-dom';
import cpa_banner from '../img/cpa_banner.png';
import SelectAutoWidth from '../components/selectAutoWidth';
import { useState, useEffect } from 'react';
import Checkbox from '@mui/material/Checkbox';

function Home(){
    const [instrumento, setInstrumento] = useState('');
    const [databases, setDatabases] = useState([]);
    const [etapas, setEtapas] = useState({});

    const ordemEtapas = ['Inserção/Análise do instrumento', 'Geração de Relatórios', 'Revisão de Relatórios', 'Correção de possíveis erros', 'Geração de PDFs', 'Entrega dos Relatórios', 'Finalizado']

    const ordenarEtapas = ordemEtapas
        .filter((key) => etapas.hasOwnProperty(key))
        .map((key) => ({key, value: etapas[key] }));

    const handleCheckboxChange = async (etapa) => { 
        setEtapas((prevEtapas) => ({
            ...prevEtapas,
            [etapa]: !prevEtapas[etapa]
        }));

        try { 
            const res = await fetch(`${process.env.REACT_APP_BACKEND}/api/instrumento/etapa/atualizar`, { 
                method: 'PUT',
                headers: { 'Content-Type': 'application/json'},
                body: JSON.stringify({ instrumento, etapa, novoValor: !etapas[etapa] })
            });
            
            if(!res.ok) { 
                throw new Error('Erro ao tentar atualizar o valor da etapa no banco');
            }
        } catch (error) { 
            console.error(error);

            setEtapas((prevEtapas) => ({
                ...prevEtapas,
                [etapa]: !prevEtapas[etapa]
            }))
        }
    }

    const getStepsDatabase = async (instrumento) => { 
        try{
            const res = await fetch(`${process.env.REACT_APP_BACKEND}/api/instrumento/etapas`, { 
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({instrumento})
            });
            
            const etapas = await res.json();
            setEtapas(etapas.etapas);
            console.log(etapas)
        } catch (error) { 
            return console.error('Ocorreu um erro ao tentar realizar o fetch', error);
        }
    }

    const listDatabases = []
    {databases.map((database) => { 
        listDatabases.push({
            label: database, value: database
        })
    }
    )}

    const handleSelectDatabaseChange = (value) => {
        setInstrumento(value);
    }

    useEffect(() => {
        const fetchDatabase = async () => { 
            try { 
                const res = await fetch(`${process.env.REACT_APP_BACKEND}/api/instrumento/listar`);

                const instrumentosDisponiveis = await res.json();
                setDatabases(instrumentosDisponiveis)

            }catch(error) { 
                console.error('Erro ao tentar fazer requisição', error)
            }
        };
        
        fetchDatabase();
    }, []);

    useEffect(() => {
        if(instrumento) { 
            getStepsDatabase(instrumento);
        }
    }, [instrumento])

    return(
        <div className={styles.home}>

            {/* Container para verificação de cada database por meio de uma checklist */}
            <div style={{display:'flex', justifyContent:'center', backgroundColor:'#000b1f', width:'100%', paddingBottom:'150px', borderTop:'1px solid rgba(255, 255, 255, 0.1)'}}>
                <div className={styles.inicio}>
                    <p style={{fontSize:'2rem', fontWeight:'600', marginBottom:'1.5rem'}}>Bem vindo ao sistema da CPA!</p>
                    <SelectAutoWidth
                    onSelectChange={handleSelectDatabaseChange}
                    label='Instrumento'
                    options={listDatabases}
                    textColor='#fff'
                    >
                    </SelectAutoWidth>
                    <div>
                        <ul className={styles.inicio_checklist}>
                            {ordenarEtapas.map(({ key, value }) => ( 
                                <li 
                                    className={styles.inicio_checklist_item} 
                                    key={key}
                                    onClick={() => handleCheckboxChange(key)}
                                >
                                    <Checkbox
                                        checked={value}
                                        onChange={() => handleCheckboxChange(key)}
                                        onClick={(e) => e.stopPropagation()}
                                        sx={{
                                            color: 'white', 
                                            '&.Mui-checked': {
                                                color: 'white', 
                                            },
                                            '& .MuiSvgIcon-root': { fontSize: 28 },
                                            pointerEvents: 'none'
                                        }}
                                    />    
                                    {key}
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
            </div>

            {/* Container contendo um tutorial passo a passo de funcionamento do sistema */}
            <div style={{textAlign:'center', marginTop:'6vh', marginBottom:'4vh'}}>
                <h2 style={{marginBottom:'1rem', fontSize:'2.75rem', fontWeight:'600', color:'#000b1f'}}>Tutorial Passo a Passo</h2>
                <p style={{fontSize:'1.4rem', color:'#666', maxWidth:'800px', margin:'0 auto', lineHeight:'1.6'}}>Siga esses passos para conseguir gerar os relatórios dos instrumentos.</p>
            </div>
            <p> </p>
            <div className={styles.sessions}>
                    <div className={styles.sessionBox_right}>
                        <p className={styles.tag}>1º Passo: Inserir Arquivo do Instrumento</p>
                        <p className={styles.resume}>Insira o arquivo CSV do instrumento para que ele possa ser processado e analisado, sendo o periodo que demanda mais tempo.</p>
                        <Link to='/importar'>
                            <button type='button' className={styles.homeButton}>Inserir Csv</button>
                        </Link>
                    </div>
                <div className={styles.sessionBox_right}>
                    <p className={styles.tag}>2º Passo: Acompanhe o Progresso da inserção</p>
                    <p className={styles.resume}>Veja o progresso de cada etapa da inserção do CSV e acompanhe para conferir se tudo está ocorrendo corretamente.</p>
                    <Link to='/progresso'>
                        <button type='button' className={styles.homeButton}>Ver progresso do csv</button>
                    </Link>
                </div>

                <div className={styles.sessionBox_right}>
                    <p className={styles.tag}>3º Passo: Gerar Relatórios</p>
                    <p className={styles.resume}>Após a inserção do CSV, caso ela tenha ocorrido sem nenhum problema, comece a geração dos relatórios Markdowns</p>
                    <Link to='/gerar_relatorio'>
                        <button type='button' className={styles.homeButton}>Gerar Relatório</button>
                    </Link>
                </div>
                <div className={styles.sessionBox_right}>
                    <p className={styles.tag}>4º Passo: Gerar PDFs</p>
                    <p className={styles.resume}>Após ter gerado os Markdowns e ter feito a revisão dos mesmos, gere os PDFs dos relatórios.</p>
                    <Link to='/gerar_pdfs'>
                        <button type='button' className={styles.homeButton}>Gerar PDFs</button>
                    </Link>
                </div>
            </div>

            {/* Container com informações sobre a CPA e o Projeto */}
            <div className={styles.session_infos}>
                <h2 style={{fontSize: '2.5rem', fontWeight:'600', marginBottom:'1rem'}}>Sobre a CPA</h2>
                <div className={styles.session_infos_cpa}>
                    <img alt='banner' style={{width:'auto', height:'auto'}} src={cpa_banner}/>
                    <ul className={styles.session_infos_text}>
                        <li className={styles.session_infos_text_item}>
                        A Comissão Própria de Avaliação (CPA) da UEM tem como função desenvolver avaliações internas sistemáticas atendendo às orienações da Lei dos SINAES e com o sistema de avaliação do Estado do Paraná. 
                        </li>
                        <li className={styles.session_infos_text_item}>Desde 2005, a CPA busca manter um processo contínuo de autoavaliação institucional para subsidiar informações à gestão da universidade, promovendo a reflexão sobre as ações tomadas pela universidade e fortalecendo suas relações com a sociedade. Os resultados gerados pela CPA são enviados aos gestores em primeiro momento. Em segundo momento, após aprovação do Conselho Universitário, a CPA publica um relatório e envia os resultados ao MEC atendendo regulamentos específicos.</li>
                        <li className={styles.session_infos_text_item}> O presente sistema trabalha como auxiliar na elaboração dos relatórios que são gerados e enviados aos coordenadores. Esses documentos refletem as percepções dos diversos atores da universidade sobre o funcionamento e impactos positivos levados à sociedade. Parte do recurso utilizado nesta plataforma adota rotinas de Inteligência Artificial. Com esse apoio, a equipe da CPA consegue interpretar os dados de forma massiva. Todo o material elaborado é revisado e corrigido antes de gerar os relatórios definitivos enviados aos gestores da universidade.</li>
                    </ul>
                </div>
                <div className={styles.session_infos_sistema}>
                    <h2 style={{fontSize: '2.5rem', fontWeight:'600', marginBottom:'1.5rem'}}>Sobre o Sistema de geração automática de relatórios</h2>
                    <p className={styles.session_infos_sistema_text}>Este site foi desenvolvido pela Comissão Própria de Avaliação (CPA) da Universidade Estadual de Maringá (UEM) com o objetivo de facilitar a geração e o acesso a relatórios detalhados e precisos. Nossa plataforma permite a coleta, armazenamento e análise de dados de forma eficiente, oferecendo ferramentas intuitivas e robustas para apoiar decisões estratégicas e melhorar continuamente a qualidade acadêmica e administrativa da UEM. Foi feito uso de um Modelo de Inteligência Artificial geradora, combinado com outras ferramentas para ser feito a geração de dados.</p>
                </div>
            </div>
        </div>
    );
}

export default Home
