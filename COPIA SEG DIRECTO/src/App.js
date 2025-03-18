import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Pacientes from "./Pacientes";
import Chat from "./chat"; // Asegúrate de que el nombre del archivo es correcto
import Inicio from "./Inicio";
import Usuario from "./Usuario";

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Inicio />} /> {}
                <Route path="/pacientes" element={<Pacientes />} />  {/* Página principal */}
                <Route path="/chat" element={<Chat />} />    {/* Nueva página Chat */}
                <Route path="/usuario" element={<Usuario     />} />    {/* Nueva página Chat */}
            </Routes>
        </Router>
    );
};

export default App;