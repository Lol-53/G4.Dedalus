document.addEventListener("DOMContentLoaded", function () {
    let sidebar = document.getElementById("navBarCollapsed");
    let page = document.getElementById("page");
    let button = document.getElementById("menu-button");

    // Verificamos si el sidebar está disponible
    if (!sidebar) {
        console.error("El elemento #navBarCollapsed no se encuentra en el DOM.");
        return;
    }

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
            // page.style.left="0px";
            
            // page.style.position="200px";
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
            // event.preventDefault();
            sidebar.classList.add("hidden");
            // page.classList.remove("hidden");
            page.classList.add("expanded");
            button.classList.add("expanded");
            button.classList.remove("hidden");
            
        } else if (window.innerWidth >= 768) {
            // Si el tamaño de la pantalla es mayor y el navbar está oculto, lo mostramos
            // event.preventDefault();
            sidebar.classList.remove("hidden");
            // page.classList.add("hidden");
            page.classList.remove("expanded");
            button.classList.remove("expanded");
            button.classList.add("hidden");
            setTimeout(function () {
                button.classList.remove("show"); // Colapsamos efectivamente el navbar
             }, 400); // Duración de la animación (debe coincidir con el tiempo en la animación CSS)
        }
    });

    // // Escuchamos cuando el navbar se va a ocultar (colapsar)
    // sidebar.addEventListener("hide.bs.collapse", function (event) {
    //     console.log("Navbar está colapsando");

    //     // Aplicamos la animación de deslizamiento
    //     sidebar.classList.add("hidden"); // Desliza fuera de la pantalla

    //     // Usamos setTimeout para esperar a que la animación termine antes de colapsar
    //     setTimeout(function () {
    //         sidebar.classList.remove("show"); // Colapsamos efectivamente el navbar
    //     }, 400); // Duración de la animación (debe coincidir con el tiempo en la animación CSS)
   
    // });

    // // Escuchamos cuando el navbar se va a expandir
    // sidebar.addEventListener("show.bs.collapse", function (event) {
    //     console.log("Navbar está expandiendo");

    //     // Aplicamos la animación de expansión
    //     sidebar.classList.remove("hidden"); // Quitamos la animación de ocultación
    //     // sidebar.classList.add("expandido"); // Restablecemos la posición original del navbar

    //     // Usamos setTimeout para esperar a que el navbar se expanda antes de quitar la animación
    //     setTimeout(function () {
    //         sidebar.classList.add("show"); // Mostramos el navbar (el colapso es manejado por Bootstrap)
    //     }, 10); // Un pequeño delay para dar tiempo a la expansión
    // });
});

// document.addEventListener("DOMContentLoaded", function () {
    
//     let sidebar = document.getElementById("navBarCollapsed");
//     // Cuando empieza a colapsar (antes de ocultarse)
//     sidebar.addEventListener("hide.bs.collapse", function (event) {
//         console.log("hola");
//         event.preventDefault(); // Detenemos el colapso para aplicar la animación manualmente
//         console.log("adios");
//         sidebar.classList.add("hidden"); // Aplicamos la clase de animación
//         setTimeout(() => {
//             sidebar.classList.remove("show"); // Oculta después de la animación
//         }, 400); // Esperamos el tiempo de la animación
//     });

//     // Cuando empieza a expandirse (antes de mostrarse)
//     sidebar.addEventListener("show.bs.collapse", function () {
//         sidebar.classList.remove("hidden"); // Quitamos la clase para mostrarlo con la animación
//     });
// });