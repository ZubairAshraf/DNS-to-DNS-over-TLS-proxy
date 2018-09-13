# DNS-to-DNS-over-TLS-proxy
DNS-Over-TLS server is use to send DNS queries over an encrypted connection, by default, DNS query is sent over the plain text connection.
In this project, DNS-over-TLS proxy server is accepting UDP DNS request from the client and convert it into TCP and send it as a query to CLOUDFLARE DNS-over-TLS server. After getting result from cloudflare it will convert that into UDP again and respond to client.

## Getting Started

Source code: myserver.py

Code is written in Python2.7

In this server, I have used Cloudflare dns-over-tls (1.1.1.1) for quering the client requests.
* It will create a socket connection and bind it with the Docker's network (172.168.1.2) on port 53
* Receive UDP DNS requests on this connection and create a thread for the request and run requesthandler
* RequestHandler will call the function to create TLS connection cloudflare dns server and after that convert UDP request into TCP DNS query and send it to Cloudflare DNS server over the tcp connection, when the server got TCP answer from Cloudflare DNS server, it will convert it into UDP and respond to the client over the same Docker network socket connection
* Currently, It is handling nslookup and dig requests

### Installing

To run this project:
* Create docker image by using Dockerfile which is in the root directory by run this command:
  - docker build -t dns-server .
* Run the container by using that docker image we created in the previous step by run this command:
  - docker run --net testNetwork  -it dns-server
* You can test this by making nslookup or dig request
  - nslookup yahoo.com
  - dig @172.168.1.2 -p 53 google.com
* On successfull response server will give 200 response code

