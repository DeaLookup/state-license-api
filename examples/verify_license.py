"""Verify a state license with the DEA Lookup.com State License API.

Requires the `requests` package and these environment variables:
SL_API_ENDPOINT, SL_API_USERNAME, SL_API_PASSWORD.

Usage: python verify_license.py A123456 CA MD DOE
"""
import os
import sys
import time

import requests

RESULT_LABELS = {1: "validated", 2: "not found", 3: "name mismatch", 4: "error"}
# Errors that will not clear on their own, so they are not retried.
NO_RETRY = ("login", "entered", "cannot be a number", "not available")


def verify_license(license_number, state, designation, last_name="", nursing_type="", retries=2):
    data = {
        "username": os.environ["SL_API_USERNAME"],
        "password": os.environ["SL_API_PASSWORD"],
        "SL_n": license_number,
        "SL_s": state,
        "SL_pd": designation,
        "SL_ln": last_name.upper(),
        "OutputFormat": "JSON",
    }
    if nursing_type:
        data["SL_pd_nursing"] = nursing_type
    for attempt in range(retries + 1):
        # Some state boards are slow; allow up to 200 seconds per request.
        resp = requests.post(os.environ["SL_API_ENDPOINT"], data=data, timeout=200)
        resp.raise_for_status()
        try:
            result = resp.json()
            code = int(result.get("Result", 4))
            message = result.get("ErrorDetail", "")
        except ValueError:
            # Non-JSON responses use the text format: "<code>|..."
            result = {"raw": resp.text}
            code = int(resp.text.split("|", 1)[0])
            message = resp.text.rsplit("|", 1)[-1]
        permanent = any(text in message for text in NO_RETRY)
        if code != 4 or permanent or attempt == retries:
            return code, result
        time.sleep(10)  # temporary state website problems usually clear on retry


if __name__ == "__main__":
    code, result = verify_license(*sys.argv[1:5])
    print(f"Result {code} ({RESULT_LABELS.get(code, 'unknown')})")
    print(result)
