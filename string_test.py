from ar_coding import ArithmeticCoding
import math

# Input
bits = 32
message = "testing" * 10
# message = "daniel's daddies"
# message = "daniel's daddies" * 500

# Create instance of class and perform arithmetic coding
ar = ArithmeticCoding(bits, message) # Set up
code = ar.arithmetic_encoder() # Encode
binary_sequence = ''.join(map(str, code)) # Turn list into binary sequence for displaying
decoded_message = ar.arithmetic_decoder() # Decode

# Display results
print(f"Original: {message}")
print(f"Encoded: {binary_sequence}")
print(f"Decoded: {decoded_message}")

# Sizes of original and compressed message
message_size = len(message)
print(f"Memory used by original message: {message_size}")
compressed_size = math.ceil(len(code) / 8)
print(f"Memory used by binary sequence: {compressed_size}")

# Calculate compression ratio
compression_ratio = message_size / compressed_size
print(f"Data compression ratio: {compression_ratio}")