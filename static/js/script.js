// Sistema di Registrazione - JavaScript principale

// Funzione per chiudere automaticamente gli alert dopo 5 secondi
document.addEventListener('DOMContentLoaded', function() {
    // Selezioniamo tutti gli elementi con classe alert
    const alerts = document.querySelectorAll('.alert');
    
    // Per ogni alert, impostiamo un timer che lo farà scomparire dopo 5 secondi
    alerts.forEach(function(alert) {
        setTimeout(function() {
            // Utilizziamo l'oggetto bootstrap per far scomparire l'alert
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Inizializza i tooltip di Bootstrap (opzionale)
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});