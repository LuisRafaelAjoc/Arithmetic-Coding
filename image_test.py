from arithmetic_coding import ArithmeticCoding
import base64
import os
import math

# Encode the image to a base64 string.
with open("examples/mona_lisa.jpg", "rb") as img:
    encode_bytes = base64.b64encode(img.read())

# Input
bits = 32
encode_str = encode_bytes.decode('utf-8')

# print(byte)

ar = ArithmeticCoding(bits, encode_str) # Set up
code = ar.arithmetic_encoder() # Encode
binary_sequence = ''.join(map(str, code)) # Turn list into binary sequence for displaying
decoded_str = ar.arithmetic_decoder() # Decode

# # Save the encoded string to a file.
# with open('encoded_image.bin', "wb") as f:
#     f.write()

decoded_bytes = decoded_str.encode("utf-8")

# f = open('encoded_image.bin', 'rb')  # Open encoded file.
# byte = f.read()  # Read data.
# f.close()

decode = open('decoded_image.jpg', 'wb')  # Open image file to save.
decode.write(base64.b64decode(decoded_bytes))  # Decode and write data.
decode.close()

# Display results
# print(f"Original: {encode_str}")
print(f"Encoded: {binary_sequence}")
# print(f"Decoded: {decoded_bytes}")

# Sizes
original_size = os.stat("examples/starry_night.jpg").st_size
print(f"Size of original image: {original_size}")
# compressed_size = len(code)
compressed_size = math.ceil(len(code) / 8)
print(f"Size of compressed image: {compressed_size}")

# Calculate compression ratio
compression_ratio = original_size / compressed_size
print(f"Data compression ratio: {compression_ratio}")
