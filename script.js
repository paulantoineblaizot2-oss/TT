// Gestion de la connexion
document.addEventListener('DOMContentLoaded', function() {
    const connectBtn = document.getElementById('connectBtn');
    const settingsBtn = document.getElementById('settingsBtn');
    
    // Simulation de connexion au PC distant
    connectBtn.addEventListener('click', function() {
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const host = document.getElementById('host').value;
        
        if (!username || !password || !host) {
            alert("Veuillez remplir tous les champs !");
            return;
        }
        
        // Simuler le processus de connexion
        connectBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Connexion en cours...';
        connectBtn.disabled = true;
        
        setTimeout(function() {
            document.getElementById('status').className = 'connection-status connected';
            document.querySelector('.status-text').innerHTML = '<i class="fas fa-check-circle"></i> Connecté au PC distant';
            
            // Réinitialiser le bouton
            connectBtn.innerHTML = '<i class="fas fa-plug"></i> Se connecter au PC';
            connectBtn.disabled = false;
            
            alert("Connexion réussie ! Vous êtes maintenant connecté à votre PC distant.");
        }, 2000);
    });
    
    // Sauvegarder les paramètres de sécurité
    settingsBtn.addEventListener('click', function() {
        const encryption = document.getElementById('encryption').value;
        const timeout = document.getElementById('timeout').value;
        
        alert(`Paramètres sauvegardés :\nChiffrement: ${encryption}\nDélai d'attente: ${timeout} minutes`);
    });
    
    // Simulation du chargement de la page
    console.log("Interface d'accès à distance chargée avec succès");
    console.log("Pour l'hébergement sur Render, vous pouvez maintenant déployer ces fichiers.");
});

// Fonctions supplémentaires pour le rendement
window.addEventListener('load', function() {
    // Animation au chargement
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 300 * (index + 1));
    });
});

// Gestion des erreurs
window.addEventListener('error', function(e) {
    console.error("Erreur sur la page :", e.error);
});
