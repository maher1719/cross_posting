// frontend/src/api/postApi.ts

import apiClient from './apiClient';
import type { Post } from '../types'; // Import the Post type

// Define the shape of the data we need to create a post
export interface PostCreateData {
  content_html: string;
  content_text: string;
  // The user_id will be added on the backend from the token,
  // but let's send it for now until we build that logic.
  user_id: string; // Assuming UUIDs are strings
}

// Function to create a new post
export const createPost = async (postData: PostCreateData): Promise<Post> => {
  // This request will AUTOMATICALLY have the JWT attached by our apiClient interceptor!
    console.log("passed data",postData)
  const response = await apiClient.post<Post>('/posts/', postData);

  return response.data;
};

// You can also add the function to get all posts here
export const getAllPosts = async (): Promise<Post[]> => {
    const response = await apiClient.get<Post[]>('/posts/');
    return response.data;
};