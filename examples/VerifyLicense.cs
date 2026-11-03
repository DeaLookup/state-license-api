// Verify a state license with the DEA Lookup.com State License API (.NET 6+).
// Requires SL_API_ENDPOINT, SL_API_USERNAME and SL_API_PASSWORD environment variables.
// Usage: dotnet run -- A123456 CA MD DOE
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Threading.Tasks;

class VerifyLicense
{
    static async Task Main(string[] args)
    {
        using var http = new HttpClient { Timeout = TimeSpan.FromSeconds(200) }; // some state boards are slow
        var form = new FormUrlEncodedContent(new Dictionary<string, string>
        {
            ["username"] = Environment.GetEnvironmentVariable("SL_API_USERNAME"),
            ["password"] = Environment.GetEnvironmentVariable("SL_API_PASSWORD"),
            ["SL_n"] = args[0],
            ["SL_s"] = args[1],
            ["SL_pd"] = args[2],
            ["SL_ln"] = args.Length > 3 ? args[3].ToUpperInvariant() : "",
            ["OutputFormat"] = "JSON",
        });
        var response = await http.PostAsync(Environment.GetEnvironmentVariable("SL_API_ENDPOINT"), form);
        Console.WriteLine(await response.Content.ReadAsStringAsync());
    }
}
