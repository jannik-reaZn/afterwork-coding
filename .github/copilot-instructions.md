# GitHub Copilot Custom Instructions for Afterwork-Coding Project

## Project Overview

This repository contains a full-stack web application with Vue.js frontend and FastAPI backend:

- Frontend: Vue 3 with TypeScript, Vite, Pinia, Vue Router and PrimeVue components
- Backend: FastAPI with SQLModel for database operations (SQLite for development) and pydantic for data validation

## Directory Structure

- `/frontend`: Vue.js application with Tailwind CSS and PrimeVue component library
- `/backend`: FastAPI application structured in a feature-based architecture

## Frontend Structure

- `/src/components`: Vue components
- `/src/pages`: Route-based Vue components
- `/src/store`: Pinia stores
- `/src/api`: API client code (Axios instances)
- `/src/style`: Theme configurations and styling
- `/src/composables`: Reusable Vue composition functions

## Backend Structure

- Feature-based architecture with each feature containing:
  - `/domain`: Business logic and models
  - `/repositories`: Data access layer
  - `/routes`: API endpoints
- `/common`: Shared utilities, configurations, and base repositories
- `/tests`: Test files organized by feature

## Coding Conventions

1. Frontend:

   - Use Vue 3 Composition API with `<script setup lang="ts">` syntax
   - Follow PrimeVue component patterns for UI elements. PrimeVue components are automatically installed via the @primevue/auto-import-resolver, so no new PrimeVue components needs to be added.
   - Use Pinia for state management with the setup stores pattern
   - Use TailwindCSS for styling alongside PrimeVue components
   - Use `@/` alias for imports from the src directory

2. Backend:
   - Use FastAPI's dependency injection pattern for services
   - Organize code by feature within the `/features` directory
   - All the domain logic should be placed within the `features/domain` folder
     - The domain logic should be written in an use case as specified in the clean architecture pattern and stored in `features/domain/use_cases`. Use cases should be a `class` and called via `__call__`. Dependencies should be injected.
     - Models should be defined in `features/domain/models` and validated with `pydantic`
     - Domain specfic exceptions should be collected in `features/domain/exceptions`
   - Follow repository pattern for database access
     - Repositories should have an abstract implementation with `ABC`
     - Use SQLModel for ORM operations
     - Concrete implementations of such abstractions should be stored in `features/repositories/sql`
   - Implement routes in `features/routse`
     - Whereever possible use dependency injection via `Depends` by FastApi. Ideally each endpoint is kept rather small and readable and the overall logic is handled in an use case.

## Common Tasks

- Creating new Vue components: Place in `/frontend/src/components` and use `<script setup>` pattern
- Adding new API endpoints: Create new route files in the appropriate feature directory
- Theme customization: Modify `/frontend/src/style/theme.ts`
- State management: Create or update stores in `/frontend/src/store`

## Environment

- Frontend env vars: VITE_AXIOS_BACKENDURL, VITE_PORT
- The application is deployed on Render.com as separate services (static site + web service)

## Testing

- Frontend: Vitest in `/frontend/tests` directory
- Backend: Pytest in `/backend/tests` directory
  - Try to initiliaze tests as much as possible with `@pytest.fixture`
  - Try to paramterize tests with `@pytest.mark.parametrize`
