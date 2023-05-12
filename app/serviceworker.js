// Base Service Worker implementation.  To use your own Service Worker, set the PWA_SERVICE_WORKER_PATH variable in settings.py

var staticCacheName = "django-pwa-v" + new Date().getTime();
var filesToCache = [
    '/offline/',
    '/static/svg/undraw_stars_re_6je7.svg',
    '/static/svg/undraw_page_not_found_re_e9o6.svg',
    '/static/svg/undraw_server_down_s-4-lk.svg',
    '/static/favicon_io/android-chrome-512x512.png',
    '/static/favicon_io/android-chrome-192x192.png',
    '/static/favicon_io/android-chrome-32x32.png',
    '/static/favicon_io/android-chrome-16x16.png',
    '/static/favicon_io/apple-touch-icon.png',
    '/static/favicon_io/favicon.ico',
    '/static/images/logo400x200.png',
];

// Cache on install
self.addEventListener("install", event => {
    this.skipWaiting();
    event.waitUntil(
        caches.open(staticCacheName)
            .then(cache => {
                return cache.addAll(filesToCache);
            })
    )
});

// Clear cache on activate
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(cacheName => (cacheName.startsWith("django-pwa-")))
                    .filter(cacheName => (cacheName !== staticCacheName))
                    .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});

// Serve from Cache
self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                return response || fetch(event.request);
            })
            .catch(() => {
                return caches.match('offline/');
            })
    )
});
