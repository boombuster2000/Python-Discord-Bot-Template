import json

class ConfigLoader():
    def __init__(self, config_fp = "./config.json") -> None:
        self.CONFIG_TEMPLATE = {
            "bot-token":"BOT-TOKEN",
            "dev-guild-id":"GUILD-ID",
        }
        self.CONFIG_FP = config_fp

    def create_config_file(self) -> None:
        with open(self.CONFIG_FP, "w") as config_file:
            json.dump(self.CONFIG_TEMPLATE, config_file, indent=4)
            
    def load_config(self) -> dict | None:
        try:
            with open(self.CONFIG_FP, "r") as config_file:
                config = json.load(config_file)
                return config
            
        except (json.decoder.JSONDecodeError):
            print("Invalid JSON in config file, resetting config file.")
            self.create_config_file()

    def update_config_file(self, new_config) -> None:
        with open(self.CONFIG_FP, "w") as config_file:
            json.dump(new_config, config_file, indent=4)

    def is_config_file_filled_in(self) -> bool:
        return_value = True # allows for loop to continue so all missing config options will be displayed in one run.

        config = self.load_config()
        for key in self.CONFIG_TEMPLATE.keys():
            try:
                if config[key] == self.CONFIG_TEMPLATE[key]: 
                    return_value = False
            except KeyError:
                config[key] = self.CONFIG_TEMPLATE[key]
                self.update_config_file(config)
                print(f"[{key}] not filled in.")
                return_value = False

        return return_value
    