// frontend/src/types/Token.ts

import type { User } from "./User";

/**
 * This interface represents the shape of the token object
 * returned by the backend's /auth/login endpoint.
 * It corresponds to the Pydantic Token model in Flask.
 */
export interface Token {
  access_token: string;
  user: User;

  token_type: 'bearer'; // We can use a literal type for added safety
}