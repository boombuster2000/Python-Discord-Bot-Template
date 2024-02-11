import json

class ConfigLoader():
    def __init__(self, config_fp = "./config.json"):
        self.CONFIG_TEMPLATE = {
            "bot-token":"BOT-TOKEN"
        }
        self.CONFIG_FP = config_fp

    def create_config_file(self):
        with open(self.CONFIG_FP, "w") as config_file:
            json.dump(self.CONFIG_TEMPLATE, config_file, indent=4)
            print("Fill in details in config file.")

    def load_config(self):
        try:
            with open(self.CONFIG_FP, "r") as config_file:
                config = json.load(config_file)
                return config
        except (json.decoder.JSONDecodeError):
            print("Invalid JSON in config file, resetting config file.")
            self.create_config_file()

    def is_config_file_filled_in(self):
        config = self.load_config()
        for key in self.CONFIG_TEMPLATE.keys():
            if config[key] == self.CONFIG_TEMPLATE[key]: 
                return True
            
        return False
    