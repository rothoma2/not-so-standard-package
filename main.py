import os
import subprocess
import argparse
from pprint import pprint
import re
import numpy as np
import json
import base64
import ast
import io
import binascii
import traceback
import sys
import hashlib
import openai
from rich.progress import Progress

openai.organization = "XXX"
openai.api_key = "XXX"
 
model_name="gpt-3.5-turbo"

from features.features import SnippetStats
from features.features_model import Features

args = None


def load_yara_rules(folder_path):
    yara_rules = []
    #print("Method Loading Yar Rules")
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

def list_python_files(directory):
    python_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))

    return python_files

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
        except(SyntaxError, UnicodeDecodeError, binascii.Error):
            pass
    return {"obfuscated_code_python": counter}

def make_shanon_features(package_id:str, package_name:str, file_name:str, file:str):

    snippet_stats = SnippetStats()

    snippet_stats.set_snippet(file)

    snippet_features = Features(
        package_id=package_id,
        package_name=package_name,
        file_name=file_name,
        # quantitative features
        shanon_entropy__file=snippet_stats.shannon_entropy__file(),
        shanon_entropy__number_outliers= snippet_stats.shannon_entropy__file(),
        shanon_entropy__mean= snippet_stats.shannon_entropy__mean(),
        shanon_entropy__median=snippet_stats.shannon_entropy__median(),
        shanon_entropy__variance=snippet_stats.shannon_entropy__variance(),
        shanon_entropy__max= snippet_stats.shannon_entropy__max(),
        shanon_entropy__1Q= snippet_stats.shannon_entropy__1Q(),
        shanon_entropy__3Q= snippet_stats.shannon_entropy__3Q(),
    )
    return(snippet_features)

def calculate_sha1(input_string):
    sha1 = hashlib.sha1()
    sha1.update(input_string.encode('utf-8'))
    sha1_hash = sha1.hexdigest()
    return sha1_hash

def talk_with_chatgpt():

    model_name="gpt-3.5-turbo"
    message = {
            'role': 'user',
            'content': "Hello World. Can you say Hello Back?"
        }
    
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=[message]
    )

    chatbot_response = response.choices[0].message['content']
    print(chatbot_response.strip())

def main():

    global args
    yara_path = "./yara"
    yara_rules = []

    #print("Start of Program")
    parser = argparse.ArgumentParser(description="Scan a folder using YARA")
    parser.add_argument("folder", help="Folder path to scan")
    parser.add_argument("--output", "-o", help="Output file path", default="output.json")

    args = parser.parse_args()

    openai.organization = os.getenv("openai_organization")
    openai.api_key = os.getenv("openai_api_key")


    # Check if the folder exists
    if not os.path.isdir(args.folder):
        print("Error: Folder does not exist.")
        return

    #print(f"Running on folder {args.folder}")
    yara_rules = load_yara_rules(yara_path)
    python_files = list_python_files(args.folder)
    top_python_files = python_files[0:7000]
    #run_yara_files(folder_path)

    results = []
    with Progress() as progress:

        task_count = len(top_python_files)
        task_id = progress.add_task("[green]Processing...", total=task_count)
    
        for file in top_python_files:

            with open(file, 'r') as file_to_be_read:

                try:
                    file_content = file_to_be_read.read()

                    result = dict()
                    parts = file.split('/')
                    last_part = parts[-1]
                    result["file_name"] = last_part
                    result["full_file_path"] = file
                    result["file_hash"] = calculate_sha1(file)

                    if file_content:
                    
                        snippet_stats = SnippetStats()
                        snippet_stats.set_snippet(file_content)
                        snippet_stats.line_entropy()
                        
                        shanon_results = {
                        "shanon_entropy__mean":  snippet_stats.shannon_entropy__mean(),
                        "shanon_entropy__median":  snippet_stats.shannon_entropy__median(),
                        "shanon_entropy__variance":  snippet_stats.shannon_entropy__variance(),
                        "shanon_entropy__max":  snippet_stats.shannon_entropy__max(),
                        "shanon_entropy__1Q":  snippet_stats.shannon_entropy__1Q(),
                        "shanon_entropy__3Q":  snippet_stats.shannon_entropy__3Q(),
                        "shanon_entropy__outliers":  snippet_stats.shannon_entropy__outliers(),
                        }

                        result.update(shanon_results)

                    stripped_file = file_content.replace(" ", "")
                    stripped_file = stripped_file.replace("\n", "")

                    if stripped_file:
                        result.update(feature_count_words(str(file_content)))
                        result.update(feature_count_lines(str(file_content)))
                        result.update(feature_count_urls(str(file_content)))
                        result.update(feature_count_ips(str(file_content)))
                        result.update(feature_square_brackets_stats(str(file_content)))
                        result.update(feature_equal_signs_stats(str(file_content)))
                        result.update(feature_plus_signs_stats(str(file_content)))
                        result.update(obfuscated_code_python(str(file_content)))

                        for rule in yara_rules:
                            yara_result = run_yara_rule(rule, file)
                            result.update(yara_result)

                        results.append(result)
                        progress.update(task_id, advance=1)

                except:
                    print("An exception occurred:", sys.exc_info()[0])  # Print exception info
                    traceback.print_exc()  # This will print the stack trace to stderr


    json_string = json.dumps(results)
    with open(args.output, "w") as file:
        file.write(json_string)

    print("JSON data has been written to", args.output)

    #talk_with_chatgpt()

if __name__ == "__main__":
    main()