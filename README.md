# What's The Fix
A shell utility which takes error output from any command and has a your local agent research it and provide the fastest routes for fixing it, all without having to `ALT + Tab` out of your shell.

For instance:
```
$ whois jacobshultz
> No whois server is known for this kind of object.

$ wtf
> The command `whois jacobshultz` failed because "jacobshultz" is not a valid domain name or registered entry in WHOIS databases. The `whois` tool searches for domain registrations, not personal names. To resolve this:  
1. Verify if "jacobshultz" is a typo; ensure you are querying a valid domain (e.g., `whois whoisjacob.com` for the domain mentioned in search results).  
2. If seeking information about the person "Jacob Schultz," use search engines or professional networks like GitHub (where his profile exists) instead of WHOIS.  
3. Confirm the domain's existence via DNS lookup tools if attempting to investigate hosting/registration details.
```