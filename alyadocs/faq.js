document.addEventListener("DOMContentLoaded", function () {
    const faqButtons = document.querySelectorAll(".faq-question");

    faqButtons.forEach(button => {
        button.addEventListener("click", function () {
            const answer = this.nextElementSibling;

            if (answer.style.display === "block") {
                answer.style.display = "none";
            } else {
                // Oculta las otras respuestas antes de abrir una nueva
                document.querySelectorAll(".faq-answer").forEach(item => item.style.display = "none");
                answer.style.display = "block";
            }
        });
    });
});
