
(See `src/*` for the complete tree.)

---

## 🔐 Authentication & RBAC

* **`app/auth/security.py`** – JWT encoding/decoding using `Settings`.  
  Provides `authenticate_user`/`authenticate_role` dependencies; raises exceptions
  defined in `http_exceptions.py`.

* **`app/auth/password_utils.py`** – wraps a `passlib` `CryptContext`
  configured via `Settings.HASHING_ALGORITHM`.

* Routes in `app/router/auth_router.py` call service functions from
  `app/services/auth_services.py`.

* RBAC enums (`RolesEnum`, `PermissionsEnum`) live in `core/enums.py`; mappings
  are in `schemas/rbac_schemas.py` / `app/schemas/rbac_schemas.py`.

---

## 🗃️ Database models & seeding

* SQLModel classes for users, roles and permissions are in
  `db/models/user_models.py` and `db/models/rbac_models.py` with many‑to‑many
  relationships via `UsersRoles` and `RolePermissions`.

* Seeding code:
  * `db/seeds/seed_tables.py` creates/drops tables and yields sessions.
  * `db/seeds/seed_rbac.py` populates the `permissions`, `roles` and linkage
    tables, using the enums and mapping.

* Lifecycle helper `db/database_lifecycle.py` runs `create_tables()` and seeds
  on startup and drops on cleanup; invoked by `app/main.py`.

---

## 🧩 Schemas

Two sets of schemas exist: under `src/schemas/` for generic/core use, and under
`src/app/schemas/` for the application layer. They define `UserBase`,
`UserRegister`, `UserCreatedResponse`, etc., all inheriting from `SQLModel`
so they double as ORM bases and pydantic models. Email validation and
unique/index constraints are declared here.

---

## ⚙️ Services

Business logic lives in the `services` package. `auth_services` wraps security
operations used by the router and handles database interactions (user creation,
login, role selection). It uses the models, schemas and helper functions from
`security.py`/`password_utils.py`.

---

## 🚦 Exception handling

Custom handlers convert SQLAlchemy `IntegrityError`s to JSON responses via
`database_handler.py`, mapping index/constraint names defined in
`database_exceptions.py`. HTTP exceptions are formatted uniformly by
`http_handler.py`. Both handlers are wired in `app/main.py`.

---

## ⚙️ Configuration

`settings/settings.py` loads environment variables (`DATABASE_URL`,
`SECRET_KEY`, `ALGORITHM`, `HASHING_ALGORITHM`) using `python-dotenv`.

---

## 🧠 Development notes

The repo reflects the audit in `previous_project_audit.md`:

* clear separation between API, service, repository/DB layers,
* RBAC implemented with enums, seed functions and relationships,
* custom exception handlers,
* pydantic/SQLModel schemas for request/response validation.

For deeper detail, open any of the linked files.