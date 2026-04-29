/**
 * Service Worker para funcionalidade PWA.
 * Permite usar o app offline e instalação como app nativo.
 */

const CACHE_NAME = 'segura-v1';
const ASSETS_TO_CACHE = [
    '/',
    '/static/css/style.css',
    '/static/js/app.js',
    '/static/js/panico.js',
    '/static/js/contatos.js',
    '/static/js/locais.js'
];

// Instala o SW e cria cache
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('Service Worker: Cache criado');
            return cache.addAll(ASSETS_TO_CACHE);
        })
    );
    self.skipWaiting();
});

// Ativa o SW
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Service Worker: Removendo cache antigo:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

// Intercepta requisições (Cache First para assets, Network First para API)
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);

    // Para requisições à API, tenta rede primeiro
    if (url.pathname.startsWith('/api')) {
        event.respondWith(
            fetch(request)
                .then((response) => {
                    if (response.ok) {
                        return response;
                    }
                    throw new Error('Network error');
                })
                .catch(() => {
                    return new Response('Funcionalidade indisponível offline', { status: 503 });
                })
        );
        return;
    }

    // Para assets estáticos, usa cache primeiro
    event.respondWith(
        caches.match(request).then((cachedResponse) => {
            if (cachedResponse) {
                return cachedResponse;
            }

            return fetch(request).then((response) => {
                if (!response || response.status !== 200 || response.type === 'error') {
                    return response;
                }

                // Copia e armazena em cache
                const responseToCache = response.clone();
                caches.open(CACHE_NAME).then((cache) => {
                    cache.put(request, responseToCache);
                });

                return response;
            });
        })
    );
});
