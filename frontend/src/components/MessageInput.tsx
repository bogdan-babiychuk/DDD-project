import React, { useState } from 'react';
import { chatApi } from '../api/client';
import { CreatedMessageResponse } from '../types/api';

interface MessageInputProps {
  chatId: string;
  onMessageSent: (message: CreatedMessageResponse) => void;
}

const MessageInput: React.FC<MessageInputProps> = ({ chatId, onMessageSent }) => {
  const [text, setText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim()) return;

    setIsLoading(true);
    setError(null);

    try {
      const newMessage = await chatApi.createMessage(chatId, { text: text.trim() });
      onMessageSent(newMessage);
      setText('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Произошла ошибка при отправке сообщения');
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="border-t border-gray-200 p-4 bg-white">
      {error && (
        <div className="text-red-600 text-sm bg-red-50 p-3 rounded-md mb-3">
          {error}
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="flex space-x-3">
        <div className="flex-1">
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Введите сообщение..."
            rows={2}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
            disabled={isLoading}
          />
        </div>
        
        <button
          type="submit"
          disabled={!text.trim() || isLoading}
          className="bg-primary-600 text-white px-6 py-2 rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors self-end"
        >
          {isLoading ? 'Отправка...' : 'Отправить'}
        </button>
      </form>
    </div>
  );
};

export default MessageInput;
