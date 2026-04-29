/**
 * Gerenciamento de contatos de emergência.
 * CRUD para adicionar, listar e remover contatos.
 */

document.addEventListener('DOMContentLoaded', () => {
    carregarContatos();

    const btnAdicionar = document.getElementById('adicionarContato');
    if (btnAdicionar) {
        btnAdicionar.addEventListener('click', adicionarContato);
    }
});

/**
 * Carrega e exibe todos os contatos
 */
async function carregarContatos() {
    try {
        const contatos = await fazerRequisicao('/api/contatos');
        const lista = document.getElementById('listaContatos');

        if (!lista) return;

        lista.innerHTML = '';

        if (contatos.length === 0) {
            lista.innerHTML = '<p class="text-center text-gray-500 py-6">Nenhum contato cadastrado</p>';
            return;
        }

        contatos.forEach(contato => {
            const card = document.createElement('div');
            card.className = 'card-item';
            card.innerHTML = `
                <div class="card-item-info flex-1">
                    <h3>${contato.nome}</h3>
                    <p>${contato.telefone}</p>
                    <p class="text-xs text-gray-500">${contato.relacao || 'Contato'}</p>
                </div>
                <button 
                    class="btn-delete" 
                    onclick="deletarContato(${contato.id})"
                    title="Deletar"
                >
                    ✕
                </button>
            `;
            lista.appendChild(card);
        });

    } catch (erro) {
        console.error('Erro ao carregar contatos:', erro);
    }
}

/**
 * Adiciona novo contato
 */
async function adicionarContato() {
    const nomeInput = document.getElementById('nomeContato');
    const telefoneInput = document.getElementById('telefoneContato');
    const relacaoInput = document.getElementById('relacaoContato');

    // Validação
    if (!nomeInput.value.trim()) {
        mostrarStatus('❌ Digite o nome', 'error');
        nomeInput.focus();
        return;
    }

    if (!telefoneInput.value.trim()) {
        mostrarStatus('❌ Digite o telefone', 'error');
        telefoneInput.focus();
        return;
    }

    try {
        mostrarStatus('⏳ Salvando contato...', 'info');

        const novoContato = {
            nome: nomeInput.value.trim(),
            telefone: telefoneInput.value.trim(),
            relacao: relacaoInput.value.trim() || 'Contato'
        };

        await fazerRequisicao('/api/contatos', {
            method: 'POST',
            body: JSON.stringify(novoContato)
        });

        // Limpa inputs
        nomeInput.value = '';
        telefoneInput.value = '';
        relacaoInput.value = '';

        // Recarrega lista
        await carregarContatos();
        mostrarStatus('✅ Contato adicionado com sucesso!', 'sucesso');

    } catch (erro) {
        console.error('Erro:', erro);
        mostrarStatus('❌ Erro ao salvar contato', 'error');
    }
}

/**
 * Deleta um contato
 */
async function deletarContato(id) {
    if (!confirm('Tem certeza que deseja deletar este contato?')) {
        return;
    }

    try {
        mostrarStatus('⏳ Deletando...', 'info');

        await fazerRequisicao(`/api/contatos/${id}`, {
            method: 'DELETE'
        });

        await carregarContatos();
        mostrarStatus('✅ Contato deletado', 'sucesso');

    } catch (erro) {
        console.error('Erro:', erro);
        mostrarStatus('❌ Erro ao deletar', 'error');
    }
}
