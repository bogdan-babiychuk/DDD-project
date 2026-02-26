export interface ChatResponse {
  chat_id: string;
  title: string;
  created_ad: string; // ISO date string
}

export interface CreateChatRequest {
  title: string;
}

export interface AddMessageRequest {
  text: string;
}

export interface CreatedMessageResponse {
  chat_id: string;
  message_id: string;
  text: string;
  datetime: string; // ISO date string
}

export interface ChatMessagesResponse {
  chat_id: string;
  messages: CreatedMessageResponse[];
}

export interface ApiError {
  error: string;
}
