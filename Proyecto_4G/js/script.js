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

  // Detectamos el cambio de tamaño de la ventana para simular el colapso
  window.addEventListener("resize", function (event) {

    // Si el navbar está colapsado (según el tamaño de la pantalla)

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


});
