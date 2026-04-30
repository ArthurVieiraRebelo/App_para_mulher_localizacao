/**
 * Gerenciamento de locais seguros.
 * CRUD para adicionar, listar e remover locais seguros.
 */

document.addEventListener('DOMContentLoaded', () => {
    carregarLocais();

    const btnAdicionar = document.getElementById('adicionarLocal');
    if (btnAdicionar) {
        btnAdicionar.addEventListener('click', adicionarLocal);
    }
});

/**
 * Carrega e exibe todos os locais seguros
 */
async function carregarLocais() {
    try {
        const locais = await fazerRequisicao('/api/locais');
        const lista = document.getElementById('listaLocais');

        if (!lista) return;

        lista.innerHTML = '';

        if (locais.length === 0) {
            lista.innerHTML = '<p class="text-center text-gray-500 py-6">Nenhum local cadastrado</p>';
            return;
        }

        locais.forEach(local => {
            const iconeTipo = obterIconeTipo(local.tipo);
            const linkMapa = local.latitude && local.longitude
                ? `https://maps.google.com/?q=${local.latitude},${local.longitude}`
                : null;

            const card = document.createElement('div');
            card.className = 'card-item';
            card.innerHTML = `
                <div class="card-item-info flex-1">
                    <h3>${iconeTipo} ${local.nome}</h3>
                    <p class="text-xs text-gray-600">${local.tipo || 'Sem tipo'}</p>
                    ${local.endereco ? `<p class="text-xs text-gray-500">${local.endereco}</p>` : ''}
                </div>
                <div class="flex gap-2">
                    ${linkMapa ? `
                        <a 
                            href="${linkMapa}" 
                            target="_blank"
                            class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded text-sm"
                            title="Ver no mapa"
                        >
                            📍
                        </a>
                    ` : ''}
                    <button 
                        class="btn-delete" 
                        onclick="deletarLocal(${local.id})"
                        title="Deletar"
                    >
                        ✕
                    </button>
                </div>
            `;
            lista.appendChild(card);
        });

    } catch (erro) {
        console.error('Erro ao carregar locais:', erro);
    }
}

/**
 * Obtém ícone baseado no tipo de local
 */
function obterIconeTipo(tipo) {
    const icones = {
        'Delegacia': '🚔',
        'Hospital': '🏥',
        'Amigo': '👨‍🤝‍👩',
        'Família': '👨‍👩‍👧',
        'Outro': '📍'
    };

    return icones[tipo] || '📍';
}

/**
 * Adiciona novo local seguro
 */
async function adicionarLocal() {
    const nomeInput = document.getElementById('nomeLocal');
    const tipoSelect = document.getElementById('tipoLocal');
    const enderecoInput = document.getElementById('enderecoLocal');

    // Validação
    if (!nomeInput.value.trim()) {
        mostrarStatus('❌ Digite o nome do local', 'error');
        nomeInput.focus();
        return;
    }

    if (!tipoSelect.value) {
        mostrarStatus('❌ Selecione um tipo de local', 'error');
        tipoSelect.focus();
        return;
    }

    try {
        mostrarStatus('⏳ Salvando local...', 'info');

        let latitude = null;
        let longitude = null;

        // Tenta obter localização se o endereço foi fornecido
        if (enderecoInput.value.trim()) {
            try {
                // Aqui poderia usar uma API de geocoding, por enquanto skip
                console.log('Endereço fornecido:', enderecoInput.value);
            } catch (e) {
                console.warn('Não foi possível geocodificar:', e);
            }
        }

        const novoLocal = {
            nome: nomeInput.value.trim(),
            tipo: tipoSelect.value,
            endereco: enderecoInput.value.trim() || null,
            latitude: latitude,
            longitude: longitude
        };

        await fazerRequisicao('/api/locais', {
            method: 'POST',
            body: JSON.stringify(novoLocal)
        });

        // Limpa inputs
        nomeInput.value = '';
        tipoSelect.value = '';
        enderecoInput.value = '';

        // Recarrega lista
        await carregarLocais();
        mostrarStatus('✅ Local adicionado com sucesso!', 'sucesso');

    } catch (erro) {
        console.error('Erro:', erro);
        mostrarStatus('❌ Erro ao salvar local', 'error');
    }
}

/**
 * Deleta um local
 */
async function deletarLocal(id) {
    if (!confirm('Tem certeza que deseja deletar este local?')) {
        return;
    }

    try {
        mostrarStatus('⏳ Deletando...', 'info');

        await fazerRequisicao(`/api/locais/${id}`, {
            method: 'DELETE'
        });

        await carregarLocais();
        mostrarStatus('✅ Local deletado', 'sucesso');

    } catch (erro) {
        console.error('Erro:', erro);
        mostrarStatus('❌ Erro ao deletar', 'error');
    }
}
