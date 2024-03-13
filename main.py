import os
import subprocess


def run_yara_files(folder_path):
    print("Method Running Yar Rules")
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            print(file)
            if file.endswith(".yara"):
                yar_file_path = os.path.join(root, file)
                #subprocess.call(["your_command_here", yar_file_path])

def run_yara_rule(yara_path, rule_path, file_path):
    try:
        result = subprocess.run([yara_path,
                                "-r",
                                rule_path,
                                file_path],
                                capture_output=True,
                                text=True,
                                check=True)

        yara_output = result.stdout
        return yara_output
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return None



def feature_placeholder_1(content):
    return ()

def feature_placeholder_2(content):
    return ()

def feature_placeholder_3(content):
    return ()


def main():
    print("Start of Program")
    folder_path = "./yara"
    run_yara_files(folder_path)


if __name__ == "__main__":
    main()