rule CmdOverwrite
{
    meta:
        description = "Identify when the 'install' command is overwritten in setup.py, indicating a piece of code automatically running when the package is installed"
        severity = "WARNING"

    strings:
        $setup1 = /setup\s*\([^)]*\bcmdclass\s*=\s*{[^}]*('install'|'develop'|'egg_info')[^}]*},/
        $setup2 = /setuptools.setup\s*\([^)]*\bcmdclass\s*=\s*{[^}]*('install'|'develop'|'egg_info')[^}]*},/
    condition:
        any of them
}