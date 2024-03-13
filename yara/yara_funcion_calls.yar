rule Suspicious_Function_Calls {
    meta:
        description = "Detects suspicious function calls in Python packages"
        author = "Your Name"
        reference = "Any relevant reference"
    strings:
        $dangerous_function_calls = /eval\(|exec\(|input\(|pickle\.loads|marshal\(/
    condition:
        $dangerous_function_calls
}