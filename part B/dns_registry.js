const express = require('express');
const app = express();
const port = 3002; // Utiliser un port différent pour le registre DNS

app.get('/getServer', (req, res) => {
  res.json({code: 200, server: "localhost:3000"});
});

app.listen(port, () => {
  console.log(`DNS Registry running at http://localhost:${port}`);
});
