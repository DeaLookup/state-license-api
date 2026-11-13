# DEA Lookup.com State License API

A unified REST API for **real-time primary source verification of state professional licenses in all 50 states and Washington, DC**. Send a license number, state, and professional designation; the API retrieves the result live from the issuing state licensing board and returns the license status, expiration date, and licensee name in JSON or text, with a result code your system can act on.

- **Primary source, live:** every request is retrieved from the state board at the time you ask. There is no aggregated database or stored copy, so each result reflects the board's current record.
- **One API for every state:** a single HTTPS POST request covers all 50 states and Washington, DC, instead of integrating with each state board separately.
- **Physicians, nurses, and more:** MD, DO, PA, NP, dentists, pharmacists, pharmacies, nursing home administrators, and nursing license types including RN, LPN, CNA, licensed midwives, and APRNs.
- **Audit-ready evidence:** an optional primary source view returns the state board's own result page, so you can keep time-stamped proof of each verification for NCQA, URAC, and Joint Commission audits.
- **Pay per lookup:** metered pricing, billed monthly. Run checks whenever you need them.

Website: [dealookup.com](https://www.dealookup.com/) · Product page: [State Medical License API](https://www.dealookup.com/LicenseLookup/State_License_API.asp) · Full documentation: [State License API Documentation](https://www.dealookup.com/LicenseLookup/State_License_API_Documentation.asp) · AI assistants: [State License MCP Usage Guide](https://www.dealookup.com/LicenseLookup/State_License_MCP_Usage_Guide.asp)

---

## Contents

- [Getting access](#getting-access)
- [Making a request](#making-a-request)
- [Professional designations](#professional-designations)
- [Nursing license types](#nursing-license-types)
- [Responses and result codes](#responses-and-result-codes)
- [Errors](#errors)
- [Response times and timeouts](#response-times-and-timeouts)
- [Monitoring licenses on your own schedule](#monitoring-licenses-on-your-own-schedule)
- [Integration tips](#integration-tips)
- [Examples](#examples)
- [Using the API from an AI assistant](#using-the-api-from-an-ai-assistant)
- [Support](#support)

## Getting access

The State License API is available to DEA Lookup.com subscribers. After you subscribe, you receive:

- API credentials (username and password) for your account
- The API endpoint address
- Access to a test interface, so you can try requests before you integrate

The endpoint address is provided with your subscription and is not published here. To evaluate the API, email [sales@dealookup.com](mailto:sales@dealookup.com) to schedule a demo.

## Making a request

Send an HTTPS `POST` request with form-encoded parameters (`application/x-www-form-urlencoded`) to the endpoint provided with your subscription. Parameters 1 through 5 are required.

| # | Parameter | Required | Description |
|---|---|---|---|
| 1 | `username` | Yes | Your API username. |
| 2 | `password` | Yes | Your API password. |
| 3 | `SL_n` | Yes | State license number. |
| 4 | `SL_s` | Yes | Two-letter state code, for example `CA`, or `DC` for Washington, DC. |
| 5 | `SL_pd` | Yes | Professional designation. See [professional designations](#professional-designations). |
| 6 | `SL_pd_nursing` | No | Nursing license type, used with `SL_pd=NP`. See [nursing license types](#nursing-license-types). |
| 7 | `SL_ln` | No | Last name, in uppercase. Optional and usually not needed. Adds a check that the license belongs to this person, which helps in the few states that return more than one result for a license number. |
| 8 | `SL_psView` | No | Set to `on` to return the state board's own result page (primary source view). Default is off. |
| 9 | `OutputFormat` | No | `JSON` for JSON output, or `HTMLdisplay` for text output suited to testing. Default is `HTMLdisplay`. |

Example (cURL):

```bash
curl -X POST "$SL_API_ENDPOINT" \
  --max-time 200 \
  -d "username=$SL_API_USERNAME" \
  -d "password=$SL_API_PASSWORD" \
  -d "SL_n=A123456" \
  -d "SL_s=CA" \
  -d "SL_pd=MD" \
  -d "SL_ln=DOE" \
  -d "OutputFormat=JSON"
```

## Professional designations

| Code | License type |
|---|---|
| `MD` | Medical Doctor |
| `DO` | Doctor of Osteopathic Medicine |
| `PA` | Physician Assistant |
| `NP` | Nurse Practitioner |
| `DDS` | Dentist |
| `RPH` | Pharmacist |
| `RX` | Pharmacy |
| `NHA` | Nursing Home Administrator |

## Nursing license types

For most nursing verifications, set `SL_pd=NP` and leave `SL_pd_nursing` out. To verify a specific nursing license type, set `SL_pd=NP` and add `SL_pd_nursing` with one of these codes:

| Code | License type |
|---|---|
| `ACNA` | Advanced Certified Nurse Aide |
| `CNA` | Certified Nurse Assistant |
| `LPN` | Licensed Practical Nurse |
| `LM` | Licensed Midwife |
| `RN` | Registered Nurse |
| `APRN_NP` | Advanced Practice Registered Nurse, Nurse Practitioner |
| `APRN_CNS` | Advanced Practice Registered Nurse, Clinical Nurse Specialist |
| `APRN_CRNA` | Advanced Practice Registered Nurse, Certified Registered Nurse Anesthetist |
| `APRN_CNM` | Advanced Practice Registered Nurse, Certified Nurse Midwife |

Availability of each license type varies by state.

## Responses and result codes

Every response includes a result code, so your system can route the result without parsing the rest of the response. The one exception is the primary source view: when `SL_psView=on`, the response is the state board's own result page as HTML, with no result code.

| Code | Meaning | Text response |
|---|---|---|
| `1` | License found and validated | `1\|State License API Result: ...` |
| `2` | License not found | `2\|License not found.` |
| `3` | License found, but the last name does not match | `3\|License invalid: Name mismatch.` |
| `4` | Error (see [errors](#errors)) | `4\|Error\|[message]` |

JSON response, license found ([samples/validated.json](samples/validated.json)):

```json
{
  "Result": 1,
  "ResultLabel": "LicenseValidated",
  "ResultDetail": "State license board website data found.",
  "State License": "A123456",
  "State": "CA",
  "Status": "LICENSE RENEWED & CURRENT",
  "Expires": "MARCH 31, 2028",
  "Name": "DOE, JANE A",
  "PD": "MD"
}
```

JSON response, license not found ([samples/not-found.json](samples/not-found.json)):

```json
{
  "Result": 2,
  "ResultLabel": "License not found.",
  "ResultDetail": "License number invalid or no longer reported on state board site."
}
```

JSON response, name mismatch ([samples/name-mismatch.json](samples/name-mismatch.json)):

```json
{
  "Result": 3,
  "ResultLabel": "License invalid: Name mismatch.",
  "ResultDetail": "The last name submitted does not match to this license."
}
```

Text response, license found ([samples/validated.txt](samples/validated.txt)):

```text
1|State License API Result:
State License: A123456
State: CA
Status: LICENSE RENEWED & CURRENT
Expires: MARCH 31, 2028
Name: DOE, JANE A
PD: MD
```

`Status` and `Expires` are reported as each state board words them, so the same status or date can be formatted differently from state to state. Route on the result code, not the status text. Example data is fictional.

### Disciplinary information

The result reports license status and expiration. Disciplinary information, where a state publishes it, is found in the primary source page (`SL_psView=on`). Every state reports disciplinary data differently, and some report little or none.

## Errors

Errors return result code `4` with a message. In JSON output the message is in `ErrorDetail` ([samples/error.json](samples/error.json)):

```json
{
  "Result": 4,
  "ResultLabel": "Error",
  "ErrorDetail": "Invalid login."
}
```

| Message | What to do |
|---|---|
| `Invalid login` | Check your API username and password. |
| `Expired login` | Your API account has expired. Contact [customerservice@dealookup.com](mailto:customerservice@dealookup.com). |
| `No state license number entered.` | Include `SL_n`. |
| `No state entered.` | Include `SL_s`. |
| `No professional designation entered.` | Include `SL_pd`. |
| `Name cannot be a number.` | Send a last name in `SL_ln`, not a number. |
| `State License API not available in [state] for professional designation [PD]` | That license type is not supported in that state. |
| `State website failure, try again.` · `Unable to reach the state database.` · `State website changed or is temporarily down.` · `State license website was slow to respond and timed out. Try again.` | The state board's website is unavailable or slow. Retry later. |
| `Unrecognized response. Try again.` · `Data link failed. Try again.` · `Unknown error.` and other "try again" messages | Temporary retrieval problem. Retry the request. |

Errors caused by a state website being slow or unavailable are usually temporary, and retrying later normally succeeds.

## Response times and timeouts

Because each result comes live from the state board, response time depends on the state. Most states respond within a few seconds. A small number of state websites are slower and can take 30 seconds or more while still returning a valid result.

- Set your client timeout to **200 seconds**. Responses over 100 seconds are rare and limited to a few states.
- For high-volume checks, send requests in parallel rather than one after another.

## Monitoring licenses on your own schedule

Because every request is a live primary source check, you monitor licenses by running checks on the schedule that fits your risk: daily, weekly, before each shift or order, or before each credentialing decision. Each check is as current as the state board itself, and with per-lookup pricing you pay only for the checks you run. Compare each new result with the last one you stored to catch status changes and approaching expirations.

## Integration tips

- **Send a last name when you want a name check.** `SL_ln` is optional and usually not needed. It helps in the few states that return more than one result for a license number.
- **Route on the result code**, not the status text. Status wording varies by state.
- **Retry state website errors** after a short delay before treating a license as unverified. Don't retry login errors or missing-parameter errors.
- **Store each result with the date and time of the check** for your audit trail. Use `SL_psView=on` when you need a copy of the state board's own result page.
- **Keep credentials on your server.** Don't place API credentials in browser code or mobile apps.

## Examples

Set these environment variables first:

```bash
export SL_API_ENDPOINT="https://your-endpoint-from-dealookup"   # provided with your subscription
export SL_API_USERNAME="your-username"
export SL_API_PASSWORD="your-password"
```

| Language | File |
|---|---|
| cURL | [examples/verify_license.sh](examples/verify_license.sh) |
| Python | [examples/verify_license.py](examples/verify_license.py) |
| JavaScript (Node.js 18+) | [examples/verifyLicense.js](examples/verifyLicense.js) |
| C# (.NET 6+) | [examples/VerifyLicense.cs](examples/VerifyLicense.cs) |

An OpenAPI 3.0 description of the request is in [openapi.yaml](openapi.yaml).

## Using the API from an AI assistant

The State License API is also available to AI assistants through the State License MCP server. You add the server to your assistant's connector settings with your API credentials, then ask in plain language to verify a license. The assistant runs the same live primary source lookup and can save the state board's primary source page as proof of licensure.

See the [State License MCP Usage Guide](https://www.dealookup.com/LicenseLookup/State_License_MCP_Usage_Guide.asp) for connection settings, what to provide for a lookup, and troubleshooting.

## Related reading

- [How to Verify a State Medical License in All 50 States](https://www.dealookup.com/how-to-verify-a-state-medical-license.asp)
- [How to Automate Provider Credential Verification: API vs. Manual](https://www.dealookup.com/automate-credential-verification.asp)
- [What Is Primary Source Verification (PSV)? Why the Data Source Matters](https://www.dealookup.com/primary-source-verification.asp)

## Support

Questions, pricing, or a demo: [sales@dealookup.com](mailto:sales@dealookup.com) · 877-482-5400

DEA Lookup.com, Inc. has built primary source verification tools for over 15 years. DEA Lookup.com is not affiliated with the Drug Enforcement Administration or any state licensing board. The example code in this repository is provided under the MIT License; use of the API itself requires a DEA Lookup.com subscription.
