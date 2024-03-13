rule Suspicious_Process_Control {
    meta:
        description = "Detects suspicious process control operations in Python packages"
        author = "Dennis Vermeulen"
        reference = "Any relevant reference"
    strings:
        $process_control = /os\.fork|os\.kill|os\.wait|os\.waitpid/
    condition:
        $process_control
}
