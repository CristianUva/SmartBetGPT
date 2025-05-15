
document.addEventListener('DOMContentLoaded', function() {
  const form = document.querySelector('form');
  
  form.addEventListener('submit', function(event) {
    const termsCheckbox = document.getElementById('terms');
    const ageCheckbox = document.getElementById('age');
    
    // Verifica se entrambi i checkbox sono spuntati
    if (!termsCheckbox.checked || !ageCheckbox.checked) {
      event.preventDefault(); // Blocca l'invio del modulo
      
      // Mostra un messaggio di errore
      let errorMessage = 'Per procedere alla registrazione, devi:';
      if (!termsCheckbox.checked) {
        errorMessage += '\n- Accettare i Termini e Condizioni';
        // Aggiungi classe di errore visuale
        termsCheckbox.parentElement.classList.add('checkbox-error');
      }
      if (!ageCheckbox.checked) {
        errorMessage += '\n- Confermare di avere almeno 18 anni';
        // Aggiungi classe di errore visuale
        ageCheckbox.parentElement.classList.add('checkbox-error');
      }
      
      alert(errorMessage);
    }
  });
  
  // Rimuovi lo stile di errore quando l'utente seleziona il checkbox
  document.getElementById('terms').addEventListener('change', function() {
    if (this.checked) {
      this.parentElement.classList.remove('checkbox-error');
    }
  });
  
  document.getElementById('age').addEventListener('change', function() {
    if (this.checked) {
      this.parentElement.classList.remove('checkbox-error');
    }
  });
});
