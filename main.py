import json
import os
from util import Util
from machine_learning.ml_model import Model
from pprint import pprint

def main():
    #processing file
    util = Util()
    util.folder_exists()

    top_python_files = util.list_python_files()

    results = util.generate_features(top_python_files)
    pprint(results)
    print(type(results))

    #ML model
    ml_results = []
    for result in results:
        model = Model(json.dumps(result))
        # ml_results.append(model.predict())
        print(model.predict())
    
    args = util.get_args()
    #json_string = json.dumps(ml_results)
    # with open(args.output, "w") as file:
    #     file.write(json_string)

if __name__ == "__main__":
    main()