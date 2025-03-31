// Fonction pour valider le formulaire côté client
function validateForm() {
    let isValid = true;

    // Réinitialiser les erreurs
    document.querySelectorAll('.error-input').forEach(input => input.classList.remove('error-input'));
    document.querySelectorAll('.error-message').forEach(message => message.remove());

    // Valider le nominal
    const nominalInput = document.querySelector('#id_nominal');
    if (nominalInput.value <= 0) {
        isValid = false;
        nominalInput.classList.add('error-input');
        const errorMessage = document.createElement('div');
        errorMessage.className = 'error-message';
        errorMessage.textContent = 'Le nominal doit être positif.';
        nominalInput.parentNode.appendChild(errorMessage);
    }

    // Valider le taux facial
    const tauxFacialInput = document.querySelector('#id_taux_facial');
    if (tauxFacialInput.value <= 0) {
        isValid = false;
        tauxFacialInput.classList.add('error-input');
        const errorMessage = document.createElement('div');
        errorMessage.className = 'error-message';
        errorMessage.textContent = 'Le taux facial doit être positif.';
        tauxFacialInput.parentNode.appendChild(errorMessage);
    }

    // Valider la maturité
    const maturiteInput = document.querySelector('#id_maturite');
    if (maturiteInput.value <= 0) {
        isValid = false;
        maturiteInput.classList.add('error-input');
        const errorMessage = document.createElement('div');
        errorMessage.className = 'error-message';
        errorMessage.textContent = 'La maturité doit être positive.';
        maturiteInput.parentNode.appendChild(errorMessage);
    }

    // Valider le prix pondéré
    const prixPondereInput = document.querySelector('#id_prix_pondere');
    if (prixPondereInput.value <= 0) {
        isValid = false;
        prixPondereInput.classList.add('error-input');
        const errorMessage = document.createElement('div');
        errorMessage.className = 'error-message';
        errorMessage.textContent = 'Le prix pondéré doit être positif.';
        prixPondereInput.parentNode.appendChild(errorMessage);
    }

    return isValid;
}

// Ajouter un écouteur d'événement pour la soumission du formulaire
document.getElementById('amortissementForm').addEventListener('submit', function(event) {
    if (!validateForm()) {
        event.preventDefault(); // Empêcher la soumission du formulaire
    }
});

// Fonction pour réinitialiser le formulaire et les résultats
function resetForm() {
    document.querySelector('form').reset(); // Réinitialiser le formulaire
    window.location.href = "{% url 'non_differe' %}"; // Recharger la page
}