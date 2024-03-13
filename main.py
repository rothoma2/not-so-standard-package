import os
import subprocess
import argparse
from pprint import pprint
import re
import numpy as np
import json

args = None


def load_yara_rules(folder_path):
    yara_rules = []
    print("Method Loading Yar Rules")
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            print(f"Rule {file}")
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

def list_python_files(directory):
    python_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))

    return python_files


# 1. Number of words in file
def feature_count_words(file_content):
    words = file_content.split()
    return len(words)

# 2. Number of lines in file
def feature_count_lines(file_content):
    lines = file_content.split("\n")
    return ("number_of_lines", len(lines))

# 3. Number of URLs in file
def feature_count_urls(file_content):
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', file_content)
    return ("number_of_urls", len(urls))

# 4. Number of IP addresses in file
def feature_count_ips(file_content):
    ips = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', file_content)
    return ("number_of_ip_addresses", len(ips))

# 5. Revised Statistics on ratio of square brackets per line
def feature_square_brackets_stats(file_content):
    lines = file_content.split("\n")
    ratios = [line.count("[") / len(line) for line in lines if len(line) > 0]
    mean = np.mean(ratios)
    std_dev = np.std(ratios)
    third_quartile = np.quantile(ratios, 0.75)
    max_value = max(ratios)
    return {
        "square_brackets_mean": mean,
        "square_brackets_std_dev": std_dev,
        "square_brackets_third_quartile": third_quartile,
        "square_brackets_max_value": max_value
    }

# 6. Revised Statistics on ratio of equal signs per line
def feature_equal_signs_stats(file_content):
    lines = file_content.split("\n")
    ratios = [line.count("=") / len(line) for line in lines if len(line) > 0]
    mean = np.mean(ratios)
    std_dev = np.std(ratios)
    third_quartile = np.quantile(ratios, 0.75)
    max_value = max(ratios)
    return {
        "equal_signs_mean": mean,
        "equal_signs_std_dev": std_dev,
        "equal_signs_third_quartile": third_quartile,
        "equal_signs_max_value": max_value
    }

# 7. Revised Statistics on ratio of plus signs per line
def feature_plus_signs_stats(file_content):
    lines = file_content.split("\n")
    ratios = [line.count("+") / len(line) for line in lines if len(line) > 0]
    mean = np.mean(ratios)
    std_dev = np.std(ratios)
    third_quartile = np.quantile(ratios, 0.75)
    max_value = max(ratios)
    return {
        "plus_signs_mean": mean,
        "plus_signs_std_dev": std_dev,
        "plus_signs_third_quartile": third_quartile,
        "plus_signs_max_value": max_value
    }


def main():

    global args
    yara_path = "./yara"
    yara_rules = []

    print("Start of Program")
    parser = argparse.ArgumentParser(description="Scan a folder using YARA")
    parser.add_argument("folder", help="Folder path to scan")
    args = parser.parse_args()

    # Check if the folder exists
    if not os.path.isdir(args.folder):
        print("Error: Folder does not exist.")
        return

    print(f"Running on folder {args.folder}")
    yara_rules = load_yara_rules(yara_path)
    python_files = list_python_files(args.folder)
    top_python_files = python_files[0:20]
    #run_yara_files(folder_path)

    results = []
    for file in top_python_files:
        with open(file, 'r') as file_to_be_read:
            file_content = file_to_be_read.read()
                
            result = dict()
            parts = file.split('/')
            last_part = parts[-1]
            result["file_name"] = last_part
            result["count_word"] = feature_count_words(str(file_content))

            for rule in yara_rules:
                yara_result = run_yara_rule(rule, file)
                result.update(yara_result)

            results.append(result)

    pprint(results)
    json_string = json.dumps(results)
    #print(json_string)

if __name__ == "__main__":
    main()