# Safe coursework-only NASL check for the controlled localhost target.
# This custom VT connects only to the synthetic TCP/9090 training service.
# The marker represents a deliberately weak configuration in the lab and is not a real CVE.

port = 9090;
soc = open_sock_tcp(port);
if (!soc) {
  display("OpenVAS NASL assessment of 127.0.0.1:9090\n");
  display("Target TCP/9090 is not reachable.\n");
  exit(0);
}

banner = recv_line(socket:soc, length:2048, timeout:5);
close(soc);

display("OpenVAS NASL vulnerability assessment of 127.0.0.1:9090\n");
display("Observed banner: ", banner, "\n");

if ("CYBERLAB-VULN-TEST" >< banner) {
  display("Finding: intentionally weak training configuration detected.\n");
  display("Scope note: synthetic localhost-only finding; not mapped to a real CVE.\n");
} else {
  display("Finding: training vulnerability marker was not detected.\n");
}
