rule Suspicious_Shell_Execution {
    meta:
        description = "Detects suspicious shell command execution in Python packages"
        author = "Dennis Vermeulen"
        reference = ":)"
    strings:
        $shell_commands = /subprocess\.call|subprocess\.Popen|os\.system|os\.popen|os\.execl|os\.execle|os\.execv|os\.execve|os\.spawnl|os\.spawnle|os\.spawnlp|os\.spawnlpe|os\.spawnv|os\.spawnve|os\.spawnvp|os\.spawnvpe/
    condition:
        $shell_commands
}
