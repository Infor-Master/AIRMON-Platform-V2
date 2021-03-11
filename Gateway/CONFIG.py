url = "https://airmon.ufp.pt/api/parse"
#url = "http://192.168.43.46:4000/api/parse"
headers = {"Content-Type": "application/json", "Accept": "application/json"}
publicKeyCert = "cert/public.pem"

networks = [
    {
    "AUTH": "WPA2E",
    "SSID": "eduroam",
    "USER": "convidado@ufp",
    "PASS": "012938"
    },{
    "AUTH": "WPA2E",
    "SSID": "eduroam",
    "USER": "teste@ufp.pt",
    "PASS": "ola123"
    },{
    "AUTH": "WPA2E",
    "SSID": "eduroam",
    "USER": "36824@ufp.pt",
    "PASS": "250595559"
    },{
    "AUTH": "WPA2",
    "SSID": "",
    "PASS": ""
    }
    ]
