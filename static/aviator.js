// BolsoBet - Aviator (front-end)
// A lógica de "quando o avião cai" acontece inteiramente no servidor (app.py).
// Este arquivo só exibe o estado e envia as ações do jogador.

const btn = document.getElementById("COMEÇAR");
const campoAposta = document.getElementById("aposta");
const saldoSpan = document.querySelector(".saldo");
const multSpan = document.querySelector(".multiplicador");
const mensagem = document.getElementById("mensagem");

const ceu = document.getElementById("ceu");
const aviao = document.getElementById("aviao");
const trilha = document.getElementById("trilha");

let emJogo = false;
let poll = null;

// Move o avião numa curva que desacelera conforme o multiplicador cresce,
// pra sempre caber dentro do "céu" mesmo em multiplicadores muito altos.
function moverAviao(mult) {
    mult = Math.max(mult, 1);

    const progresso = Math.min(1, 1 - 1 / mult);

    const maxX = 82;
    const maxY = 70;

    const x = progresso * maxX;
    const y = progresso * maxY;

    // Move o avião
    aviao.style.left = `calc(8% + ${x}%)`;
    aviao.style.bottom = `calc(10% + ${y}%)`;

    // Calcula a linha
    const dx = x;
    const dy = y/2;

    const comprimento = Math.sqrt(dx * dx + dy * dy);

    const angulo = -Math.atan2(dy, dx) * 180 / Math.PI;

    trilha.style.width = `${comprimento}%`;
    trilha.style.transform = `rotate(${angulo}deg)`;
}

function resetarAviao() {
    ceu.classList.remove("tremer");
    aviao.classList.remove("caiu");
    aviao.classList.add("idle");
    aviao.textContent = "✈️";
    aviao.style.left = "8%";
    aviao.style.bottom = "10%";
    trilha.style.width = "0";
    trilha.style.height = "0";
}

function decolarAviao() {
    ceu.classList.remove("tremer");
    aviao.classList.remove("idle", "caiu");
    aviao.textContent = "✈️";
    aviao.style.left = "8%";
    aviao.style.bottom = "10%";
    trilha.style.width = "0";
    trilha.style.height = "0";
}

function explodirAviao() {
    aviao.classList.remove("idle");
    aviao.classList.add("caiu");
    aviao.textContent = "💥";
    ceu.classList.add("tremer");
}

function formatar(valor) {
    return Number(valor).toFixed(2).replace(".", ",");
}

function travarControles(travado) {
    campoAposta.disabled = travado;
}

async function apostar() {
    const valor = parseFloat(campoAposta.value);

    if (isNaN(valor)) {
        mensagem.textContent = "Digite um valor de aposta.";
        return;
    }

    const resp = await fetch("/aviator/apostar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ aposta: valor }),
    });
    const data = await resp.json();

    if (!resp.ok) {
        mensagem.textContent = data.erro;
        return;
    }

    saldoSpan.textContent = formatar(data.saldo);
    multSpan.textContent = "1,00";
    mensagem.textContent = "";

    decolarAviao();

    emJogo = true;
    btn.textContent = "SACAR";
    travarControles(true);

    poll = setInterval(atualizarStatus, 100);
}

async function atualizarStatus() {
    const resp = await fetch("/aviator/status");
    const data = await resp.json();

    if (data.ativa) {
        multSpan.textContent = formatar(data.multiplicador);
        moverAviao(data.multiplicador);
        return;
    }

    // rodada acabou (caiu) sem o jogador ter sacado a tempo
    clearInterval(poll);
    emJogo = false;
    btn.textContent = "COMEÇAR";
    travarControles(false);

    if (data.caiu) {
        multSpan.textContent = formatar(data.multiplicador);
        mensagem.textContent = "💥 O avião caiu! Você perdeu a aposta.";
        saldoSpan.textContent = formatar(data.saldo);
        explodirAviao();
    }
}

async function sacar() {
    const resp = await fetch("/aviator/sacar", { method: "POST" });
    const data = await resp.json();

    clearInterval(poll);
    emJogo = false;
    btn.textContent = "COMEÇAR";
    travarControles(false);

    multSpan.textContent = formatar(data.multiplicador);
    saldoSpan.textContent = formatar(data.saldo);

    if (data.ok) {
        mensagem.textContent = `✅ Você sacou em ${formatar(data.multiplicador)}x! Prêmio: R$${formatar(data.premio)}`;
    } else {
        mensagem.textContent = "💥 O avião caiu antes do seu saque!";
        explodirAviao();
    }
}

btn.addEventListener("click", () => {
    if (emJogo) {
        sacar();
    } else {
        apostar();
    }
});
