import requests
import configparser
class request_url:
    cfgpath = ("./config.ini")
    conf = configparser.ConfigParser()
    conf.read(cfgpath, encoding="utf-8")
    url = conf.get("service", "url")
    port = conf.get("service", "port")
    method = conf.get("service", "method")
    last_url = url + ":" + port + "/" + method

    def __init__(self):
        cfgpath = ("./config.ini")
        conf = configparser.ConfigParser()
        conf.read(cfgpath, encoding="utf-8")

    def get_url(self):
        url = self.conf.get("service", "url")
        port = self.conf.get("service", "port")
        method = self.conf.get("service", "method")
        last_url = url+":"+port+"/"+method
        return last_url

if __name__ == '__main__':
    # response = requests.get("http://192.168.0.122:8081/hello")
    response = requests.get(request_url.last_url)
    details = response.content
    print(details)