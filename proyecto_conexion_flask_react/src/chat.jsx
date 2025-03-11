import React, { useState } from "react";
import "./Chat.css"; // Importa los estilos específicos del chat

const Chat = () => {
    const [message, setMessage] = useState(""); // Guarda el mensaje escrito
    const [messages, setMessages] = useState([]); // Guarda el historial del chat

    const handleChange = (e) => {
        setMessage(e.target.value); // Actualiza el estado con lo que escribe el usuario
    };

    const handleSubmit = async (e) => {
        e.preventDefault(); // Evita que la página se recargue

        if (!message.trim()) return; // Evita enviar mensajes vacíos

        // Agregar el mensaje del usuario al chat
        setMessages([...messages, { role: "user", content: message }]);

        // Enviar el mensaje al backend Flask
        await sendMessageToBackend(message);

        setMessage(""); // Limpiar el input después de enviar
    };

    const sendMessageToBackend = async (userMessage) => {
        try {
            const response = await fetch("http://localhost:5000/ask-ai", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: userMessage }),
            });

            const data = await response.json();

            // Agregar la respuesta de la IA al chat
            setMessages((prev) => [...prev, { role: "ai", content: data.response }]);
        } catch (error) {
            console.error("Error al enviar el mensaje:", error);
        }
    };

    return (
        <div className="chat-container">
            <div className="chat-body">
                {messages.map((msg, index) => (
                    <div key={index} className={`chat-bubble ${msg.role}`}>
                        {msg.content}
                    </div>
                ))}
            </div>
            <div className="chat_text_area">
                <form onSubmit={handleSubmit} className="chat-form">
                    <input className="chat_input"
                        type="text"
                        value={message}
                        onChange={handleChange}
                        placeholder="Escribe un mensaje..."
                    />
                    <button type="submit">Enviar</button>
                </form>
            </div>
        </div>
    );
};

export default Chat;