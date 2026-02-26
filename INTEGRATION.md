# Интеграция Frontend и Backend

## Обзор

Этот документ описывает, как интегрировать React фронтенд с вашим FastAPI бэкендом.

## Предварительные требования

1. **Node.js** версии 16 или выше
2. **Python** с установленными зависимостями из `pyproject.toml`
3. **Запущенный FastAPI сервер** на порту 8000

## Шаги по интеграции

### 1. Запуск Backend

Убедитесь, что ваш FastAPI сервер запущен:

```bash
# В корневой папке проекта
python main.py
# или
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Запуск Frontend

Перейдите в папку `frontend` и запустите React приложение:

```bash
cd frontend
npm install
npm start
```

Или используйте готовые скрипты:

**Windows:**
```bash
start.bat
```

**Unix/Linux/macOS:**
```bash
chmod +x start.sh
./start.sh
```

### 3. Проверка интеграции

1. Откройте браузер и перейдите на `http://localhost:3000`
2. Создайте новый чат
3. Отправьте сообщение
4. Проверьте, что данные сохраняются в вашем бэкенде

## API Endpoints

Фронтенд использует следующие эндпоинты:

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/chat/` | Создание нового чата |
| GET | `/chat/{chat_id}/` | Получение информации о чате |
| POST | `/chat/{chat_id}/messages` | Отправка сообщения |
| GET | `/chat/{chat_id}/messages` | Получение сообщений чата |

## CORS настройки

В вашем `main.py` уже добавлена поддержка CORS для `http://localhost:3000`. Если вы измените порт фронтенда, обновите настройки:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Измените на нужный порт
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Структура данных

### Chat
```typescript
interface ChatResponse {
  chat_id: string;
  title: string;
  created_ad: string; // ISO date string
}
```

### Message
```typescript
interface CreatedMessageResponse {
  chat_id: string;
  message_id: string;
  text: string;
  datetime: string; // ISO date string
}
```

## Возможные проблемы

### 1. CORS ошибки
- Убедитесь, что CORS middleware добавлен в FastAPI
- Проверьте, что `allow_origins` содержит правильный URL фронтенда

### 2. API недоступен
- Проверьте, что FastAPI сервер запущен на порту 8000
- Убедитесь, что нет конфликтов портов

### 3. Ошибки типов
- Проверьте, что TypeScript типы соответствуют вашим Pydantic схемам
- Обновите типы в `frontend/src/types/api.ts` при изменении API

## Разработка

### Добавление новых функций

1. **Backend**: Добавьте новые эндпоинты в FastAPI
2. **Frontend**: Обновите типы в `types/api.ts`
3. **Frontend**: Добавьте методы в `api/client.ts`
4. **Frontend**: Создайте новые компоненты в `components/`

### Тестирование

1. Запустите backend и frontend
2. Протестируйте все функции через UI
3. Проверьте консоль браузера на ошибки
4. Проверьте логи FastAPI сервера

## Продакшн

Для продакшн развертывания:

1. **Frontend**: `npm run build` создаст оптимизированную сборку
2. **Backend**: Настройте CORS для продакшн домена
3. **Deploy**: Разверните оба сервиса на вашем хостинге

## Поддержка

При возникновении проблем:
1. Проверьте логи FastAPI сервера
2. Проверьте консоль браузера
3. Убедитесь, что все зависимости установлены
4. Проверьте версии Node.js и Python



