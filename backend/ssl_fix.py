import ssl
import urllib3

# Disable SSL verification (for development only!)
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)