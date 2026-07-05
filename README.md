# What's The Fix
A shell utility which takes error output from any command and has a your local agent research it and provide the fastest routes for fixing it, all without having to `Alt + Tab` out of your shell.

For instance:
```
$ whois jacobshultz
> No whois server is known for this kind of object.

$ wtf
> The command `whois jacobshultz` failed because "jacobshultz" is not a valid domain name or registered entry in WHOIS databases. The `whois` tool searches for domain registrations, not personal names. To resolve this:  
> 1. Verify if "jacobshultz" is a typo; ensure you are querying a valid domain (e.g., `whois whoisjacob.com` for the domain mentioned in search results).  
> 2. If seeking information about the person "Jacob Schultz," use search engines or professional networks like GitHub (where his profile exists) instead of WHOIS.  
> 3. Confirm the domain's existence via DNS lookup tools if attempting to investigate hosting/registration details.
```

Yes, that is a real example of output I got on my machine locally.

## Dependencies
Download and install:
- [Ollama](https://ollama.com/download)
- [Python + pip](https://www.python.org/downloads/)

## Running
Very soon I plan to create a fancy installer script. But, in the meantime, if there is anyone in the void is dying to try this:

1. Be on Linux (should work on 99% of distros I theorize, but I am on Debian. Windows support in progress.)
2. Pull the repo
3. Run `pip install --user -e .` in repo dir
4. Logout and back in
5. Create directory `~/.config/wtf/`
6. Copy `PROMPT.txt`, `wtf-run.sh`, and `wtf-settings.json` into the new dir
7. Add `source ~/.config/wtf/wtf-run.sh` to `/.bashrc`
8. Restart terminal if open
9. run `ollama pull qwen3:4b`
10. run `wtf` to run the program.

If that looks intimidating, you can also check back in about a month. By then I should have a fancy installer script for you to run and more instructions on how to get it working with tools, etc.