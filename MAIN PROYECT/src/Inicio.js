import React, {useEffect, useRef, useState} from "react";
import 'bootstrap/dist/css/bootstrap.min.css'; // Importar estilos
import 'bootstrap/dist/js/bootstrap.bundle.min.js'; // Importar JS de Bootstrap
import 'bootstrap-icons/font/bootstrap-icons.css';
import "./style.css";
import {getTTFB} from "web-vitals"; // Importar iconos de Bootstrap

const Inicio = () => {

    return (
        <div className={"d-flex h-100 text-center text-bg-light d-flex justify-content-center align-items-center"}>
            <div className="position-absolute z-3 bg-body-tertiary rounded-end-pill shadow align-content-center px-5"
                 id="presentacion">
                <h1 className="display-4 fw-bold mb-3 text-center">Dedalus AI</h1>
                <p className="lead my-4 text-">Descubre la manera más sencilla de analizar y generar informes sobre
                    datos clínicos. Obtén información valiosa sobre tu salud y mejora la atención a tus pacientes con
                    mayor precisión y confianza.</p>
                <div>
                    <a href="/pacientes" className="btn btn-lg btn-light fw-bold border-white shadow"
                       id="button-start">Empieza ahora</a>
                </div>
            </div>

            <div className="carousel slide" data-bs-ride="carousel">
                <div className="carousel-inner">
                    <div className="carousel-item active" data-bs-interval="5000">
                        <img src="img/img2.jpg" className="d-block-w-100" loading="eager"/>
                    </div>
                    <div className="carousel-item" data-bs-interval="5000">
                        <img src="img/img3.jpg" className="d-block-w-100" loading="lazy"/>
                    </div>
                    <div className="carousel-item" data-bs-interval="5000">
                        <img src="img/img4.jpg" className="d-block-w-100" loading="lazy"/>
                    </div>
                </div>
            </div>
        </div>
    )
};

export default Inicio;