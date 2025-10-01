# cross_posting
# Cross-Posting Application

This is a full-stack application...

## Development Setup

1. Make sure you have Docker installed.
2. Create a `.env` file from the `.env.example` template.
3. Load the project helper commands into your shell:
   ```bash
   source ./project.sh
   ```


---

### **Architectural Blueprint: The "Cross-Posting Platform"**

**Project Version:** 1.0
**Lead Architect:** Maher Ben Abdessalem
**Architectural Consultant:** Gemini

### **1. Core Philosophy: The Pyramid of Stability & Innovation**

The entire project is built on a foundational philosophy that prioritizes stability at the lower levels while enabling rapid innovation at the higher levels.

*   **The Bedrock (Infrastructure):** Rock-solid, slow-moving, and configuration-minimal. This is our Docker environment running on a stable OS.
*   **The Stable Core (Frameworks & Backend):** Deliberately designed, well-tested, and built for long-term maintainability. This is our Flask Clean Architecture, our generic CRUD framework, and our core libraries.
*   **The Edge (Features & UI):** The layer where rapid iteration and experimentation occur. This is our React frontend.

### **2. System Architecture: A Multi-Service, Containerized Application**

The application is a distributed system composed of five core, containerized services, orchestrated for local development using **Docker Compose.**

*   **`backend`:** A **Flask** web server that provides the primary API.
*   **`frontend`:** A **Vite** development server for the **React** single-page application.
*   **`db`:** A **PostgreSQL** database for persistent data storage.
*   **`broker`:** A **Redis** instance, acting as the message broker for Celery.
*   **`worker`:** A **Celery** worker process for executing asynchronous background tasks.

### **3. Backend Architecture: Pragmatic Clean Architecture ("The Onion")**

The Flask backend is structured using a "Pragmatic Clean Architecture" pattern, ensuring a strong separation of concerns, testability, and maintainability.

*   **`domain` Layer (The Core):**
    *   **Technology:** Pydantic Models.
    *   **Responsibility:** Defines the framework-agnostic data contracts and shapes (DTOs). This is the "single source of truth" for what our data looks like (e.g., `UserCreate`, `PostDisplay`). Uses smart types like `UUID4` for validation and coercion.

*   **`models` Layer:**
    *   **Technology:** SQLAlchemy 2.0 with `Mapped` columns.
    *   **Responsibility:** Defines the data mapping between our Python objects and the PostgreSQL database tables. This is the only layer that knows about the database schema. Primary keys are **UUIDs** for security and scalability.

*   **`repositories` Layer (Persistence):**
    *   **Responsibility:** The only layer that directly communicates with the database via SQLAlchemy. It is a "dumb" layer responsible for Create, Read, Update, and Delete operations.
    *   **Implementation:** Built on a generic, type-safe **`CRUDBase`** helper, making new repositories trivial to create.

*   **`use_cases` Layer (Business Logic):**
    *   **Responsibility:** The "brain" of the application. Contains all core business logic (e.g., password verification, checking permissions). It orchestrates the flow of data between the API and the repositories. It knows nothing about HTTP.
    *   **Implementation:** Built on a generic, type-safe **`CRUDUseCases`** helper, allowing for rapid scaffolding while providing clear extension points for custom logic (like calling a Celery task).

*   **`tasks` Layer (Asynchronous Services):**
    *   **Technology:** Celery.
    *   **Responsibility:** Defines long-running or slow background jobs (e.g., posting to social media APIs). This ensures the main API remains fast and responsive.

*   **`api` Layer (Presentation):**
    *   **Technology:** Flask Blueprints.
    *   **Responsibility:** The "thin controller" layer. Its only job is to handle incoming HTTP requests, validate the data against the `domain` models, call the appropriate `use_case`, and return a proper JSON response. It contains no business logic.

### **4. API Design: A Resilient Hybrid Model (REST + GraphQL)**

The platform exposes a hybrid API, leveraging the best of both worlds for maximum clarity, performance, and resilience.

*   **REST API (`/api/...`):**
    *   **Used for:** All "write" operations (**`POST`, `PATCH`, `DELETE`**) and simple, state-changing actions (e.g., **`/auth/login`**).
    *   **Includes "Full GET" endpoints** (`GET /api/posts/{id}`): These serve as a simple, stable "Plan B" fallback, a form of living documentation, and a universally compatible interface for simple clients.

*   **GraphQL API (`/graphql`):**
    *   **Used for:** All complex "read" operations.
    *   **Purpose:** To empower frontend clients to fetch the exact, nested data they need in a single request, eliminating over-fetching and under-fetching. Enables the creation of "specialized, premade" queries for optimizing critical paths.

*   **Security:**
    *   Authentication is handled via **JWTs** issued by the REST `/login` endpoint.
    *   All subsequent requests (both REST and GraphQL) are authenticated using this token.
    *   A **"Rescue Token" (Privileged Access)** protocol is designed for the "Full GET" REST endpoints, requiring a second, secret developer token to prevent potential data exposure, ensuring the "Plan B" is secure.

### **5. Frontend Architecture: React Clean Architecture**

The React frontend is also structured with a strict separation of concerns, mirroring the backend's philosophy.

*   **`api` (Infrastructure):** A single, configured **Axios** client (`apiClient.ts`) with interceptors for automatically attaching JWTs and handling global errors like `401 Unauthorized`.
*   **`types` (Domain):** TypeScript interfaces that mirror the backend's Pydantic `domain` models.
*   **`store` (Application State):** A global **Zustand** store for managing authentication state (`token`, `isAuthenticated`).
*   **`hooks` (Application Logic):** Custom hooks (`useLoginForm`, `useRegisterForm`) encapsulate all form state, validation, and API-calling logic, keeping the UI components clean.
*   **`components` (UI):** A library of reusable, "dumb" UI components styled with **Tailwind CSS.**
*   **`pages` (UI):** "Smart" components that compose the dumb components and connect them to the application logic via hooks.
*   **Routing:** Handled by **React Router.**

### **6. Development & Deployment: A Containerized, DevOps-Ready Workflow**

*   **Local Environment:** Fully orchestrated by **Docker Compose**, allowing for a one-command startup (`dcup`).
*   **Workflow Automation:** A `project.sh` script provides a suite of aliases (`dcdown`, `dcrestart`, `migrate`, `upgrade`, `killport`) to streamline the entire development and debugging lifecycle.
*   **Deployment Strategy:** The project is structured for easy deployment to any modern PaaS (like Fly.io or Render). A dedicated `deploy` branch in Git triggers automated deployments, and secrets are managed securely through the platform's environment variables.

