// Corresponds to the Pydantic PostDisplay model
export interface Post {
    id: number;
    content_text: string;
    content_html: string;
    user_id: number;
    created_at: string;
}