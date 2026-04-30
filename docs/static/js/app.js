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
        if (url.startsWith('/api/')) {
            return fazerRequisicaoLocal(url, opcoes);
        }

        console.error('Erro na requisição:', erro);
        mostrarStatus(`❌ Erro: ${erro.message}`, 'error');
        throw erro;
    }
}

function obterColecaoLocal(nome) {
    return JSON.parse(localStorage.getItem(nome) || '[]');
}

function salvarColecaoLocal(nome, dados) {
    localStorage.setItem(nome, JSON.stringify(dados));
}

function proximoIdLocal(dados) {
    return dados.length ? Math.max(...dados.map(item => Number(item.id) || 0)) + 1 : 1;
}

async function fazerRequisicaoLocal(url, opcoes = {}) {
    const metodo = (opcoes.method || 'GET').toUpperCase();
    const corpo = opcoes.body ? JSON.parse(opcoes.body) : {};

    if (url === '/api/contatos' && metodo === 'GET') {
        return obterColecaoLocal('segura_contatos');
    }

    if (url === '/api/contatos' && metodo === 'POST') {
        const contatos = obterColecaoLocal('segura_contatos');
        const contato = {
            id: proximoIdLocal(contatos),
            nome: corpo.nome,
            telefone: (corpo.telefone || '').replace(/\D/g, ''),
            relacao: corpo.relacao || 'Contato'
        };
        contatos.push(contato);
        salvarColecaoLocal('segura_contatos', contatos);
        return contato;
    }

    if (url.startsWith('/api/contatos/') && metodo === 'DELETE') {
        const id = Number(url.split('/').pop());
        const contatos = obterColecaoLocal('segura_contatos').filter(item => item.id !== id);
        salvarColecaoLocal('segura_contatos', contatos);
        return { mensagem: 'Contato deletado' };
    }

    if (url === '/api/locais' && metodo === 'GET') {
        return obterColecaoLocal('segura_locais');
    }

    if (url === '/api/locais' && metodo === 'POST') {
        const locais = obterColecaoLocal('segura_locais');
        const local = {
            id: proximoIdLocal(locais),
            nome: corpo.nome,
            tipo: corpo.tipo || 'Outro',
            endereco: corpo.endereco || null,
            latitude: corpo.latitude || null,
            longitude: corpo.longitude || null
        };
        locais.push(local);
        salvarColecaoLocal('segura_locais', locais);
        return local;
    }

    if (url.startsWith('/api/locais/') && metodo === 'DELETE') {
        const id = Number(url.split('/').pop());
        const locais = obterColecaoLocal('segura_locais').filter(item => item.id !== id);
        salvarColecaoLocal('segura_locais', locais);
        return { mensagem: 'Local deletado' };
    }

    if (url === '/api/localizacao' && metodo === 'POST') {
        localStorage.setItem('segura_ultima_localizacao', JSON.stringify({
            ...corpo,
            timestamp: new Date().toISOString()
        }));
        return {
            sucesso: true,
            mensagem: `Localizacao recebida: ${corpo.latitude}, ${corpo.longitude}`
        };
    }

    throw new Error(`Rota indisponivel no GitHub Pages: ${url}`);
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
