# Enterprise DevSecOps Workflow Adoption Guide
**Author:** Rahul Motvani ([GitHub](https://github.com/rahulmotvani0-sketch) · [Portfolio](https://rahul.techiking.com))

---

## 🚀 3-Minute Quickstart

To adopt this production-grade DevSecOps pipeline in any application repository (Go, Python, Node, Java, Rust), add a single workflow file to your repo:

### `.github/workflows/security.yml`
```yaml
name: Security & Quality Gates

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

permissions:
  contents: read
  id-token: write          # Required for Sigstore Cosign keyless image signing
  security-events: write   # Required for native GitHub Code Scanning SARIF tab

jobs:
  devsecops:
    name: DevSecOps Quality Gate
    uses: rahulmotvani0-sketch/devsecops-secure-cicd-template/.github/workflows/devsecops-pipeline.yml@main
    with:
      fail_on_critical: true
      enable_sast: true
      enable_sca: true
      enable_iac: true
      enable_container_scan: true
      enable_sbom: true
      enable_cosign: false
      dockerfile_path: "./Dockerfile"
      image_name: "my-app:latest"
```

---

## ⚙️ Input Parameters Reference

| Input | Type | Default | Description |
|:---|:---|:---|:---|
| `fail_on_critical` | `boolean` | `true` | When `true`, halts the pipeline immediately if any CRITICAL severity finding is detected. |
| `enable_sast` | `boolean` | `true` | Executes Semgrep Static Application Security Testing with OWASP Top 10 rules. |
| `enable_sca` | `boolean` | `true` | Executes Aqua Trivy Software Composition Analysis on package manifests. |
| `enable_iac` | `boolean` | `true` | Executes Checkov static scanning against Dockerfiles, Terraform, and K8s manifests. |
| `enable_container_scan` | `boolean` | `true` | Builds the target container and scans it with Trivy against the NVD database. |
| `enable_sbom` | `boolean` | `true` | Generates SPDX 2.3 JSON and CycloneDX 1.5 JSON SBOMs using Anchore Syft. |
| `enable_cosign` | `boolean` | `false` | Cryptographically signs the container image using Sigstore keyless OIDC identity. |
| `dockerfile_path` | `string` | `"./Dockerfile"` | Path to Dockerfile for container build and scan. |
| `image_name` | `string` | `"sample-service:latest"` | Tag name for the built container image. |

---

## 🔒 Recommended GitHub Branch Protection Rule

To prevent vulnerable code from reaching production, configure your repository's branch protection rules:
1. Navigate to **Settings → Branches → Branch protection rules**.
2. Add rule for branch `main`.
3. Check **Require status checks to pass before merging**.
4. Require the following checks:
   - `Secret Leak Detection (Gitleaks)`
   - `SAST Code Analysis (Semgrep)`
   - `Dependency SCA Audit (Trivy)`
   - `IaC Security Scan (Checkov)`
   - `Container Build & Image Scan`

---

## 📊 Viewing Results in Native GitHub Security Tab

All scanners output standard OASIS SARIF v2.1.0 format. Findings automatically appear in:
* **Repository → Security → Vulnerability alerts → Code scanning**
* Pull Requests receive inline line-by-line annotations showing the exact vulnerable line, CVE/CWE reference, and suggested fix!
