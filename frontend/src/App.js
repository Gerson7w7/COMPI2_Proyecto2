import "./App.css";
import {
  BrowserRouter as Router,
  Routes,
  Route
} from "react-router-dom";
import Inicio from "./components/Inicio";
import Errores from "./components/Errores";
import SimbolosReport from "./components/Simbolos";

function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' element={<Inicio />} />
        <Route path='/errores' element={<Errores />} />
        <Route path='/simbolos' element={<SimbolosReport />} />
      </Routes>
    </Router>
  );
}

export default App;