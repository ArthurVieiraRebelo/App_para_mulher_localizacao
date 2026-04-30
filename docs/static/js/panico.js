/**
 * Lógica do botão de pânico.
 * Captura geolocalização e prepara mensagem para WhatsApp.
 */

document.addEventListener('DOMContentLoaded', () => {
    const botaoPanico = document.getElementById('botaoPanico');

    if (botaoPanico) {
        botaoPanico.addEventListener('click', acionarPanico);
    }
});

async function acionarPanico() {
    console.log('🆘 Botão de pânico acionado');

    try {
        // Obtém localização
        mostrarStatus('📍 Obtendo sua localização...', 'info');
        const { latitude, longitude } = await obterLocalizacao();

        console.log(`Localização obtida: ${latitude}, ${longitude}`);

        // Carrega contatos para seleção
        const contatos = await fazerRequisicao('/api/contatos');

        if (contatos.length === 0) {
            mostrarStatus('❌ Nenhum contato de emergência cadastrado', 'error');
            return;
        }

        // Se houver apenas um contato, envia direto
        if (contatos.length === 1) {
            await enviarMensagem(contatos[0], latitude, longitude);
        } else {
            // Se houver vários, mostra modal para seleção
            selecionarContatoParaEnvio(contatos, latitude, longitude);
        }

    } catch (erro) {
        console.error('Erro:', erro);
        mostrarStatus('❌ ' + erro.message, 'error');
    }
}

/**
 * Envia mensagem de pânico via WhatsApp
 */
async function enviarMensagem(contato, latitude, longitude) {
    try {
        // Cria link do Google Maps
        const linkMapa = `https://maps.google.com/?q=${latitude},${longitude}`;

        // Mensagem que será enviada
        const mensagem = `🆘 SITUAÇÃO DE EMERGÊNCIA!\n\nEstou em perigo e preciso de ajuda urgente.\n\n📍 Minha localização: ${linkMapa}\n\nPor favor, avise às autoridades ou venha me ajudar.`;

        // Formata número para WhatsApp (remove caracteres especiais)
        const numeroWhatsApp = contato.telefone.replace(/\D/g, '');

        // Cria link do WhatsApp
        const linkWhatsApp = `https://wa.me/${numeroWhatsApp}?text=${encodeURIComponent(mensagem)}`;

        console.log('📞 Redirecionando para WhatsApp...');

        // Abre WhatsApp (web ou app)
        window.location.href = linkWhatsApp;

        // Também salva localização no backend (futuro log)
        await fazerRequisicao('/api/localizacao', {
            method: 'POST',
            body: JSON.stringify({
                latitude,
                longitude,
                contato_id: contato.id,
                timestamp: new Date().toISOString()
            })
        });

        mostrarStatus(`✅ Enviando para ${contato.nome}...`, 'sucesso');

    } catch (erro) {
        console.error('Erro ao enviar:', erro);
        mostrarStatus('❌ Erro ao preparar mensagem', 'error');
    }
}

/**
 * Modal para seleção de contato (quando houver vários)
 */
function selecionarContatoParaEnvio(contatos, latitude, longitude) {
    // Cria modal simples com botões
    const html = `
        <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div class="bg-white rounded-lg p-6 max-w-sm w-full">
                <h3 class="text-lg font-bold mb-4 text-gray-800">Qual contato avisar?</h3>
                <div class="space-y-2 mb-4 max-h-60 overflow-y-auto">
                    ${contatos.map(c => `
                        <button 
                            class="w-full text-left p-3 rounded border-2 border-gray-200 hover:border-purple-600 transition"
                            onclick="enviarMensagem(${JSON.stringify(c).replace(/"/g, '&quot;')}, ${latitude}, ${longitude})"
                        >
                            <div class="font-semibold text-gray-800">${c.nome}</div>
                            <div class="text-sm text-gray-600">${c.telefone}</div>
                        </button>
                    `).join('')}
                </div>
                <button 
                    class="w-full py-2 bg-gray-300 text-gray-700 rounded font-semibold"
                    onclick="this.closest('.fixed').remove()"
                >
                    Cancelar
                </button>
            </div>
        </div>
    `;

    document.body.insertAdjacentHTML('beforeend', html);
}
