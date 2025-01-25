# About

# Frontend

The frontend setup is made with [Vite](https://vite.dev/guide/).

In Vue werden Websites in Komponenten zerlegt, welche jeweils HTML-Block, Style und Script in einer Datei vereinen. Diese werden anschließend in der übergelagerten `App.vue` importiert und ergeben die eigentliche Website. Komponenten sind im Ordner `src\components` gespeichert.

Werden verschiedene Ansichten der Website

### Node

Node.js is a JavaScript runtime built on Chrome's V8 engine, designed for executing JavaScript code server-side.Its package ecosystem, npm (Node Package Manager), provides access to a vast collection of libraries and tools, enabling rapid development and scalability.

Install the latest version of [node](https://nodejs.org/en/download). Download the .msi isntaller for windows. Follow the instructions in the installer.

Verify wether node is installed via `node -v`.
Verify wether npm is installed via `npm -v`.

### Setup

- To run the frontend locally go into the frontend directory via `cd frontend`. Install
- Install the frontend dependencies with `npm install`
- Run the frontend with `npm run dev`
- Open the server `http://localhost:5173/`

Während der Entwicklung wird das Frontend in einer speziellen Konfiguration geladen. Diese ist näher in der Datei `package.json` spezifizert. Außerdem finden sich dort auch die weiteren Möglichkeiten, das Frontend zu starten.

### UI Framework

In this project [PrimeVue](https://primevue.org/) is used as an UI framework. PrimeVue is a rich component library for Vue.js, offering a wide range of pre-built UI components, including forms, tables, charts, and interactive widgets. It supports modern features like themes, customizable styling, and accessibility compliance. It includes

- **Component Richness:** Includes commonly used components such as buttons, dropdowns, and data tables, as well as advanced ones like calendars and charts.

- **Theming Support:** Offers a variety of pre-built themes and the ability to create custom themes.

- **Responsive Design:** Components are designed to adapt to different screen sizes seamlessly.

The configuration of PrimeVue is done in the `main.ts` file. Different themes such as `Aura` can be installed and used as a preset. Different components need to be imported individually and set to `app.component`. In the following there is a basic setup is shown:

```ts title="main.ts"
import { createApp } from "vue";
import App from "./App.vue";
import PrimeVue from "primevue/config";
import Aura from "@primevue/themes/aura"; // theme
import Button from "primevue/button"; // component

const app = createApp(App);
app.use(PrimeVue, {
  theme: {
    preset: Aura,
  },
});
app.component("Button", Button);
app.mount("#app");
```

The installed components can be used within vue components directly without any further imports.

```ts
<template>
  <Button label="Verify" />
</template>

<script setup lang="ts"></script>

<style scoped></style>
```

### Router

For routing in a Vue application the library [Vue Router](https://router.vuejs.org/) is used.

### Pinia Store

[Pinia](https://pinia.vuejs.org/) is a store library for Vue, it allows you to share a state across components/pages. For pinia the [setup stores](https://pinia.vuejs.org/core-concepts/#Setup-Stores) should be used to keep as close to Vue Composition API's setup function.

### Testing

For testing [Vitest](https://vitest.dev/) is used. Each test should be located in the `frontend/tests` folder. Each test needs to include `<name>.test.ts`. To run tests for the frontend, follow these steps:

- Go into the frontend folder via `cd frontend`
- Execute `npm run test`

# Backend

[FastApi](https://fastapi.tiangolo.com/) is a modern, fast (high-performance), web framework for building APIs with Python based on standard Python type hints.

## Routing

The project backend is built using FastAPI, and `APIRouter` is utilized to organize and modularize the API endpoints. APIRouter allows you to group routes based on functionality or features, making the application more maintainable and scalable.

- **Modularity:** Enables grouping related routes into separate modules.
- **Reusability:** Routes can be defined and reused in different parts of the application.
- **Dependency Injection:** Supports FastAPI’s dependency injection system seamlessly.
- **Path Prefixing:** Automatically applies a prefix to all routes in a router, simplifying URL management.

Example usage:

1. **Define a Router:** Create a router in a separate module, e.g., users.py. The prefix parameter in APIRouter (e.g., /users) ensures that all endpoints within the router have consistent URL paths like /users/. Assign tags for OpenAPI documentation.

```python
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
async def get_users():
    return {"message": "List of users"}

@router.post("/")
async def create_user(user: dict):
    return {"message": "User created", "user": user}
```

1. **Import all individual routers and expose:** In the `routers/__init__.py` file, import all individual routers and expose them as individual variables:

```python
from .users import router as users_router
```

2. **Include the Router in the Main Application:** In your main app.py or equivalent, include the router:

```python
from fastapi import FastAPI
from users import users_router

app = FastAPI()
app.include_router(users_router)
```

## Conda

The project setup is done with conda. Follow the [instructions](https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html) for installing conda on windows.

- Create conda environment in the terminal by executing `conda env create -f environment.yml`
- Afterwards activate the environment `conda activate afterwork-coding`
- Within VSCode the installed python version needs to be selected as a interpreter. Open any .py file. In the bottom right corner of VSCode the interpreter can be selected. Select the one for `afterwork-coding`.
- Run the backend in debug mode by selecting the `Run and Debug` icon in the left panel of VSCode
- Select `Python: FastApi (afterwork coding)`
- Open the server `http://127.0.0.1:8000`

# Git Commands

## Status

To check whether someone updated the branch or if you are generally up-to-date enter `git status` in the terminal.

## Pull

1. Click on the `Source Control` icon in the left panel
2. In the section `Source Control` click the three dots
3. Select `pull`

Alternatively run `git pull` in the terminal.

## Push

1. Click on the `Source Control` icon in the left panel
2. In the section `Changes` click on the plus button to `Stage Changes`
3. Afterwards a commit message in the input field and click `Commit`
4. Then click `Push`

Alternatively run `git add .`, `git commit -m "message..."` and `git push`

# GitHub

## Branch Protection

- **Restrict deletions**
  Only allow users with bypass permissions to delete matching refs.

- **Require a pull request before merging**

  All commits must be made to a non-protected branch and submitted via a pull request before they can be merged into a branch that matches this rule.

- **Require approvals**

  Pull requests targeting a matching branch require a number of approvals and no changes requested before they can be merged. Required number of of approvals before merging is 1 (develop) and 2 (main).

- **Dismiss stale pull request approvals when new commits are pushed**
  New, reviewable commits pushed will dismiss previous pull request review approvals.

- **Require approval of the most recent reviewable push**

  Whether the most recent reviewable push must be approved by someone other than the person who pushed it.

- **Require conversation resolution before merging**

  All conversations on code must be resolved before a pull request can be merged into a branch that matches this rule.

- **Block force pushes**
  Prevent users with push access from force pushing to refs.
