# 03-OmniStore-Frontend-Portal

Modern, production-ready frontend portal for the **OmniChain FullStack Roadmap (Module 03)**, built to connect directly to `02-CoreAuth-Order-API`.

## Tech Stack & Standards
- **Framework:** React 19 + TypeScript (`strict`) + Vite
- **Styling & a11y:** Tailwind CSS v4, Semantic HTML landmarks, ARIA labels, keyboard skip-links, responsive Flexbox/Grid
- **Routing & Auth:** React Router v7, Protected Routes, Closure-encapsulated token store, automatic JWT refresh on `401`, RFC 7807 `ApiError` parsing
- **Server State:** TanStack Query (`useQuery`, `useMutation`, automatic cache invalidation, loading skeletons, error retry states)
- **Quality & Testing:** Vitest, React Testing Library, Oxlint, TypeScript `tsc -b`, GitHub Actions CI

## Quick Start

```bash
cp .env.example .env
npm install
npm run dev
```

## Quality Checks

```bash
npm run typecheck
npm run lint
npm run test
npm run build
```
