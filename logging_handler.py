import json
import os.path
import datetime

class Logger:

    def __init__(self, settings_hook, scan_folder_name, file):
        self.settings_hook = settings_hook
        self.scan_folder_name = scan_folder_name
        self.file = file

    def generate_simple_logs(self):
        dictionary_logs = {
            "source_name": "",
            "description": "",
            "image": "",
            "date": ""
        }

    dictionary_logs["date"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    dictionary_logs["source_name"] = source_name
    dictionary_logs["description"] = description
    seperator = re.compile('\/')
    folder_source_name = seperator.split(source_name)[-1]
    dictionary["image"] = dictionary["description"] + "/" + folder_source_name

    json_object = json.dumps(dictionary_logs, indent=4)
    with open("{}".format("logger_data"), "w") as f:
        f.write(json_object)


