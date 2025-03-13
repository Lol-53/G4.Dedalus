document.addEventListener("DOMContentLoaded", function () {
  let sidebar = document.getElementById("navBarCollapsed");
  let page = document.getElementById("page");
  let button = document.getElementById("menu-button");

  // Verificamos si el sidebar está disponible
  if (!sidebar) {
    console.error("El elemento #navBarCollapsed no se encuentra en el DOM.");
    return;
  }

  sidebar.style.height = page.offsetHeight + "px";
  if(window.innerWidth < 768 && (!sidebar.classList.contains("hidden"))){
    sidebar.classList.add("hidden");
    page.classList.add("expanded");

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
      button.classList.add("expanded");
      button.classList.remove("hidden");
      page.style.width = "calc("+page.style.width+"+200px)"
      sidebar.style.height = page.offsetHeight + "px";

    } else if (window.innerWidth >= 768) {
      // Si el tamaño de la pantalla es mayor y el navbar está oculto, lo mostramos
      sidebar.classList.remove("hidden");
      page.classList.remove("expanded");
      button.classList.remove("expanded");
      button.classList.add("hidden");
      sidebar.style.height = page.offsetHeight + "px";
    }
  });


});
