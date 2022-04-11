url = "http://airmon.ufp.pt/api/parse"
headers = {"Content-Type": "application/json", "Accept": "application/json"}
publicKeyCert = "cert/public.pem"

networks = [
    {
    "AUTH": "WPA2E",
    "SSID": "eduroam",
    "USER": "convidado@ufp",
    "PASS": "012938"
    },{
    "AUTH": "WPA2",
    "SSID": "ufp",
    "PASS": ""
    }
    ]
