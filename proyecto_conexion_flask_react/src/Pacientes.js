import React, {useEffect, useRef, useState} from "react";
import Papa from "papaparse";
import "./style.css"; // Importa los estilos específicos del chat
import 'bootstrap/dist/css/bootstrap.min.css'; // Importar estilos
import 'bootstrap/dist/js/bootstrap.bundle.min.js'; // Importar JS de Bootstrap
import 'bootstrap-icons/font/bootstrap-icons.css';
import {getTTFB} from "web-vitals"; // Importar iconos de Bootstrap

const Pacientes = () => {

    const [card, setCard] = useState(""); // Guarda la tarjeta a añadir
    const [cards, setCards] = useState([]); // Guarda el historial de tarjetas
    const [tipoBusqueda, setTipoBusqueda] = useState("");
    const [textoFiltro, setTextoFiltro] = useState("");
    const [ordenSeleccionado, setOrdenSeleccionado] = useState("");
    const [triggerOrden, setTriggerOrden] = useState(false); // Estado para disparar el useEffect
    const [sentidoOrden, setSentidoOrden] = useState(null);
    const [checkPlanta, setCheckPlanta] = useState(false);
    const [pacientesRecientes, setPacientesRecientes] = useState([]);

    //NUEVO PACIENTE
    const [nuevoNombre, setNuevoNombre]=useState("");
    const [nuevoEdad, setNuevoEdad]=useState(0);
    const [nuevoSexo, setNuevoSexo]=useState("Masculino");
    const [nuevoAlergias, setNuevoAlergias]=useState("");
    const [nuevoMotivo, setNuevoMotivo]=useState("");
    const [nuevoDiagnostico, setNuevoDiagnostico]=useState("");
    const [nuevoCondiciones, setNuevoCondiciones]=useState("");
    const [nuevoFechaIngreso, setNuevoFechaIngreso]=useState("");
    const [nuevoServicio, setNuevoServicio]=useState("");
    const [nuevoEstado, setNuevoEstado]=useState("");
    const [nuevoCama, setNuevoCama]=useState(0);
    const [nuevoNUHSA, setNuevoNUHSA]=useState("");






    const navBarCollapsed = useRef(null);
    const page_element = useRef(null);
    const menu_button = useRef(null);

    const ordenarAlfabetico = (cards) => {
        return [...cards].sort((a, b) => a.nombre.localeCompare(b.nombre));
    };

    const ordenarFecha = (cards, par) => {
        return [...cards].sort((a, b) => new Date(a[par]) - new Date(b[par])).reverse();
    }

    const getSetterRecientes = (pacientes) => {
        let ordenados = ordenarFecha(pacientes, "acceso");
        ordenados = ordenados.slice(0,3);
        setPacientesRecientes(ordenados);
    }

    function updtRecientes(){
        getSetterRecientes(cards);
    }

    // Maneja la carga del archivo CSV
    const handleFiles = () => {
        fetch("/info_pacientes.csv")
            .then(response => response.text()) // Obtiene el contenido del CSV
            .then(csvText => {
                Papa.parse(csvText, {
                    complete: (result) => {
                        const data = result.data;
                        console.log(data[0]);
                        // Verifica si hay datos y si la cabecera es válida
                        if (data.length > 1 && data[0][0] === "ID") {
                            const extractedCards = data.slice(1).map((row) => ({
                                nombre: row[1],   // "Nombre"
                                nuhsa: row[12],   // "NUHSA"
                                cama: row[11],    // "Cama"
                                id: row[0],       // "ID"
                                fueraplanta: Math.round(Math.random()),
                                color: Math.floor(Math.random() * 4) + 1,
                                display: 1,
                                acceso: new Date(Date.now()),
                                creacion: new Date(Date.now()-1)
                            }));

                            setCards(extractedCards);
                            getSetterRecientes(extractedCards);
                        } else {
                            alert("Formato de CSV incorrecto");
                        }
                    },
                    header: false, // La primera fila contiene los encabezados
                    skipEmptyLines: true,
                });
            })
        console.log("datos de las tarjetas cargados correctamente: " + cards);
    };

    function handleTipoBusquedaChange(event) {
        setTipoBusqueda(event.target.value);
    }

    function handleTextoFiltroChange(event) {
        setTextoFiltro(event.target.value);
    }

    const filtrar = async (e) => {
        e.preventDefault();

        const updatedCards = [...cards];

        if(tipoBusqueda !== "1"){
            switch (tipoBusqueda){
                case "2":
                    for(let i = 0; i < updatedCards.length; i++){
                        if(!updatedCards[i].nombre.toLowerCase().includes(textoFiltro.toLowerCase().trim())){
                            updatedCards[i].display = 0;
                        }else{
                            updatedCards[i].display = 1;
                        }
                    }
                    break;
                case "3":
                    for(let i = 0; i < updatedCards.length; i++){
                        if(!updatedCards[i].id.includes(textoFiltro.trim())){
                            updatedCards[i].display = 0;
                        }else{
                            updatedCards[i].display = 1;
                        }
                    }
                    break;
                case "4":
                    for(let i = 0; i < updatedCards.length; i++){
                        if(!updatedCards[i].nuhsa.toLowerCase().includes(textoFiltro.toLowerCase().trim())){
                            updatedCards[i].display = 0;
                        }else{
                            updatedCards[i].display = 1;
                        }
                    }
                    break;
                default:
                    for(let i = 0; i < updatedCards.length; i++){
                        if(!updatedCards[i].cama.includes(textoFiltro.trim())){
                            updatedCards[i].display = 0;
                        }else{
                            updatedCards[i].display = 1;
                        }
                    }
                    break;
            }
        }else{
            if(checkPlanta){
                console.log("entro");
                setCheckPlanta(false);
            }
            for(let i = 0; i < updatedCards.length; i++){
                updatedCards[i].display = 1;
            }


        }

        setCards(updatedCards);
    }



    const handleOrdenChange = (orden) => {
        setOrdenSeleccionado(orden); // Establece la opción seleccionada
        setTriggerOrden(true); // Dispara el useEffect
    };

    const handleSentidoOrden = (modo) => {
        if(ordenSeleccionado !== ""){
            //Hay un orden seleccionado
            if(sentidoOrden !== modo){
                //se cambia el modo
                setSentidoOrden(modo)
                //invertimos orden de cards
                const updatedCards = [...cards].reverse();
                setCards(updatedCards);
            }
        }
    }

    const handleCheckPlanta = () => {
        setCheckPlanta(!checkPlanta); //invertimos valor
        //filtramos

        const updatedCards = [...cards];

        const check = checkPlanta ? 0 : 1;

        for(let i = 0; i < updatedCards.length; i++){
            if(updatedCards[i].fueraplanta === check){
                updatedCards[i].display = 1;
            }else{
                updatedCards[i].display = 0;
            }
        }
    }

    useEffect(() => {
        if (triggerOrden) {
            let updatedCards;

            if (ordenSeleccionado === "Orden alfabético") {
                console.log("alfabetico")
                updatedCards = ordenarAlfabetico(cards);
            } else if (ordenSeleccionado === "Fecha de acceso") {
                console.log("acceso")
                updatedCards = ordenarFecha(cards, "acceso");
            } else if (ordenSeleccionado === "Fecha de creación") {
                console.log("creacion")
                updatedCards = ordenarFecha(cards, "creacion");
            }
            setSentidoOrden(1);
            setCards(updatedCards); // Actualiza el estado de las tarjetas
            setTriggerOrden(false); // Restablece el trigger para evitar ejecución innecesaria
        }
    }, [triggerOrden, ordenSeleccionado]);

    useEffect(() => {

        const sidebar = navBarCollapsed.current;
        const page = page_element.current;
        const button = menu_button.current;

        if(cards.length === 0){
            handleFiles();
        }

        console.log("script.js cargado correctamente en React.");

        // Verificamos si el sidebar está disponible
        if (!sidebar) {
            console.error("El elemento #navBarCollapsed no se encuentra en el DOM.");
            return;
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


    });

    const actualizarAcceso = (paciente) => {
        paciente.acceso=new Date(Date.now());
        updtRecientes();
    }

    const crearNuevoPaciente = () =>{
        //TODO
    }

    return (
        <div className="container-fluid d-flex flex-nowrap p-0 position-relative" style={{overflowY: "scroll"}}>
            <nav className="d-flex flex-nowrap navbar navbar-expand-md flex-column p-0 position-relative">
                <div
                    className="d-flex flex-nowrap start-0 top-0 position-relative vh-100   collapse collapse-horizontal navbar-collapse lateral"
                    id="navBarCollapsed" ref={navBarCollapsed}>
                    <div className="position-fixed vh-100 start-0 top-0 flex-column shadow lateral ">
                        <ul className="navbar-nav p-4 mt-3 w-100 d-flex flex-column">
                            <li className="nav-item my-1 border-bottom w-100 pe-5 "><a
                                className="nav-link d-block w-100 pe-4" href="index.html">Inicio</a></li>
                            <li className="nav-item my-1 border-bottom w-100 pe-5 "><a
                                className="nav-link d-block w-100 pe-4" href="#collapseRecientes"
                                data-bs-toggle="collapse" role="button" aria-expanded="false"
                                aria-controls="collapseRecientes">Recientes </a></li>
                            <div className="collapse" id="collapseRecientes">
                                <ul ref={pacientesRecientes}>
                                    {pacientesRecientes.map((paciente) => (
                                        <li><a>{paciente.nombre}</a></li>
                                    ))}
                                </ul>
                            </div>
                            <li className="nav-item my-1 border-bottom w-100 pe-5 "><a
                                className="nav-link d-block w-100 pe-4" id="active" href="#">Pacientes</a></li>
                            <li className="nav-item my-1 border-bottom w-100 pe-5 "><a
                                className="nav-link d-block w-100 pe-4" href="Usuario.html">Usuario</a></li>
                        </ul>
                    </div>
                </div>
            </nav>

            <div className="position-relative m-2 container-md pt-0 mt-0 vw-100" id="page" ref={page_element} >
                <button className="d-flex flex-nowrap z-3  btn btn-light d-md-none mt-2"
                        type="button"
                        data-bs-toggle="collapse"
                        data-bs-target="#navBarCollapse"
                        aria-controls="navBarCollapsed"
                        aria-expanded="false"
                        aria-label="Toggle navigation"
                        id="menu-button" ref={menu_button}><i className="bi bi-list"></i>
                </button>
                <header>
                    <h1>Dedalus</h1>
                    <div className="searchbar">

                    </div>
                </header>

                <div id="accessibility-buttons"
                     className="w-100 border-bottom d-flex flex-wrap mb-3 pb-3 align-items-center">
                    <form id="buscar-paciente"
                          className="d-flex flex-nowrap bg-body-tertiary py-2 px-4 shadow rounded-pill me-4 my-2"
                          role="search"
                          onSubmit={filtrar}>
                        <div className="input-group d-flex">
                            <input type="search" placeholder="Buscar..." className="flex-grow-1 form-control"
                                   value={textoFiltro}
                                   onChange={handleTextoFiltroChange}/>
                            <select className="form-select flex-shrink-1 bg-body-secondary" id="tipo-busqueda"
                                    value={tipoBusqueda}
                                    onChange={handleTipoBusquedaChange}>
                                <option value="1">Ninguno</option>
                                <option value="2">Nombre</option>
                                <option value="3">Identificador</option>
                                <option value="4">NUHSA</option>
                                <option value="5">Nº de cama</option>
                            </select>
                        </div>
                        <button id="search-button" type="submit"
                                className="border-0 rounded-circle ms-3 bg-body-secondary btn"><i
                            className="bi bi-search"></i></button>
                    </form>


                    <div className="dropdown btn-group shadow me-4 align-self-center my-2" role="group">
                        <button type="button" className="btn btn-light border-end" onClick={() => handleSentidoOrden(1)}><i className="bi bi-arrow-up"></i>
                        </button>
                        <button type="button" className="btn btn-light border-start border-end" onClick={() => handleSentidoOrden(2)}><i
                            className="bi bi-arrow-down"></i></button>
                        <button className="btn btn-light dropdown-toggle border-start" type="button"
                                data-bs-toggle="dropdown" aria-expanded="false">Ordenar
                        </button>
                        <ul className="dropdown-menu" id="ordenar">
                            <li className={`dropdown-item ${ordenSeleccionado === "Orden alfabético" ? "active" : ""}`}
                                onClick={() => handleOrdenChange("Orden alfabético")}>
                                Orden alfabético
                            </li>
                            <li className={`dropdown-item ${ordenSeleccionado === "Fecha de acceso" ? "active" : ""}`}
                                onClick={() => handleOrdenChange("Fecha de acceso")}>
                                Fecha de acceso
                            </li>
                            <li className={`dropdown-item ${ordenSeleccionado === "Fecha de creación" ? "active" : ""}`}
                                onClick={() => handleOrdenChange("Fecha de creación")}>
                                Fecha de creación
                            </li>
                        </ul>
                    </div>


                    <input className="btn-check" type="checkbox" id="fuera-de-planta" autoComplete="off" onChange={handleCheckPlanta} checked={checkPlanta}/>
                    <label key={checkPlanta} className={`btn btn-light shadow align-self-center my-2 ${checkPlanta ? "checked" : ''}`} htmlFor="fuera-de-planta"
                           id="button-fuera-de-planta">Fuera de Planta</label>


                </div>

                <div className={"container-fluid d-flex flex-wrap justify-content-start"} id="pacientes"  >
                    <div className={"card shadow"} id="newPaciente" data-bs-toggle="modal" data-bs-target="#nuevo-paciente">
                        <a>
                            <i className="bi bi-plus"></i>
                        </a>
                    </div>
                    <div className="modal fade" tabIndex="-1" id="nuevo-paciente">
                        <div className="modal-dialog modal-dialog-centered modal-dialog-scrollable">
                            <div className="modal-content">
                                <div className="modal-header">
                                    <h3 className="modal-title">Nuevo paciente</h3>
                                    <button type="button" className="btn-close" data-bs-dismiss="modal"
                                            aria-label="Close"></button>
                                </div>
                                <div className="modal-body w-100" style={{overflowX:"hidden"}}>
                                    <form className={"m-3"} onSubmit={crearNuevoPaciente}>
                                        <div className={"mb-5 d-flex flex-column w-100"}>
                                            <div className={"d-flex w-100 justify-content-between align-items-center my-1"}><span className={"fw-semibold"}>Nombre: </span><input onChange={(e) => setNuevoNombre(e.target.value)} className={" ms-5 flex-grow-1 border-0 border-bottom"} type="text" name="Nombre"/></div>
                                            <div className={"d-flex w-100 justify-content-between align-items-center my-1"}><span className={"fw-semibold"}>Edad: </span><input onChange={(e) => setNuevoEdad(e.target.value)} className={" ms-5 flex-grow-1 border-0 border-bottom"} type="number" name="Edad"/></div>
                                            <div className={"d-flex w-100 justify-content-between align-items-center my-1"}><span
                                                className={"fw-semibold"}>Sexo: </span>
                                               <div className={" ms-5 d-flex flex-grow-1 justify-content-around"}>
                                                   <input type="radio" id="Masculino" value="Masculino" name="Sexo" autoComplete="off"
                                                          className={"btn-check"} onChange={(e) => setNuevoSexo(e.target.value)} checked={nuevoSexo === "Masculino"}/>
                                                   <label className={"btn me-1"} htmlFor="Masculino">Masculino</label>
                                                   <input type="radio" id="Femenino" value="Femenino" name="Sexo" autoComplete="off"
                                                          className={"btn-check"} onChange={(e) => setNuevoSexo(e.target.value)} checked={nuevoSexo === "Femenino"}/>
                                                   <label className={"btn ms-1"} htmlFor="Femenino">Femenino</label>
                                               </div>
                                            </div>
                                            <div className={"d-flex w-100 justify-content-between align-items-center my-1"}><span
                                                className={"fw-semibold"}>Alergias: </span><input onChange={(e) => setNuevoAlergias(e.target.value)} className={" ms-5 flex-grow-1 border-0 border-bottom"} type="text" name="Alergias"/></div>
                                            <div className={"d-flex w-100 justify-content-between align-items-center my-1"}><span
                                                className={"fw-semibold"}>Motivo de Ingreso: </span><input onChange={(e) => setNuevoFechaIngreso(e.target.value)} className={" ms-5 flex-grow-1 border-0 border-bottom"} type="text" name="MotivoIngreso"/></div>
                                            <div className={"d-flex w-100 justify-content-between align-items-center my-1"}><span
                                                className={"fw-semibold"}>Diagnóstico Principal: </span><input onChange={(e) => setNuevoDiagnostico(e.target.value)} className={" ms-5 flex-grow-1 border-0 border-bottom"} type="text" name="DiagnosticoPrincipal"/></div>
                                            <div className={"d-flex w-100 justify-content-between align-items-center my-1"}><span
                                                className={"fw-semibold"}>Condiciones Previas: </span><input onChange={(e) => setNuevoCondiciones(e.target.value)} className={" ms-5 flex-grow-1 border-0 border-bottom"} type="text" name="CondicionesPrevias"/></div>
                                            <div className={"d-flex w-100 justify-content-between align-items-center my-1"}><span
                                                className={"fw-semibold"}>Fecha de Ingreso: </span><input onChange={(e) => setNuevoFechaIngreso(e.target.value)} className={" ms-5 flex-grow-1 border-0 border-bottom"} type="date" name="FechaIngreso"/></div>
                                            <div className={"d-flex w-100 justify-content-between align-items-center my-1"}><span
                                                className={"fw-semibold"}>Servicio: </span>
                                                <select id="Servicio" className={" ms-5 flex-grow-1 border-0 border-bottom form-select"} onChange={(e) => setNuevoServicio(e.target.value)}>
                                                    <option value="Neumología">Neumología</option>
                                                    <option value="Cardiología">Cardiología</option>
                                                    <option value="UCI">UCI</option>
                                                    <option value="Cirugía General">Cirugía General</option>
                                                    <option value="Medicina Interna">Medicina Interna</option>
                                                    <option value="Neurología">Neurología</option>
                                                    <option value="Gastroenterología">Gastroenterología</option>
                                                </select></div>
                                            <div className={"d-flex w-100 justify-content-between align-items-center my-1"}><span
                                                className={"fw-semibold"}>Estado al ingreso: </span><input onChange={(e) => setNuevoEstado(e.target.value)} className={" ms-5 flex-grow-1 border-0 border-bottom"} type="text" name="EstadoAlIngreso"/></div>
                                            <div className={"d-flex w-100 justify-content-between align-items-center my-1"}><span
                                                className={"fw-semibold"}>Número de Cama: </span><input onChange={(e) => setNuevoCama(e.target.value)} className={" ms-5 flex-grow-1 border-0 border-bottom"} type="number" name="Cama"/></div>
                                            <div className={"d-flex w-100 justify-content-between align-items-center my-1"}><span
                                                className={"fw-semibold"}>NUHSA: </span><input onChange={(e) => setNuevoNUHSA(e.target.value)} className={" ms-5 flex-grow-1 border-0 border-bottom"} type="text" name="NUHSA"/></div>

                                        </div>
                                        <div className="modal-footer w-100">
                                            <input type="submit" className={"btn btn-primary w-100"} value="Crear Conversación" id="botonnuevopaciente"/>
                                        </div>
                                    </form>
                                </div>

                            </div>
                        </div>
                    </div>
                    {cards.map((card, index) => (
                        <div key={index} className={`card shadow ${card.display === 0 ? 'd-none' : ''}`}>
                            <a href="#">
                                <div className={`card-gradient gr${card.color} card-img-top`}></div>
                                <div className="card-body mt-0 pt-2">
                                    {card.nombre}
                                    <ul className="m-0 ps-3 pt-0 text-body-secondary">
                                        <li>NUHSA: {card.nuhsa}</li>
                                        <li>Cama: {card.cama}</li>
                                        <li>ID: {card.id}</li>
                                    </ul>
                                </div>
                            </a>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )
};

export default Pacientes;