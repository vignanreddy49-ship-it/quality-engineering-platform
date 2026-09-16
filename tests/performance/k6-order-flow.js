import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  scenarios: {
    order_flow: {
      executor: 'constant-vus',
      vus: 5,
      duration: '30s',
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.01'],
    'http_req_duration{endpoint:orders}': ['p(95)<750', 'p(99)<1200'],
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';

export default function () {
  const payload = JSON.stringify({
    customer_email: `load-${__VU}-${__ITER}@example.com`,
    items: [{ product_id: 'p-100', quantity: 1 }],
  });

  const response = http.post(`${BASE_URL}/api/orders`, payload, {
    headers: { 'Content-Type': 'application/json' },
    tags: { endpoint: 'orders' },
  });

  check(response, {
    'order creation returns 201': (r) => r.status === 201,
    'order response contains id': (r) => Boolean(r.json('id')),
    'order response is created': (r) => r.json('status') === 'CREATED',
  });

  sleep(0.5);
}
