from typing import Dict, List, Optional, TypedDict


Headers = TypedDict("Headers", {
    "Allow": str,
    "CF-Cache-Status": str,
    "CF-RAY": str,
    "Cache-Control": str,
    "Connection": str,
    "Content-Encoding": str,
    "Content-Type": str,
    "Cross-Origin-Opener-Policy": str,
    "Date": str,  # important for record info
    "Expires": str,  # important for record info
    "RateLimit-Limit": str,  # used for ratelimit manager
    "RateLimit-Remaining": str,  # used for ratelimit manager
    "RateLimit-Reset": str,  # used for ratelimit manager
    "Referrer-Policy": str,
    "Server": str,
    "Transfer-Encoding": str,
    "Vary": str,
    "Version": str,
    "Via": str,
    "WWW-Authenticate": str,
    "X-Content-Type-Options": str,
    "X-Frame-Options": str,
    "X-Kong-Proxy-Latency": str,
    "X-Kong-Upstream-Latency": str,
    "X-RateLimit-Limit-Minute": str,
    "X-RateLimit-Remaining-Minute": str,
})

# example
# {'Allow': 'GET, HEAD, OPTIONS',
#  'CF-Cache-Status': 'DYNAMIC',
#  'CF-RAY': '8367df12ac6b7233-CGK',
#  'Cache-Control': 'max-age=120',
#  'Connection': 'keep-alive',
#  'Content-Encoding': 'gzip',
#  'Content-Type': 'application/json',
#  'Cross-Origin-Opener-Policy': 'same-origin',
#  'Date': 'Sat, 16 Dec 2023 15:13:38 GMT',
#  'Expires': 'Sat, 16 Dec 2023 15:15:37 GMT',
#  'RateLimit-Limit': '180',
#  'RateLimit-Remaining': '179',
#  'RateLimit-Reset': '23',
#  'Referrer-Policy': 'same-origin',
#  'Server': 'cloudflare',
#  'Transfer-Encoding': 'chunked',
#  'Vary': 'Cookie, origin',
#  'Version': 'v3.2',
#  'Via': 'kong/3.2.2',
#  'WWW-Authenticate': 'Key realm="kong"',
#  'X-Content-Type-Options': 'nosniff',
#  'X-Frame-Options': 'DENY',
#  'X-Kong-Proxy-Latency': '0',
#  'X-Kong-Upstream-Latency': '146',
#  'X-RateLimit-Limit-Minute': '180',
#  'X-RateLimit-Remaining-Minute': '179'}
