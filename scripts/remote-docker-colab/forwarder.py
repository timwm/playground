from mitmproxy import http

# Replace this with whatever url was displayed to you on the remote machine 
# in the last step (1.e)
REMOTE = "https://cactus-xyz-123.loca.lt"

def request(flow: http.HTTPFlow) -> None:
    flow.request.host = REMOTE.replace("https://", "").replace("http://", "")
    flow.request.scheme = "https"
    flow.request.port = 443
    flow.request.headers["Host"] = flow.request.host
    flow.request.headers["bypass-tunnel-reminder"] = "1"

    # Optionally rewrite Origin/Referer headers for Colab
    if "Origin" in flow.request.headers:
        flow.request.headers["Origin"] = REMOTE
    if "Referer" in flow.request.headers:
        flow.request.headers["Referer"] = REMOTE

