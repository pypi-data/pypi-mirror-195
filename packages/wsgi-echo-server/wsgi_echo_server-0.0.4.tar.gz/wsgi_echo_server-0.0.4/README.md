# wsgi-echo-server

A wsgi and http echo server.


## How to use

```shell
docker run -e "WSGI_PORT=9000" ghcr.io/buserbrasil/wsgi-echo-server
```

## Response

```
{
    "environment": {
        "PATH_INFO": "/",
        "QUERY_STRING": "",
        "RAW_URI": "/",
        "REMOTE_ADDR": "127.0.0.1",
        "REQUEST_METHOD": "GET",
        "REQUEST_URI": "/",
        "SCRIPT_NAME": "",
        "SERVER_NAME": "localhost",
        "SERVER_PORT": "80",
        "SERVER_PROTOCOL": "HTTP/1.1"
    },
    "host": {
        "hostname": "mockedhostname"
    },
    "http": {
        "method": "GET"
    },
    "request": {
        "body": "",
        "cookies": {},
        "headers": {
            "host": "localhost",
            "user-agent": "werkzeug/2.2.3"
        },
        "query": {}
    }
}
```
