 <div align="center">

<!-- Minimalist, Ultra-Clean Modern Dark Header -->
<img src="https://capsule-render.vercel.app/api?type=rect&color=0:090D16,100:131C31&height=180&section=header&text=OmniChain%20Core&fontSize=52&fontColor=F8FAFC&fontAlignY=42&desc=Enterprise%20Commerce%20%26%20Supply%20Chain%20Engine%20%7C%20Engineering%20Blueprint&descAlignY=68&descSize=16&descColor=94A3B8" width="100%" />

<br/>

<p align="center">
  <img src="https://img.shields.io/badge/Core_Stack-Python_%E2%80%A2_PostgreSQL_%E2%80%A2_FastAPI_%E2%80%A2_React-0F172A?style=for-the-badge&logo=python&logoColor=38BDF8" />
  <img src="https://img.shields.io/badge/Infrastructure-Docker_%E2%80%A2_Redis_%E2%80%A2_AWS_%E2%80%A2_Kafka_%E2%80%A2_K8s-0F172A?style=for-the-badge&logo=kubernetes&logoColor=38BDF8" />
  <img src="https://img.shields.io/badge/Quality-ACID_%E2%80%A2_OWASP_%E2%80%A2_%3E70%25_Coverage-0F172A?style=for-the-badge&logo=pytest&logoColor=10B981" />
</p>

</div>

---

## 🎯 The Engineering Mission

**OmniChain Core** is an end-to-end, production-grade Commerce & Supply Chain platform built to solve four real-world distributed systems challenges:
1. **Zero-Overselling Guarantee:** Atomic row-level locking in PostgreSQL during high-concurrency flash sales.
2. **Sub-Millisecond Discovery:** Multi-layer Redis caching and semantic AI vector search across massive product catalogs.
3. **Zero-Trust Security:** Stateless JWT authentication, strict Role-Based Access Control (RBAC), rate limiting, and OWASP Top 10 hardening.
4. **Fault-Tolerant Async Processing:** Decoupling payment captures and notifications via event queues so traffic spikes never degrade API latency.

---

## 🧭 Progressive Build Architecture (How 6 Modules Become 1 Platform)

Rather than writing monolithic tutorial code, this platform is engineered incrementally across **6 standalone repositories** (Months 1–6) and unified into **Project 7 (Capstone)** & **Phase 8 (Hyperscale)**:

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'background': '#0B0F19', 'primaryColor': '#1E293B', 'primaryTextColor': '#F8FAFC', 'primaryBorderColor': '#38BDF8', 'lineColor': '#64748B', 'secondaryColor': '#0F172A', 'tertiaryColor': '#1E293B', 'fontFamily': 'Inter, system-ui, sans-serif'}}}%%
flowchart LR
    %% Clean Architectural Color Palette
    classDef m1 fill:#0C4A6E,stroke:#38BDF8,stroke-width:2px,color:#F0F9FF;
    classDef m2 fill:#1E3A8A,stroke:#60A5FA,stroke-width:2px,color:#EFF6FF;
    classDef m3 fill:#4C1D95,stroke:#A78BFA,stroke-width:2px,color:#F5F3FF;
    classDef m4 fill:#78350F,stroke:#FBBF24,stroke-width:2px,color:#FFFBEB;
    classDef m5 fill:#064E3B,stroke:#34D399,stroke-width:2px,color:#ECFDF5;
    classDef m6 fill:#831843,stroke:#F472B6,stroke-width:2px,color:#FDF2F8;
    classDef cap fill:#7F1D1D,stroke:#F87171,stroke-width:2.5px,color:#FEF2F2;
    classDef hyp fill:#111827,stroke:#F59E0B,stroke-width:3px,color:#FDE68A;

    subgraph PHASE_1 ["Foundations & Core API"]
        direction TB
        M1["<b>01. SmartStock-CLI-DB</b><br/>Linux • Python OOP • PostgreSQL ACID"]:::m1
        M2["<b>02. CoreAuth-Order-API</b><br/>Flask • FastAPI • JWT/RBAC • Pytest"]:::m2
        M1 -->|"Exposes DB Engine"| M2
    end

    subgraph PHASE_2 ["Experience & Speed"]
        direction TB
        M3["<b>03. OmniStore-Frontend</b><br/>React • TypeScript • Tailwind • Query"]:::m3
        M4["<b>04. SearchMedia-DevOps</b><br/>Redis Cache • Docker • CI/CD Actions"]:::m4
        M3 <-->|"Cached API"| M4
    end

    subgraph PHASE_3 ["Production & Scale"]
        direction TB
        M5["<b>05. CloudShield-Gateway</b><br/>AWS • HTTPS • OWASP Top 10 • CDN"]:::m5
        M6["<b>06. AsyncQueue-Notifier</b><br/>Message Queue • Load Balancer • APIs"]:::m6
        M5 -->|"Offloads Tasks"| M6
    end

    subgraph FINAL ["Enterprise Unification"]
        direction TB
        P7["<b>07. OmniChain-Enterprise</b><br/>Unified Microservices + API Gateway"]:::cap
        P8["<b>08. Hyperscale Upgrade</b><br/>Kafka • Kubernetes • AI Search • Saga"]:::hyp
        P7 ==>|"Scales To"| P8
    end

    PHASE_1 ==> PHASE_2 ==> PHASE_3 ==> FINAL
