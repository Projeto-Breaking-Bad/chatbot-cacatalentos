// Função para rolar suavemente para o topo da página
function topFunction() {
    document.body.scrollTop = 0; // Para navegadores Safari
    document.documentElement.scrollTop = 0; // Para outros navegadores
}

// Mostrar o botão "Voltar ao Topo" quando o usuário rolar para baixo 20px a partir do topo da página
window.onscroll = function () { scrollFunction() };

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        document.getElementById("myBtn").style.display = "block";
    } else {
        document.getElementById("myBtn").style.display = "none";
    }
}
