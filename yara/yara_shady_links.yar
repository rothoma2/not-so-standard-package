rule ShadyLinks
{
    meta:
        description = "Identify when a package contains an URL to a domain with a suspicious extension"
        severity = "WARNING"
    strings:
        $shady_extensions = /http[s]?:\/\/.*\.(link|xyz|tk|ml|ga|cf|gq|pw|top|club|mw|bd|ke|am|sbs|date|quest|cd|bid|cd|ws|icu|cam|uno|email|stream)/
    condition:
        $shady_extensions
} 