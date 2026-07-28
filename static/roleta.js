// BolsoBet - Roleta (front-end)
// O sorteio e o cálculo de vitória acontecem inteiramente no servidor (app.py).
// Este arquivo cuida da seleção da aposta, da animação da roda e dos sons.

const botoes = document.querySelectorAll(".aposta-btn");
const campoAposta = document.getElementById("aposta");
const btnGirar = document.getElementById("COMEÇAR");
const saldoSpan = document.querySelector(".saldo");
const numeroSpan = document.querySelector(".numero-sorteado");
const mensagem = document.getElementById("mensagem");
const apostaSelecionadaLabel = document.getElementById("aposta-selecionada");
const rodaImg = document.getElementById("roda-roleta");
const configSons = document.getElementById("config-sons");

let apostaTipo = null;
let apostaValor = null;
let rotacaoAtual = 0;

const NOMES_APOSTA = {
    "red": "Vermelho",
    "black": "Preto",
    "par": "Par",
    "impar": "Ímpar",
    "1~18": "1 a 18",
    "19~36": "19 a 36",
};

// Ordem real dos números na imagem da roleta, no sentido horário,
// começando no topo (ver descrição_da_img_roleta.txt)
const ORDEM_RODA = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23,
    10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26,
];
const ANGULO_SEGMENTO = 360 / ORDEM_RODA.length;
const DURACAO_GIRO_MS = 4200;

// --- Sons ---
const somGiro = new Audio(configSons.dataset.spin);
somGiro.loop = true;

const somPremio = new Audio(configSons.dataset.premio);

function formatar(valor) {
    return Number(valor).toFixed(2).replace(".", ",");
}

function nomeDaAposta(tipo, valor) {
    if (tipo === "numero") return `Número ${valor}`;
    if (tipo === "duzia") return `${valor}ª dúzia`;
    return NOMES_APOSTA[valor] || valor;
}

botoes.forEach((btn) => {
    btn.addEventListener("click", () => {
        botoes.forEach((b) => b.classList.remove("selecionado"));
        btn.classList.add("selecionado");

        apostaTipo = btn.dataset.tipo;
        apostaValor = btn.dataset.valor;

        apostaSelecionadaLabel.textContent = `Aposta selecionada: ${nomeDaAposta(apostaTipo, apostaValor)}`;
    });
});

// Calcula o ângulo final (acumulado) pra roda parar com o número sorteado
// alinhado ao ponteiro no topo, sempre girando pra frente.
function calcularRotacaoFinal(numeroSorteado) {
    const indice = ORDEM_RODA.indexOf(numeroSorteado);
    const centroSegmento = indice * ANGULO_SEGMENTO + ANGULO_SEGMENTO / 2;
    const anguloNecessario = (360 - centroSegmento) % 360;

    const voltasExtras = 5; // só efeito visual
    const baseAtual = Math.ceil(rotacaoAtual / 360) * 360;

    return baseAtual + voltasExtras * 360 + anguloNecessario;
}

function girarRoda(numeroSorteado) {
    return new Promise((resolve) => {
        rotacaoAtual = calcularRotacaoFinal(numeroSorteado);

        rodaImg.style.transition = `transform ${DURACAO_GIRO_MS}ms cubic-bezier(0.17, 0.67, 0.14, 1)`;
        rodaImg.style.transform = `rotate(${rotacaoAtual}deg)`;

        const aoTerminar = () => {
            rodaImg.removeEventListener("transitionend", aoTerminar);
            resolve();
        };
        rodaImg.addEventListener("transitionend", aoTerminar);
    });
}

async function girar() {
    if (!apostaTipo) {
        mensagem.textContent = "Escolha uma casa na mesa antes de girar.";
        return;
    }

    const valorAposta = parseFloat(campoAposta.value);
    if (isNaN(valorAposta)) {
        mensagem.textContent = "Digite um valor de aposta.";
        return;
    }

    btnGirar.disabled = true;
    mensagem.textContent = "Girando...";

    let data;
    try {
        const resp = await fetch("/roleta/girar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                aposta: valorAposta,
                tipo: apostaTipo,
                valor: apostaValor,
            }),
        });
        data = await resp.json();

        if (!resp.ok) {
            mensagem.textContent = data.erro;
            btnGirar.disabled = false;
            return;
        }
    } catch (erro) {
        mensagem.textContent = "Erro de conexão. Tente novamente.";
        btnGirar.disabled = false;
        return;
    }

    // já sabemos o resultado; agora só animamos a roda até parar nele
    somGiro.currentTime = 0;
    somGiro.play().catch(() => {});

    await girarRoda(data.numero);

    somGiro.pause();
    somGiro.currentTime = 0;

    numeroSpan.textContent = data.numero;
    saldoSpan.textContent = formatar(data.saldo);
    btnGirar.disabled = false;

    if (data.venceu) {
        mensagem.textContent = `🎉 Deu ${data.numero} (${data.cor})! Você ganhou R$${formatar(data.premio)}`;
        somPremio.currentTime = 0;
        somPremio.play().catch(() => {});
    } else {
        mensagem.textContent = `Deu ${data.numero} (${data.cor}). Você perdeu a aposta.`;
    }
}

btnGirar.addEventListener("click", girar);
