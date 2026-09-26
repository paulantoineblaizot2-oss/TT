const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const { exec } = require('child_process');

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});

// Middleware
app.use(express.static('public'));

// Route de base
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/public/index.html');
});

// Gestion des connexions Socket.IO
io.on('connection', (socket) => {
  console.log('Un client s\'est connecté');

  // Réception du mot de passe
  socket.on('auth', (password) => {
    if (password === process.env.PASSWORD) {
      socket.emit('auth-success');
      
      // Envoi des commandes shell au client
      socket.on('command', (cmd) => {
        exec(cmd, (error, stdout, stderr) => {
          if (error) {
            socket.emit('output', { error: error.message });
            return;
          }
          if (stderr) {
            socket.emit('output', { error: stderr });
            return;
          }
          socket.emit('output', { data: stdout });
        });
      });

    } else {
      socket.emit('auth-fail');
    }
  });

  // Fermeture de la connexion
  socket.on('disconnect', () => {
    console.log('Un client s\'est déconnecté');
  });
});

const PORT = process.env.PORT || 5001;
server.listen(PORT, () => {
  console.log(`Serveur démarré sur le port ${PORT}`);
});
