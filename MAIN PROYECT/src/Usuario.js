import React, {useEffect, useRef, useState} from "react";
import "./style.css"; // Importa los estilos específicos del chat
import 'bootstrap/dist/css/bootstrap.min.css'; // Importar estilos
import 'bootstrap/dist/js/bootstrap.bundle.min.js'; // Importar JS de Bootstrap
import 'bootstrap-icons/font/bootstrap-icons.css'; // Importar iconos de Bootstrap
import {type} from "@testing-library/user-event/dist/type";
import Papa from "papaparse";
import { useNavigate } from "react-router-dom";

const Usuario = () => {

    const [cards, setCards] = useState([]); // Guarda el historial de tarjetas
    const [pacientesRecientes, setPacientesRecientes] = useState([]);

    const navBarCollapsed = useRef(null);
    const page_element = useRef(null);
    const menu_button = useRef(null);

    const navigate = useNavigate();

    const ordenarFecha = (cards, par) => {
        return [...cards].sort((a, b) => new Date(a[par]) - new Date(b[par])).reverse();
    }

    const getSetterRecientes = (pacientes) => {
        let ordenados = ordenarFecha(pacientes, "acceso");
        ordenados = ordenados.slice(0,3);
        setPacientesRecientes(ordenados);
    }

    const recibirRecientes = () => {
        let recientes = localStorage.getItem('recientes');
        if(recientes){
            recientes = JSON.parse(recientes);
            setPacientesRecientes(recientes);
        }
    }

    const actualizarPaciente = (pacienteActualizado) => {
        let cargadas = localStorage.getItem('recientes');
        cargadas=JSON.parse(cargadas);
        const nuevasCards = (cartas) =>
            cartas.map((paciente) =>
                paciente.id === pacienteActualizado.id ? pacienteActualizado : paciente);

        const ids = new Set();
        let nuevas = [pacienteActualizado, ...cargadas]
        const duplicados = nuevas.filter((paciente) => {
            if (ids.has(paciente.id)) {
                return true; // Si ya existe el id, es un duplicado
            } else {
                ids.add(paciente.id);
                return false;
            }
        });
        ;
        if(duplicados.length>0){
            nuevas=[...cargadas];
            nuevas=nuevasCards(nuevas); //Sustituimos y ya
            nuevas=ordenarFecha(nuevas, "acceso");
        }else{
            nuevas.slice(0,3);
        }

        console.log(nuevas);
        setPacientesRecientes(nuevas);
        localStorage.setItem('recientes', JSON.stringify(nuevas));
    };

    const deRecientesAChat = (paciente) => {
        paciente.acceso = new Date(Date.now());
        actualizarPaciente(paciente);
        localStorage.setItem('paciente', JSON.stringify(paciente));
        navigate("/chat");
    }


    useEffect(() => {

        recibirRecientes();

        const sidebar = navBarCollapsed.current;
        const page = page_element.current;
        const button = menu_button.current;

        console.log("script.js cargado correctamente en React.");

        // Verificamos si el sidebar está disponible
        if (!sidebar) {
            console.error("El elemento #navBarCollapsed no se encuentra en el DOM.");
            //return;
        }

        page.style.width = `calc( ${window.innerWidth} + 200px)`;

        if(page.offsetHeight > window.innerHeight){
            sidebar.style.height = page.offsetHeight + "px";
        }else{
            sidebar.style.height = window.offsetHeight + "px";
        }

        if(window.innerWidth < 768 && (!sidebar.classList.contains("hidden"))){
            sidebar.classList.add("hidden");
            page.classList.add("expanded");

        }

        if(window.innerWidth < 768){
            button.classList.add("expanded");
        }


        button.addEventListener("click", function(event){

            event.preventDefault();
            //console.log(button);
            sidebar.style.display="flex";

            if (sidebar.classList.contains("hidden")){


                // page.classList.add("hidden");
                sidebar.classList.remove("hidden");

                page.classList.remove("expanded");

            }else{
                event.preventDefault();


                page.classList.add("expanded");
                sidebar.classList.add("hidden");


            }
        });

        // Detectamos el cambio de tamaño de la ventana para simular el colapso
        window.addEventListener("resize", function (event) {

            // Si el navbar está colapsado (según el tamaño de la pantalla)



            if (window.innerWidth < 768 ) {
                // Aplicamos la animación de deslizamiento

                sidebar.classList.add("hidden");
                page.classList.add("expanded");
                if(!button.classList.contains("expanded")){
                    button.classList.add("expanded");
                    button.classList.remove("hidden");
                }

                page.style.width = "calc("+page.style.width+"px + 200px)"


                if(page.offsetHeight > window.innerHeight){
                    sidebar.style.height = page.offsetHeight + "px";
                }else{
                    sidebar.style.height = window.innerHeight + "px";
                }


            } else if (window.innerWidth >= 768) {
                // Si el tamaño de la pantalla es mayor y el navbar está oculto, lo mostramos


                sidebar.classList.remove("hidden");
                page.classList.remove("expanded");
                button.classList.remove("expanded");
                button.classList.add("hidden");

                page.style.width = window.innerWidth + "px";

                if(page.offsetHeight > window.innerHeight){
                    sidebar.style.height = page.offsetHeight + "px";
                }else{
                    sidebar.style.height = window.innerHeight + "px";
                }
            }


        });


    },[]);

    return (
        <div className="container-fluid d-flex flex-nowrap p-0 position-relative">
            <nav className="d-flex flex-nowrap navbar navbar-expand-md flex-column p-0 position-relative">
                <div
                    className="d-flex flex-nowrap start-0 top-0 position-relative vh-100   collapse collapse-horizontal navbar-collapse lateral"
                    id="navBarCollapsed" ref={navBarCollapsed}>
                    <div className="position-fixed vh-100 start-0 top-0 flex-column shadow lateral ">
                        <ul className="navbar-nav p-4 mt-3 w-100 d-flex flex-column">
                            <li className="nav-item my-1 border-bottom w-100 pe-5 "><a
                                className="nav-link d-block w-100 pe-4" href="/">Inicio</a></li>
                            <li className="nav-item my-1 border-bottom w-100 pe-5 "><a
                                className="nav-link d-block w-100 pe-4" href="#collapseRecientes"
                                data-bs-toggle="collapse" role="button" aria-expanded="false"
                                aria-controls="collapseRecientes">Recientes </a></li>
                            <div className="collapse" id="collapseRecientes">
                                <ul ref={pacientesRecientes}>
                                    {pacientesRecientes.map((paciente) => (
                                        <li><a onClick={() => deRecientesAChat(paciente)}>{paciente.nombre}</a></li>
                                    ))}
                                </ul>
                            </div>
                            <li className="nav-item my-1 border-bottom w-100 pe-5 "><a
                                className="nav-link d-block w-100 pe-4" href="/pacientes">Pacientes</a></li>
                            <li className="nav-item my-1 border-bottom w-100 pe-5 "><a
                                className="nav-link d-block w-100 pe-4" id="active" href="#">Usuario</a></li>
                        </ul>
                    </div>
                </div>
            </nav>

            <div className="position-relative m-2 container-md w-100 pt-0 mt-0 " id="page" ref={page_element}>
                <button className="d-flex flex-nowrap z-3  btn btn-light d-md-none mt-2"
                        type="button"
                        data-bs-toggle="collapse"
                        data-bs-target="#navBarCollapse"
                        aria-controls="navBarCollapsed"
                        aria-expanded="false"
                        aria-label="Toggle navigation"
                        id="menu-button" ref={menu_button}><i className="bi bi-list"></i>
                </button>
                <header className="d-flex flex-wrap justify-content-start align-items-center">
                    <span className="me-4"><i className="bi bi-person-circle"></i></span>
                    <h1>Usuario</h1>
                </header>
                <div className="d-flex flex-wrap row">
                    <div className="col">
                        <div className="card shadow m-2">
                            <div className="card-header p-3 px-4"><h3>Información personal</h3></div>
                            <ul className="list-group list-group-flush py-2">
                                <li className="list-group-item"><span className="fw-semibold">Nombre: </span>Agustín
                                </li>
                                <li className="list-group-item"><span className="fw-semibold">Apellidos: </span>Ramos
                                    Ujaldón
                                </li>
                                <li className="list-group-item"><span className="fw-semibold">Localidad: </span>Málaga
                                </li>
                            </ul>
                        </div>
                    </div>
                    <div className="col">
                        <div className="card shadow m-2">
                            <div className="card-header p-3 px-4"><h3>Información profesional</h3></div>
                            <ul className="list-group list-group-flush py-2">
                                <li className="list-group-item"><span className="fw-semibold">Hospital: </span>Hospital
                                    Virgen de la Victoria
                                </li>
                                <li className="list-group-item"><span className="fw-semibold">Especialidad: </span>Patología
                                </li>

                                <li className="list-group-item"><span className="fw-semibold">Status: </span>Activo</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
};

export default Usuario;