"""
TEST FIXTURE: Deliberately Vulnerable Code Samples
FOR DEMONSTRATION AND QUALITY GATE VERIFICATION ONLY.

This file contains commented, deliberate security anti-patterns used to test
that our DevSecOps scanners (Semgrep, Gitleaks, Checkov) reliably detect
vulnerabilities during Pull Request reviews before merging.
"""

import os
import subprocess


# ==============================================================================
# VULNERABILITY 1: Hardcoded API Secret / Credential
# CWE-798: Use of Hard-coded Credentials
# TOOL TRIGGERED: Gitleaks (Rule: generic-api-key) & Semgrep (p/secrets)
# REMEDIATION: Inject credentials at runtime via AWS Secrets Manager or HashiCorp Vault.
# ==============================================================================
# In production, Gitleaks immediately blocks commits matching this entropy pattern.
MOCK_UNENCRYPTED_API_KEY = "insecure_dummy_raw_token_xyz9876543210"  # gitleaks:allow (allowlisted for test fixture)


# ==============================================================================
# VULNERABILITY 2: SQL Injection via String Concatenation
# CWE-89: Improper Neutralization of Special Elements used in an SQL Command
# TOOL TRIGGERED: Semgrep (Rule: python.lang.security.audit.sqli.raw-query)
# REMEDIATION: Use parameterized queries or ORM binds (e.g. cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,)))
# ==============================================================================
def insecure_database_query(db_cursor, untrusted_user_id: str):
    """VULNERABLE: Direct string formatting into SQL query allows payload injection."""
    bad_query = f"SELECT * FROM users WHERE user_id = '{untrusted_user_id}'"
    return db_cursor.execute(bad_query)


# ==============================================================================
# VULNERABILITY 3: Remote Command Injection
# CWE-78: Improper Neutralization of Special Elements used in an OS Command
# TOOL TRIGGERED: Semgrep (Rule: python.lang.security.audit.subprocess-shell-true)
# REMEDIATION: Set shell=False and pass arguments as a list: subprocess.run(["ping", "-c", "1", sanitized_ip])
# ==============================================================================
def insecure_ping_service(untrusted_ip: str):
    """VULNERABLE: shell=True with unescaped input allows arbitrary command chaining (e.g. 8.8.8.8; rm -rf /)."""
    return subprocess.Popen(f"ping -c 1 {untrusted_ip}", shell=True)


# ==============================================================================
# VULNERABILITY 4: Insecure Deserialization
# CWE-502: Deserialization of Untrusted Data
# TOOL TRIGGERED: Semgrep (Rule: python.lang.security.deserialization.pickle)
# REMEDIATION: Use safe serialization formats like JSON (json.loads) instead of pickle.
# ==============================================================================
def insecure_load_session(serialized_user_blob: bytes):
    """VULNERABLE: Python pickle can execute arbitrary bytecode upon deserialization."""
    import pickle
    return pickle.loads(serialized_user_blob)
