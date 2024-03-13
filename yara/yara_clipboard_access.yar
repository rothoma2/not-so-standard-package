rule ClipboardAccess
{
    meta:
        description = "Identify when a package reads or writes data from the clipboard"
        severity = "WARNING"

    strings:
        $pyperclipPaste = "pyperclip.paste()"
        $pyperclipCopy = "pyperclip.copy("
        $pandasReadClipboard = "pandas.read_clipboard("
        $varToClipboard = "$VAR.to_clipboard("

    condition:
        any of them
}
