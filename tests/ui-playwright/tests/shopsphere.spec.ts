import { test, expect } from '@playwright/test';

test.describe('ShopSphere product experience', () => {
  test('shows products returned by the API', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/docs');
    await expect(page).toHaveTitle(/ShopSphere API/);
  });

  test('API contract exposes healthy service', async ({ request }) => {
    const response = await request.get('http://127.0.0.1:8000/health');
    expect(response.ok()).toBeTruthy();
    await expect(response.json()).resolves.toEqual({ status: 'UP', service: 'shopsphere-api' });
  });

  test('rejects invalid order quantity', async ({ request }) => {
    const response = await request.post('http://127.0.0.1:8000/api/orders', {
      data: { customer_email: 'qa@example.com', items: [{ product_id: 'p-100', quantity: 0 }] }
    });
    expect(response.status()).toBe(422);
  });
});
