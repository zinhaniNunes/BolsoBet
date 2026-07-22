const casas = document.querySelectorAll(".linha span");
const primeiraLinha = document.querySelector(".linha");
const colunasPorLinha = primeiraLinha ? primeiraLinha.children.length : 5;

const matrizEl = document.getElementById("matriz");
const comprarSpins = document.getElementById("comprar_spins");
const botao = document.getElementById("girar");
const aposta = document.getElementById("aposta");
const mascoteImg = document.getElementById("mascote-img");

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
                atualizarMascote(resultado.resultados[i].multiplicador);


                i++;

                setTimeout(() => {

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
