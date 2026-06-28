function falar(texto) {
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel(); // Para leituras anteriores
        const msg = new SpeechSynthesisUtterance(texto);
        msg.lang = 'pt-BR';
        msg.rate = 1.1; 
        window.speechSynthesis.speak(msg);
    }
}

// Execução inteligente baseada em elementos ocultos na página
document.addEventListener("DOMContentLoaded", () => {
    const speechElement = document.getElementById("speech-payload");
    if (speechElement) {
        falar(speechElement.textContent);
    }
});