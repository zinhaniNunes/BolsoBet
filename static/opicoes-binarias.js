document.addEventListener("DOMContentLoaded", () => {
    const matriz = document.getElementById("matriz");
    const mensagem = document.getElementById("mensagem");
    const saldoSpan = document.getElementById("saldo-valor");
    const inputAposta = document.getElementById("aposta");
    const btnSubir = document.getElementById("SUBIR");
    const btnDescer = document.getElementById("DESCER");
    const btnComecar = document.getElementById("COMEÇAR");
    const selectMoeda = document.getElementById("moeda-select");

    const DURACAO_ANIMACAO_MS = 5000;
    const MAX_VELAS_VISIVEIS = 15;

    let direcaoSelecionada = null;
    let carregando = false;
    let historico = []; // velas confirmadas (vindas do backend)
    let moedaAtual = null;

    // ---------- estrutura do gráfico ----------
    matriz.classList.add("chart-opbin");
    matriz.innerHTML = `
        <div class="chart-trilho">
            <div class="chart-linha-preco"></div>
        </div>
    `;
    const trilho = matriz.querySelector(".chart-trilho");
    const linhaPreco = matriz.querySelector(".chart-linha-preco");

    function formatarReais(valor) {
        return valor.toFixed(2).replace(".", ",");
    }

    function atualizarSaldo(saldo) {
        saldoSpan.textContent = formatarReais(saldo);
    }

    // ---------- escala de preços ----------
    function calcularEscala(velasVisiveis) {
        let min = Infinity;
        let max = -Infinity;
        velasVisiveis.forEach((v) => {
            min = Math.min(min, v.abertura, v.fechamento);
            max = Math.max(max, v.abertura, v.fechamento);
        });
        if (!isFinite(min) || !isFinite(max) || min === max) {
            min = 0;
            max = 100;
        }
        const folga = (max - min) * 0.12 || 5;
        return { min: min - folga, max: max + folga };
    }

    function posicaoY(preco, escala, alturaPx) {
        const proporcao = (preco - escala.min) / (escala.max - escala.min);
        return proporcao * alturaPx;
    }

    // ---------- desenho ----------
    function desenharCandleEl(el, vela, escala, alturaPx) {
        const topoCorpo = Math.max(vela.abertura, vela.fechamento);
        const baseCorpo = Math.min(vela.abertura, vela.fechamento);

        const corpoBottom = posicaoY(baseCorpo, escala, alturaPx);
        const corpoTop = posicaoY(topoCorpo, escala, alturaPx);

        const corpoEl = el.querySelector(".candle-corpo");

        corpoEl.style.bottom = corpoBottom + "px";
        corpoEl.style.height = Math.max(2, corpoTop - corpoBottom) + "px";

        const verde = vela.fechamento >= vela.abertura;
        el.classList.toggle("candle-verde", verde);
        el.classList.toggle("candle-vermelha", !verde);
    }

    function criarCandleEl() {
        const el = document.createElement("div");
        el.className = "candle";
        el.innerHTML = `
            <div class="candle-corpo"></div>
        `;
        return el;
    }

    function renderTudo(velaFormando) {
        // a trilha é o container real onde as velas moram — usar a altura
        // dela (não a do #matriz, que inclui o padding) evita o
        // desalinhamento entre as velas e a linha de preço.
        const alturaPx = trilho.clientHeight || 500;
        const visiveis = historico.slice(-MAX_VELAS_VISIVEIS);
        const todas = velaFormando ? [...visiveis, velaFormando] : visiveis;
        const escala = calcularEscala(todas.length ? todas : [{ abertura: 0, fechamento: 100 }]);

        trilho.querySelectorAll(".candle").forEach((el) => el.remove());

        visiveis.forEach((vela) => {
            const el = criarCandleEl();
            trilho.appendChild(el);
            desenharCandleEl(el, vela, escala, alturaPx);
        });

        let elFormando = null;
        if (velaFormando) {
            elFormando = criarCandleEl();
            elFormando.classList.add("candle-formando");
            trilho.appendChild(elFormando);
            desenharCandleEl(elFormando, velaFormando, escala, alturaPx);
        }

        // a linha pontilhada sempre marca o fechamento da última vela PARADA
        // (nunca a vela em formação, para não "pular" durante a animação),
        // usando a MESMA referência de altura das velas (trilho.clientHeight)
        const precoReferencia = historico.length ? historico[historico.length - 1].fechamento : 50;
        const yLinha = posicaoY(precoReferencia, escala, alturaPx);
        linhaPreco.style.bottom = yLinha + "px";

        return elFormando;
    }

    // ---------- seletor de moeda ----------
    function popularSelectMoeda(moedas, moedaSelecionada) {
        selectMoeda.innerHTML = "";
        moedas.forEach((moeda) => {
            const opt = document.createElement("option");
            opt.value = moeda;
            opt.textContent = moeda;
            opt.selected = moeda === moedaSelecionada;
            selectMoeda.appendChild(opt);
        });
    }

    selectMoeda.addEventListener("change", () => {
        if (carregando) return;
        moedaAtual = selectMoeda.value;
        direcaoSelecionada = null;
        marcarSelecao();
        mensagem.textContent = "";
        carregarEstado(moedaAtual);
    });

    // ---------- carregar estado inicial ----------
    async function carregarEstado(moeda) {
        try {
            const url = moeda ? `/opbin/estado?moeda=${encodeURIComponent(moeda)}` : "/opbin/estado";
            const resp = await fetch(url);
            if (!resp.ok) return;
            const dados = await resp.json();
            historico = dados.velas || [];
            moedaAtual = dados.moeda;
            atualizarSaldo(dados.saldo);
            if (dados.aposta_minima) {
                inputAposta.min = dados.aposta_minima;
            }
            if (dados.moedas_disponiveis) {
                popularSelectMoeda(dados.moedas_disponiveis, moedaAtual);
            }
            renderTudo(null);
        } catch (erro) {
            console.error("Erro ao carregar estado:", erro);
        }
    }

    function setBotoesDesabilitados(desabilitado) {
        btnSubir.disabled = desabilitado;
        btnDescer.disabled = desabilitado;
        btnComecar.disabled = desabilitado;
        selectMoeda.disabled = desabilitado;
    }

    function marcarSelecao() {
        btnSubir.classList.toggle("selecionado", direcaoSelecionada === "subir");
        btnDescer.classList.toggle("selecionado", direcaoSelecionada === "descer");
    }

    btnSubir.addEventListener("click", () => {
        direcaoSelecionada = "subir";
        marcarSelecao();
    });

    btnDescer.addEventListener("click", () => {
        direcaoSelecionada = "descer";
        marcarSelecao();
    });

    // ---------- animação da vela até o resultado ----------
    function animarAteResultado(abertura, velaFinal, duracaoMs) {
        return new Promise((resolve) => {
            const inicio = performance.now();

            // pontos intermediários aleatórios que convergem para o fechamento final
            const numPontos = 14;
            const pontos = [abertura];
            for (let i = 1; i < numPontos; i++) {
                const progresso = i / numPontos;
                const alvo = abertura + (velaFinal.fechamento - abertura) * progresso;
                const amplitude = Math.abs(velaFinal.topo - velaFinal.fundo) * (1 - progresso) * 0.6;
                const ruido = (Math.random() - 0.5) * amplitude;
                pontos.push(alvo + ruido);
            }
            pontos.push(velaFinal.fechamento);

            function passo(agora) {
                const t = Math.min((agora - inicio) / duracaoMs, 1);
                const idxFloat = t * (pontos.length - 1);
                const idx0 = Math.floor(idxFloat);
                const idx1 = Math.min(idx0 + 1, pontos.length - 1);
                const frac = idxFloat - idx0;
                const fechamentoAtual = pontos[idx0] + (pontos[idx1] - pontos[idx0]) * frac;

                const velaTemporaria = {
                    abertura: abertura,
                    fechamento: t >= 1 ? velaFinal.fechamento : fechamentoAtual,
                };

                renderTudo(velaTemporaria);

                if (t < 1) {
                    requestAnimationFrame(passo);
                } else {
                    resolve();
                }
            }
            requestAnimationFrame(passo);
        });
    }

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
        mensagem.textContent = "";
        mensagem.style.color = "";

        try {
            const resp = await fetch("/opbin/jogar", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ direcao: direcaoSelecionada, aposta: aposta, moeda: moedaAtual }),
            });

            const dados = await resp.json();

            if (!resp.ok) {
                mensagem.textContent = dados.erro || "Não foi possível jogar.";
                return;
            }

            const abertura = historico.length
                ? historico[historico.length - 1].fechamento
                : dados.vela.abertura;

            await animarAteResultado(abertura, dados.vela, DURACAO_ANIMACAO_MS);

            historico.push(dados.vela);
            if (historico.length > MAX_VELAS_VISIVEIS) {
                historico.shift();
            }
            renderTudo(null);

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
