const themeSwitch = document.getElementById("theme-switch");

// Función para aplicar el tema
function applyTheme(theme) {
    document.body.classList.toggle("dark", theme === "dark");
    document.body.classList.toggle("light", theme === "light");
    localStorage.setItem("theme", theme);
}

// Detectar el tema del sistema o el guardado en localStorage
function initTheme() {
    const savedTheme = localStorage.getItem("theme");
    const systemDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    
    if (savedTheme) {
        applyTheme(savedTheme);
        themeSwitch.checked = savedTheme === "dark";
    } else {
        applyTheme(systemDark ? "dark" : "light");
        themeSwitch.checked = systemDark;
    }
}

// Cambiar el tema manualmente
themeSwitch.addEventListener("change", () => {
    const newTheme = themeSwitch.checked ? "dark" : "light";
    applyTheme(newTheme);
});

// Inicializar el tema
initTheme();

function downloadVideo() {
    const url = document.getElementById("video-url").value;
    if (!url) {
        alert("Por favor, ingrese una URL de YouTube.");
        return;
    }
    window.open(`/download_video?url=${encodeURIComponent(url)}`, "_blank");
}

function downloadAudio() {
    const url = document.getElementById("audio-url").value;
    if (!url) {
        alert("Por favor, ingrese una URL de YouTube.");
        return;
    }
    window.open(`/download_audio?url=${encodeURIComponent(url)}`, "_blank");
}