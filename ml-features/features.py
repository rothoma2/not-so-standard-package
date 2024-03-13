
import re
import numpy as np
import base64
import ast
import io
import binascii

# 1. Number of words in file
def count_words(file_content):
    words = file_content.split()
    return ("number_of_words", len(words))

# 2. Number of lines in file
def count_lines(file_content):
    lines = file_content.split("\n")
    return ("number_of_lines", len(lines))

# 3. Number of URLs in file
def count_urls(file_content):
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', file_content)
    return ("number_of_urls", len(urls))

# 4. Number of IP addresses in file
def count_ips(file_content):
    ips = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', file_content)
    return ("number_of_ip_addresses", len(ips))

# 5. Revised Statistics on ratio of square brackets per line
def square_brackets_stats(file_content):
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
def equal_signs_stats(file_content):
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
def plus_signs_stats(file_content):
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

def obfuscated_code_python(file_content):
    matches = re.findall(r'(?s)\"\"*[^\']*\"\"*|\'\'*[^\']*\'\'*', file_content)
    counter = 0
    stripped_matches = [match.strip('\"\'') for match in matches]
    for match in stripped_matches:
        try:
            decoded_data = base64.b64decode(match.encode())
            module = ast.parse(io.BytesIO(decoded_data).read().decode())
            counter += 1
        except(SyntaxError, UnicodeDecodeError, binascii.Error):
            pass
    return ("obfuscated_code_python", counter)

def malicious_dependencies(file_content, blacklist):
    tree = ast.parse(file_content)
    dependencies = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                dependencies.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                dependencies.append(alias.name)
                if node.module:
                    dependencies.append(node.module)

    blacklisted_count = sum(1 for dependency in dependencies if dependency in blacklist)

    return {"blacklisted_dependencies": blacklisted_count}