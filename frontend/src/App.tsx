import React, { useState } from 'react';
import ChatList from './components/ChatList';
import ChatView from './components/ChatView';
import CreateChat from './components/CreateChat';
import { ChatResponse } from './types/api';

const App: React.FC = () => {
  const [chats, setChats] = useState<ChatResponse[]>([]);
  const [selectedChat, setSelectedChat] = useState<ChatResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // В реальном приложении здесь был бы API для получения списка чатов
  // Пока что используем локальное состояние
  const handleChatCreated = (newChat: ChatResponse) => {
    setChats(prev => [newChat, ...prev]);
    setSelectedChat(newChat);
  };

  const handleChatSelect = (chat: ChatResponse) => {
    setSelectedChat(chat);
  };

  return (
    <div className="h-screen bg-gray-100 flex flex-col overflow-hidden">
      {/* Заголовок */}
      <header className="bg-white shadow-sm border-b border-gray-200 flex-shrink-0">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Kafka Chat</h1>
              <p className="text-gray-600">Асинхронный чат на FastAPI и Kafka</p>
            </div>
            <div className="text-sm text-gray-500">
              {chats.length} чат{chats.length !== 1 ? 'ов' : ''}
            </div>
          </div>
        </div>
      </header>

      {/* Основной контент */}
      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 overflow-hidden">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8 h-full">
          {/* Левая панель - создание чата и список */}
          <div className="lg:col-span-1 space-y-6 overflow-y-auto">
            <CreateChat onChatCreated={handleChatCreated} />
            
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-lg font-semibold text-gray-800 mb-4">Чаты</h2>
              <ChatList
                chats={chats}
                selectedChatId={selectedChat?.chat_id || null}
                onChatSelect={handleChatSelect}
              />
            </div>
          </div>

          {/* Правая панель - просмотр чата */}
          <div className="lg:col-span-3 h-full">
            <div className="bg-white rounded-lg shadow-md overflow-hidden h-full flex flex-col">
              <ChatView chat={selectedChat} />
            </div>
          </div>
        </div>
      </main>

      {/* Футер */}
      <footer className="bg-white border-t border-gray-200 flex-shrink-0">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-gray-500 text-sm">
            <p>© 2024 Kafka Chat. Разработано с использованием FastAPI и React.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;
