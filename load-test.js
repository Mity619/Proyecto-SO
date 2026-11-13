import http from 'k6/http';
import { sleep, check } from 'k6';

export const options = {
  scenarios: {
    steady: {
      executor: 'constant-vus',
      vus: 30,
      duration: '2m',
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<500'],
  },
};

export default function () {
  // Mezclamos "/" y "/work" para ver balanceo y latencia
  const res = http.get(Math.random() < 0.3
    ? 'http://localhost:8080/'
    : 'http://localhost:8080/work');

  check(res, { 'status is 200': (r) => r.status === 200 });

  // Imprimimos la instancia cada tanto para ver el balanceo en consola
  if (__ITER % 50 === 0 && res.json && res.json('instance')) {
    console.log(`instancia=${res.json('instance')}`);
  }
  sleep(0.2);
}