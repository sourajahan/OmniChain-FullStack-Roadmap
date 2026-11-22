 ---

# 🚀 Part II: Production Deliverables Architecture

<div align="center">

<img src="https://img.shields.io/badge/SYSTEM_TOPOLOGY-3--TIER_MODULAR_ARCHITECTURE-0F172A?style=for-the-badge&logo=diagramsdotnet&logoColor=38BDF8" />
<img src="https://img.shields.io/badge/CONCURRENCY-ACID_%2B_ROW--LEVEL_LOCKING-064E3B?style=for-the-badge&logo=postgresql&logoColor=34D399" />
<img src="https://img.shields.io/badge/RUNTIME-PYTHON_3.12_%2B_POSTGRES_16-1E1B4B?style=for-the-badge&logo=python&logoColor=FACC15" />

</div>

<br/>

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'background': '#0B0F19', 'primaryTextColor': '#FFFFFF', 'lineColor': '#38BDF8', 'fontFamily': 'JetBrains Mono, Fira Code, monospace'}}}%%
flowchart TB
    classDef client fill:#4C1D95,stroke:#C4B5FD,stroke-width:2px,color:#FFFFFF,rx:10,ry:10;
    classDef app1 fill:#1E3A8A,stroke:#93C5FD,stroke-width:2px,color:#FFFFFF,rx:10,ry:10;
    classDef app2 fill:#831843,stroke:#F9A8D4,stroke-width:2px,color:#FFFFFF,rx:10,ry:10;
    classDef core fill:#065F46,stroke:#6EE7B7,stroke-width:2px,color:#FFFFFF,rx:10,ry:10;
    classDef db fill:#0C4A6E,stroke:#7DD3FC,stroke-width:2.5px,color:#FFFFFF,rx:12,ry:12;

    subgraph INTERFACE_LAYER ["🌐 ENTRYPOINTS & CLIENT INTERFACES"]
        direction LR
        CLI["🖥️ <b>DELIVERABLE 02: SmartStock CLI Engine</b><br/>Terminal Operations • Flash-Sale Checkout • JSON Audit"]:::app1
        API["🔌 <b>DELIVERABLE 03: SmartStock REST Gateway</b><br/>HTTP/JSON Endpoints • CORS • Cookies • Postman Suite"]:::app2
    end

    subgraph DOMAIN_LAYER ["⚙️ SHARED TYPED DOMAIN & CONCURRENCY ENGINE"]
        CORE["🧠 <b>Python 3.12 Core & ACID Transaction Manager</b><br/>@dataclass Models • O(1) dict/set SKU Index • OutOfStockError"]:::core
    end

    subgraph STORAGE_LAYER ["🗄️ RELATIONAL PERSISTENCE ENGINE"]
        DB[("💎 <b>DELIVERABLE 01: Store Relational Database (store_db)</b><br/>PostgreSQL 16 • 3NF Schema • CHECK(stock >= 0) • FOR UPDATE Locks")]:::db
    end

    CLI ==>|"Direct Method Calls"| CORE
    API ==>|"JSON / REST Payloads"| CORE
    CORE ==>|"BEGIN -> SELECT FOR UPDATE -> COMMIT"| DB
