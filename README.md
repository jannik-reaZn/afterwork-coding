# About

This project contains multiple singleplayer and multiplayer mini games.

# Development Setup

## Requirements

- [Visual Studio Code](https://code.visualstudio.com/)
- [Node.js (LTS)](https://nodejs.org/en)
- [Miniforge](https://github.com/conda-forge/miniforge)
- Optional: [Linux subsystem for windows](https://learn.microsoft.com/en-us/windows/wsl/install) with WSL2

## VSCode

For coding the coding editor Visual Studio Code is recommended as this project already sets up extensions and a debugging environment.

- Download VSCode from the official [website](https://code.visualstudio.com/)
- Install it following the instructions for your operating system
- Install the extensions for the project that VSCode recommends. They can be inspected in `Extensions` tab under `Recommended`.
- Optional: Install WSL2 for linux subsystem

## Linux Subsystem

For this project a unix based environment is not a must have but recommended. On a windows operation sytem, developers can access the power of both Windows and Linux at the same time on a Windows machine. The Windows Subsystem for Linux (WSL) lets developers install a Linux distribution such as Ubuntu and use Linux applications, utilities, and Bash command-line tools directly on Windows, unmodified, without the overhead of a traditional virtual machine or dualboot setup.

For installation follow the instruction steps on the [offical microsoft website](https://learn.microsoft.com/en-us/windows/wsl/install).

If you encounter problem while the installation process, have a look into the [troubleshooting guide](https://learn.microsoft.com/en-us/windows/wsl/troubleshooting).

## Miniforge

Follow the [instructions](https://github.com/conda-forge/miniforge) for installing miniforge on windows.

### Linux

- Download the latest 64-bit version of the miniforge installer

```
wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
```

- Install conda

```
bash Miniforge3-$(uname)-$(uname -m).sh
```

## Node

Node.js is a JavaScript runtime built on Chrome's V8 engine, designed for executing JavaScript code server-side.Its package ecosystem, npm (Node Package Manager), provides access to a vast collection of libraries and tools, enabling rapid development and scalability.

### Windows

- Install the latest version of [node](https://nodejs.org/en/download). Download the .msi isntaller for windows and follow the instructions in the installer.
- Verify node installation via `node -v` and npm is installed via `npm -v`.

### Linux

- Install node with nvm `nvm install 22.1.0`
- Check the current node version `node --version`
- Switch between node version by using `nvm use <node_version>`

# Getting Started

## Frontend

- To run the frontend locally go into the frontend directory via `cd frontend`. Install
- Install the frontend dependencies with `npm install`
- Run the frontend with `npm run dev`
- Open the server `http://localhost:5173/`

Während der Entwicklung wird das Frontend in einer speziellen Konfiguration geladen. Diese ist näher in der Datei `package.json` spezifizert. Außerdem finden sich dort auch die weiteren Möglichkeiten, das Frontend zu starten.

## Backend

- Create conda environment in the terminal by executing `conda env create -f environment.yml`
- Afterwards activate the environment `conda activate afterwork-coding`
- Within VSCode the installed python version needs to be selected as a interpreter. Open any .py file. In the bottom right corner of VSCode the interpreter can be selected. Select the one for `afterwork-coding`.
- Run the backend in debug mode by selecting the `Run and Debug` icon in the left panel of VSCode
- Select `Python: FastApi (afterwork coding)`
- Open the server `http://127.0.0.1:8000`

# Frontend

The frontend setup is made with [Vite](https://vite.dev/guide/).

## UI Framework

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

## Router

For routing in a Vue application the library [Vue Router](https://router.vuejs.org/) is used.

## Pinia Store

[Pinia](https://pinia.vuejs.org/) is a store library for Vue, it allows you to share a state across components/pages. For pinia the [setup stores](https://pinia.vuejs.org/core-concepts/#Setup-Stores) should be used to keep as close to Vue Composition API's setup function.

## Testing

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

## Database

In this project all CRUD operations (create, read, update, delete) are made on a relational database, more specifically SQLite. The creation of the database connection and the SQLite setting are within the `database.py`. For local development and testing SQLite is fine, but in a production environment more robust databases such as PostgreSQL, MySQL or MariaDB should be considered.

All database related operations are made by `SQLAlchemy`. The `get_db` function is a dependency that will be used to create a new database session for each request following the principles of `Dependency Injection`. This setup allows to inject different session into the backend endpoints as dependencies for easier testing.

```python
from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.orm import sessionmaker

SQLITE_DATABASE_URL = "sqlite:///backend/development.db"

engine = create_engine(
    SQLITE_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_db():
    with Session(engine) as session:
        yield session
```

## Database Table Definitions

The database table definitions are stored in the `db` folder. It relys on `SQLModel`, is built on top of `SQLAlchemy` and `Pydantic` for data validation. The `Item` class is very similar to a Pydantic model, altough `table=True` tells SQLModel that this is a table model, it should represent a table in the SQL database, it's not just a data model. `Field(default=None, primary_key=True)` tells SQLModel that the id is the primary key in the SQL database. SQLModel knows that how to handle pythons string and int types into the respective database types (e.g. TEXT or VARCHAR).

```python
from sqlmodel import SQLModel, Field
from typing import Optional

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
```

## Testing

[Pytest](https://docs.pytest.org/en/stable/) is a powerful testing framework for Python. It simplifies the process of writing and running tests, supports a wide range of test types, and provides a rich ecosystem of plugins.

- **Simple Syntax:** Tests are written as functions prefixed with test\_.
- **Rich Assertions:** Provides detailed feedback on failed assertions.
- **Fixtures:** Modular and reusable setup/teardown code for tests.
- **Plugins:** Extend functionality (e.g., pytest-django, pytest-cov).
- **Test Discovery:** Automatically finds tests based on file names and function prefixes.

In bigger applications it makes sense to have tests in a separate folder called `tests`. Since FastApi is composed of several files/modules each test should also lay in these files/modules. For example router specfic tests should be part of the `routers` folder. A file called `src/utils.py` should have a separate test folder and file `tests/src/test_utils.py`

Create functions with a name that starts with `test_` (this is standard pytest conventions). The TestClient object is based on httpx and used to tests requests to the application. Write simple assert statements with the standard Python expressions that you need to check (again, standard pytest).

```python
from backend.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_example():
  response = client.get("/")
  assert response.status_code == 200
  assert response.json() == {"message": "Welcome to FastAPI with Conda!"}
```

Before writing any tests, they should be keept isolated, independent and repeatable. This means tests can run in any order. This means tests can run in any order. It is best practice to abstract the implementation detail. To handle all of this, Pytest offers `fixtures` for setup and teardown functions. For testing, a separate test database in SQLite is created to avoid using the real database and causing side effects. That setup is part of the `conftest.py` file. It created a test database in SQLite and sets up the test client for the FastAPI app. The test client is used in the tests to make requests to the app endpoints and test its CRUD operations.

## HTTP Response Codes

Every http request has a response with a status code that indicate the state of the response. Responses are grouped in five classes and can be viewed in detail [here](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

- Informational responses (100–199)
- Successful responses (200–299)
- Redirection messages (300–399)
- Client error responses (400–499)
- Server error responses (500–599)

## Swagger and OpenAPI

For endpoint documentation FastApi provides API documentation, so called `Swagger UI`, which can be found under `http://127.0.0.1:8000/docs`.

# Git Commands

### Status

To check whether someone updated the branch or if you are generally up-to-date enter `git status` in the terminal.

### Pull

1. Click on the `Source Control` icon in the left panel
2. In the section `Source Control` click the three dots
3. Select `pull`

Alternatively run `git pull` in the terminal.

### Push

1. Click on the `Source Control` icon in the left panel
2. In the section `Changes` click on the plus button to `Stage Changes`
3. Afterwards a commit message in the input field and click `Commit`
4. Then click `Push`

Alternatively run `git add .`, `git commit -m "message..."` and `git push`

### Delete remote branches

Delete local branches that have been deleted on the remote (origin).

```bash
git fetch --prune && git branch -vv | grep ': gone]' | awk '{print $1}' | xargs git branch -D
```

# GitHub

## Kanban Board

The Kanban board is used to track the progress of tasks, issues, and features in this project. It provides a visual workflow to organize work efficiently.

### How Issues Relate to Board Items

Each item on the board represents a GitHub issue or pull request. When an issue is created, it can be assigned to a column based on its status. Moving an issue across columns reflects its progress in the development cycle.

### Board Columns

Use the board to prioritize tasks, track development flow, and ensure smooth progress.

- **Backlog**: Holds all created PBIs (Product Backlog Items).
- **Ready**: PBIs that are planned but have not been started.
- **In Progress** – PBIs that are actively being worked on.
- **In Review** – PBIs or PRs that need review before merging.
- **Done** – Completed tasks that are ready for deployment or have been merged.

### How to Create a Backlog item

- Open the Kanban Board and click on `Add Item` in the column for `Backlog`
- Click on the `+` symbol and click `Create new issue`
- Add a meaningful `title` and `description` and click `Create`
- Afterwards an `Assignee` can be assigned to the ticket and `labels` (optional)

### Create a Feature Branch

- Most importantly branches can be created by clicking on the `Create a branch` button
- Make sure to add `feature` as a prefix of the branch name, e.g. `feature/1-example-issue`. This is important for merging to develop later since branches in pull requests need to have `feature/` in the branch name!
- Set the `Branch source` to develop and create the branch
- Afterwards you need to run `git fetch` and `git checkout feature/<your-branch-name>` locally

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

# Deployment

The application is hosted on [render.com](render.com). It simplifies the deployment and hosting of web web applications and static sites. It offers static sites, which is perfect for hosting frontend application with Vue.js, and web services, which is perfect for the backend part with python and FastApi. That means that the frontend and backend are hosted as separate services.

## Frontend

The frontend is hosted as a static site. On render it is documented how to setup a [static site](https://render.com/docs/static-sites) and [Vue.js applications](https://render.com/docs/deploy-vue-js).

### Static Site

The static site service by renders offers a `settings` section to setup everything for the application in different steps:

1. General
   - A unique of the static site. That name will also be part of the URL like that `https://<name>.onrender.com`
2. Build & Deploy

- **Repository:** The repository used for the static site. Public repositories can be directly linked
- **Branch:** The Git branch to build and deploy, typically this is the `main` branch.
- **Root Directory:** For monorepos, which is the case in this project, the root directory needs to be specified. Since the frontend should be served as a static site, `frontend` needs to be set.
- **Build Command:** The command that render runs to build the app before each deploy. In this case it `npm install` and `npm run build`
- **Publish Directory:** The relative path of the directory containing built assets to publish. In this case it is `dist`

It is also possible to include Render as a [github action](https://render.com/docs/deploy-hooks#using-with-github-actions) the CICD pipeline. The `deploy hook url` is needed for that.

### Client-Side Routing

A static site with Vue.js and Vue Router also needs a [setup for client side routing](https://render.com/docs/deploy-vue-js#using-client-side-routing). Without a proper server configuration, the users will get a 404 error if they access subdomains, e.g. `https://example.com/user/id`

To solve that issue, all all routing requests needs to be directed to `index.html` so they can be handled by the routing library, in this case Vue Router.

This can be done in the `Rewrite Rule` section for static sites. A rule with values for source path, destination path and action needs to be added as stated in the documentation:

| Name             | Value       |
| ---------------- | ----------- |
| Source Path      | /\*         |
| Destination Path | /index.html |
| Action           | Rewrite     |

### Environment Variables

In the section for `Environment` secrets can be set. In this project, a variable for setting the connection to the backend and the axios port is needed. The environment variables names are the following and needs to be set accordingly:

| Name                  | Value                       | Explanation                              |
| --------------------- | --------------------------- | ---------------------------------------- |
| VITE_AXIOS_BACKENDURL | https://<name>/onrender.com | URL of the web service (backend)         |
| VITE_PORT             | ...                         | Port number of the web service (backend) |

## Backend

The backend is hosted as a web service. On render it is documented how to setup a [web service](https://render.com/docs/web-services) and [FastAPI applications](https://render.com/docs/deploy-fastapi).

### Web Service

The steps for setting up a web service are similar to static sites:

1. General
   - A unique of the web service. That name will also be part of the URL like that `https://<name>.onrender.com`. This URL is needed as an environment variable `VITE_AXIOS_BACKENDURL` in the static site.
2. Build & Deploy

- **Repository:** The repository used for the static site. Public repositories can be directly linked
- **Branch:** The Git branch to build and deploy, typically this is the `main` branch.
- **Root Directory:** For monorepos, which is the case in this project, the root directory needs to be specified. Normally this should be `backend`. But since the import paths in the python files are absolute and start with `import backend...`, the root directory needs to be kept empty!
- **Build Command:** The command that render runs to build the app before each deploy. In this case it `pip install -r backend/requirements.txt`. Notice that `backend/` needs to be set since the root directory is empty.
- **Start Command:** The command that render runs to start the app with each deploy. In this case it `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`. Notice that `backend/` needs to be set since the root directory is empty.
