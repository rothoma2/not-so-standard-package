import os
import json
import pickle
import openai
import pandas as pd
#  the 3 imports below are not used. I have commented them
# and should be deleted in the future
# from pprint import pprint 
# import xgboost as xgb
# from sklearn.preprocessing import OrdinalEncoder


class Model:
    def __init__(self, json_content):

        NUM_FEATURES = [
            'count_words', 
            'number_of_lines', 
            'number_of_urls', 
            'number_of_ip_addresses',
            'square_brackets_mean', 
            'square_brackets_std_dev', 
            'square_brackets_third_quartile', 
            'square_brackets_max_value', 
            'equal_signs_mean', 
            'equal_signs_std_dev', 
            'equal_signs_third_quartile', 
            'equal_signs_max_value', 
            'plus_signs_mean',
            'plus_signs_std_dev', 
            'plus_signs_third_quartile', 
            'plus_signs_max_value', 
            'yara_sensitive_data_exfiltration', 
            'yara_suspicious_process_control', 
            'yara_shady_links', 
            'yara_command_overwrite', 
            'yara_clipboard_access', 
            'yara_eval_obfuscation', 
            'yara_base64_decode', 
            'yara_steganography', 
            'yara_anti_analysis', 
            'yara_suspicious_file_ops', 
            'yara_funcion_calls', 
            'yara_command_execution', 
            'yara_silent_process_execution', 
            'shanon_entropy__mean', 
            'shanon_entropy__median', 
            'shanon_entropy__variance', 
            'shanon_entropy__max', 
            'shanon_entropy__1Q', 
            'shanon_entropy__3Q', 
            'shanon_entropy__outliers', 
            'obfuscated_code_python'
        ]
        # i have commented CAT_FEATURES since it is not used
        #  to delete
        # CAT_FEATURES = [
        #     'file_name_category'
        # ]
        self.FEATURES = NUM_FEATURES # + CAT_FEATURES

        self.json_content = json_content
        json_data = json.loads(json_content)
        # json_data["shanon_entropy__max"] = 8

        self.pandas_df = pd.DataFrame([json_data])
        self.pandas_df['file_name_category'] = self.pandas_df.apply(
            lambda row: self.file_name_category(row),
            axis=1
        )

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

        self.pandas_df["predicted_label"] = self.loaded_model.predict(
            self.pandas_df[[x for x in final_list_of_features]]
        )
        self.pandas_df["probability_xgboost"] = \
            self.loaded_model.predict_proba(
                self.pandas_df[[x for x in final_list_of_features]]
            )[:, 1]

        if self.pandas_df["predicted_label"][0] == 1:
            
            print(f"This file is: MALICIOUS ! ! !: {self.pandas_df['file_name'][0]}")
            print("With a confidence score of: ", round(
                self.pandas_df["probability_xgboost"][0], 2)
            )
            file_path = self.pandas_df["full_file_path"][0]
            print(file_path)

            with open(file_path, 'r') as file:
                file_contents = file.read()

        else:
            print(f"This file is: OK ! ! !: {self.pandas_df['file_name'][0]}")
            print("With a confidence score of: ", round(
                (1-self.pandas_df["probability_xgboost"][0]), 2)
            )

        # pprint(json.dumps(self.json_content))
        with open("debug.json", "w") as file:
            file.write(json.dumps(self.json_content))

        self.talk_with_chatgpt("Say Hello Back Please")

    def talk_with_chatgpt(question_to_gpt):
        model_name = "gpt-3.5-turbo"

        openai.organization = os.getenv("openai_organization")
        openai.api_key = os.getenv("openai_api_key")

        message = {
                'role': 'user',
                'content': question_to_gpt
            }
        
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[message]
        )

        chatbot_response = response.choices[0].message['content']
        print(chatbot_response.strip())
