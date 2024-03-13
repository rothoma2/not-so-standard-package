// Rule to identify silent execution of an external binary in Python
rule SilentProcessExecution
{
    meta:
        description = "Identify when a package silently executes an executable"
        severity = "WARNING"

    strings:
        $function_call = /\w+\([^)]*\)/
        $stdout_devnull = /stdout\s*=\s*\w+\.DEVNULL/
        $stderr_devnull = /stderr\s*=\s*\w+\.DEVNULL/
        $stdin_devnull = /stdin\s*=\s*\w+\.DEVNULL/

    condition:
        $function_call and
        2 of ($stdout_devnull, $stderr_devnull, $stdin_devnull)
}
