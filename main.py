import json
from util import Util


def main():

    #print("Start of Program")
    Util()
    args = Util.get_args()
    Util.folder_exists()

    python_files = Util.list_python_files()
    top_python_files = python_files[0:500]

    results = Util.generate_features(top_python_files)

    json_string = json.dumps(results)
    print(json_string)

if __name__ == "__main__":
    main()