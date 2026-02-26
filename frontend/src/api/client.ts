import axios, { AxiosResponse } from 'axios';
import {
  ChatResponse,
  CreateChatRequest,
  AddMessageRequest,
  CreatedMessageResponse,
  ChatMessagesResponse,
  ApiError
} from '../types/api';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response interceptor для обработки ошибок
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.data?.error) {
      return Promise.reject(new Error(error.response.data.error));
    }
    return Promise.reject(error);
  }
);

export const chatApi = {
  // Создание нового чата
  createChat: async (data: CreateChatRequest): Promise<ChatResponse> => {
    const response: AxiosResponse<ChatResponse> = await apiClient.post('/chat/', data);
    return response.data;
  },

  // Получение чата по ID
  getChat: async (chatId: string): Promise<ChatResponse> => {
    const response: AxiosResponse<ChatResponse> = await apiClient.get(`/chat/${chatId}/`);
    return response.data;
  },

  // Создание сообщения в чате
  createMessage: async (chatId: string, data: AddMessageRequest): Promise<CreatedMessageResponse> => {
    const response: AxiosResponse<CreatedMessageResponse> = await apiClient.post(`/chat/${chatId}/messages`, data);
    return response.data;
  },

  // Получение сообщений чата
  getChatMessages: async (chatId: string): Promise<ChatMessagesResponse> => {
    const response: AxiosResponse<ChatMessagesResponse> = await apiClient.get(`/chat/${chatId}/messages`);
    return response.data;
  },
};

export default apiClient;
