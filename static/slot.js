const casas = document.querySelectorAll(".linha span");
const primeiraLinha = document.querySelector(".linha");
const colunasPorLinha = primeiraLinha ? primeiraLinha.children.length : 5;

const matrizEl = document.getElementById("matriz");
const comprarSpins = document.getElementById("comprar_spins");
const botao = document.getElementById("girar");
const aposta = document.getElementById("aposta");
const mascoteImg = document.getElementById("mascote-img");

// --- Sons ---
const somRolagem = new Audio("/static/sounds/slot_roll.mp3");
somRolagem.loop = true;

const somPremioPequeno = new Audio("/static/sounds/premio_pequeno_.mp3");
const somPremioMedio = new Audio("/static/sounds/premio_medio_.mp3");
const somPremioGrande = new Audio("/static/sounds/premio_grande_.mp3");

function tocarSom(audio) {
    audio.currentTime = 0;
    audio.play().catch(() => {}); // ignora erro caso o navegador bloqueie autoplay
}

function iniciarSomRolagem() {
    if (fadeRolagemId) {
        clearInterval(fadeRolagemId);
        fadeRolagemId = null;
    }
    somRolagem.volume = 1;
    somRolagem.currentTime = 0;
    somRolagem.play().catch(() => {});
}

// Fade-out suave em vez de corte seco: reduz o volume aos poucos até pausar
let fadeRolagemId = null;

function pararSomRolagem(duracaoMs = 250) {
    if (fadeRolagemId) {
        clearInterval(fadeRolagemId);
        fadeRolagemId = null;
    }

    const passos = 10;
    const volumeInicial = somRolagem.volume;
    const decremento = volumeInicial / passos;
    const intervaloMs = duracaoMs / passos;

    fadeRolagemId = setInterval(() => {
        const novoVolume = somRolagem.volume - decremento;

        if (novoVolume <= 0) {
            somRolagem.pause();
            somRolagem.currentTime = 0;
            somRolagem.volume = 1; // restaura para o próximo giro
            clearInterval(fadeRolagemId);
            fadeRolagemId = null;
        } else {
            somRolagem.volume = novoVolume;
        }
    }, intervaloMs);
}

function tocarSomPremio(multiplicador) {
    if (multiplicador >= 5) {
        tocarSom(somPremioGrande);
    } else if (multiplicador >= 2) {
        tocarSom(somPremioMedio);
    } else if (multiplicador > 0) {
        tocarSom(somPremioPequeno);
    }
    // multiplicador == 0 -> sem prêmio, sem som
}

const FALLBACK_SIMBOLOS = ["🍒", "⭐", "💎"];
const simbolosAnimacao = matrizEl?.dataset.simbolos
    ? matrizEl.dataset.simbolos.split(",")
    : FALLBACK_SIMBOLOS;

const IMAGENS_MASCOTE = mascoteImg ? {
    normal:  mascoteImg.getAttribute("src"),
    pequeno: mascoteImg.dataset.imgPequeno || mascoteImg.getAttribute("src"),
    medio:   mascoteImg.dataset.imgMedio   || mascoteImg.getAttribute("src"),
    grande:  mascoteImg.dataset.imgGrande  || mascoteImg.getAttribute("src"),
} : null;

function atualizarMascote(multiplicador) {

    if (!mascoteImg || !IMAGENS_MASCOTE) return;

    let novaImagem = IMAGENS_MASCOTE.normal;

    if (multiplicador >= 5) {
        novaImagem = IMAGENS_MASCOTE.grande;
    } else if (multiplicador >= 2) {
        novaImagem = IMAGENS_MASCOTE.medio;
    } else if (multiplicador > 0) {
        novaImagem = IMAGENS_MASCOTE.pequeno;
    }

    if (mascoteImg.getAttribute("src") !== novaImagem) {
        mascoteImg.src = novaImagem;
    }
}

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
        casa.style.animation = "none";
        void casa.offsetWidth;
        casa.style.animation = "";
    });
}

function destacarGanhos(posicoes) {

    if (!Array.isArray(posicoes)) return;

    posicoes.forEach(([linha, coluna]) => {
        const indice = linha * colunasPorLinha + coluna;
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

function simboloAleatorio() {
    return simbolosAnimacao[Math.floor(Math.random() * simbolosAnimacao.length)];
}

function embaralhar() {
    casas.forEach(casa => {
        casa.textContent = simboloAleatorio();
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

    iniciarSomRolagem();
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
            pararSomRolagem();
            return;
        }

        setTimeout(() => {

            clearInterval(animacao);
            pararSomRolagem();

            let i = 0;

            async function proximaSpin() {

                if (i >= resultado.resultados.length) {
                    botao.disabled = false;
                    return;
                }

                mostrarResultado(resultado.resultados[i].matriz);
                atualizarSaldoLocal(resultado.resultados[i].saldo);
                destacarGanhos(resultado.resultados[i].posicoes);
                atualizarMascote(resultado.resultados[i].multiplicador);
                tocarSomPremio(resultado.resultados[i].multiplicador);


                i++;

                setTimeout(() => {

                    if (i < resultado.resultados.length) {

                    iniciarSomRolagem();
                    animacao = setInterval(embaralhar, 50);

                    setTimeout(() => {

                        clearInterval(animacao);
                        pararSomRolagem();

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
        pararSomRolagem();
        alert("Erro ao comunicar com o servidor.");
    }

});
