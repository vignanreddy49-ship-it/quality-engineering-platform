import { test, expect } from '@playwright/test';

test('ShopSphere health endpoint is available', async ({ request }) => {
  const response = await request.get('/health');
  expect(response.ok()).toBeTruthy();
  await expect(response.json()).resolves.toMatchObject({ status: 'UP' });
});

test('ShopSphere product API exposes a usable catalog', async ({ request }) => {
  const response = await request.get('/api/products');
  expect(response.status()).toBe(200);
  const products = await response.json();
  expect(products.length).toBeGreaterThanOrEqual(3);
  expect(products[0]).toEqual(expect.objectContaining({
    id: expect.any(String),
    name: expect.any(String),
    price: expect.any(Number),
    stock: expect.any(Number),
  }));
});
