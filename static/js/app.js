/**
 * Script principal do app.
 * Gerencia navegação entre abas e funcionalidades gerais.
 */

document.addEventListener('DOMContentLoaded', () => {
    console.log('✅ App iniciado');

    // Sistema de abas
    const abaBtns = document.querySelectorAll('.aba-btn');
    const abaConteudos = document.querySelectorAll('.aba-conteudo');

    abaBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const nomeAba = btn.dataset.aba;

            // Remove active de todos
            abaBtns.forEach(b => b.classList.remove('active', 'border-purple-600', 'text-purple-600'));
            abaConteudos.forEach(c => c.classList.add('hidden'));

            // Ativa a selecionada
            btn.classList.add('active', 'border-purple-600', 'text-purple-600');
            btn.classList.remove('border-gray-300', 'text-gray-600');
            document.getElementById(`aba-${nomeAba}`).classList.remove('hidden');
        });
    });
});

/**
 * Função helper para fazer requisições à API
 */
async function fazerRequisicao(url, opcoes = {}) {
    try {
        const response = await fetch(url, {
            ...opcoes,
            headers: {
                'Content-Type': 'application/json',
                ...opcoes.headers
            }
        });

        if (!response.ok) {
            throw new Error(`Erro ${response.status}`);
        }

        return await response.json();
    } catch (erro) {
        console.error('Erro na requisição:', erro);
        mostrarStatus(`❌ Erro: ${erro.message}`, 'error');
        throw erro;
    }
}

/**
 * Mostra mensagem de status ao usuário
 */
function mostrarStatus(mensagem, tipo = 'sucesso') {
    const statusEl = document.getElementById('statusPanico');
    const statusTexto = document.getElementById('statusTexto');

    if (!statusEl) return;

    statusTexto.textContent = mensagem;
    statusEl.classList.remove('hidden', 'bg-red-100', 'text-red-700', 'bg-blue-100', 'text-blue-700', 'bg-green-100', 'text-green-700');

    if (tipo === 'error') {
        statusEl.classList.add('bg-red-100', 'text-red-700');
    } else if (tipo === 'info') {
        statusEl.classList.add('bg-blue-100', 'text-blue-700');
    } else {
        statusEl.classList.add('bg-green-100', 'text-green-700');
    }

    // Auto-hide após 5 segundos
    setTimeout(() => {
        statusEl.classList.add('hidden');
    }, 5000);
}

/**
 * Solicita permissão de geolocalização
 */
function obterLocalizacao() {
    return new Promise((resolve, reject) => {
        if (!navigator.geolocation) {
            reject(new Error('Geolocalização não suportada'));
            return;
        }

        navigator.geolocation.getCurrentPosition(
            (position) => {
                const { latitude, longitude } = position.coords;
                resolve({ latitude, longitude });
            },
            (erro) => {
                reject(new Error(`Erro de geolocalização: ${erro.message}`));
            }
        );
    });
}

/**
 * Formata número de telefone
 */
function formatarTelefone(telefone) {
    const numeros = telefone.replace(/\D/g, '');

    if (numeros.length === 11) {
        return `(${numeros.slice(0, 2)}) ${numeros.slice(2, 7)}-${numeros.slice(7)}`;
    }

    return telefone;
}
