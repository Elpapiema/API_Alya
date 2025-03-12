document.addEventListener("DOMContentLoaded", async () => {
    const container = document.getElementById("collaborators-container");

    const users = [
        "Elpapiema",
        "The-King-Destroy",
        "keyarga69"
    ];

    for (const user of users) {
        try {
            const response = await fetch(`https://api.github.com/users/${user}`);
            const data = await response.json();

            const collaboratorElement = document.createElement("div");
            collaboratorElement.classList.add("collaborator");

            collaboratorElement.innerHTML = `
                <a href="${data.html_url}" target="_blank">
                    <img src="${data.avatar_url}" alt="Avatar de ${data.login}">
                </a>
                <h3>${data.login}</h3>
            `;

            container.appendChild(collaboratorElement);
        } catch (error) {
            console.error(`Error al obtener datos de ${user}`, error);
        }
    }

    // Aplica la animación cuando los elementos sean visibles
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("show");
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll(".collaborator").forEach(el => observer.observe(el));
});
