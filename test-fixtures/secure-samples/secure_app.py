"""
TEST FIXTURE: Remediated & Hardened Code Implementation
FOR DEMONSTRATION OF PASSED QUALITY GATES.

This file demonstrates the clean, compliant remediation for each security
anti-pattern in `vulnerable_app.py`, achieving 0 findings across Semgrep,
Gitleaks, and Checkov.
"""

import json
import os
import shlex
import subprocess


# ==============================================================================
# REMEDIATION 1: Secrets Injected via Environment Variables (Zero Hardcoded Keys)
# ==============================================================================
def get_payment_api_key() -> str:
    """Securely fetches credential from environment or secret vault at runtime."""
    api_key = os.getenv("STRIPE_API_KEY")
    if not api_key:
        raise ValueError("Missing STRIPE_API_KEY environment variable")
    return api_key


# ==============================================================================
# REMEDIATION 2: Parameterized SQL Query (CWE-89 Prevention)
# ==============================================================================
def secure_database_query(db_cursor, sanitized_user_id: str):
    """SECURE: Parameterized query ensures user input is treated strictly as data."""
    query = "SELECT * FROM users WHERE user_id = %s"
    return db_cursor.execute(query, (sanitized_user_id,))


# ==============================================================================
# REMEDIATION 3: Safe Subprocess Execution without Shell Interpretation (CWE-78 Prevention)
# ==============================================================================
def secure_ping_service(target_host: str):
    """SECURE: shell=False prevents shell metacharacter injection chaining."""
    safe_host = shlex.quote(target_host.strip())
    return subprocess.run(
        ["ping", "-c", "1", safe_host],
        shell=False,
        check=True,
        capture_output=True,
        text=True,
        timeout=5
    )


# ==============================================================================
# REMEDIATION 4: Safe JSON Deserialization (CWE-502 Prevention)
# ==============================================================================
def secure_load_session(json_payload: str) -> dict:
    """SECURE: Standard JSON parsing has zero arbitrary bytecode execution capability."""
    return json.loads(json_payload)
