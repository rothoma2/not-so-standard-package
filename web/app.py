from flask import Flask, render_template, request
import subprocess
import time
from pathlib import Path
import os
import zipfile
import tarfile
import requests
import json


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_program():
    try:
        # Get the uploaded files
        requirements_file = request.files.get('requirements')
        package_file = request.files.get('package')
        pypi_url = request.form.get('pypi-url')

        # Save the uploaded files to a specific location
        if requirements_file:
            path = f"uploads/{Path(requirements_file.filename).with_suffix('')}_{time.strftime('%Y%m%d-%H%M%S')}.txt"
            requirements_file.save(path)
            process_requirements(path)
        if package_file:
            path = f"uploads/{Path(package_file.filename)}"
            package_file.save(path)
            process_package(path)
        if pypi_url:
            process_pypi(pypi_url)
        
        print('Starting main.py ...')
        result = subprocess.run(['python3', '/opt/not-so-standard-package/main.py', '/opt/web/downloaded_packages/'], cwd="/opt/not-so-standard-package/", capture_output=True, text=True, check=True)
        
        
        print(f"RESULT: {result.stdout}")

        malicious_files = []
        
        # get malicious files
        for line in result.stdout.split('\n'):
            if line.strip():
                line = line.replace("'", '"')
                try:
                    dic = json.loads(line)
                    if dic['malicious'] == 1:
                        malicious_files.append(dic)
                except json.JSONDecodeError:
                    print("Error decoding JSON:", line)

        malicious_detected=False
        confidence_score=0
        chat_gpt_output=''
        if malicious_files:
            malicious_detected=True
            # Get the confidence score for the first file
            confidence_score = malicious_files[0]['confidence_score']

            # Get the filename of the first file
            malicious_filename = malicious_files[0]['filename']

            # Get the ChatGPT output for the first file
            chat_gpt_output = malicious_files[0].get('llm', ' ')

        return render_template('index.html', result=result.stdout, malicious_detected=malicious_detected, confidence_score=confidence_score, chat_gpt=chat_gpt_output)

    except Exception as e:
        error = f"An error occurred: {str(e)}"
        return render_template('index.html', error=error)

def process_requirements(requirements_path):
    try:
        subprocess.check_call(['pip', 'download', '--dest', 'downloaded_packages/', '-r', requirements_path])
    except subprocess.CalledProcessError as e:
        print(f"Error downloading: {e}")

    downloaded_packages_dir = 'downloaded_packages/'

    # Unzip all downloaded packages
    print("Unzipping .whl files")
    for filename in os.listdir(downloaded_packages_dir):
        if filename.endswith('.whl'):
            whl_file = os.path.join(downloaded_packages_dir, filename)
            output_directory = os.path.join(downloaded_packages_dir, filename[:-4])  # Remove .whl extension
            unzip_whl(whl_file, output_directory)

    print("Deleting .whl files")
    # Delete all .whl files
    for filename in os.listdir(downloaded_packages_dir):
        if filename.endswith('.whl'):
            os.remove(os.path.join(downloaded_packages_dir, filename))

def process_package(package_path):
    try:
        # Extract the package into the downloaded_packages directory
        with tarfile.open(package_path, 'r:gz') as tar:
            tar.extractall('downloaded_packages')

        # Rename the extracted folder to match the package name
        extracted_folder = os.path.join('downloaded_packages', os.path.splitext(os.path.basename(package_path))[0])
        os.rename(extracted_folder, os.path.join('downloaded_packages', os.path.splitext(os.path.basename(package_path))[0]))
        
    except Exception as e:
        print(f"Error processing package: {e}")

def process_pypi(pypi_url):
    try:
        r = requests.get(pypi_url)
        filename = pypi_url.split('/')[-1]
        with open(f"uploads/{filename}", 'wb') as file:
            file.write(r.content)
        process_package(f"uploads/{filename}")
        os.remove(f"uploads/{filename}")
    except Exception as e:
        print(f"Error processing PyPI package: {e}")

def unzip_whl(file_path, output_dir):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        # If the directory already exists, skip unzipping
        print(f"Destination directory '{output_dir}' already exists. Skipping unzip.")
        return

    # Open the .whl file
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        # Extract all contents into the output directory
        zip_ref.extractall(output_dir)

if __name__ == '__main__':
    app.run(debug=True)