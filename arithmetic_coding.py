from collections import Counter

class ArithmeticCoding:
    def __init__(self, bits, message):
        self.precision = bits # Bits for representing numbers
        self.whole = 1 << self.precision # Highest value of range
        self.half = self.whole >> 1 # Half value of range
        self.quarter = self.whole >> 2 # Quarter value of range

        self.eof = '␄'  # End-Of-File character used to determine if entire message has been decoded
        self.message = message + self.eof # Append EOF symbol to message
        self.total_chars = len(self.message)

        self.freq_table = Counter(self.message) # Determine how many times a symbol appears in the message
        self.prob_table = self.get_probability_table() # Probabilities of symbol occurrence
        self.subrange_bounds = self.get_range_bounds() # Stores the subranges in the range occupied by a symbol
        self.code = [] # Stores encoded binary sequence

    # Returns a dictionary that contains each symbol and probability of occurrence
    def get_probability_table(self):
        prob_table = {}
        for char in self.freq_table:
            prob_table[char] = self.freq_table[char] / self.total_chars # Calculate probability
        return prob_table

    # Returns a dictionary that contains each symbol and a tuple that contains their lower and upper range bounds
    def get_range_bounds(self):
        range_bounds = {}
        cumulative = 0.0 # Start with lowest value in range
        for char in self.prob_table:
            low = cumulative
            high = cumulative + self.prob_table[char]
            range_bounds[char] = (low, high)
            cumulative = high
        return range_bounds

    # Used for encoding one bit
    def emit_bit(self, bit):
        self.code.append(int(bit))

    # Used for encoding multiple bits of the same value
    def emit_bit_counter(self, bit, scale):
        for _ in range(scale):
            self.emit_bit(bit)

    def arithmetic_encoder(self):
        low = 0
        high = self.whole - 1
        scale = 0 # Counter for bits to be added due to underflow

        # For every symbol encoded, the range is narrowed down
        for char in self.message:
            current_range = high - low
            char_low, char_high = self.subrange_bounds[char] # Get symbol's subrange
            high = low + int(current_range * char_high) # Narrow down range to new upper bound
            low = low + int(current_range * char_low) # Narrow down range to new lower bound

            # Rescaling operations
            while True:
                if high < self.half:
                    # Emit 0 and scale delayed 1s
                    self.emit_bit(0)
                    self.emit_bit_counter(1, scale)
                    scale = 0
                    low <<= 1
                    high = (high << 1) | 1
                elif low >= self.half:
                    # Emit 1 and scale delayed 0s
                    self.emit_bit(1)
                    self.emit_bit_counter(0, scale)
                    scale = 0
                    low = (low - self.half) << 1
                    high = (high - self.half) << 1 | 1
                elif low >= self.quarter and high <= 3 * self.quarter:
                    # Underflow: delay decision
                    scale += 1
                    low = (low - self.quarter) << 1
                    high = (high - self.quarter) << 1
                else:
                    break

        # Emit final sequence to complete encoding
        scale += 1
        if low < self.quarter:
            self.emit_bit(0)
            self.emit_bit_counter(1, scale)
        else:
            self.emit_bit(1)
            self.emit_bit_counter(0, scale)

        return self.code

    def arithmetic_decoder(self):
        low = 0
        high = self.whole - 1
        value = 0 # position in the current range

        # Initialize value with first N bits from code
        for i in range(self.precision):
            if i < len(self.code):
                value = (value << 1) | self.code[i]
            else:
                value <<= 1 # Pad with zeros if code is shorter than expected
        index = self.precision # Index in code bitstream
        decoded_message = ''

        while True:
            current_range = high - low + 1

            # Find character corresponding to current subinterval and update high and low
            for char, (char_low, char_high) in self.subrange_bounds.items():
                char_low = low + int(current_range * char_low)
                char_high = low + int(current_range * char_high)
                if char_low <= value < char_high:
                    decoded_message += char
                    if char == self.eof:
                        return decoded_message[:-1] # Remove EOF and return decoded message
                    low = char_low
                    high = char_high
                    break

            # Rescaling operations
            while True:
                if high < self.half:
                    pass # No adjustments
                elif low >= self.half:
                    value -= self.half
                    low -= self.half
                    high -= self.half
                elif low >= self.quarter and high <= 3 * self.quarter:
                    value -= self.quarter
                    low -= self.quarter
                    high -= self.quarter
                else:
                    break

                # Double all three values to maintain precision
                low <<= 1
                high <<= 1
                value <<= 1
                if index < len(self.code):
                    value |= self.code[index]
                    index += 1