import numpy as np
import re
import binascii
import base64
import ast 
import io
def feature_count_words(file_content):
    words = file_content.split()
    return {"count_words" : len(words) }

def feature_count_lines(file_content):
    lines = file_content.split("\n")
    return {"number_of_lines": len(lines)}

def feature_count_urls(file_content):
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', file_content)
    return {"number_of_urls": len(urls)}

def feature_count_ips(file_content):
    ips = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', file_content)
    return {"number_of_ip_addresses": len(ips)}


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

def feature_underscore_signs_stats(file_content):
    lines = file_content.split("\n")
    ratios = [line.count("_") / len(line) for line in lines if len(line) > 0]
    mean = np.mean(ratios)
    std_dev = np.std(ratios)
    third_quartile = np.quantile(ratios, 0.75)
    max_value = max(ratios)
    return {
        "underscore_signs_mean": mean,
        "underscore_signs_std_dev": std_dev,
        "underscore_signs_third_quartile": third_quartile,
        "underscore_signs_max_value": max_value
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
        except:
            return {"obfuscated_code_python": 1}
        
    return {"obfuscated_code_python": counter}

def get_paper_features(file_content):
    result = dict()
    file_content = str(file_content)
    result.update(feature_count_words(file_content))
    result.update(feature_count_lines(file_content))
    result.update(feature_count_urls(file_content))
    result.update(feature_count_ips(file_content))
    result.update(feature_square_brackets_stats(file_content))
    result.update(feature_equal_signs_stats(file_content))
    result.update(feature_plus_signs_stats(file_content))
    result.update(obfuscated_code_python(file_content))
    return result