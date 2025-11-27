# Исправление Service Worker

## Проблема
Service Worker пытался кэшировать все запросы, включая POST/PUT/DELETE к API, что вызывало:
1. CORS ошибки при редиректах
2. Попытки кэшировать запросы с методами, отличными от GET
3. Ошибку "Failed to execute 'put' on 'Cache': Request method 'POST' is unsupported"

## Исправление

Обновлен `frontend/public/sw.js`:

```javascript
// Не кэшируем API запросы и не-GET запросы
if (event.request.url.includes('/api/') || event.request.method !== 'GET') {
  event.respondWith(fetch(event.request));
  return;
}
```

## Что изменилось

1. ✅ API запросы (`/api/*`) больше не кэшируются
2. ✅ POST, PUT, DELETE запросы проходят напрямую без кэширования
3. ✅ Только GET запросы к статическим ресурсам кэшируются
4. ✅ Убраны CORS ошибки

## Как очистить старый кэш

В браузере:
1. Откройте DevTools (F12)
2. Перейдите в Application → Service Workers
3. Нажмите "Unregister" для старого Service Worker
4. Перейдите в Application → Cache Storage
5. Удалите все кэши
6. Обновите страницу (Ctrl+Shift+R)

Или просто откройте в режиме инкогнито для тестирования.

## Проверьте

1. Создание задач - должно работать без CORS ошибок
2. Создание заметок - должно работать
3. Создание маршрутов - должно работать
4. Создание отпусков - должно работать
5. Все POST/PUT/DELETE запросы должны работать корректно

Frontend перезапущен с исправленным Service Worker.
