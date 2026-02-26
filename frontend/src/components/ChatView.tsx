import React, { useState, useEffect } from 'react';
import { ChatResponse, CreatedMessageResponse } from '../types/api';
import { chatApi } from '../api/client';
import MessageList from './MessageList';
import MessageInput from './MessageInput';

interface ChatViewProps {
  chat: ChatResponse | null;
}

const ChatView: React.FC<ChatViewProps> = ({ chat }) => {
  const [messages, setMessages] = useState<CreatedMessageResponse[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (chat) {
      loadMessages();
    }
  }, [chat]);

  const loadMessages = async () => {
    if (!chat) return;

    setIsLoading(true);
    setError(null);

    try {
      const response = await chatApi.getChatMessages(chat.chat_id);
      setMessages(response.messages);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Ошибка при загрузке сообщений');
    } finally {
      setIsLoading(false);
    }
  };

  const handleMessageSent = (newMessage: CreatedMessageResponse) => {
    setMessages(prev => [...prev, newMessage]);
  };

  if (!chat) {
    return (
      <div className="flex-1 flex items-center justify-center bg-gray-50">
        <div className="text-center text-gray-500">
          <p className="text-lg">Выберите чат</p>
          <p className="text-sm">или создайте новый для начала общения</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col bg-gray-50 h-full">
      {/* Заголовок чата - фиксированная высота */}
      <div className="bg-white border-b border-gray-200 p-4 flex-shrink-0">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl font-semibold text-gray-900">{chat.title}</h1>
            <p className="text-sm text-gray-500">
              ID: {chat.chat_id}
            </p>
          </div>
          <button
            onClick={loadMessages}
            disabled={isLoading}
            className="text-primary-600 hover:text-primary-700 text-sm font-medium disabled:opacity-50"
          >
            Обновить
          </button>
        </div>
      </div>

      {/* Сообщения - фиксированная высота с внутренним скроллингом */}
      <div className="flex-1 overflow-hidden bg-gray-50">
        {error ? (
          <div className="h-full flex items-center justify-center">
            <div className="text-center text-red-600">
              <p>{error}</p>
              <button
                onClick={loadMessages}
                className="mt-2 text-primary-600 hover:text-primary-700 underline"
              >
                Попробовать снова
              </button>
            </div>
          </div>
        ) : (
          <MessageList messages={messages} isLoading={isLoading} />
        )}
      </div>

      {/* Поле ввода сообщения - фиксированная высота */}
      <div className="flex-shrink-0">
        <MessageInput chatId={chat.chat_id} onMessageSent={handleMessageSent} />
      </div>
    </div>
  );
};

export default ChatView;
