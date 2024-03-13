// Rule to identify common obfuscation methods in Python code
rule eval_Obfuscation
{
    meta:
        description = "Identify when a package uses a common obfuscation method often used by malware"
        severity = "WARNING"

    strings:
        $obfuscation1 = "eval(\"\\145\\166\\141\\154\")"
        $obfuscation2 = "eval(\"\\x65\\x76\\x61\\x6c\")"
        $obfuscation3 = "___=eval("

    condition:
        any of them
}
