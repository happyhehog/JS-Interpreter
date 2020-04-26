class InterpreterException(Exception):
    error_code = ""


class FeatureNotImplemented(InterpreterException):
    def __init__(self, feature_name: str):
        self.error_code = "00"
        print("Error code: " + self.error_code + " -- " + feature_name + " Not implemented!")
