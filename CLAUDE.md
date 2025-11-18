# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

**YOU MUSTn't generate too many documents, which is too verbose and tedious!!! Unless with explicit instruction/permission!**

- Never read PDF files yourself
- You nay use bash commands to assign gemini a one-time task. Put prompt directly after the command like `gemini "hello"`
- Utilize gemini to help you with reading PDF files, large single files and works requiring en extensive context window


## Project Overview

This is a **Web Development Technology course project** building the **GoodServices** platform - a community service platform that facilitates matching service requests with service providers. The platform handles service publishing, responses, acceptance, and statistical reporting.

**Project Status:** Planning & Design Phase

- Database schema designed and documented
- Technical architecture planned (FastAPI + Vue 3)
- 15 specialized development agents configured
- Implementation ready to begin

**Key Documentation:**

- `goodservices.sql` - MySQL database schema
- `goodservices_database_documentation.md` - Database design documentation
- `technical_solution.md` - Complete technical architecture (FastAPI + SQLAlchemy + Vue 3)
- `subagent_design.md` - Multi-agent development workflow design
- `requirements.pdf` - Course project requirements
- `report.md` - Assignment report template
- `process.md` - Team assignment progress template

## Database Information

- **Database Type:** MySQL 8.0
- **Schema Name:** goodservices
- **Main Schema File:** `goodservices.sql`
- **Documentation:** `goodservices_database_documentation.md`

## Core Business Model

The platform follows this flow:

```
User publishes service request → Other users respond → Publisher accepts response → Service completion recorded → Monthly statistics
```

**Key Tables:**

- `buser_table` - Business users (core user table)
- `sr_info` - Service requests (published needs)
- `response_info` - Service responses (offers to fulfill needs)
- `accept_info` - Service completion records
- `service_type` - Service categories (6 types: plumbing, elderly care, cleaning, medical, meals, transportation)

## Working with the Database

### Importing the Schema

The `goodservices.sql` file is in **MySQL format** and contains MySQL-specific syntax (backticks, ENGINE=InnoDB, charset declarations, etc.).

**For MySQL:**

```bash
# Create database and import
mysql -u root -p -e "CREATE DATABASE goodservices;"
mysql -u root -p goodservices < goodservices.sql

# Access database
mysql -u root -p goodservices
```

**For SQLite (requires conversion):**

```bash
# Clean MySQL-specific syntax
cat goodservices.sql | \
  sed 's/`/"/g' | \
  sed '/^SET NAMES/d' | \
  sed '/^SET FOREIGN_KEY_CHECKS/d' | \
  sed 's/ ENGINE = InnoDB[^;]*//g' | \
  sed 's/ CHARACTER SET = [^ ]*//g' | \
  sed 's/ COLLATE = [^ ]*//g' | \
  sed 's/ USING BTREE//g' | \
  sed 's/int([0-9]*)/INTEGER/g' | \
  sed 's/varchar([0-9]*)/TEXT/g' | \
  sed 's/datetime([0-9]*)/TEXT/g' | \
  sed 's/tinyint([0-9]*)/INTEGER/g' | \
  sed 's/ AUTO_INCREMENT = [0-9]*//g' | \
  sed 's/ROW_FORMAT = [A-Za-z]*//g' | \
  sqlite3 goodservices.db
```

**For Docker MySQL:**

```bash
docker run -d --name mysql-goodservices \
  -e MYSQL_ROOT_PASSWORD=password \
  -e MYSQL_DATABASE=goodservices \
  -p 3306:3306 mysql:8

