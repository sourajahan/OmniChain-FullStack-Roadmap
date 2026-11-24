<div align="center">

# 📦 SmartStock CLI & DB

**Clean-Architecture Inventory Management System backed by PostgreSQL**  
*Project 01 of the **OmniChain Full-Stack Roadmap***

<p>
  <img src="[https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)" alt="Python" />
  <img src="[https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)" alt="PostgreSQL" />
  <img src="[https://img.shields.io/badge/SQLAlchemy-2.x-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white](https://img.shields.io/badge/SQLAlchemy-2.x-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)" alt="SQLAlchemy" />
  <img src="[https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)" alt="Docker" />
  <img src="[https://img.shields.io/badge/CLI-Typer%20%2B%20Rich-009688?style=for-the-badge&logo=gnubash&logoColor=white](https://img.shields.io/badge/CLI-Typer%20%2B%20Rich-009688?style=for-the-badge&logo=gnubash&logoColor=white)" alt="Typer" />
  <img src="[https://img.shields.io/badge/Tests-Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white](https://img.shields.io/badge/Tests-Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)" alt="Pytest" />
</p>

</div>

---

## ✨ Highlights

- **Strict Layered Architecture:** Clean separation between CLI, Service, Repository, Domain, and Infra.
- **Bulletproof Data Integrity:** Non-negative stock enforced at both the service layer and PostgreSQL (CheckConstraint).
- **Full Audit Trail:** Every stock change is recorded in stock_movements with cascade relations.
- **Versioned Migrations:** Schema evolution managed cleanly via Alembic.
- **Rich Terminal UX:** Color-coded tables and clear feedback powered by Typer & Rich.

---

## 🏗️ Architecture Flow

```mermaid
flowchart LR
    CLI["CLI Layer<br/>(Typer + Rich)"] --> SVC["Service Layer<br/>(Business Rules)"]
    SVC --> DOM["Domain Layer<br/>(Exceptions)"]
    SVC --> REPO["Repository Layer<br/>(SQLAlchemy)"]
    REPO --> INFRA["Infra & DB<br/>(PostgreSQL 16)"]

    style CLI fill:#009688,color:#fff,stroke:#00695c
    style SVC fill:#3776AB,color:#fff,stroke:#1d4e78
    style DOM fill:#E67E22,color:#fff,stroke:#a04000
    style REPO fill:#6C3483,color:#fff,stroke:#4a235a
    style INFRA fill:#4169E1,color:#fff,stroke:#27408b
```

---

## 🧰 Tech Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Core** | Python 3.12+ | Application runtime |
| **Database** | PostgreSQL 16 (Docker) | Persistent relational storage |
| **ORM & Migrations** | SQLAlchemy 2.x, Alembic, psycopg | Models, sessions, and schema versioning |
| **Interface** | Typer & Rich | Interactive, colorized CLI |
| **Quality & Testing** | Pytest, Ruff, Black, Mypy | Automated tests, linting, formatting, typing |

---

## 🚀 Quick Start

```bash
cp .env.example .env
docker compose up -d
alembic upgrade head
pytest
```

---

## 💻 CLI Commands

| Action | Command |
| :--- | :--- |
| **Add Product** | `python -m smartstock add --sku MAC-001 --name "MacBook Pro" --qty 10` |
| **Adjust Stock** | `python -m smartstock adjust --sku MAC-001 --delta -2 --reason "customer order"` |
| **List Inventory** | `python -m smartstock list` |
| **View History** | `python -m smartstock show --sku MAC-001` |
