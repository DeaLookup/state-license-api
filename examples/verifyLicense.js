// Verify a state license with the DEA Lookup.com State License API (Node.js 18+).
// Requires SL_API_ENDPOINT, SL_API_USERNAME and SL_API_PASSWORD environment variables.
// Usage: node verifyLicense.js A123456 CA MD DOE

async function verifyLicense(licenseNumber, state, designation, lastName = "") {
  const body = new URLSearchParams({
    username: process.env.SL_API_USERNAME,
    password: process.env.SL_API_PASSWORD,
    SL_n: licenseNumber,
    SL_s: state,
    SL_pd: designation,
    SL_ln: lastName.toUpperCase(),
    OutputFormat: "JSON",
  });
  const res = await fetch(process.env.SL_API_ENDPOINT, {
    method: "POST",
    body,
    signal: AbortSignal.timeout(200_000), // some state boards are slow
  });
  const text = await res.text();
  try {
    return JSON.parse(text);
  } catch {
    return { Result: Number(text.split("|")[0]), raw: text };
  }
}

const [n, s, pd, ln] = process.argv.slice(2);
verifyLicense(n, s, pd, ln).then((r) => console.log(r));
