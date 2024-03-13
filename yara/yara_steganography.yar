rule Steganography
{
    meta:
        description = "Identify when a package retrieves hidden data from an image and executes it"
        severity = "WARNING"

    strings:
        $decodeFunc1 = "steganography.steganography.Steganography.decode("
        $decodeFunc2 = "lsb.reveal("
        $decodeFunc3 = "$SOMETHING.lsb.reveal("

    condition:
        any of them
}
