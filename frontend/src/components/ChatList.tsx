import React from 'react';
import { ChatResponse } from '../types/api';
import { format } from 'date-fns';
import { ru } from 'date-fns/locale';

interface ChatListProps {
  chats: ChatResponse[];
  selectedChatId: string | null;
  onChatSelect: (chat: ChatResponse) => void;
}

const ChatList: React.FC<ChatListProps> = ({ chats, selectedChatId, onChatSelect }) => {
  if (chats.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <p>Чаты не найдены</p>
        <p className="text-sm">Создайте первый чат, чтобы начать общение</p>
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {chats.map((chat) => (
        <div
          key={chat.chat_id}
          onClick={() => onChatSelect(chat)}
          className={`p-4 rounded-lg cursor-pointer transition-colors ${
            selectedChatId === chat.chat_id
              ? 'bg-primary-100 border-2 border-primary-500'
              : 'bg-white hover:bg-gray-50 border-2 border-transparent'
          }`}
        >
          <div className="flex justify-between items-start">
            <div className="flex-1 min-w-0">
              <h3 className="font-medium text-gray-900 truncate">{chat.title}</h3>
              <p className="text-sm text-gray-500">
                Создан: {format(new Date(chat.created_ad), 'dd MMM yyyy, HH:mm', { locale: ru })}
              </p>
            </div>
            {selectedChatId === chat.chat_id && (
              <div className="ml-2">
                <div className="w-2 h-2 bg-primary-500 rounded-full"></div>
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};

export default ChatList;
