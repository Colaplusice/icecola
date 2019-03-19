import os


class FlaskEnv:
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)

    def init_app(self, app):
        """
        load env file to app.config
        """
        if self.app is None:
            self.app = app
        #  test don't need flask_env
        if app.config["ENV"] == "testing":
            return
        env_file = os.path.join(os.getcwd(), ".env")
        if not env_file:
            raise FileNotFoundError(".env file not found")
        self.__import_vars(env_file)

    def __import_vars(self, env_file):
        with open(env_file) as opener:
            lines = opener.readlines()
            for line in lines:
                line = line.replace("'", "")
                line = line.strip("\n")
                # export
                if not line:
                    continue
                if line.split(" ")[0] == "export":
                    line = line.split(" ")[1]
                config_list = line.split("=")
                key, value = config_list[0], config_list[1]
                if value.isdigit():
                    value = int(value)
                self.app.config[key] = value
