// Scripts principais para o convite romântico

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar componentes
    initFloatingHearts();
    initSmoothScrolling();
    initAnimations();
    initFormValidation();
    
    console.log('💕 Convite Iara & Samuel carregado com amor! 💕');
});

// Criar corações flutuantes
function initFloatingHearts() {
    const heartsContainer = document.createElement('div');
    heartsContainer.className = 'floating-hearts';
    document.body.appendChild(heartsContainer);
    
    setInterval(createHeart, 3000);
}

function createHeart() {
    const heart = document.createElement('div');
    heart.className = 'heart';
    heart.innerHTML = '💕';
    heart.style.left = Math.random() * 100 + '%';
    heart.style.animationDuration = (Math.random() * 3 + 2) + 's';
    heart.style.opacity = Math.random() * 0.5 + 0.3;
    
    const heartsContainer = document.querySelector('.floating-hearts');
    if (heartsContainer) {
        heartsContainer.appendChild(heart);
        
        // Remover coração após animação
        setTimeout(() => {
            if (heart.parentNode) {
                heart.parentNode.removeChild(heart);
            }
        }, 5000);
    }
}

// Scroll suave para âncoras
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Animações ao rolar a página
function initAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, observerOptions);
    
    // Observar elementos para animação
    document.querySelectorAll('.detail-card, .presente-card, .admin-card').forEach(el => {
        observer.observe(el);
    });
}

// Validação de formulários
function initFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

// Confirmação de presença
function confirmarPresenca(token) {
    const form = document.getElementById('confirmacao-form');
    if (!form) return;
    
    const formData = new FormData(form);
    const acompanhantes = formData.get('acompanhantes');
    const observacoes = formData.get('observacoes');
    
    if (acompanhantes < 0) {
        showAlert('Número de acompanhantes deve ser positivo.', 'error');
        return;
    }
    
    // Mostrar loading
    showLoading('Confirmando presença...');
    
    fetch(`/convite/${token}/confirmar`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        if (data.success) {
            showAlert('Presença confirmada com sucesso! 💕', 'success');
            setTimeout(() => {
                location.reload();
            }, 2000);
        } else {
            showAlert(data.message || 'Erro ao confirmar presença.', 'error');
        }
    })
    .catch(error => {
        hideLoading();
        showAlert('Erro ao confirmar presença. Tente novamente.', 'error');
        console.error('Erro:', error);
    });
}

// Escolher presente
function escolherPresente(token, presenteId) {
    if (!confirm('Deseja escolher este presente?')) {
        return;
    }
    
    showLoading('Escolhendo presente...');
    
    fetch(`/convite/${token}/escolher-presente/${presenteId}`, {
        method: 'POST'
    })
    .then(response => {
        hideLoading();
        if (response.ok) {
            showAlert('Presente escolhido com sucesso! 🎁', 'success');
            setTimeout(() => {
                location.reload();
            }, 1500);
        } else {
            showAlert('Erro ao escolher presente.', 'error');
        }
    })
    .catch(error => {
        hideLoading();
        showAlert('Erro ao escolher presente. Tente novamente.', 'error');
        console.error('Erro:', error);
    });
}

// Remover presente
function removerPresente(token, escolhaId) {
    if (!confirm('Deseja remover este presente da sua lista?')) {
        return;
    }
    
    showLoading('Removendo presente...');
    
    fetch(`/convite/${token}/remover-presente/${escolhaId}`, {
        method: 'POST'
    })
    .then(response => {
        hideLoading();
        if (response.ok) {
            showAlert('Presente removido da sua lista.', 'info');
            setTimeout(() => {
                location.reload();
            }, 1500);
        } else {
            showAlert('Erro ao remover presente.', 'error');
        }
    })
    .catch(error => {
        hideLoading();
        showAlert('Erro ao remover presente. Tente novamente.', 'error');
        console.error('Erro:', error);
    });
}

// Funções de UI
function showAlert(message, type = 'info') {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
    alertContainer.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertContainer.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertContainer);
    
    // Auto-remover após 5 segundos
    setTimeout(() => {
        if (alertContainer.parentNode) {
            alertContainer.parentNode.removeChild(alertContainer);
        }
    }, 5000);
}

function showLoading(message = 'Carregando...') {
    const loadingModal = document.createElement('div');
    loadingModal.id = 'loading-modal';
    loadingModal.className = 'modal fade show';
    loadingModal.style.display = 'block';
    loadingModal.innerHTML = `
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content border-0 bg-transparent text-center">
                <div class="modal-body">
                    <div class="romantic-spinner"></div>
                    <p class="mt-3 text-white">${message}</p>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(loadingModal);
}

function hideLoading() {
    const loadingModal = document.getElementById('loading-modal');
    if (loadingModal) {
        loadingModal.parentNode.removeChild(loadingModal);
    }
}

// Funções específicas para área administrativa
function deleteItem(id, type, name) {
    if (!confirm(`Deseja excluir ${type} "${name}"?`)) {
        return;
    }
    
    showLoading(`Excluindo ${type}...`);
    
    fetch(`/admin/${type}s/${id}/delete`, {
        method: 'POST'
    })
    .then(response => {
        hideLoading();
        if (response.ok) {
            showAlert(`${type} excluído com sucesso!`, 'success');
            setTimeout(() => {
                location.reload();
            }, 1500);
        } else {
            showAlert(`Erro ao excluir ${type}.`, 'error');
        }
    })
    .catch(error => {
        hideLoading();
        showAlert('Erro na operação. Tente novamente.', 'error');
        console.error('Erro:', error);
    });
}

// Máscaras para formulários
function applyMasks() {
    // Máscara para telefone
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/(\d{2})(\d)/, '($1) $2');
            value = value.replace(/(\d{5})(\d)/, '$1-$2');
            e.target.value = value;
        });
    });
    
    // Máscara para preço
    const priceInputs = document.querySelectorAll('input[data-mask="currency"]');
    priceInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = (value / 100).toFixed(2);
            value = value.replace('.', ',');
            value = value.replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1.');
            e.target.value = 'R$ ' + value;
        });
    });
}

// Inicializar máscaras quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', applyMasks);

// Preview de imagem
function previewImage(input, previewId) {
    const file = input.files[0];
    const preview = document.getElementById(previewId);
    
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    } else {
        preview.style.display = 'none';
    }
}

// Copiar link do convite
function copyInviteLink(token) {
    const link = `${window.location.origin}/convite/${token}`;
    navigator.clipboard.writeText(link).then(() => {
        showAlert('Link do convite copiado! 📋', 'success');
    }).catch(() => {
        // Fallback para browsers mais antigos
        const textarea = document.createElement('textarea');
        textarea.value = link;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showAlert('Link do convite copiado! 📋', 'success');
    });
}

// Funcionalidade de busca nas tabelas
function filterTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);
    
    if (!input || !table) return;
    
    input.addEventListener('keyup', function() {
        const filter = this.value.toLowerCase();
        const rows = table.getElementsByTagName('tr');
        
        for (let i = 1; i < rows.length; i++) { // Começar do 1 para pular o cabeçalho
            const row = rows[i];
            const cells = row.getElementsByTagName('td');
            let found = false;
            
            for (let j = 0; j < cells.length; j++) {
                const cell = cells[j];
                if (cell.textContent.toLowerCase().indexOf(filter) > -1) {
                    found = true;
                    break;
                }
            }
            
            row.style.display = found ? '' : 'none';
        }
    });
}
