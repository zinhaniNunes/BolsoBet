const simbolos = [
    "🍒", "🍊", "🪙", "🧧", "🪭",
    "🥁", "👑", "💎", "⭐", "🐯"
];

const casas = document.querySelectorAll(".linha span");
const botao = document.getElementById("girar");
const aposta = document.getElementById("aposta");

function emojiAleatorio() {
    return simbolos[Math.floor(Math.random() * simbolos.length)];
}

function embaralhar() {
    casas.forEach(casa => {
        casa.textContent = emojiAleatorio();
    });
}

function mostrarResultado(matriz) {

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

    const animacao = setInterval(embaralhar, 50);

    try {

        const resposta = await fetch("/spin", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                aposta: parseFloat(aposta.value)
            })

        });

        const resultado = await resposta.json();

        // espera 2 segundos antes de parar
        setTimeout(() => {

            clearInterval(animacao);

            mostrarResultado(resultado.matriz);

            const saldoBtn = document.querySelector(".saldo-btn");

            if (saldoBtn) {
                saldoBtn.innerHTML = `💰 R$ ${resultado.saldo.toFixed(2)}`;
            }

        }, 1000);

        // Atualiza o botão de saldo
        const saldoBtn = document.querySelector(".saldo-btn");

        if (saldoBtn) {
            saldoBtn.innerHTML = `💰 R$ ${resultado.saldo.toFixed(2)}`;
        }

        // Se ganhou dinheiro
        if (resultado.ganho > 0) {
            console.log("Ganhou R$", resultado.ganho);
        }

        // Se ganhou spins
        if (resultado.spin_bonus > 0) {
            console.log("Ganhou", resultado.spin_bonus, "spins bônus");
        }

    } catch (erro) {

        clearInterval(animacao);

        console.error(erro);

        alert("Erro ao conectar com o servidor.");

    }

    botao.disabled = false;

});