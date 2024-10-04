# Digital Land Platform

[![Digital-Land-Server CI](https://github.com/Digital-Land-Platform/Digital-Land-Server/actions/workflows/ci.yml/badge.svg)](https://github.com/Digital-Land-Platform/Digital-Land-Server/actions/workflows/ci.yml)
&nbsp;&nbsp;
<!-- [![Build Status](https://github.com/Digital-Land-Platform/Digital-Land-Server/workflows/ci.yml/badge.svg)](https://github.com/Digital-Land-Platform/Digital-Land-Server/actions)-->&nbsp;&nbsp;
[![Test Coverage](https://codecov.io/gh/Digital-Land-Platform/Digital-Land-Server/branch/develop/graph/badge.svg)](https://codecov.io/gh/Digital-Land-Platform/Digital-Land-Server/)&nbsp;&nbsp;
<!-- [![Code Quality](https://api.codeclimate.com/v1/badges/yourbadgeid/maintainability)](https://codeclimate.com/github/Digital-Land-Platform/Digital-Land-Server/maintainability)-->&nbsp;&nbsp;
![Auto Assign](https://github.com/Digital-Land-Platform/Digital-Land-Server/actions/workflows/auto-assign.yml/badge.svg)

## Description

The Digital Land Platform is designed to facilitate the buying and selling of land properties (plots, land, and houses). A key advantage of the platform is that buyers receive the ownership document instantly after purchasing the land, making it a significant improvement over existing systems and global real estate development.

## Overview

The system enables landowners to list their properties, upload multimedia content to showcase the land, and manage the selling process. Buyers can browse listings, verify their identity, and purchase properties, receiving immediate ownership documents upon completion. The platform also integrates with external APIs for property verification, loan status checks, and tax calculations and approved land for sale.

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
   git clone https://github.com/
   cd 
   ```

2. Set up virtual environment:

    ```bash
    python3 -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. Run database migrations:

```bash
    alembic upgrade head
```

4. Start the backend server:

```bash
    uvicorn main:app --reload
```

### Running Tests

```bash
pytest
```

### Contributing

We welcome contributions from the Team. Please read our Contributing Guidelines and Code of Conduct before making a pull request.

### N.B: Remember to run pre-commit tests before releasing your changes

Just run:

```bash
    pre-commit install
```

#### Reporting Issues

If you find any issues, please report them using the GitHub Issues feature.

#### Badges

The project integrates various badges to provide key information at a glance:

`Build Status:` Indicates the current build status of the project.

`Test Coverage:` Shows the test coverage percentage of the codebase.

`Code Quality:` Reflects the maintainability and code quality of the project.
