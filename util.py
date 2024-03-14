import argparse
import os
import subprocess
from pprint import pprint
import re
import numpy as np
import base64
import ast
import io
import binascii
import traceback
import sys

from features.features import SnippetStats
from features.features_model import Features
from features import yara_features
from features.paper_features import get_paper_features

class Util:
    def __init__(self):
        parser = argparse.ArgumentParser(description="Scan a folder using YARA")
        parser.add_argument("folder", help="Folder path to scan")
        parser.add_argument("--output", "-o", help="Output file path", default="output.json")
        self.args = parser.parse_args()

        yara_path = "./yara"
        self.yara_rules = yara_features.load_yara_rules(yara_path)
    
    def get_args(self):
        return self.args
    
    def folder_exists(self):
        if not os.path.isdir(self.args.folder):
            raise Exception("Error: Folder does not exist.")
    
    def list_python_files(self):
        python_files = []

        for root, dirs, files in os.walk(self.args.folder):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))

        return python_files
    
    def generate_features(self, python_files):
        results = []
        for file in python_files:

            with open(file, 'r') as file_to_be_read:
                try:
                    file_content = file_to_be_read.read()
                    result = dict()
                    parts = file.split('/')
                    last_part = parts[-1]
                    result["file_name"] = last_part

                    if file_content:
                        shanon_results = self.generate_statistic_features(file_content)
                        result.update(shanon_results)

                    stripped_file = file_content.replace(" ", "")
                    stripped_file = stripped_file.replace("\n", "")

                    if stripped_file:
                        result.update(self.generate_paper_features(file_content))
                        result.update(self.generate_yara_features(self.yara_rules, file))
                        results.append(result)
                except:
                    print("An exception occurred:", sys.exc_info()[0])  # Print exception info
                    traceback.print_exc()  # This will print the stack trace to stderr
        return results
                
    def generate_statistic_features(self, file_content):
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
        return shanon_results
    
    def generate_yara_features(self, yara_rules, file):
        result = dict()
        for rule in yara_rules:
            yara_result = yara_features.run_yara_rule(rule, file)
            result.update(yara_result)
        return result
    
    def generate_paper_features(self, file_content):
        return get_paper_features(file_content)


            