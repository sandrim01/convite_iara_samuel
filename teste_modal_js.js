// Teste simples para verificar se a função JavaScript está carregando
console.log('Script de teste carregado');

// Teste da função do modal
function testarModal() {
    console.log('Testando função do modal...');
    
    // Verificar se o elemento existe
    const modal = document.getElementById('modalAdicionarPresente');
    if (modal) {
        console.log('Modal encontrado!');
        modal.style.display = 'flex';
    } else {
        console.error('Modal NÃO encontrado!');
    }
}

// Testar quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM carregado');
    
    // Adicionar evento de teste ao botão
    const botao = document.querySelector('button[onclick="abrirModalAdicionarPresente()"]');
    if (botao) {
        console.log('Botão encontrado!');
        botao.addEventListener('click', function(e) {
            console.log('Botão clicado!');
        });
    } else {
        console.error('Botão NÃO encontrado!');
    }
});
