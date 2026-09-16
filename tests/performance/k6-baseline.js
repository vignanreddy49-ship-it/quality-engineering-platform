import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 5,
  duration: '30s',
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';

export default function () {
  const health = http.get(`${BASE_URL}/health`);
  check(health, { 'health is 200': (r) => r.status === 200 });

  const products = http.get(`${BASE_URL}/api/products`);
  check(products, {
    'products is 200': (r) => r.status === 200,
    'products has data': (r) => Array.isArray(r.json()) && r.json().length > 0,
  });

  sleep(1);
}
