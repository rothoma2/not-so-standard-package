import re

class Features:
    def __init__(self, input):
        self.features = []
        self.nr_chars = len(input)
        self.features.append({"nr_of_words", self.nr_of_words(input)})
        self.features.append({"nr_of_lines", self.nr_of_lines(input)})
        self.features.append({"nr_of_urls", self.nr_of_urls(input)})
        self.features.append({"nr_of_ip_address", self.nr_of_ip_address(input)})
        
        self.features.append({"ratio_square_bracket_sign", self.ratio_char(self.nr_of_square_bracket_signs(input))})
        self.features.append({"ratio_equals_sign", self.ratio_char(self.nr_of_plus_signs(input))})
        self.features.append({"ratio_plus_sign", self.ratio_char(self.nr_of_equal_signs(input))})

    def nr_of_words(self, input):
        return len(input.strip().split())
    
    def nr_of_lines(self, input):
        return len(input.splitlines())
    
    def nr_of_urls(self, input):
        url_pattern = re.compile(r'\b((?:https?|ftp|file):\/\/[-a-zA-Z0-9+&@#\/%?=~_|!:,.;]*[-a-zA-Z0-9+&@#\/%=~_|])')
        return len(url_pattern.findall(input))
    
    def nr_of_ip_address(self, input):
        ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
        return len(ip_pattern.findall(input))

    def nr_all_chars(self, input):
        return input.count()

    def nr_of_square_bracket_signs(self, input):
        return input.count("[") + input.count("]")

    def nr_of_plus_signs(self, input):
        return input.count("+")

    def nr_of_equal_signs(self, input):
        return input.count("=")
    
    def ratio_char(self, nr):
        return nr / self.nr_chars

