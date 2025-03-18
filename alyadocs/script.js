document.getElementById('menu-toggle').addEventListener('click', function () {
    document.getElementById('sidebar').classList.toggle('show');
});

document.getElementById('github').addEventListener('click', function() {
    window.open('https://github.com/Elpapiema/AlyaBot_MD', '_blank');
});

document.getElementById('descargar').addEventListener('click', function() {
    window.open('https://github.com/Elpapiema/AlyaBot_MD/releases/download/v2.2.1/alya-stable.zip', '_blank');
});

/*document.addEventListener("DOMContentLoaded", () => {
    const menuToggle = document.getElementById("menu-toggle");
    const sidebar = document.getElementById("sidebar");
    const content = document.querySelector(".content");

    // Alternar la barra lateral al hacer clic en el botón
    menuToggle.addEventListener("click", () => {
        sidebar.classList.toggle("active");
    });

    // Cerrar la barra lateral si se hace clic fuera de ella
    content.addEventListener("click", () => {
        if (sidebar.classList.contains("active")) {
            sidebar.classList.remove("active");
        }
    });
});*/
