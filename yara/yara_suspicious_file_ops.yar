rule Suspicious_File_Operations {
    meta:
        description = "Detects suspicious file operations in Python packages"
        author = "Dennis Vermeulen"
        reference = "Any relevant reference"
    strings:
        $suspicious_file_operations = /open\(|os\.open|os\.chmod|os\.chown|os\.remove|os\.unlink|os\.rmdir|os\.mkdir|os\.listdir|os\.rename|os\.walk/
    condition:
        $suspicious_file_operations
}
