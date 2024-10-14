# Digital Land Platform

## Description

The Digital Land Platform is designed to facilitate the buying and selling of land properties (plots, land, and houses). A key advantage of the platform is that buyers receive the ownership document instantly after purchasing the land, making it a significant improvement over existing systems and global real estate development.

## Overview

The system enables landowners to list their properties, upload multimedia content to showcase the land, and manage the selling process. Buyers can browse listings, verify their identity, and purchase properties, receiving immediate ownership documents upon completion. The platform also integrates with external APIs for property verification, loan status checks, and tax calculations and approved land for sale.

Click here to get the latest -> <a href="#dev_guide">Developer Guidelines</a>

## Technology Stack

- **Backend:**
  - FastAPI
  - PostgreSQL
  - SQLAlchemy
  - Alembic
  - Strawberry (GraphQL)

- **Frontend:**
  - React with TypeScript and
  - Apollo Client

- **Others:**
  - Docker
  - GitHub Actions (CI/CD)
  - Codecov (Test Coverage)
  - CodeClimate (Code Quality)

## Installation and Setup

### Prerequisites

- Python 3.*
- PostgreSQL
- Node.js and npm (for frontend)
- Docker (optional, for containerization)

### Backend Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Digital-Land-Platform/Digital-Land-Server.git
   cd Digital-Land-Server
   ```

2. Set up virtual environment:

    ```bash
    python3 -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. Install all dependencies by:

   ```bash
   pip3 install
   ```
   
4. Run database migrations:

```bash
    alembic upgrade head
```

5. Start the backend server:

```bash
    uvicorn main:app --reload
```

### Running Tests

```bash
pytest
```

### Contributing

We welcome contributions from the Team. Please, read our Contributing Guidelines and Code of Conduct before making a pull request.

### Contributing Guidelines and Code of Conduct:

- You have to make a new branch every time you are going to work either on a new feature or issue
- Changes must be reviewed and approved by the CTO before merging them into the default branch.
- All PR must be merged by the CTO only
- PR has to be reviewed by the Peers before being merged `(Recommended)`.
- It would be better to run pre-commit tests before releasing your changes

Just run:

```bash
    pre-commit install
```

---

<h3 id="dev_guide">Developer Guidelines</h3>

**Database Name**: The *database* name should be **digitalLandDb** for consistency.

#### Environment variables

```
# Database connection string for the application
DB_CONFIG=postgresql+asyncpg://<postgres>:<DEV_DB_PASS>@<DEV_DB_HOST>:<DEV_DB_PORT>/digitalLandDb

# Hostname or IP address of the database server
DEV_DB_HOST=********************************

# Port number on which the database server is listening
DEV_DB_PORT=********************************

# Username for connecting to the database
DEV_DB_USER=********************************

# Password for the database user
DEV_DB_PASS=********************************

# Name of the database to connect to
DEV_DB_NAME=********************************

# Environment in which the application is running (e.g., development, production)
APP_ENV=********************************

# Name of the database (used for configuration or logging)
DB_NAME=ditalLandDb

# Password for the database (used for configuration or logging)
DB_PASSWORD=********************************

# Username for the application, typically for connecting to external services
DB_USER=********************************

# Secret key used for securing sessions or cryptographic operations
SECRET_KEY=********************************


```

#### Naming Conventions

1. *Function* names should be written as action words or phrases.

2. *Controllers* should be independent of each other in respective folders. Each folder should contain the files, __init__.py, index.py, mutation.py, query.py, and services.py. *Controller classes* in these files should be appended with the file names and written in **PascalCase** as in *UserMutation*, *UserQuery*, and *UserService*.

3. *Model file* names should be written in **PascalCase**.

4. *Middleware file* names should be written in **PascalCase** and be appended with the word, *Handler*, as in *CustomErrorHandler*.


The headers of the following table make up the naming standards to be adopted in developing the system.
The names of the items under each column should be written according to the style of the table header for that column.

| PascalCase        | lower_snake_case | UPPER_SNAKE_CASE | camelCase        | khebab-case      |
|  ---------------- | ---------------- | ---------------- | ---------------- | ---------------- |
| Classes           | methods          | Constants        | Functions        | docker-compose   |
|                   | variables        |                  |                  | git-branch  |
|                   | schemas/tables   |        |      |                  |
|                   | attributes/columns |        |      |                  |
|                   | route_methods    |        |      |                  |
|                   | test_functions   |        |      |                  |


#### Important Note: 
**Developers should update the README file with their updates. This is to serve as a documentation for each task completed.**

The documentation should follow the following format:

=======

#### Task Title
**Description:**
A brief overview of the task.

**Acceptance Criteria:**
- List of acceptance criteria to validate the task.

**Validation:**
Instructions on how to test or validate the task.

**Other Important things to note**
- Any additional information or considerations relevant to the task.

========

---


#### Reporting Issues

If you find any issues, please report them using the GitHub Issues feature.

---

#### Badges

The project integrates various badges to provide key information at a glance:

`Build Status:` Indicates the current build status of the project.

`Test Coverage:` Shows the test coverage percentage of the codebase.

`Code Quality:` Reflects the maintainability and code quality of the project.
