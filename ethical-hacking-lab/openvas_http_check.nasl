# Safe coursework-only NASL check for the controlled localhost target.
# It sends an HTTP OPTIONS request to TCP/8080 and reports whether TRACE is advertised.

port = 8080;
soc = open_sock_tcp(port);
if (!soc) {
  display("OpenVAS NASL assessment\n");
  display("Target TCP/8080 is not reachable.\n");
  exit(0);
}

req = "OPTIONS / HTTP/1.0\r\nHost: 127.0.0.1\r\n\r\n";
send(socket:soc, data:req);
resp = recv(socket:soc, length:4096);
close(soc);

display("OpenVAS NASL HTTP assessment of 127.0.0.1:8080\n");
display(resp, "\n");

if ("TRACE" >< resp) {
  display("Finding: TRACE is enabled and advertised by the web service.\n");
} else {
  display("Finding: TRACE was not advertised by the web service.\n");
}
