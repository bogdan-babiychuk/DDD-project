import React, { useState } from 'react';
import { chatApi } from '../api/client';
import { ChatResponse } from '../types/api';

interface CreateChatProps {
  onChatCreated: (chat: ChatResponse) => void;
}

const CreateChat: React.FC<CreateChatProps> = ({ onChatCreated }) => {
  const [title, setTitle] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    setIsLoading(true);
    setError(null);

    try {
      const newChat = await chatApi.createChat({ title: title.trim() });
      onChatCreated(newChat);
      setTitle('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Произошла ошибка при создании чата');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Создать новый чат</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="chat-title" className="block text-sm font-medium text-gray-700 mb-2">
            Название чата
          </label>
          <input
            type="text"
            id="chat-title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Введите название чата"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            disabled={isLoading}
          />
        </div>

        {error && (
          <div className="text-red-600 text-sm bg-red-50 p-3 rounded-md">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={!title.trim() || isLoading}
          className="w-full bg-primary-600 text-white py-2 px-4 rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {isLoading ? 'Создание...' : 'Создать чат'}
        </button>
      </form>
    </div>
  );
};

export default CreateChat;
