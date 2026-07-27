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
```
$ ping 192.168.12.246/24
> ping: 192.168.12.246/24: Name or service not known

$ wtf
> The error occurs because the `ping` command expects a single IP address as its destination, not a CIDR notation (e.g., `192.168.12.246/24`), which is invalid syntax for the `ping` utility in Linux. The `/24` suffix indicates a subnet mask, but the `ping` command processes only host IP addresses (not network ranges), causing the system to interpret the address as invalid and return exit code 2. To resolve this, remove the CIDR notation and use the IP address directly: `ping 192.168.12.246`. This ensures the command targets the correct host without syntax errors.

```

Yes, these are real examples that I actually ran on my machine locally.

## Dependencies
Download and install:
- [Ollama](https://ollama.com/download)
- [Python + pip](https://www.python.org/downloads/)
- [Pipx](https://github.com/pypa/pipx#install-pipx)

## Install
Very soon I plan to create a fancy installer script. But, in the meantime, if there is anyone in the void is dying to try this:

1. Be on Linux (should work on 99% of distros I theorize, but I am on Debian. Windows support in progress.)
3. Run `pipx install git+https://github.com/jacobshultz/wtf`
4. Logout and back in
5. Create directory `~/.config/wtf/`
6. Copy `PROMPT.txt`, `wtf-run.sh`, and `wtf-settings.json` into the new dir
7. Add `source ~/.config/wtf/wtf-run.sh` to `/.bashrc` file
8. Restart terminal if open
9. run `ollama pull qwen3:4b`
10. run `wtf` to run the program.

If that looks intimidating, you can also check back in about a month. By then I should have a fancy installer script for you to run and more instructions on how to get it working with tools, etc.