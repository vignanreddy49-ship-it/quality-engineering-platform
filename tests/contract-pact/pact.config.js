module.exports = {
  consumer: 'shopsphere-web',
  provider: 'shopsphere-api',
  contract: {
    request: { method: 'GET', path: '/api/products' },
    response: {
      status: 200,
      headers: { 'content-type': 'application/json' },
      body: [{ id: 'p-100', name: 'Wireless Headphones', price: 7999, stock: 25 }]
    }
  },
  note: 'Reference contract shape for the next Pact implementation milestone.'
};
