import os
import subprocess


def load_yara_rules(folder_path):
    yara_rules = []
    print("Method Loading Yar Rules")
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            #print(f"Rule {file}")
            if file.endswith(".yar"):
                yar_file_path = os.path.abspath(os.path.join(root, file))
                yara_rules.append(yar_file_path)
    return yara_rules

def count_yara_hits(content):
    lines = content.split('\n')
    clear_lines = [item for item in lines if item != ""]
    count = 0
    for item in clear_lines:
        if isinstance(item, str) and item.startswith("0x"):
            count += 1
    return count

def run_yara_rule(rule, file_path):
    yara_path = "/usr/bin/yara"
    try:
        result = subprocess.run([yara_path,
                                "-rs",
                                rule,
                                file_path],
                                capture_output=True,
                                text=True,
                                check=True)

        yara_output = result.stdout
        rule_name = os.path.splitext(os.path.basename(rule))[0]
        hits = count_yara_hits(yara_output)
        result = dict({rule_name: hits})
        return dict({rule_name: hits})

    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return None