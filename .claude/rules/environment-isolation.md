---
paths:
  - "**/infra/**"
  - "**/terraform/**"
  - "**/*.tf"
  - "**/*.tfvars"
  - "**/appsettings*.json"
  - "**/src/environments/**"
  - "**/.github/workflows/**"
  - "**/Dockerfile"
  - "**/*.Dockerfile"
---

# TST and PROD never share anything

This rule exists because PROD auth configuration once reached TST and silently redirected TST users
to production.

- **No value may be identical across TST and PROD**: Key Vault names, connection strings, Entra
  `clientId`s, API scopes, redirect URIs, Terraform state keys, resource groups, image names. When
  you add a setting for one environment, add the other's in the same change and check they differ.
- **Terraform:** `PICA/infra/terraform` is per environment (`environments/<env>` tfvars + backend);
  `PICA.Infrastructure/terraform` is global. Before any `init`/`plan`/`apply`, print and confirm the
  backend (storage account, container, key) you are about to use. `fmt -recursive` and `validate`
  are free; `plan` is read-only; **`apply`/`destroy` against a shared environment needs an explicit
  go-ahead in this conversation** — the guard hook asks for it.
- **Secrets** go to Key Vault (per environment) or user-secrets locally. Never into `appsettings*.json`,
  tfvars, workflow files or a commit.
- **Workflows:** a job that deploys PROD must never be reachable from a push to `main`; prod is a
  `release/*` push and passes the E2E gate. Repo-level variables, not org-level (GitHub Free).
- Changing a container app's image, env vars or scale by hand (`az containerapp update`) is drift:
  make the change in Terraform or the deploy workflow instead.
