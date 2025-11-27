# Звуковые файлы для уведомлений

## Текущий статус

В данный момент используются **сгенерированные звуки через Web Audio API**.

Для улучшения качества звуков, добавьте настоящие аудио файлы:

## Необходимые файлы

1. **telegram.mp3** - Звук уведомления Telegram
2. **icq.mp3** - Классический звук ICQ "Uh-oh!"
3. **whatsapp.mp3** - Звук уведомления WhatsApp
4. **default.mp3** - Стандартный звук уведомления

## Где скачать

### Telegram
- Извлечь из приложения Telegram Desktop
- Путь (Windows): `%APPDATA%\Telegram Desktop\tdata\user_data\sounds`
- Или найти онлайн: "telegram notification sound download"

### ICQ
- https://www.myinstants.com/en/instant/icq-uh-oh/
- Скачать и конвертировать в MP3

### WhatsApp
- Извлечь из приложения WhatsApp
- Путь (Android): `/data/data/com.whatsapp/files/Notifications/`
- Или найти онлайн: "whatsapp notification sound download"

### Default
- Любой короткий звук уведомления
- Рекомендуется длительность: 0.3-0.5 секунд
- Формат: MP3, битрейт: 128kbps

## Конвертация

Если звуки в другом формате, используйте FFmpeg:

```bash
# Конвертация в MP3
ffmpeg -i input.wav -codec:a libmp3lame -qscale:a 2 output.mp3

# Обрезка до 0.5 секунд
ffmpeg -i input.mp3 -t 0.5 -codec:a copy output.mp3

# Нормализация громкости
ffmpeg -i input.mp3 -af "volume=0.7" output.mp3
```

## Требования к файлам

- **Формат**: MP3
- **Длительность**: 0.2-0.5 секунд
- **Битрейт**: 128kbps
- **Размер**: < 50KB
- **Частота дискретизации**: 44100 Hz

## Альтернатива

Пока файлы не добавлены, система автоматически использует сгенерированные звуки через Web Audio API.

Характеристики сгенерированных звуков:
- **telegram**: 800 Hz, sine wave, 0.3s
- **icq**: 600 Hz, square wave, 0.2s  
- **whatsapp**: 1000 Hz, sine wave, 0.25s
- **default**: 700 Hz, sine wave, 0.4s
