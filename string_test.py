from arithmetic_coding import ArithmeticCoding
import sys
import math

# Input
bits = 32
message = "testing" * 10
# message = "daniel's daddies"
# message = "daniel's daddies" * 500

# Create instance of class and perform arithmetic coding
ar = ArithmeticCoding(bits, message) # Set up
code = ar.arithmetic_encoder() # Encode
# binary_sequence = ''.join(map(str, code)) # Turn list into binary sequence
# binary_sequence = len(bytes(code))
decoded_message = ar.arithmetic_decoder() # Decode

# Display results
print(f"Original: {message}")
print(f"Encoded: {code}")
print(f"Decoded: {decoded_message}")

# Size of original and compressed message
message_space = sys.getsizeof(message)
print(f"Memory used by original message: {message_space}")
compressed_space = math.ceil(len(code) / 8)
print(f"Memory used by binary sequence: {compressed_space}")

# Calculate compression ratio
compression_ratio = message_space / compressed_space
print(f"Data compression ratio: {compression_ratio}")
