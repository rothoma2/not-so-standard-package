import json
from util import Util
from machine_learning.ml_model import Model


def main():
    #processing file
    util = Util()
    util.folder_exists()

    top_python_files = util.list_python_files()[0:500]

    results = util.generate_features(top_python_files)

    #ML model
    ml_results = []
    for result in results:
        model = Model(json.dumps(result))
        ml_results.append(model.predict())
    
    print(json.dumps(ml_results))
    
if __name__ == "__main__":
    main()