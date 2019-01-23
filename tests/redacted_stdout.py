import io, sys, re

class STDOutOptions:
    ERROR = 0
    STDOUT = 1

class RedactedPrint:

    def __init__(self, option, redacted_list):
        self.origOut = None
        self.option = option
        self.redacted_list = redacted_list

    def enable(self):

            if self.option == STDOutOptions.STDOUT:
                sys.stdout = self
            else:
                sys.stderr = self

            ## Monkey Patch
            self.origOut = sys.__stdout__ \
                if self.option == STDOutOptions.STDOUT \
                else sys.__stderr__

    def disable(self):
        self.origOut.flush()
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def write(self, text):
        return self.origOut.write(redact_text(text, self.redacted_list))
        

    #pass all other methods to __stdout__ so that we don't have to override them
    def __getattr__(self, attr_name):
        return self.origOut.__getattribute__(attr_name)


class RedactedFile:

    def __init__(self, real_file, redacted_list):
        self.origOut = real_file
        self.redacted_list = redacted_list

    # provide everything a file has
    def __getattr__(self, attr_name):
        return self.origOut.__getattribute__(attr_name)

    def write(self, text):
        return self.origOut.write(redact_text(text, self.redacted_list))


def redact_text(text, redacted_list):
    for word in redacted_list:
        text = re.sub(word, "REDACTED", text)
    return text