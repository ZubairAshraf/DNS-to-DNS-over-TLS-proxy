import socket
import ssl
import sys
import thread       
import binascii

#-----Add Length to query datagram
def dnsquery(dns_query):
  pre_length = "\x00"+chr(len(dns_query))
  _query = pre_length + dns_query
  return _query

#-----Send Qquery to cloudfare server to get result
def sendquery(tls_conn_sock,dns_query):
  tcp_query=dnsquery(dns_query)
  tls_conn_sock.send(tcp_query)
  result=tls_conn_sock.recv(1024)
  return result

  
#------TLS connection with cloudflare server  
def tcpconnection(DNS):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.settimeout(10)
  context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
  context.verify_mode = ssl.CERT_REQUIRED
  context.load_verify_locations('/etc/ssl/certs/ca-certificates.crt')
  wrappedSocket = context.wrap_socket(sock, server_hostname=DNS)
  wrappedSocket.connect((DNS , 853))
  print(wrappedSocket.getpeercert())
  return wrappedSocket

#------ handle requests
def requesthandle(data,address,DNS):
  tls_conn_sock=tcpconnection(DNS) 
  tcp_result = sendquery(tls_conn_sock, data)
  if tcp_result:
     rcode = tcp_result[:6].encode("hex")
     rcode = str(rcode)[11:]
     if (int(rcode, 16) ==1):
        print ("not a dns query")
     else:
	udp_result = tcp_result[2:]
        s.sendto(udp_result,address)
        print ("200")   
  else:
     print ("not a dns query")

if __name__ == '__main__':
   DNS = '1.1.1.1'
   port = 53
   host='172.168.1.2'
   try:
      s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      s.bind((host, port))
      while True:
        data,addr = s.recvfrom(1024)
        thread.start_new_thread(requesthandle,(data, addr, DNS))
   except Exception, e:
      print (e)
      s.close()
                      



  







