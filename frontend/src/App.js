import './App.css';
import NavBar from './components/layout/NavBar';
import Footer from './components/layout/Footer.js';
import Home from './pages/Home';
import Progresso from './pages/Progresso.js';
import Importar from './pages/Importar';
import GerarRelatorio from './pages/GerarRelatorio';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Container from './components/layout/Container';

function App() {
  return (
    <Router>
      <NavBar/>
      <Container>
        <Routes>
              <Route path="/" element={<Home/>}/>
              <Route path="/progresso" element={<Progresso/>}/>
              <Route path="/importar" element={<Importar/>}/>
              <Route path="/gerar_relatorio" element={<GerarRelatorio/>}/>
        </Routes>
      </Container>
      <Footer/>
    </Router>
  );
}

export default App;