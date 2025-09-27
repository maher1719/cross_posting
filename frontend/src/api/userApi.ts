import apiClient from './apiClient'; // <-- IMPORT OUR CONFIGURED INSTANCE
import type { User } from '../types';

export interface UserCreateData {
  username: string;
  email: string;
  password: string;
}

export const registerUser = async (userData: UserCreateData): Promise<User> => {
  // Use the pre-configured apiClient instead of axios.post
  const response = await apiClient.post<User>('/users/register', userData);
  return response.data;
};