# About

# Frontend

The frontend setup is made with [Vite](https://vite.dev/guide/).

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

## Conda

The project setup is done with conda. Follow the [instructions](https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html) for installing conda on windows.

- Create conda environment in the terminal by executing `conda env create -f environment.yml`
- Afterwards activate the environment `conda activate afterwork-coding`
- Within VSCode the installed python version needs to be selected as a interpreter. Open any .py file. In the bottom right corner of VSCode the interpreter can be selected. Select the one for `afterwork-coding`.
- Run the backend in debug mode by selecting the `Run and Debug` icon in the left panel of VSCode
- Select `Python: FastApi (afterwork coding)`
- Open the server `http://127.0.0.1:8000`

# Git Commands

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
