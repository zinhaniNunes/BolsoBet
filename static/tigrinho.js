const simbolos = [
    "🍒", "🍊", "🪙", "🧧", "🪭",
    "🥁", "👑", "💎", "⭐", "🐯"
];

const casas = document.querySelectorAll(".linha span");
const comprarSpins = document.getElementById("comprar_spins");
const botao = document.getElementById("girar");
const aposta = document.getElementById("aposta");

async function atualizarSaldo() {

    const resposta = await fetch("/saldo");
    const dados = await resposta.json();

    const saldo = dados.saldo.toFixed(2).replace(".", ",");

    document.querySelectorAll(".saldo").forEach(elemento => {
        elemento.textContent = saldo;
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

                await atualizarSaldo();

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