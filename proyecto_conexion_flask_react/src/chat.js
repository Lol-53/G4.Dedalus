import React, {useEffect, useRef, useState} from "react";
import "./style.css"; // Importa los estilos específicos del chat
import 'bootstrap/dist/css/bootstrap.min.css'; // Importar estilos
import 'bootstrap/dist/js/bootstrap.bundle.min.js'; // Importar JS de Bootstrap
import 'bootstrap-icons/font/bootstrap-icons.css'; // Importar iconos de Bootstrap
import { useNavigate } from "react-router-dom";
import {type} from "@testing-library/user-event/dist/type";

const Chat = () => {

    const [idPaciente, setIdPaciente]= useState(0);
    const [nombrePaciente, setNombrePaciente] = useState("");
    const [pacientesRecientes, setPacientesRecientes] = useState([]);

    const [message, setMessage] = useState(""); // Guarda el mensaje escrito
    const [msgTemporal, setMsgTemporal] = useState("");
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);
    const [peticionResumen, setPeticionResumen] =useState(false);

    const [convHistory, setConvHistory] = useState([]);

    const navBarCollapsed = useRef(null);
    const page_element = useRef(null);
    const menu_button = useRef(null);
    const chat_body = useRef(null);
    const contenido_Chat = useRef(null);
    const text_bubble = useRef(null);
    const campo_msg = useRef(null);
    const chat_text_area = useRef(null);

    const navigate = useNavigate();

    function scrollToBottom() {
        const chat = chat_body.current;

        // Usa setTimeout para esperar a que el mensaje se agregue al DOM
        setTimeout(() => {
            chat.scrollTop = chat.scrollHeight;
        }, 0); // Retraso mínimo para asegurar que el DOM se actualiza
    }

    async function getHistory() {
        try {
            const response = await fetch("http://localhost:5000/get-history", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({id_paciente: idPaciente}),
            });

            console.log("Paso " + idPaciente);

            const data = await response.json();

            if (!Array.isArray(data)) {
                console.error("El historial no es un array:", data);
                return [];
            }

            console.log("Historial cargado:", data);
            return data; // Devuelve el historial de mensajes
        } catch (error) {
            console.error("Error al obtener historial:", error);
            return [];
        }

        scrollToBottom();
    }

    async function fetchHistory() {
        const history = await getHistory();
        setConvHistory(history); // Guardamos el historial en el estado
    }

    const infoPacientes = () => {
        let paciente = localStorage.getItem('paciente');

        if(paciente){
            paciente = JSON.parse(paciente);
            console.log(paciente.id);
            setIdPaciente(paciente.id);
            setNombrePaciente(paciente.nombre);
        }

        let recientes = localStorage.getItem('recientes');
        if(recientes){
            recientes = JSON.parse(recientes);
            setPacientesRecientes(recientes);
        }
    };

    useEffect(() => {
        document.body.style.overflow = "hidden";
        infoPacientes()
        fetchHistory();

        const sidebar = navBarCollapsed.current;
        const page = page_element.current;
        const button = menu_button.current;
        const chat = chat_body.current;
        const contenidoChat = contenido_Chat.current;
        const bubble = text_bubble.current;
        const textInput = campo_msg.current;
        const chatTextArea = chat_text_area.current;

        console.log("script.js cargado correctamente en React.");

        // Verificamos si el sidebar está disponible
        if (!sidebar) {
            console.error("El elemento #navBarCollapsed no se encuentra en el DOM.");
            return;
        }

        if(page.offsetHeight > window.innerHeight){
            sidebar.style.height = page.offsetHeight + "px";
        }else{
            sidebar.style.height = window.offsetHeight + "px";
        }

        if(window.innerWidth < 768 && (!sidebar.classList.contains("hidden"))){
            sidebar.classList.add("hidden");
            page.classList.add("expanded");
            if(chat){
                chat.style.setProperty("width", (window.innerWidth-250) + "px", "important");
            }
        }

        if(chat && (window.innerWidth < 768 && (sidebar.classList.contains("hidden")))){
            chat.style.setProperty("width", (window.innerWidth-50) + "px", "important");
        }

        if(window.innerWidth >= 768){
            if(chat){
                chat.style.setProperty("width", (window.innerWidth-250) + "px", "important");
            }
        }

        if(window.innerWidth < 768){
            button.classList.add("expanded");
        }

        if(chat){
            chat.style.setProperty("max-height", (window.innerHeight-200) + "px", "important");
        }

        button.addEventListener("click", function(event){

            event.preventDefault();
            sidebar.style.display="flex";

            if (sidebar.classList.contains("hidden")){


                // page.classList.add("hidden");
                sidebar.classList.remove("hidden");
                if(chat){
                    chat.style.setProperty("width", (window.innerWidth-250) + "px", "important");
                }
                page.classList.remove("expanded");

            }else{
                event.preventDefault();


                page.classList.add("expanded");
                sidebar.classList.add("hidden");
                if(chat){
                    chat.style.setProperty("width", (window.innerWidth-50) + "px", "important");
                }

            }
        });

        // Detectamos el cambio de tamaño de la ventana para simular el colapso
        window.addEventListener("resize", function (event) {

            // Si el navbar está colapsado (según el tamaño de la pantalla)



            if (window.innerWidth < 768 ) {
                // Aplicamos la animación de deslizamiento
                if(chat){
                    setTimeout(function(){chat.style.setProperty("max-height", (window.innerHeight-200) + "px", "important")}, 100);
                }
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
                setTimeout(function(){if(chat){
                    chat.style.setProperty("width", (window.innerWidth-50) + "px", "important");
                }},30);

            } else if (window.innerWidth >= 768) {
                // Si el tamaño de la pantalla es mayor y el navbar está oculto, lo mostramos
                if(chat){
                    setTimeout(function(){chat.style.setProperty("max-height", (window.innerHeight-200) + "px", "important");
                        chat.style.setProperty("width", (window.innerWidth-250) + "px", "important")
                    }, 100);
                }

                sidebar.classList.remove("hidden");
                page.classList.remove("expanded");
                button.classList.remove("expanded");
                button.classList.add("hidden");

                if(page.offsetHeight > window.innerHeight){
                    sidebar.style.height = page.offsetHeight + "px";
                }else{
                    sidebar.style.height = window.innerHeight + "px";
                }
            }

            if(contenidoChat){

                contenidoChat.style.height=window.innerHeight-100 + "px";
            }
        });

        if (!bubble || !textInput || !chatTextArea) return; // Evita errores si algún elemento no existe

        // Ajustar la altura inicial
        let initialHeight =  40;
        let initialBubble= bubble.style.width;
        textInput.style.height = textInput.value === "" ? "40px" : `${bubble.offsetHeight}px`;
        contenidoChat.style.height=window.innerHeight-100 + "px";

        textInput.addEventListener("input", function () {

            if (this.value.trim() === "") {
                bubble.style.height= initialBubble;
                textInput.style.height = `${initialHeight}px`; // Vuelve a la altura inicial si está vacío
                chatTextArea.style.height = "auto"; // Resetea la altura del contenedor también
                return;
            }

            this.style.height = "auto"; // Restablece la altura para recalcular
            this.style.height = `${this.scrollHeight-15}px`; // Ajusta según el contenido
            chat.styleheight =`${window.innerHeight-200-this.scrollHeight-50}px !important`
            bubble.style.height = `calc(40px + ${textInput.style.fontSize})`;
            // Ajustar el contenedor principal (chat_text_area)
            if (this.scrollHeight< 150) {
                this.style.height=this.scrollHeight;
                // chatTextArea.style.height = `${this.scrollHeight -150}px`;
                chatTextArea.style.height = "auto";
                this.style.overflowY = "hidden";
            } else {
                chatTextArea.style.height = "150px"; // Mantiene el tamaño máximo
                this.style.overflowY = "auto";
                this.style.height="120px";
                chatTextArea.style.height="150px";
            }
            bubble.style.height = `calc(${this.innerHeight}px + ${initialBubble}px)`;
        });

        window.addEventListener('load', function() {

            // Desplaza el scroll hacia abajo
            scrollToBottom();
        });

        if (idPaciente) {
            setContext(idPaciente);
        }
        return () => {
            document.body.style.overflow = "hidden";
        };
    }, [idPaciente, chat_body, chat_text_area, text_bubble, campo_msg, contenido_Chat, menu_button, page_element, navBarCollapsed]);

    useEffect(() => {
        const sidebar = navBarCollapsed.current;
        const page = page_element.current;
        const button = menu_button.current;
        const chat = chat_body.current;
        const contenidoChat = contenido_Chat.current;
        const bubble = text_bubble.current;
        const textInput = campo_msg.current;
        const chatTextArea = chat_text_area.current;

        console.log("script.js cargado correctamente en React.");

        // Verificamos si el sidebar está disponible
        if (!sidebar) {
            console.error("El elemento #navBarCollapsed no se encuentra en el DOM.");
            return;
        }

        if(page.offsetHeight > window.innerHeight){
            sidebar.style.height = page.offsetHeight + "px";
        }else{
            sidebar.style.height = window.offsetHeight + "px";
        }

        if(window.innerWidth < 768 && (!sidebar.classList.contains("hidden"))){
            sidebar.classList.add("hidden");
            page.classList.add("expanded");
            if(chat){
                chat.style.setProperty("width", (window.innerWidth-250) + "px", "important");
            }
        }

        if(chat && (window.innerWidth < 768 && (sidebar.classList.contains("hidden")))){
            chat.style.setProperty("width", (window.innerWidth-50) + "px", "important");
        }

        if(window.innerWidth >= 768){
            if(chat){
                chat.style.setProperty("width", (window.innerWidth-250) + "px", "important");
            }
        }

        if(window.innerWidth < 768){
            button.classList.add("expanded");
        }

        if(chat){
            chat.style.setProperty("max-height", (window.innerHeight-200) + "px", "important");
        }

        button.addEventListener("click", function(event){

            event.preventDefault();
            sidebar.style.display="flex";

            if (sidebar.classList.contains("hidden")){


                // page.classList.add("hidden");
                sidebar.classList.remove("hidden");
                if(chat){
                    chat.style.setProperty("width", (window.innerWidth-250) + "px", "important");
                }
                page.classList.remove("expanded");

            }else{
                event.preventDefault();


                page.classList.add("expanded");
                sidebar.classList.add("hidden");
                if(chat){
                    chat.style.setProperty("width", (window.innerWidth-50) + "px", "important");
                }

            }
        });

        // Detectamos el cambio de tamaño de la ventana para simular el colapso
        window.addEventListener("resize", function (event) {

            // Si el navbar está colapsado (según el tamaño de la pantalla)



            if (window.innerWidth < 768 ) {
                // Aplicamos la animación de deslizamiento
                if(chat){
                    setTimeout(function(){chat.style.setProperty("max-height", (window.innerHeight-200) + "px", "important")}, 100);
                }
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
                setTimeout(function(){if(chat){
                    chat.style.setProperty("width", (window.innerWidth-50) + "px", "important");
                }},30);

            } else if (window.innerWidth >= 768) {
                // Si el tamaño de la pantalla es mayor y el navbar está oculto, lo mostramos
                if(chat){
                    setTimeout(function(){chat.style.setProperty("max-height", (window.innerHeight-200) + "px", "important");
                        chat.style.setProperty("width", (window.innerWidth-250) + "px", "important")
                    }, 100);
                }

                sidebar.classList.remove("hidden");
                page.classList.remove("expanded");
                button.classList.remove("expanded");
                button.classList.add("hidden");

                if(page.offsetHeight > window.innerHeight){
                    sidebar.style.height = page.offsetHeight + "px";
                }else{
                    sidebar.style.height = window.innerHeight + "px";
                }
            }

            if(contenidoChat){

                contenidoChat.style.height=window.innerHeight-100 + "px";
            }
        });

        if (!bubble || !textInput || !chatTextArea) return; // Evita errores si algún elemento no existe

        // Ajustar la altura inicial
        let initialHeight = 40;
        let initialBubble= bubble.style.width;
        textInput.style.height = textInput.value === "" ? "40px" : `${bubble.offsetHeight}px`;
        contenidoChat.style.height=window.innerHeight-100 + "px";

        textInput.addEventListener("input", function () {

            if (this.value.trim() === "") {
                bubble.style.height= initialBubble;
                textInput.style.height = `${initialHeight}px`; // Vuelve a la altura inicial si está vacío
                chatTextArea.style.height = "auto"; // Resetea la altura del contenedor también
                return;
            }

            this.style.height = "auto"; // Restablece la altura para recalcular
            this.style.height = `${this.scrollHeight-15}px`; // Ajusta según el contenido
            chat.styleheight =`${window.innerHeight-200-this.scrollHeight-50}px !important`
            bubble.style.height = `calc(40px + ${textInput.style.fontSize})`;
            // Ajustar el contenedor principal (chat_text_area)
            if (this.scrollHeight< 150) {

                this.style.height=this.scrollHeight;
                // chatTextArea.style.height = `${this.scrollHeight -150}px`;
                chatTextArea.style.height = "auto";
                this.style.overflowY = "hidden";
            } else {

                chatTextArea.style.height = "150px"; // Mantiene el tamaño máximo
                this.style.overflowY = "auto";
                this.style.height="120px";
                chatTextArea.style.height="150px";
            }
            bubble.style.height = `calc(${this.innerHeight}px + ${initialBubble}px)`;
        });



        window.addEventListener('load', function() {

            // Desplaza el scroll hacia abajo
            scrollToBottom();
        });

        if (idPaciente) {
            setContext(idPaciente);
        }
        return () => {
            document.body.style.overflow = "hidden";
        };
    }, []);

    useEffect(() => {
        const sidebar = navBarCollapsed.current;
        const page = page_element.current;
        const button = menu_button.current;
        const chat = chat_body.current;
        const contenidoChat = contenido_Chat.current;
        const bubble = text_bubble.current;
        const textInput = campo_msg.current;
        const chatTextArea = chat_text_area.current;

        console.log("script.js cargado correctamente en React.");

        // Verificamos si el sidebar está disponible
        if (!sidebar) {
            console.error("El elemento #navBarCollapsed no se encuentra en el DOM.");
            return;
        }

        if(page.offsetHeight > window.innerHeight){
            sidebar.style.height = page.offsetHeight + "px";
        }else{
            sidebar.style.height = window.offsetHeight + "px";
        }

        if(window.innerWidth < 768 && (!sidebar.classList.contains("hidden"))){
            sidebar.classList.add("hidden");
            page.classList.add("expanded");
            if(chat){
                chat.style.setProperty("width", (window.innerWidth-250) + "px", "important");
            }
        }

        if(chat && (window.innerWidth < 768 && (sidebar.classList.contains("hidden")))){
            chat.style.setProperty("width", (window.innerWidth-50) + "px", "important");
        }

        if(window.innerWidth >= 768){
            if(chat){
                chat.style.setProperty("width", (window.innerWidth-250) + "px", "important");
            }
        }

        if(window.innerWidth < 768){
            button.classList.add("expanded");
        }

        if(chat){
            chat.style.setProperty("max-height", (window.innerHeight-200) + "px", "important");
        }

        button.addEventListener("click", function(event){

            event.preventDefault();
            sidebar.style.display="flex";

            if (sidebar.classList.contains("hidden")){


                // page.classList.add("hidden");
                sidebar.classList.remove("hidden");
                if(chat){
                    chat.style.setProperty("width", (window.innerWidth-250) + "px", "important");
                }
                page.classList.remove("expanded");

            }else{
                event.preventDefault();


                page.classList.add("expanded");
                sidebar.classList.add("hidden");
                if(chat){
                    chat.style.setProperty("width", (window.innerWidth-50) + "px", "important");
                }

            }
        });

        // Detectamos el cambio de tamaño de la ventana para simular el colapso
        window.addEventListener("resize", function (event) {

            // Si el navbar está colapsado (según el tamaño de la pantalla)



            if (window.innerWidth < 768 ) {
                // Aplicamos la animación de deslizamiento
                if(chat){
                    setTimeout(function(){chat.style.setProperty("max-height", (window.innerHeight-200) + "px", "important")}, 100);
                }
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
                setTimeout(function(){if(chat){
                    chat.style.setProperty("width", (window.innerWidth-50) + "px", "important");
                }},30);

            } else if (window.innerWidth >= 768) {
                // Si el tamaño de la pantalla es mayor y el navbar está oculto, lo mostramos
                if(chat){
                    setTimeout(function(){chat.style.setProperty("max-height", (window.innerHeight-200) + "px", "important");
                        chat.style.setProperty("width", (window.innerWidth-250) + "px", "important")
                    }, 100);
                }

                sidebar.classList.remove("hidden");
                page.classList.remove("expanded");
                button.classList.remove("expanded");
                button.classList.add("hidden");

                if(page.offsetHeight > window.innerHeight){
                    sidebar.style.height = page.offsetHeight + "px";
                }else{
                    sidebar.style.height = window.innerHeight + "px";
                }
            }

            if(contenidoChat){

                contenidoChat.style.height=window.innerHeight-100 + "px";
            }
        });

        if (!bubble || !textInput || !chatTextArea) return; // Evita errores si algún elemento no existe

        // Ajustar la altura inicial
        let initialHeight = 40;
        let initialBubble= bubble.style.width;
        textInput.style.height = textInput.value === "" ? "40px" : `${bubble.offsetHeight}px`;
        contenidoChat.style.height=window.innerHeight-100 + "px";

        textInput.addEventListener("input", function () {

            if (this.value.trim() === "") {
                bubble.style.height= initialBubble;
                this.style.height = `${initialHeight}px`; // Vuelve a la altura inicial si está vacío
                chatTextArea.style.height = "auto"; // Resetea la altura del contenedor también
                return;
            }

            this.style.height = "auto"; // Restablece la altura para recalcular
            this.style.height = `${this.scrollHeight-15}px`; // Ajusta según el contenido
            chat.styleheight =`${window.innerHeight-200-this.scrollHeight-50}px !important`
            bubble.style.height = `calc(40px + ${textInput.style.fontSize})`;
            // Ajustar el contenedor principal (chat_text_area)
            if (this.scrollHeight< 150) {

                this.style.height=this.scrollHeight;
                // chatTextArea.style.height = `${this.scrollHeight -150}px`;
                chatTextArea.style.height = "auto";
                this.style.overflowY = "hidden";
            } else {

                chatTextArea.style.height = "150px"; // Mantiene el tamaño máximo
                this.style.overflowY = "auto";
                this.style.height="120px";
                chatTextArea.style.height="150px";
            }
            bubble.style.height = `calc(${this.innerHeight}px + ${initialBubble}px)`;
        });

        window.addEventListener('load', function() {

            // Desplaza el scroll hacia abajo
            scrollToBottom();
        });

        if (idPaciente) {
            setContext(idPaciente);
        }
        return () => {
            document.body.style.overflow = "hidden";
        };
    }, [idPaciente]);


    const setContext = async (idPaciente) => {
        try {
            const response = await fetch("http://localhost:5000/set-context", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ id_paciente: idPaciente }),
            });

            const data = await response.json();
            console.log("Contexto cargado:", data.message);
        } catch (error) {
            console.error("Error al establecer el contexto:", error);
        }
    };

    const handleChange = (e) => {
        setMessage(e.target.value); // Actualiza el estado con lo que escribe el usuario
    };

    const handleSubmit = async (e) => {
        if (e && e.preventDefault) e.preventDefault(); // Evita que la página se recargue

        if (!message.trim()) return; // Evita enviar mensajes vacíos

        // Agregar el mensaje del usuario al chat
        setLoading(true);
        setMsgTemporal(message);
        fetchHistory();

        const bubble = text_bubble.current;
        const textInput = campo_msg.current;
        const chatTextArea = chat_text_area.current;

        let initialHeight = 40;
        let initialBubble= bubble.style.width;


        bubble.style.height= initialBubble;
        textInput.style.height = `${initialHeight}px`; // Vuelve a la altura inicial si está vacío
        chatTextArea.style.height = "auto"; // Resetea la altura del contenedor también

        const messageSend = message;

        setMessage(""); // Limpiar el input después de enviar

        scrollToBottom();
        // Enviar el mensaje al backend Flask

        await sendMessageToBackend(messageSend);
        scrollToBottom();
        setLoading(false);
    };

    const enterMandar = (event) =>{
        const textInput = campo_msg.current;
        textInput.addEventListener("keydown", function(event){
            if(event.key === "Enter" && !event.shiftKey && !event.ctrlKey && !event.altKey){
                event.preventDefault();
                console.log("hola");
                handleSubmit(event);
            }
        });
    }


    useEffect(() => {
        enterMandar();
    }, [campo_msg, handleSubmit]);


    const sendMessageToBackend = async (userMessage) => {
        try {
            const response = await fetch("http://localhost:5000/ask-ai", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: userMessage, 
                                        id_paciente: idPaciente }),
            });

            const data = await response.json();

            fetchHistory();

            scrollToBottom();
        } catch (error) {
            console.error("Error al enviar el mensaje:", error);
        }
    };

    const renderMessageContent = (msg) => {
        console.log(msg);
        if (msg.type === "image") {
            scrollToBottom();
            return (
                <img
                    src={msg.content}
                    alt="Imagen recibida"
                    loading="eager"
                    onError={(e) => {
                        e.target.onerror = null;
                        e.target.src = "/placeholder-image.png";
                    }}
                />
            );
        } else {
            scrollToBottom();
            return <p dangerouslySetInnerHTML={{ __html: msg.content.replace(/\n/g, "<br>") }}></p>;
        }
    };

    const ordenarFecha = (cards, par) => {
        return [...cards].sort((a, b) => new Date(a[par]) - new Date(b[par])).reverse();
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
            nuevas = nuevas.slice(0,3);
        }

        console.log(nuevas);
        setPacientesRecientes(nuevas);
        localStorage.setItem('recientes', JSON.stringify(nuevas));
    };

    const generarResumen = async () => {

        setPeticionResumen(true)

        const response=await fetch("http://localhost:5000/generate-report", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({id_paciente: idPaciente}),
        });

        if (response.ok) {
            const fileResponse = await fetch("/informe_generado.pdf");

            // Verificar si el archivo se obtuvo correctamente
            if (fileResponse.ok) {
                // const blob = await fileResponse.blob();  // Crear un Blob con el archivo recibido
                // const url = URL.createObjectURL(blob);   // Crear una URL de objeto para el Blob
                //
                // // Usar la URL del objeto para crear un "pseudo-enlace" sin necesidad de <a>
                // const fileName = "informe_generado.pdf"; // Nombre del archivo a descargar
                // window.open( `/${fileName}`, "_blank");

                const blob = await fileResponse.blob();
                const url = URL.createObjectURL(blob);

// Crear enlace oculto
                const link = document.createElement("a");
                link.href = url;
                link.download = "informe_generado.pdf"; // Nombre con el que quieres guardar el archivo
                document.body.appendChild(link);

// Simular clic
                link.click();

// Limpiar
                document.body.removeChild(link);
                URL.revokeObjectURL(url); // Liberar memoria

           }
            setPeticionResumen(false);
        }
    }

    const deRecientesAChat = (paciente) => {
        paciente.acceso=new Date(Date.now());
        actualizarPaciente(paciente);
        localStorage.setItem('paciente', JSON.stringify(paciente));
        setIdPaciente(paciente.id);
        setNombrePaciente(paciente.nombre);
        navigate("/chat");
    }

    return (
        <div style={{overflow: 'hidden'}}>
            <div className="container-fluid d-flex flex-nowrap p-0 position-relative">
                <nav className="d-flex flex-nowrap navbar navbar-expand-md flex-column p-0 position-relative" >
                    <div className="d-flex flex-nowrap start-0 top-0 position-relative vh-100 collapse collapse-horizontal navbar-collapse lateral"  ref={navBarCollapsed} id="navBarCollapsed">
                        <div className="position-fixed vh-100 start-0 top-0 flex-column shadow lateral ">
                            <ul className="navbar-nav p-4 mt-3 w-100 d-flex flex-column">
                                <li className="nav-item my-1 border-bottom w-100 pe-5 "><a className="nav-link d-block w-100 pe-4" href="/">Inicio</a></li>
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
                                <li className="nav-item my-1 border-bottom w-100 pe-5 "><a className="nav-link d-block w-100 pe-4" href="/usuario">Usuario</a></li>
                            </ul>
                        </div>
                    </div>
                </nav>

                <div className="m-2 container-md pt-0 mt-0 pe-0 mx-0 d-flex flex-column" ref={page_element} id="page">
                    <div className="position-relative d-flex" id="navigation-buttons">

                        <button id="button-back" className="mx-2 btn btn-light mt-2">
                            <a href="/pacientes">
                                <i className="bi bi-arrow-left"></i>
                            </a>
                        </button>

                        <button className="d-flex flex-nowrap z-3 btn btn-light d-md-none mt-2"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#navBarCollapse"
                                aria-controls="navBarCollapsed"
                                aria-expanded="false"
                                aria-label="Toggle navigation"
                                ref={menu_button}
                                id="menu-button"><i className="bi bi-list"></i>
                        </button>
                    </div>

                    <header>
                        <h2>{nombrePaciente}</h2>
                    </header>

                    <div className="container-fluid justify-content-start pe-0 d-flex flex-column" ref={contenido_Chat} id="contenidoChat">
                        <div className="d-flex flex-column justify-content-start me-6 vh-50 p-3 flex-shrink- h-100" ref={chat_body} id="chat-body">


                            {convHistory.map((msg, index) => (
                                <div key={`msg-${index}-${msg.type}`} className={`chat-bubble from${msg.role} shadow`}>
                                    {renderMessageContent(msg)}
                                </div>

                            ))}
                            <div className={`chat-bubble fromuser shadow ${loading ? "d-inline" : "d-none"}`}>
                                {msgTemporal}
                            </div>
                            <div className={`chat-bubble fromassistant shadow flex-wrap flex-row ${loading || peticionResumen ? "d-flex" : "d-none"}`}>
                                <div className="spinner-grow d-flex spinner-grow-sm me-2 text-body-secondary"
                                     role="status">
                                    <span className="visually-hidden">Loading...</span>
                                </div>
                                <div className="spinner-grow spinner-grow-sm text-body-secondary" role="status">
                                    <span className="visually-hidden">Loading...</span>
                                </div>
                                <div className="spinner-grow spinner-grow-sm ms-2 text-body-secondary" role="status">
                                    <span className="visually-hidden">Loading...</span>
                                </div>
                            </div>
                        </div>
                        <div ref={chat_text_area} id="chat-text-area"
                             className="d-flex flex-wrap align-items-center mb-3 align-items-center mt-0 flex-grow-1">
                            <form onSubmit={handleSubmit}
                                  className="d-flex flex-wrap flex-column flex-fill bg-body-tertiary rounded-pill shadow d-flex position-relative align-self-center m-2 mt-0"
                                  ref={text_bubble} id="text-bubble">
                                <div className="d-flex align-items-center justify-content-between my-1 h-100">
                                    <textarea
                                        type="text"
                                        value={message}
                                        onChange={handleChange}
                                        ref={campo_msg}
                                        id="campo-msg"
                                        className="chat_input my-2 mx-3 bg-body-tertiary border-0 border-bottom ms-5"
                                        placeholder="Escribe un mensaje..."
                                        disabled={loading || peticionResumen}
                                    />
                                    <button type="submit" className="rounded-circle border-0 px-2 py-1 me-2" id="button-send" disabled={loading || peticionResumen}><i className="bi bi-send"></i></button>
                                </div>
                            </form>
                            <button className="mx-2 py-1 px-2 border-0 rounded-circle  align-self-center" name="Generar resumen" id="generar-resumen" onClick={generarResumen} disabled={loading || peticionResumen}><i className="bi bi-file-earmark-arrow-down"></i></button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Chat;