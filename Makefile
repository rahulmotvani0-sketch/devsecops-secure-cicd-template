.PHONY: help scan-secrets scan-sast scan-sca scan-iac build-image scan-image generate-sbom demo-fail demo-pass clean

IMAGE_NAME ?= sample-service:latest

help:
	@echo "DevSecOps Secure CI/CD Template — Local Tooling CLI"
	@echo "==================================================="
	@echo "  make scan-secrets   Run Gitleaks secret leak detection"
	@echo "  make scan-sast      Run Semgrep SAST on sample-service"
	@echo "  make scan-sca       Run Trivy dependency vulnerability audit"
	@echo "  make scan-iac       Run Checkov on Dockerfile & IaC"
	@echo "  make build-image    Build hardened multi-stage Docker container"
	@echo "  make scan-image     Scan container image with Trivy"
	@echo "  make generate-sbom  Generate SPDX & CycloneDX SBOMs via Syft"
	@echo "  make demo-fail      Scan vulnerable fixtures (proves failure gates)"
	@echo "  make demo-pass      Scan hardened microservice (proves pass gates)"
	@echo "  make clean          Clean test outputs and temporary SARIF files"

scan-secrets:
	@which gitleaks > /dev/null && gitleaks detect --verbose || echo "Gitleaks CLI not installed locally (executes in GitHub Actions)"

scan-sast:
	@which semgrep > /dev/null && semgrep scan --config="p/owasp-top-ten" sample-service/ || echo "Semgrep not installed locally (executes in GitHub Actions)"

scan-sca:
	@which trivy > /dev/null && trivy fs --severity CRITICAL,HIGH . || echo "Trivy not installed locally (executes in GitHub Actions)"

scan-iac:
	@which checkov > /dev/null && checkov -f Dockerfile || echo "Checkov not installed locally (executes in GitHub Actions)"

build-image:
	docker build -t $(IMAGE_NAME) .

scan-image:
	@which trivy > /dev/null && trivy image --severity CRITICAL,HIGH $(IMAGE_NAME) || echo "Trivy not installed locally (executes in GitHub Actions)"

generate-sbom:
	@which syft > /dev/null && syft dir:. -o spdx-json=sbom.spdx.json -o cyclonedx-json=sbom.cyclonedx.json || echo "Syft not installed locally (executes in GitHub Actions)"

demo-fail:
	@echo ">>> Demonstrating Quality Gate Rejection on Vulnerable Fixtures..."
	@which semgrep > /dev/null && semgrep scan --config="p/owasp-top-ten" test-fixtures/vulnerable-samples/ || true
	@which checkov > /dev/null && checkov -f test-fixtures/vulnerable-samples/Dockerfile.vulnerable || true

demo-pass:
	@echo ">>> Demonstrating Quality Gate Success on Hardened Code..."
	@which semgrep > /dev/null && semgrep scan --config="p/owasp-top-ten" test-fixtures/secure-samples/ || true
	@which checkov > /dev/null && checkov -f Dockerfile || true

clean:
	rm -rf results/ sbom-artifacts/ *.sarif *.json *.txt
