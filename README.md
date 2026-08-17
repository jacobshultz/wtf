# What's The Fix v1.0.0
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

## Min Hardware Reqs
4 core processor and 16 gigs of RAM.

## Dependencies
Download and install:
- [Ollama](https://ollama.com/download)
- [Python + pip](https://www.python.org/downloads/)
- [Pipx](https://github.com/pypa/pipx#install-pipx)

## Install
Supported distros: Windows, Debian (will probably work on other linux distros as well).

Download the appropriate `install` script for your distro from the repo and execute it. Follow any instructions to resolve conflicts.

Configuration is located at `~/.config/wtf`.

Simply delete this directory and remove the lines from `bashrc` (deb) or the powershell profile (win).

## Dev
`pipx install --editable .` in repo dir to get a live dev build of the application.