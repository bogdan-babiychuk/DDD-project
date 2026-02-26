import React, { useEffect, useRef } from 'react';
import { CreatedMessageResponse } from '../types/api';
import { format } from 'date-fns';
import { ru } from 'date-fns/locale';

interface MessageListProps {
  messages: CreatedMessageResponse[];
  isLoading: boolean;
}

const MessageList: React.FC<MessageListProps> = ({ messages, isLoading }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  if (isLoading) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="text-gray-500">Загрузка сообщений...</div>
      </div>
    );
  }

  if (messages.length === 0) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="text-center text-gray-500">
          <p>Сообщений пока нет</p>
          <p className="text-sm">Напишите первое сообщение!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full overflow-y-auto p-4 space-y-4">
      {messages.map((message) => (
        <div key={message.message_id} className="flex flex-col">
          <div className="bg-white rounded-lg p-3 shadow-sm border border-gray-200 max-w-xs lg:max-w-md">
            <p className="text-gray-900 break-words">{message.text}</p>
            <p className="text-xs text-gray-500 mt-2">
              {format(new Date(message.datetime), 'dd MMM yyyy, HH:mm', { locale: ru })}
            </p>
          </div>
        </div>
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList;
