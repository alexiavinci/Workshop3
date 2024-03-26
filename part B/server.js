const express = require('express');
const app = express();
const fs = require('fs');
app.use(express.json());
app.use(express.static('public'));

// Import products data from json file
let products = JSON.parse(fs.readFileSync('products.json', 'utf8'));
let orders = [];
let carts = {};

// Products routes
app.get('/products', (req, res) => {
  res.json(products);
});

app.get('/products/:id', (req, res) => {
  const product = products.find(p => p.id === parseInt(req.params.id));
  if (!product) return res.status(404).send('Product not found');
  res.json(product);
});

app.post('/products', (req, res) => {
  const { name, description, price, category, stock } = req.body;
  const product = { id: products.length + 1, name, description, price, category, stock };
  products.push(product);
  res.status(201).send(product);
});

app.put('/products/:id', (req, res) => {
  const product = products.find(p => p.id === parseInt(req.params.id));
  if (!product) return res.status(404).send('Product not found');

  const { name, description, price, category, stock } = req.body;
  product.name = name ?? product.name;
  product.description = description ?? product.description;
  product.price = price ?? product.price;
  product.category = category ?? product.category;
  product.stock = stock ?? product.stock;

  res.json(product);
});

app.delete('/products/:id', (req, res) => {
  const index = products.findIndex(p => p.id === parseInt(req.params.id));
  if (index === -1) return res.status(404).send('Product not found');

  products = products.filter(p => p.id !== parseInt(req.params.id));
  res.send('Product deleted');
});

// Orders routes
app.post('/orders', (req, res) => {
  const { productIds } = req.body; // Assume a simple array of product IDs for simplicity
  const newOrder = {
    id: orders.length + 1,
    products: productIds.map(id => products.find(p => p.id === id)),
    status: 'Received'
  };
  orders.push(newOrder);
  res.status(201).send(newOrder);
});

// Cart routes
app.post('/cart/:userId', (req, res) => {
  const { userId } = req.params;
  const { productId, quantity } = req.body;

  if (!carts[userId]) carts[userId] = [];
  carts[userId].push({ productId, quantity });

  res.status(201).send(carts[userId]);
});

app.get('/cart/:userId', (req, res) => {
  const { userId } = req.params;
  res.json(carts[userId] || []);
});

app.delete('/cart/:userId/item/:productId', (req, res) => {
  const { userId, productId } = req.params;
  if (!carts[userId]) return res.status(404).send('Cart not found');

  carts[userId] = carts[userId].filter(item => item.productId !== parseInt(productId));
  res.send(carts[userId]);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