docker exec -i mysql-goodservices mysql -uroot -ppassword goodservices < goodservices.sql
```

## Schema Modifications

When modifying the schema:

1. **Always update both files:**

   - Update `goodservices.sql` with DDL changes
   - Update `goodservices_database_documentation.md` to reflect changes

2. **Maintain foreign key integrity:**

   - Core relationships: buser_table ← sr_info ← response_info ← accept_info
   - service_type → sr_info
   - All foreign keys use ON DELETE RESTRICT

3. **Index considerations:**

   - Primary keys are auto-indexed
   - Existing indexes on: psr_userid, stype_id, response_userid, srid, response_id
   - Add indexes for columns frequently used in WHERE/JOIN clauses

4. **State management:**
   - sr_info.ps_state: 0 (published), -1 (cancelled)
   - response_info.response_state: 0 (pending), 1 (accepted), 2 (rejected), 3 (cancelled)

## Important Design Constraints

- **report table issue:** Primary key is only `monthID`, but should be composite `(monthID, stype_id, cityID)` to avoid conflicts
- **No unique constraints:** Missing on buser_table.uname, buser_table.phoneNo, buser_table.idno (should be unique)
- **Password security:** bpwd field stores plain text - should be hashed
- **Sensitive data:** idno (ID numbers) stored unencrypted
- **File storage:** file_list fields contain comma-separated filenames - actual files stored externally

## Common Query Patterns

See `goodservices_database_documentation.md` section 7 for:

- User service request queries
- Response listing for requests
- Service completion records
- Service type statistics
- Active user rankings

## Data Population

Currently all tables are **empty** except:

- `auser_table`: 1 admin user (admin/admin)
- `service_type`: 6 service categories

Test data should populate buser_table first (users), then sr_info (requests), then response_info (responses), then accept_info (completions).

## Document Conversion

**Converting DOCX to Markdown:**

```bash
# Using pandoc (already installed)
pandoc input.docx -o output.md

# Extract images to a folder
pandoc input.docx -o output.md --extract-media=./media

# Without line wrapping
pandoc input.docx -o output.md --wrap=none
```

**Example:**

```bash
pandoc "2025秋季学期-Web开发技术-平时实验作业分组及进展情况说明.docx" -o process.md
```

## Technology Stack

### Backend (Python)

- **FastAPI** 0.104+ - Modern async web framework with auto-generated API docs
- **SQLAlchemy** 2.0+ - ORM for database operations (satisfies persistence requirement)
- **Pydantic** 2.x - Data validation and serialization
- **PyJWT** - JWT authentication
- **Passlib** - Password hashing (BCrypt)
- **Uvicorn** - ASGI server

### Frontend (JavaScript)

- **Vue 3** - Progressive JavaScript framework with Composition API
- **Element Plus** - Vue 3 UI component library
- **ECharts** - Data visualization for statistics module
- **Axios** - HTTP client
- **Pinia** - State management
- **Vue Router** - SPA routing
- **Vite** - Build tool and dev server

### Database

- **MySQL 8.0** - Primary database
- **PyMySQL** - Python MySQL driver

**Course Requirements Met:**
✅ 1 frontend framework (Vue 3)
✅ 2+ backend frameworks (FastAPI web framework + SQLAlchemy ORM persistence framework)

## Specialized Agents

This project uses 15 specialized Claude Code agents to assist development. Invoke them using the Task tool:

### Development Agents

- **Backend Developer** - FastAPI + SQLAlchemy development, RESTful API design, JWT auth
- **Frontend Developer** - Vue 3 + Element Plus development, SPA architecture
- **Database Schema Architect** - MySQL design, optimization, migration with Alembic
- **Component Designer** - Reusable Vue components, design system

### Design & Planning Agents

- **UI Designer** - Element Plus design system, responsive layouts
- **Project Manager** - Task allocation, progress tracking, coordination

### Testing Agents

- **API Tester** - Automated pytest testing for backend APIs
- **E2E Tester** - Playwright end-to-end testing
- **Performance Tester** - Locust load testing and optimization

### Documentation Agents

- **API Doc** - Swagger/OpenAPI documentation, API references
- **User Doc** - User manuals, deployment guides, development docs

### DevOps Agents

- **Deploy** - Docker containerization, CI/CD pipelines
- **Config** - Environment configuration management

Example usage:

```bash
# Launch backend development agent to create authentication module
Task: "Implement user registration and login APIs with JWT authentication"
Agent: Backend Developer

