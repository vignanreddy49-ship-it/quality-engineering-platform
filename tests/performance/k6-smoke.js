import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 5,
  duration: '10s',
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<500'],
  },
};

export default function () {
  const base = __ENV.BASE_URL || 'http://localhost:8000';
  const response = http.get(`${base}/api/products`);
  check(response, {
    'catalog returns 200': (r) => r.status === 200,
    'catalog is JSON': (r) => r.headers['Content-Type']?.includes('application/json'),
  });
  sleep(1);
}
