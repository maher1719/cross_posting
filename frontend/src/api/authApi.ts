import apiClient from './apiClient'; // <-- SAME INSTANCE
import type { Token, LoginData} from '../types'; // You would define the Token type


export const loginUser = async (credentials: LoginData): Promise<Token> => {
  const response = await apiClient.post<Token>('/auth/login', credentials);
  return response.data;
};