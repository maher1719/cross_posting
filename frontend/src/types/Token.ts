// frontend/src/types/Token.ts

/**
 * This interface represents the shape of the token object
 * returned by the backend's /auth/login endpoint.
 * It corresponds to the Pydantic Token model in Flask.
 */
export interface Token {
  access_token: string;
  token_type: 'bearer'; // We can use a literal type for added safety
}