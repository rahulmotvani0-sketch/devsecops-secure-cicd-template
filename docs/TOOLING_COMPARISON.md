# DevSecOps Tooling Comparison & Architecture Rationale
**Author:** Rahul Motvani ([GitHub](https://github.com/rahulmotvani0-sketch) · [Portfolio](https://rahul.techiking.com))

---

## 1. SAST: Semgrep OSS vs. SonarQube Community vs. Snyk Code

| Dimension | Semgrep OSS (Selected) | SonarQube Community | Snyk Code |
|:---|:---|:---|:---|
| **Execution Architecture** | Fast, lightweight AST engine running inside runner container (<30s). | Heavyweight client-server architecture requiring external server instance or VM. | Cloud-hosted SaaS engine requiring source code egress. |
| **Custom Rule Syntax** | Declarative YAML matching pattern code directly (`$VAR == $VAL`). | Complex Java custom plugin development. | Proprietary rules engine. |
| **SARIF & CI Integration** | Native SARIF v2.1.0 output into GitHub Actions. | Requires SonarQube server token and quality gate webhook. | Requires Snyk API token and plan limits. |
| **Cost** | 100% Free & Open-Source. | Free Community Edition (lacks PR decoration in basic tier). | Freemium (limited monthly test runs). |
| **Why We Picked Semgrep:** | Zero server maintenance, sub-minute execution times, completely offline-friendly, and native PR-blocking capability. |

---

## 2. SCA: Aqua Trivy vs. Snyk vs. Dependabot

| Dimension | Aqua Trivy (Selected) | Snyk CLI | GitHub Dependabot |
|:---|:---|:---|:---|
| **Scan Breadth** | Unified scanner for OS packages, language dependencies, containers, and licenses. | Strong vulnerability DB, separate container and code commands. | Manifest-only dependency checking (does not scan built containers). |
| **Execution Context** | Local CLI or composite action, zero cloud egress. | Requires Snyk account authentication. | Native GitHub backend job. |
| **False-Positive Tuning** | Simple `.trivyignore` file with documented justifications. | Web UI or `.snyk` policy file. | Dismiss button in UI only. |
| **Speed** | Downloadable cached DB, parses lockfiles in under 10 seconds. | Cloud API round-trips. | Asynchronous PR generation. |
| **Why We Picked Trivy:** | Single unified tool for both Dependency SCA and Container Image CVE scanning with zero external API dependencies. |

---

## 3. Secret Detection: Gitleaks vs. TruffleHog vs. Git-secrets

| Dimension | Gitleaks (Selected) | TruffleHog v3 | Git-secrets |
|:---|:---|:---|:---|
| **Scanning Speed** | Extremely fast Go binary; scans 10,000 commits in ~3 seconds. | Fast, but heavier detector suite with active API canary verification. | Regex-only Bash script; prone to high false-positive noise. |
| **False-Positive Tuning** | Declarative `.gitleaks.toml` with regex, path, and entropy allowlists. | Flag-based exclusions. | Pattern-based allowlists. |
| **Active Verification** | Safe offline pattern & entropy matching without triggering canary alarms. | Can make live network calls to verify token validity (can accidentally trigger canary alerts). | Purely offline regex. |
| **Why We Picked Gitleaks:** | Industry gold-standard in CI pipelines, zero network noise, sub-second PR scanning, and native SARIF reporting. |

---

## 4. Supply Chain: Sigstore Cosign vs. Docker Content Trust (Notary)

| Dimension | Sigstore Cosign (Selected) | Docker Content Trust (Notary v1/v2) |
|:---|:---|:---|
| **Key Management** | **Keyless OIDC:** Signs using ephemeral OIDC tokens from GitHub Actions. No private keys to rotate or compromise! | Requires managing and protecting long-lived root and repository private signing keys. |
| **Auditability** | Public Rekor transparency log provides tamper-evident proof of signature time and builder identity. | Centralized TUF server metadata. |
| **SLSA Compatibility** | Native support for SLSA provenance attestations and in-toto metadata. | Basic image tagging signature only. |
| **Industry Adoption** | Adopted by Kubernetes, OpenSSF, Linux Foundation, Google Cloud, and AWS. | Deprecated / transitioning to Notary v2. |
| **Why We Picked Cosign:** | Keyless signing eliminates catastrophic private key leakage risks while meeting SLSA Build Level 3 requirements. |
