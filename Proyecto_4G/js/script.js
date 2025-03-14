document.addEventListener("DOMContentLoaded", function () {
  let sidebar = document.getElementById("navBarCollapsed");
  let page = document.getElementById("page");
  let button = document.getElementById("menu-button");
  let chat = document.getElementById("chat-body");

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

  let contenidoChat = document.getElementById("contenidoChat");

  // Detectamos el cambio de tamaño de la ventana para simular el colapso
  window.addEventListener("resize", function (event) {

    // Si el navbar está colapsado (según el tamaño de la pantalla)

    if(contenidoChat){
      contenidoChat.style.height=window.innerHeight-100 + "px";
    }

    if (window.innerWidth < 768 ) {
      // Aplicamos la animación de deslizamiento
      if(chat){
        chat.style.setProperty("max-height", (window.innerHeight-200) + "px", "important");
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
        chat.style.setProperty("width", (window.innerWidth-250) + "px", "important");
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
  });

  let bubble = document.getElementById("text-bubble");
  let textInput = document.getElementById("campo-msg");
  let chatTextArea = document.getElementById("chat-text-area"); // Asegúrate de obtenerlo

  if (!bubble || !textInput || !chatTextArea) return; // Evita errores si algún elemento no existe

  // Ajustar la altura inicial
  let initialHeight = bubble.offsetHeight - 40;
  let initialBubble= bubble.style.width;
  textInput.style.height = `${bubble.offsetHeight - 40}px`;
  document.getElementById("contenidoChat").style.height=window.innerHeight-100 + "px";

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
    bubble.style.height = `calc(${this.style.height} + ${textInput.style.fontSize})`;
    // Ajustar el contenedor principal (chat-text-area)
    if (this.scrollHeight< 150) {
      console.log("B");
      this.style.height=this.scrollHeight;
      // chatTextArea.style.height = `${this.scrollHeight -150}px`;
      chatTextArea.style.height = "auto";
      this.style.overflowY = "hidden";
    } else {
      console.log("C");
      chatTextArea.style.height = "150px"; // Mantiene el tamaño máximo

      // if(this.innerHeight < this.scrollHeight){
      //     bubble.style.height = `calc(${this.innerHeight}px - ${textInput.style.fontSize})`;
      //     this.style.overflowY = "hidden";
      // }else{
      //     bubble.style.height = "150px";
      //     this.style.overflowY = "auto"; // Habilita el scrollbar dentro del textarea
      //     this.style.height = `${275-150}px`; // Ajusta según el contenido
      // }
      this.style.overflowY = "auto";
      this.style.height="120px";
      chatTextArea.style.height="150px";
    }
    bubble.style.height = `calc(${this.innerHeight}px + ${initialBubble}px)`;
  });


});
