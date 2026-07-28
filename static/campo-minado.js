document.addEventListener('DOMContentLoaded', () => {
    const matrizEl = document.getElementById('matriz');
    const linhas = matrizEl.querySelectorAll('.linha');
    const btnPrincipal = document.getElementById('COMEÇAR');
    const inputAposta = document.getElementById('aposta');
    const inputBombas = document.getElementById('bombas');
    const spanMultiplicador = document.querySelector('.multiplicador');
    const spansSaldo = document.querySelectorAll('.saldo');
    const mensagemEl = document.getElementById('mensagem');
    const mascoteImg = document.getElementById('mascote-img');

    let jogoAtivo = false;
    let processando = false; // trava contra cliques duplos durante fetch
    let timerFinalizacao = null; // id do setTimeout pendente de finalizarRodada

    const SONS = {
        bomba: '/static/sounds/boom.mp3',
        gema: '/static/sounds/premio_medio_.mp3',
        premio: '/static/sounds/ihe.mp3'
    };

    // Cria uma instância nova de Audio a cada chamada, então um som nunca
    // interrompe/corta o outro no meio — cada um toca até o fim natural.
    function tocarSom(chave) {
        const caminho = SONS[chave];
        if (!caminho) return;
        const audio = new Audio(caminho);
        audio.play()
            .then(() => {
                //console.log(`[som] "${chave}" iniciou. duration=${audio.duration}s volume=${audio.volume} muted=${audio.muted}`);
            })
            .catch(erro => {
                console.error(`[som] falha ao tocar "${chave}" (${caminho}):`, erro.name, erro.message);
            });
    }

    // Dá coordenadas (linha/coluna) a cada botão do tabuleiro e liga o clique
    linhas.forEach((linhaEl, i) => {
        const botoes = linhaEl.querySelectorAll('button');
        botoes.forEach((btn, j) => {
            btn.dataset.linha = i;
            btn.dataset.coluna = j;
            btn.addEventListener('click', onClickCasa);
        });
    });

    btnPrincipal.addEventListener('click', onClickPrincipal);

    // ---------- helpers de exibição ----------

    function formatarMoeda(valor) {
        return Number(valor).toFixed(2).replace('.', ',');
    }

    function atualizarSaldo(valor) {
        spansSaldo.forEach(span => { span.textContent = formatarMoeda(valor); });
    }

    function atualizarMultiplicador(valor) {
        spanMultiplicador.textContent = Number(valor).toFixed(2).replace('.', ',');
    }

    // ganho atual = aposta * multiplicador (o quanto o jogador levaria se sacasse agora)
    function calcularGanhoAtual(multiplicador) {
        const apostaAtual = parseFloat(inputAposta.value) || 0;
        return apostaAtual * Number(multiplicador);
    }

    function resetarTabuleiro() {
        linhas.forEach(linhaEl => {
            linhaEl.querySelectorAll('button').forEach(btn => {
                const span = btn.querySelector('span');
                span.textContent = '🪨';
                span.classList.remove('bomba', 'gema');
                btn.classList.remove('aberta');
                btn.disabled = false;
            });
        });
    }

    function travarTabuleiro() {
        linhas.forEach(linhaEl => {
            linhaEl.querySelectorAll('button').forEach(btn => { btn.disabled = true; });
        });
    }

    // reabilita apenas as casas que ainda não foram abertas
    function destravarAbertas() {
        linhas.forEach(linhaEl => {
            linhaEl.querySelectorAll('button').forEach(btn => {
                if (!btn.classList.contains('aberta')) btn.disabled = false;
            });
        });
    }

    function definirEstadoBotaoPrincipal(estado) {
        if (estado === 'sacar') {
            btnPrincipal.textContent = 'SACAR';
            btnPrincipal.style.background = "#d83b3b"; // vermelho
        } else {
            btnPrincipal.textContent = 'COMEÇAR';
            btnPrincipal.style.background = "linear-gradient(90deg,#FFD700,#9be015)";
        }
    }

    // Estados possíveis do mascote, cada um ligado a um data-attr do próprio <img>:
    //   neutro  -> antes de começar / após reset
    //   procura -> jogo ativo, ainda sem casas abertas (multiplicador <= 1)
    //   ganho   -> pelo menos uma gema aberta (multiplicador > 1)
    //   perda   -> pisou numa bomba
    function definirEstadoMascote(estado) {
        if (!mascoteImg) return;
        const chave = 'img' + estado.charAt(0).toUpperCase() + estado.slice(1); // ex: 'imgGanho'
        const src = mascoteImg.dataset[chave];
        if (src) mascoteImg.src = src;
    }

    function atualizarMascote(multiplicador) {
        const m = Number(multiplicador);
        if (m > 1) {
            definirEstadoMascote('ganho');
        } else if (jogoAtivo) {
            definirEstadoMascote('procura');
        } else {
            definirEstadoMascote('neutro');
        }
    }

    function finalizarRodada() {
        inputAposta.disabled = false;
        inputBombas.disabled = false;
        definirEstadoBotaoPrincipal('iniciar');

        if (timerFinalizacao) clearTimeout(timerFinalizacao);
        timerFinalizacao = setTimeout(() => {
            resetarTabuleiro();
            definirEstadoMascote('neutro');
            timerFinalizacao = null;
        }, 2000);
    }

    // ---------- ações ----------

    async function onClickPrincipal() {
        if (processando) return;
        if (!jogoAtivo) {
            await iniciarJogo();
        } else {
            await sacar();
        }
    }

    async function iniciarJogo() {
        const aposta = parseFloat(inputAposta.value);
        const bombas = parseInt(inputBombas.value, 10);

        if (isNaN(aposta) || aposta < 0.40) {
            //erro
            return;
        }
        if (isNaN(bombas) || bombas < 25 || bombas > 35) {
            //erro
            return;
        }

        // Cancela qualquer reset/troca de mascote que ainda estivesse
        // agendado da rodada anterior, senão ele dispara em cima da rodada nova.
        if (timerFinalizacao) {
            clearTimeout(timerFinalizacao);
            timerFinalizacao = null;
        }

        processando = true;
        btnPrincipal.disabled = true;

        try {
            const resp = await fetch('/mines/iniciar', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ aposta, bombas })
            });
            const dados = await resp.json();

            if (!resp.ok) {
                //erro
                return;
            }

            jogoAtivo = true;
            resetarTabuleiro();
            atualizarSaldo(dados.saldo);
            atualizarMultiplicador(dados.multiplicador ?? 0);
            atualizarMascote(dados.multiplicador ?? 0);
            inputAposta.disabled = true;
            inputBombas.disabled = true;
            definirEstadoBotaoPrincipal('sacar');
            //erro
        } catch (e) {
            //erro
        } finally {
            processando = false;
            btnPrincipal.disabled = false;
        }
    }

    async function onClickCasa(evento) {
        if (!jogoAtivo || processando) return;

        const btn = evento.currentTarget;
        if (btn.classList.contains('aberta')) return;

        const linha = parseInt(btn.dataset.linha, 10);
        const coluna = parseInt(btn.dataset.coluna, 10);

        processando = true;
        travarTabuleiro();
        btnPrincipal.disabled = true;

        try {
            const resp = await fetch('/mines/abrir', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ linha, coluna })
            });
            const dados = await resp.json();

            if (!resp.ok) {
                //erro
                destravarAbertas();
                return;
            }

            if (dados.resultado === 'bomba') {
                const span = btn.querySelector('span');
                span.textContent = '💣';
                span.classList.add('bomba');
                btn.classList.add('aberta');

                if (Array.isArray(dados.bombas)) {
                    dados.bombas.forEach(([li, co]) => {
                        const alvo = linhas[li].querySelectorAll('button')[co];
                        const alvoSpan = alvo.querySelector('span');
                        alvoSpan.textContent = '💣';
                        alvoSpan.classList.add('bomba');
                        alvo.classList.add('aberta');
                    });
                }

                jogoAtivo = false;
                atualizarSaldo(dados.saldo);
                atualizarMultiplicador(0);
                definirEstadoMascote('perda');
                tocarSom('bomba');
                const apostaPerdida = parseFloat(inputAposta.value) || 0;
                //erro
                finalizarRodada();
            } else {
                const span = btn.querySelector('span');
                span.textContent = '💎';
                span.classList.add('gema');
                btn.classList.add('aberta');
                atualizarMultiplicador(dados.multiplicador);
                atualizarMascote(dados.multiplicador);
                tocarSom('gema');
                const ganhoAtual = calcularGanhoAtual(dados.multiplicador);
                destravarAbertas();
            }
        } catch (e) {
            //erro!
            destravarAbertas();
        } finally {
            processando = false;
            btnPrincipal.disabled = false;
        }
    }

    async function sacar() {
        processando = true;
        btnPrincipal.disabled = true;
        travarTabuleiro();

        try {
            const resp = await fetch('/mines/sacar', { method: 'POST' });
            const dados = await resp.json();

            if (!resp.ok) {
                //erro!
                return;
            }

            atualizarSaldo(dados.saldo);
            jogoAtivo = false;

            if (dados.ganho > 1) {
                tocarSom('premio');
            }
            finalizarRodada();
        } catch (e) {
            //erro!
        } finally {
            processando = false;
            btnPrincipal.disabled = false;
        }
    }
});
