// Script para efeito de rolagem
document.addEventListener("DOMContentLoaded", () => {
    const fadeInElements = document.querySelectorAll(".fade-in");

    const onScroll = () => {
        fadeInElements.forEach((el) => {
            const rect = el.getBoundingClientRect();
            if (rect.top < window.innerHeight - 100) {
                el.classList.add("visible");
            }
        });
    };

    window.addEventListener("scroll", onScroll);
    onScroll();
});

function openWhatsApp() {
    const phoneNumber = "5575981231019"; // Número em formato internacional
    const message = "Olá, estou entrando em contato pelo seu site!";
    const url = `https://wa.me/${phoneNumber}?text=${encodeURIComponent(message)}`;
    window.open(url, '_blank');
}