# Launch frontend agent to build statistics dashboard
Task: "Create statistics page with ECharts visualization"
Agent: Frontend Developer
```

## Project Structure (Planned)

```
web_full_stack/
├── backend/                    # FastAPI backend (to be created)
│   ├── app/
│   │   ├── api/v1/            # API routes (auth, users, services, stats)
│   │   ├── models/            # SQLAlchemy ORM models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── crud/              # Database operations
│   │   ├── core/              # Security, config
│   │   └── main.py            # FastAPI app entry
│   ├── tests/                 # pytest test files
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables
├── frontend/                   # Vue 3 frontend (to be created)
│   ├── src/
│   │   ├── views/             # Page components
│   │   ├── components/        # Reusable components
│   │   ├── api/               # API client
│   │   ├── stores/            # Pinia stores
│   │   ├── router/            # Vue Router config
│   │   └── main.js            # Vue app entry
│   ├── package.json           # npm dependencies
│   └── vite.config.js         # Vite configuration
├── goodservices.sql           # Database schema
├── technical_solution.md      # Complete architecture guide
└── subagent_design.md         # Agent workflow documentation
```

## Development Commands

### Backend Setup (When Implementation Starts)

```bash
# Create and activate virtual environment
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Access API documentation
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc

# Run tests
pytest
pytest tests/test_auth.py -v

# Database migrations (Alembic)
alembic init alembic
alembic revision -m "initial migration"
alembic upgrade head
```

### Frontend Setup (When Implementation Starts)

```bash
# Create Vite + Vue 3 project
npm create vite@latest frontend -- --template vue
cd frontend

# Install dependencies
npm install
npm install element-plus axios pinia vue-router echarts

# Run development server
npm run dev
# Access: http://localhost:5173

# Build for production
npm run build

# Preview production build
npm run preview
```

### Database Operations

```bash
# Import schema
mysql -u root -p -e "CREATE DATABASE goodservices;"
mysql -u root -p goodservices < goodservices.sql

# Apply optimizations (recommended)
mysql -u root -p goodservices < db_optimization.sql

# Export database with data
mysqldump -u root -p goodservices > backup.sql

# Docker MySQL (alternative)
docker run -d --name mysql-goodservices \
  -e MYSQL_ROOT_PASSWORD=password \
  -e MYSQL_DATABASE=goodservices \
  -p 3306:3306 mysql:8

docker exec -i mysql-goodservices mysql -uroot -ppassword goodservices < goodservices.sql
```

## Core Business Logic

### Service Matching Flow

```
1. User A publishes service request (sr_info table, ps_state=0)
2. User B browses requests and submits response (response_info, response_state=0)
3. User A reviews responses and accepts one (response_state=1, create accept_info record)
4. Service completion recorded (accept_info with createdate)
5. Monthly statistics aggregated (report table)
```

### State Management

- **Service Requests** (sr_info.ps_state): 0=published, -1=cancelled
- **Responses** (response_info.response_state): 0=pending, 1=accepted, 2=rejected, 3=cancelled

### Password Validation Rules

Required implementation (enforced by Pydantic validators):

- Minimum 6 characters
- At least 2 digits
- Cannot be all uppercase OR all lowercase
- Must be BCrypt hashed before storage

## Course Project Context

This repository is part of a Web Development Technology course assignment (Week 15-17). The `process.md` template should be filled out with:

- Team member information and task division
- Technology stack (language, IDE, OS, database, frameworks)
- Progress updates on completed work

**Deliverables Required:**

- Source code (frontend + backend)
- Database SQL export
- Project report with screenshots
- Team division of labor documentation
- Running environment setup instructions

When working on this project, always consider both the technical implementation and the educational/documentation requirements for the course assignment.

## Key Architecture Decisions

1. **Frontend-Backend Separation**: RESTful API architecture with JWT authentication
2. **Auto-Generated API Docs**: FastAPI automatically generates Swagger/OpenAPI documentation
3. **Type Safety**: Pydantic for runtime validation, Python type hints for development
4. **Layered Architecture**: Router → CRUD → Model separation for maintainability
5. **Statistics Module Priority**: Required feature with ECharts visualization (折线图/柱状图)

## Common Workflows

### Adding a New API Endpoint

1. Define Pydantic schemas in `app/schemas/`
2. Create SQLAlchemy model in `app/models/` (if new table)
3. Implement CRUD operations in `app/crud/`
4. Add route handler in `app/api/v1/`
5. Write tests in `tests/`
6. Verify in Swagger docs at `/docs`

### Adding a New Frontend Page

1. Design UI using Element Plus components
2. Create view component in `src/views/`
3. Add route in `src/router/index.js`
4. Create API client functions in `src/api/`
5. Add navigation link in layout
6. Implement state management if needed (Pinia)

For detailed implementation guidance, refer to `technical_solution.md` which contains complete code examples and patterns.
