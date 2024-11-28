import socket 
import ssl
import argparse 
from  pprint import pprint
from urllib.parse import urlparse



def get_http(host):
    port = 80
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((host,port))
            request = f"GET / HTTP/1.1\r\nHost: {host}\r\n\r\n"
            client.sendall(request.encode())
            buff = client.recv(1024).decode()
            pprint(buff)
    except Exception:
        print("Port may be closed")

def get_https(host):
    port = 443
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS)
            client = context.wrap_socket(client, server_hostname=host)
            client.connect((host,port))
            request = f"GET / HTTP/1.1\r\nHost: {host}\r\n\r\n"
            client.sendall(request.encode())
            buff = client.recv(1024).decode('utf-8')
            if "301 Moved Permanently" in buff:
                print("Redirecting ...")
                location = [line.split(": ")[1] for line in buff.split("\r\n") if line.startswith('Location')][0]
                get_https(location)
                parsed_url = urlparse(location)
                get_https(parsed_url.hostname)
                buff = client.recv(1024).decode('utf-8')
                pprint(buff)
    except Exception as e:
        print (e)

    
def main():
    parser = argparse.ArgumentParser(description="HTTP/HTTPS Client")
    parser.add_argument('host', help="Host to connect to (e.g., google.com)")
    parser.add_argument('--https', action='store_true', help="Use HTTPS (default is HTTP)")
    args = parser.parse_args()
    
    if args.https:
        get_https(args.host)
    else:
        get_http(args.host)

if __name__ == "__main__":
    main()