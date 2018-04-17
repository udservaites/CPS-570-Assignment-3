#from urllib.parse import urlparse # the existing urlparse does not satisfy our requirements
#
# from .py import class
from tcpsocket import TCPsocket  # from tcpsocket.py file import class TCPsocket
from urlparser import URLparser
from request import Request
from queue import Queue

# define a main() function so that variables will be local to main(), instead of global
def main():
    print("Starting ...")
    Q = Queue()
    print("number of urls:", Q.qsize())
    ps = URLparser()    # create an url parser object
    r = Request()       # create an request builder object
    ws = TCPsocket()    # create a tcp socket object
    try:
        with open("URL-input-100.txt") as file:
            for line in file:
                Q.put(line)
    except IOError:
        print('No such file')
        exit(1)

    count = 0
    while not Q.empty():
        url = Q.get()
        count += 1
        print(count)
        print("url: ", url)
        host, port, path, query = ps.parse(url)  # port in int, other returned values are str
    #    print("host: ", host)
    #    print("query: ", query)
    #    print("path: ", path)
        request = r.getRequest(host, path, query)  # host: str, path: str, query: str, request: str
        print("request: ", request)
        ws.crawl(host, port, request)   # host: str, port: int, request: str


# call main() method:
if __name__ == "__main__":
   main()