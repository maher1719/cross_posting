// Corresponds to the Pydantic UserDisplay model
export interface User {
    id: string;
    username: string;
    email: string;
    created_at: string; // Dates come as strings from JSON
}