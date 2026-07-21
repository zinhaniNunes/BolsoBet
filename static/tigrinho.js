const simbolos = [
    "🍒", "🍊", "🪙", "🧧", "🪭",
    "🥁", "👑", "💎", "⭐", "🐯"
];

const casas = document.querySelectorAll(".linha span");
const comprarSpins = document.getElementById("comprar_spins");
const botao = document.getElementById("girar");
const aposta = document.getElementById("aposta");
const tigerImg = document.getElementById("tiger-img");

// ATENÇÃO: troque esses caminhos pelos arquivos de imagem que você
// realmente tem em /static/assets/imgs/. São só nomes de exemplo.
const IMAGENS_TIGRE = {
    normal:  "/static/assets/imgs/tiger(neutro).png", // sem ganho
    pequeno: "/static/assets/imgs/tiger(boa).png",    // ganho pequeno
    medio:   "/static/assets/imgs/tiger(grito).png",  // ganho médio
    grande:  "/static/assets/imgs/tiger(chora).png",     // ganho grande
    mega:    "/static/assets/imgs/tiger(rico).png"      // ganho enorme
};

// Define os limites de multiplicador para cada imagem.
// "multiplicador" é o total de vezes a aposta ganho naquele giro (0 = sem ganho).
function atualizarTigre(multiplicador) {

    if (!tigerImg) return;

    let novaImagem = IMAGENS_TIGRE.normal;

    if (multiplicador >= 15) {
        novaImagem = IMAGENS_TIGRE.mega;
    } else if (multiplicador >= 5) {
        novaImagem = IMAGENS_TIGRE.grande;
    } else if (multiplicador >= 2) {
        novaImagem = IMAGENS_TIGRE.medio;
    } else if (multiplicador > 0) {
        novaImagem = IMAGENS_TIGRE.pequeno;
    }

    if (tigerImg.getAttribute("src") !== novaImagem) {
        tigerImg.src = novaImagem;
    }
}

// Injeta a animação de piscar (3x, meio segundo cada) sem precisar mexer no style.css
(function injetarEstiloPiscar() {
    const style = document.createElement("style");
    style.textContent = `
        @keyframes piscarGanho {
            50%           { background-color: #ffd700; }
            0% ,100%      { background-color: #182437; }
        }
        .casa-ganhou {
            animation: piscarGanho 0.3s ease-in-out 3;
            animation-fill-mode: forwards;
        }
    `;
    document.head.appendChild(style);
})();

function limparDestaques() {
    casas.forEach(casa => {
        casa.classList.remove("casa-ganhou");
        casa.style.backgroundColor = "";
        // força reinício da animação caso a mesma casa ganhe de novo no próximo giro
        casa.style.animation = "none";
        void casa.offsetWidth; // reflow
        casa.style.animation = "";
    });
}

function destacarGanhos(posicoes) {

    if (!Array.isArray(posicoes)) return;

    posicoes.forEach(([linha, coluna]) => {
        const indice = linha * 5 + coluna;
        const casa = casas[indice];
        if (casa) {
            casa.classList.add("casa-ganhou");
        }
    });
}

function atualizarSaldoLocal(saldo) {
    const texto = saldo.toFixed(2).replace(".", ",");
    document.querySelectorAll(".saldo").forEach(elemento => {
        elemento.textContent = texto;
    });
}

function emojiAleatorio() {
    return simbolos[Math.floor(Math.random() * simbolos.length)];
}

function embaralhar() {
    casas.forEach(casa => {
        casa.textContent = emojiAleatorio();
    });
}

function mostrarResultado(matriz) {

    if (!Array.isArray(matriz)) {
        console.error("Matriz inválida:", matriz);
        return;
    }

    limparDestaques();

    let indice = 0;

    matriz.forEach(linha => {
        linha.forEach(simbolo => {
            casas[indice].textContent = simbolo;
            indice++;
        });
    });

}

botao.addEventListener("click", async () => {

    botao.disabled = true;
    limparDestaques();

    let animacao = setInterval(embaralhar, 50);

    try {
        const resposta = await fetch("/spin", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                aposta: parseFloat(aposta.value),
                comprar_spins: comprarSpins ? parseInt(comprarSpins.value) : 1
            })
        });

        const resultado = await resposta.json();

        if (!resposta.ok) {
            alert(resultado.erro);
            botao.disabled = false;
            clearInterval(animacao);
            return;
        }

        setTimeout(() => {

            clearInterval(animacao);

            let i = 0;

            async function proximaSpin() {

                if (i >= resultado.resultados.length) {
                    botao.disabled = false;
                    return;
                }

                mostrarResultado(resultado.resultados[i].matriz);
                atualizarSaldoLocal(resultado.resultados[i].saldo);
                destacarGanhos(resultado.resultados[i].posicoes);
                atualizarTigre(resultado.resultados[i].multiplicador);


                i++;

                // Espera 1 segundo mostrando o resultado
                setTimeout(() => {

                    // Se ainda houver outra spin, faz a animação novamente
                    if (i < resultado.resultados.length) {

                    animacao = setInterval(embaralhar, 50);

                    setTimeout(() => {

                        clearInterval(animacao);

                        proximaSpin();

                    }, 1000);

                } else {

                        botao.disabled = false;

                    }

                }, 1000);

            }

            proximaSpin();

        }, 1000);

    } catch (erro) {
        console.error(erro);
        botao.disabled = false;
        clearInterval(animacao);
        alert("Erro ao comunicar com o servidor.");
    }

});