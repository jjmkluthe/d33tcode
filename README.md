# Welcome to D33TCode!

D33tcode is a small teaching app built for **CS 665 Intro to Database Systems**.

The purpose of D33tcode is somewhat similar to leetcode, in that it provides problems for the user to solve and be graded on their solution.

It differs, however, that instead of supplying DSA problems that are rarely relevant to real work, it provides github links to applications that work to some degree, but have bugs that must be fixed or features that must be implemented.

This mirrors what the actual day-to-day work of a developer is really involves.

In this sample setup, none of the projects, videos, or github links provide real data. Additional work must be done to make this a truly usable application, but it demonstrates:

- A **PostgreSQL** database with 6 related tables (`app_user`, `problem`, `project`, `solution`, `video`, `submission`)
- A **FastAPI** backend using SQLAlchemy and JWT-based auth
- A **Vue 3 + Vite** frontend that supports login, project browsing, basic admin tools, and a simple data visualization (projects grouped by difficulty)

---

## Database Overview

The core schema:

- `app_user`: users (admin/standard), login credentials, flags
- `problem`: problem descriptions and Git links
- `solution`: example solutions and Git links
- `project`: student-facing projects linked to a problem & solution with difficulty
- `video`: YouTube codes attached to projects
- `submission`: junction table between users and projects, with completion + grade

You can see the ER-style diagram (Mermaid) below.
``` mermaid
    erDiagram

        USER {
            int id PK
            string username
            string password
            string email_address
            string type
            bool update_password
        }

        PROJECT {
            int id PK
            string title
            string description
            int problem FK
            int solution FK
            int difficulty
        }

        PROBLEM {
            int id PK
            string git_link
            string problem_description
        }

        SOLUTION {
            int id PK
            string git_link
            string solution_description
        }

        VIDEO {
            int id PK
            int project_id FK
            string yt_code
            string type
            int ordinal
        }

        SUBMISSION {
            int user_id PK
            int project_id PK
            bool is_complete
            float grade            
        }

        USER ||--o{ SUBMISSION : ""
        SUBMISSION }o--|| PROJECT : ""
        PROJECT ||--|| PROBLEM : ""
        PROJECT ||--|| SOLUTION : ""
        PROJECT ||--|{ VIDEO : ""

````

## Prerequisites

This project provides a makefile containing commands for easy setup. However, you need the following installed before using the Makefile:

**PostgreSQL** (server + client tools)

- Download / install: https://www.postgresql.org/download/

**Python 3.11+**

- Download: https://www.python.org/downloads/

**uv** (Python package & project manager)

- Install instructions: https://docs.astral.sh/uv/getting-started/installation/

**Node.js (LTS) + npm** (for the Vue frontend)

- Download: https://nodejs.org/

**NOTE: pip** can also be used in place of **uv** for package management. The package requirements are found in **/backend/pyproject.toml**

## Building the Project

Once the prerequisites have been met, the makefile found at the project root contains a number of commands to help build the project easily. They are:

```
# Drop & recreate database, run schema + seed, fix example passwords
make db-reset

# Create the database schema (tables) only
make db-build-schema

# Seed example data into existing tables
make db-seed

# Run the password hashing script for all example users
make db-fix-passwords

# Drop and recreate the database
make db-drop

# Start the FastAPI backend (http://127.0.0.1:8000)
make run-backend

# Build the frontend for production (Vite)
make build-frontend

# Start the Vue dev server (http://127.0.0.1:5173)
make run-frontend

# Start both the backend server and the frontend dev server
make run-all
```

A typical setup assumes you have created a database called d33tcode through psql using the command
```
createdb d33tcode
```

Then, to build the schemas, insert dummy values, and hash passwords simply run:

```
make db-reset
```

You can run the backend and frontend separately in different shells with
```
make run-backend
make run-frontend
```

Or run them from the same shell with
```
make run-all
```

## Users

In the example database there are two types of users: "standard" and "admin". standard users can log in and view a list of projects. admin users can login and see a list of users and statistics about projects grouped by difficulty. Additionally, admin users can navigate to /projects and see the same list of projects as standard users, but with the ability to edit those projects.

All users have the same password in this example database: **password123**
The only admin user is simply called **admin**. A good test standard username is **alice**

## Swagger

OpenAPI/Swagger docs are shown at /docs in the application. Most of these require admin user authentication to access, so simply use the "Authorize" button at the top of the page and put in the **admin** username with password **password123** to utilize the Swagger interface.