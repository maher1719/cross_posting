// Corresponds to the Pydantic PostDisplay model
export interface Post {
    id: number;
    content: string;
    user_id: number;
    created_at: string;
}