import json

import xgboost as xgb
from sklearn.preprocessing import OrdinalEncoder
import pandas as pd
import pickle
from pprint import pprint 

class Model:
    def __init__(self, json_content):

        NUM_FEATURES = [
            'count_words', 'number_of_lines', 'number_of_urls', 'number_of_ip_addresses', 'square_brackets_mean', 'square_brackets_std_dev', 'square_brackets_third_quartile', 'square_brackets_max_value', 'equal_signs_mean', 'equal_signs_std_dev', 'equal_signs_third_quartile', 'equal_signs_max_value', 'plus_signs_mean', 'plus_signs_std_dev', 'plus_signs_third_quartile', 'plus_signs_max_value', 'yara_sensitive_data_exfiltration', 'yara_suspicious_process_control', 'yara_shady_links', 'yara_command_overwrite', 'yara_clipboard_access', 'yara_eval_obfuscation', 'yara_base64_decode', 'yara_steganography', 'yara_anti_analysis', 'yara_suspicious_file_ops', 'yara_funcion_calls', 'yara_command_execution', 'yara_silent_process_execution', 'shanon_entropy__mean', 'shanon_entropy__median', 'shanon_entropy__variance', 'shanon_entropy__max', 'shanon_entropy__1Q', 'shanon_entropy__3Q', 'shanon_entropy__outliers', 'obfuscated_code_python'
        ]
        CAT_FEATURES = [
            'file_name_category'
        ]
        self.FEATURES = NUM_FEATURES + CAT_FEATURES

        self.json_content = json_content
        json_data = json.loads(json_content)
        #json_data["shanon_entropy__max"] = 8

        self.pandas_df = pd.DataFrame([json_data])
        print(list(self.pandas_df.columns))

        self.pandas_df['file_name_category'] = self.pandas_df.apply(lambda row: self.file_name_category(row), axis=1)

        encoder_path = 'machine_learning/encoder.pkl'
        self.loaded_encoder = self.load_model(encoder_path)

        

        # encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
        # Fit the encoder on the training data
        # encoder.fit(self.pandas_df[CAT_FEATURES])
        # Transform both training and test data
        self.pandas_df_encoded = self.loaded_encoder.transform(self.pandas_df[CAT_FEATURES])
        # Create new columns for encoded values in train and test dataframes
        for i, feature in enumerate(CAT_FEATURES):
            self.pandas_df[f'{feature}_encoded'] = self.pandas_df_encoded[:, i] # without substituting original columns

            # Adjusting the FEATURES VECTOR
            self.FEATURES.append(f'{feature}_encoded')
            self.FEATURES.remove(feature)
        
        model_path = 'machine_learning/xgboost_model.pkl'
        self.loaded_model = self.load_model(model_path)

    def file_name_category(self, row):
        if "main" in row['file_name']:
            return "main"
        elif "init" in row['file_name']:
            return "init"
        elif "setup" in row['file_name']:
            return "setup"
        elif row['file_name'].startswith("_"):
            return "class"
        else:
            return "other"

    def load_model(self, model_path):
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        return model
    
    def predict(self):
        final_list_of_features = self.FEATURES
        pprint(final_list_of_features)
        self.pandas_df.iloc[0]['file_name_category_encoded'] = 1

        self.pandas_df["predicted_label"] = self.loaded_model.predict(self.pandas_df[[x for x in final_list_of_features]])
        self.pandas_df["probability_xgboost"] = self.loaded_model.predict_proba(self.pandas_df[[x for x in final_list_of_features]])[:,1]

        if self.pandas_df["predicted_label"][0] == 1:
            print(f"This file is: MALICIOUS ! ! !: {self.pandas_df['file_name'][0]}")
            print("With a confidence score of: ", round(self.pandas_df["probability_xgboost"][0], 2))
        else:
            print(f"This file is: OK ! ! !: {self.pandas_df['file_name'][0]}")
            print("With a confidence score of: ", round((1-self.pandas_df["probability_xgboost"][0]), 2))

        #pprint(json.dumps(self.json_content))
        with open("debug.json", "w") as file:
            file.write(json.dumps(self.json_content))
