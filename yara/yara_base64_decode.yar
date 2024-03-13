rule method_base64_b64decode
{
    strings:
        $text = /b64decode\(.*\)/
    condition:
        $text
}
