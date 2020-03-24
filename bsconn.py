import urllib.request


class Main:
    def __init__(self):
        self.h_oem = ""
        self.h_email = ""
        self.h_machineid = ""
        self.h_vermachineid = ""
        self.h_apitoken = ""
        self.h_vmname = ""
        self.h_googleaid = ""
        self.h_androidid = ""
        self.h_vmid = 0
        self.h_useragent = ""
        self.mode = ""
        self.port = 0
        self.path = ""
        self.body = {}

    def get_response(self):
        url = "http://127.0.0.1:%d%s" % (self.port, self.path)
        headers = {
            "x_oem": self.h_oem,
            "x_email": self.h_email,
            "x_machine_id": self.h_machineid,
            "x_version_machine_id": self.h_vermachineid,
            "x_api_token": self.h_apitoken,
            "vmname": self.h_vmname,
            "x_google_aid": self.h_googleaid,
            "x_android_id": self.h_androidid,
            "vmid": self.h_vmid,
            "User-Agent": self.h_useragent
            }

        body = {}

        if self.body != {}:
            body = self.body
        elif self.mode == "SET_FPS":
            body = {"arg": ""}
        elif self.mode == "SET_SHOWFPSON":
            body = {"isshowfps": 1}
        elif self.mode == "SET_SHOWFPSOFF":
            body = {"isshowfps": 0}
            
        req_method = "GET"
        
        if body != {}:
            req_method = "POST"
            
        body = urllib.parse.urlencode(body).encode("utf-8")
        req = urllib.request.Request(url, bytes(body), headers, method=req_method)
        print("====================")
        print(">> Mode: %s" % (self.mode))
        print(">> Sending request to: %s" % (url))
        print(">> HTTP Request Method: %s" % (req_method))
        print(">> Headers:")
        print(headers)
        print(">> Body:")
        print(body.decode("utf-8"))
        
        try:
            with urllib.request.urlopen(req, timeout=1) as f: # Timeout = 1 because of local connection
                resp = f.read().decode("utf-8")
                print(">> Response:")
                print(resp)
                print("====================")
                return resp
        except Exception as e:
            print(">> Error:")
            print(e)
            print("====================")
            return ""
        
