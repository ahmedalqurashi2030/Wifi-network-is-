# Ethical Hacking Midterm - Verified Execution Evidence

Active scans were restricted to 127.0.0.1 on an ephemeral GitHub-hosted Ubuntu runner. Footprinting used passive public sources only.

## Required topics and executed tools
- Footprinting: theHarvester, Sublist3r
- Network Scanning: Nmap, Hping3
- Vulnerability Scanning: Nikto, Nmap NSE HTTP assessment scripts
- Enumeration: smbclient, SnmpWalk

## Course-alignment note
The course Vulnerability Analysis slides explicitly present OpenVAS and Nikto. OpenVAS was not used in this ephemeral runner because a complete Greenbone/OpenVAS scanner requires vulnerability feeds and substantially more persistent resources. Nmap NSE was used as the second practical vulnerability-assessment tool; Nmap is taught in the course scanning module. This substitution must be stated rather than presented as OpenVAS execution.

## Evidence integrity
Raw command output is preserved under raw/. Screenshot images are captures of concise selections from those same outputs; no results were invented.
