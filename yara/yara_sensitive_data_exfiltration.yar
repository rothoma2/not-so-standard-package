rule ExfiltrateSensitiveData
{
    meta:
        description = "Identify when a package reads and exfiltrates sensitive data from the local system"
        severity = "WARNING"

    strings:
        $SENSITIVE_DATA_SOURCE1 = "os.environ.items()"
        $SENSITIVE_DATA_SOURCE3 = "socket.gethostname()"
        $SENSITIVE_DATA_SOURCE4 = "getpass.getuser()"
        $SENSITIVE_DATA_SOURCE5 = "platform.node()"
        $SENSITIVE_DATA_SOURCE6 = "browser_cookie3.$BROWSER(...)"
        $SENSITIVE_DATA_SOURCE7 = /open\(([^)]*\.aws\/credentials[^)]*)\)/
        $SENSITIVE_DATA_SOURCE8 = /open\(([^)]*\.docker\/config.json[^)]*)\)/
        $SENSITIVE_DATA_SOURCE9 = /os\.getenv\(([^)]*AWS_ACCESS_KEY_ID[^)]*)\)/ nocase
        $SENSITIVE_DATA_SOURCE10 = /os\.getenv\(([^)]*AWS_SECRET_ACCESS_KEY[^)]*)\)/ nocase
        $SENSITIVE_DATA_SOURCE11 = /os\.getenv\(([^)]*AWS_SESSION_TOKEN[^)]*)\)/ nocase

        $SENSITIVE_DATA_SINK2 = "urllib.request.Request(" 
        $SENSITIVE_DATA_SINK3 = "urllib.urlopen(" 
        $SENSITIVE_DATA_SINK4 = "urllib.request.urlopen(" 
        $SENSITIVE_DATA_SINK5 = "request()" 

    condition:
        any of ($SENSITIVE_DATA_SOURCE*) and any of ($SENSITIVE_DATA_SINK*)
}
