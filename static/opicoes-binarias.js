document.addEventListener("DOMContentLoaded", () => {
    const matriz = document.getElementById("matriz");
    const mensagem = document.getElementById("mensagem");
    const saldoSpan = document.getElementById("saldo-valor");
    const inputAposta = document.getElementById("aposta");
    const btnSubir = document.getElementById("SUBIR");
    const btnDescer = document.getElementById("DESCER");
    const btnComecar = document.getElementById("COMEÇAR");

    let direcaoSelecionada = null;
    let carregando = false;

    function formatarReais(valor) {
        return valor.toFixed(2).replace(".", ",");
    }

    function atualizarSaldo(saldo) {
        saldoSpan.textContent = formatarReais(saldo);
    }

    function criarVelaEl(vela) {
        const el = document.createElement("div");
        el.className = "vela-opbin " + (vela.cor === "verde" ? "vela-verde" : "vela-vermelha");

        const altura = Math.max(20, Math.round(vela.valor * 100));
        el.style.height = altura + "px";
        el.title = vela.valor.toFixed(2);

        if (vela.resultado === "vitoria") {
            el.classList.add("vela-vitoria");
        } else if (vela.resultado === "derrota") {
            el.classList.add("vela-derrota");
        }

        return el;
    }

    function renderVelas(velas) {
        matriz.innerHTML = "";
        const trilho = document.createElement("div");
        trilho.className = "trilho-velas";
        velas.forEach((vela) => trilho.appendChild(criarVelaEl(vela)));
        matriz.appendChild(trilho);
    }

    function marcarSelecao() {
        btnSubir.classList.toggle("selecionado", direcaoSelecionada === "subir");
        btnDescer.classList.toggle("selecionado", direcaoSelecionada === "descer");
    }

    async function carregarEstado() {
        try {
            const resp = await fetch("/opbin/estado");
            if (!resp.ok) return;
            const dados = await resp.json();
            renderVelas(dados.velas);
            atualizarSaldo(dados.saldo);
            if (dados.aposta_minima) {
                inputAposta.min = dados.aposta_minima;
            }
        } catch (erro) {
            console.error("Erro ao carregar estado:", erro);
        }
    }

    function setBotoesDesabilitados(desabilitado) {
        btnSubir.disabled = desabilitado;
        btnDescer.disabled = desabilitado;
        btnComecar.disabled = desabilitado;
    }

    btnSubir.addEventListener("click", () => {
        direcaoSelecionada = "subir";
        marcarSelecao();
    });

    btnDescer.addEventListener("click", () => {
        direcaoSelecionada = "descer";
        marcarSelecao();
    });

    btnComecar.addEventListener("click", async () => {
        if (carregando) return;

        if (!direcaoSelecionada) {
            mensagem.textContent = "Escolha SUBIR ou DESCER antes de começar.";
            return;
        }

        const aposta = parseFloat(inputAposta.value);
        if (isNaN(aposta) || aposta <= 0) {
            mensagem.textContent = "Digite um valor de aposta válido.";
            return;
        }

        carregando = true;
        setBotoesDesabilitados(true);
        mensagem.textContent = "Rodando...";

        try {
            const resp = await fetch("/opbin/jogar", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ direcao: direcaoSelecionada, aposta: aposta }),
            });

            const dados = await resp.json();

            if (!resp.ok) {
                mensagem.textContent = dados.erro || "Não foi possível jogar.";
                return;
            }

            const velaEl = criarVelaEl(dados.vela);
            const trilho = matriz.querySelector(".trilho-velas");
            trilho.appendChild(velaEl);
            while (trilho.children.length > 10) {
                trilho.removeChild(trilho.firstChild);
            }

            atualizarSaldo(dados.saldo);

            if (dados.venceu) {
                mensagem.textContent = `Você ganhou! +R$ ${formatarReais(dados.premio)}`;
                mensagem.style.color = "#3f8b0b";
            } else {
                mensagem.textContent = "Você perdeu essa rodada.";
                mensagem.style.color = "#970909";
            }
        } catch (erro) {
            console.error("Erro ao jogar:", erro);
            mensagem.textContent = "Erro de conexão. Tente novamente.";
        } finally {
            carregando = false;
            setBotoesDesabilitados(false);
        }
    });

    carregarEstado();
});
