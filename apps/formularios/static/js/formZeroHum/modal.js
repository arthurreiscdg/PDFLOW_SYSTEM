document.addEventListener('DOMContentLoaded', function () {
    // Elementos do modal
    const statusModal = document.getElementById('statusModal');
    const closeModal = document.getElementById('closeModal');
    const modalContent = document.getElementById('modalContent');
    const modalActionButton = document.getElementById('modalActionButton');

    // Elemento do formulário
    const form = document.getElementById('formZeroHum'); // <-- Substitua pelo ID do seu formulário

    // Funções do Modal
    function showModal() {
        statusModal.classList.add('active');
    }

    function hideModal() {
        statusModal.classList.remove('active');
    }

    function showProcessingStatus() {
        modalContent.innerHTML = `
            <div class="status-icon status-processing">
                <div class="spinner"></div>
            </div>
            <div class="status-message">
                <h4 class="status-title">Processando seu pedido</h4>
                <p class="status-description">Estamos enviando suas informações. Por favor, aguarde...</p>
            </div>
        `;
        modalActionButton.style.display = 'none';
        showModal();
    }

    function showSuccessStatus(arquivos = []) {
        let listaArquivos = '';
        if (arquivos.length > 0) {
            listaArquivos = `
                <div class="status-files">
                    <p><strong>Arquivos enviados:</strong></p>
                    <ul>
                        ${arquivos.map(nome => `<li>${nome}</li>`).join('')}
                    </ul>
                </div>
            `;
        }
    
        modalContent.innerHTML = `
            <div class="status-icon status-success">
                <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
            </div>
            <div class="status-message">
                <h4 class="status-title">Pedido Enviado com Sucesso!</h4>
                <p class="status-description">Seu pedido foi recebido e será processado em breve.</p>
                ${listaArquivos}
            </div>
        `;
        modalActionButton.style.display = 'block';
        modalActionButton.textContent = 'Fechar';
        showModal();
    }
    

    function showErrorStatus() {
        modalContent.innerHTML = `
            <div class="status-icon status-error">
                <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="8" x2="12" y2="12"></line>
                    <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
            </div>
            <div class="status-message">
                <h4 class="status-title">Erro ao Enviar Pedido</h4>
                <p class="status-description">Ocorreu um problema ao processar seu pedido. Por favor, tente novamente ou entre em contato conosco.</p>
            </div>
        `;
        modalActionButton.style.display = 'block';
        modalActionButton.textContent = 'Tentar Novamente';
        showModal();
    }

    // Enviar formulário via fetch
    if (form) {
        form.addEventListener('submit', async function (event) {
            event.preventDefault(); // Impede o comportamento padrão

            showProcessingStatus(); // Mostra carregamento

            const formData = new FormData(form);

            try {
                const response = await fetch(form.action, {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    const data = await response.json();
                    if (data.message) {
                        showSuccessStatus(data.arquivos || []);
                        form.reset(); // Limpa o formulário
                    } else {
                        showErrorStatus();
                    }
                }
                
            } catch (error) {
                console.error('Erro ao enviar formulário:', error);
                showErrorStatus();
            }
        });
    }

    // Botões para fechar o modal
    closeModal.addEventListener('click', hideModal);
    modalActionButton.addEventListener('click', hideModal);
});
