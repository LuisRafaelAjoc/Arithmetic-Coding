from arithmetic_coding import ArithmeticCoding
import os

with open("examples/memo.pdf", "rb") as img:
    raw_bytes = img.read()

# Input
bits = 256
encode_str = raw_bytes.decode('ISO-8859-1')

ar = ArithmeticCoding(bits, encode_str) # Set up
code = ar.arithmetic_encoder() # Encode
binary_sequence = ''.join(map(str, code)) # Turn list into binary sequence for displaying
decoded_str = ar.arithmetic_decoder() # Decode

decoded_bytes = decoded_str.encode('ISO-8859-1')

with open('decoded_file.pdf', 'wb') as decode: # Open image file to save.
    decode.write(decoded_bytes)  # Decode and write data.

# Display results
print(f"Encoded: {binary_sequence}")

# Save bitstream to file
with open("pdf_encoded.bin", "wb") as f:
    byte_array = bytearray()
    for i in range(0, len(code), 8):
        byte = 0
        for j in range(8):
            if i + j < len(code):
                byte = (byte << 1) | code[i + j]
            else:
                byte <<= 1  # pad with 0
        byte_array.append(byte)
    f.write(byte_array)

# Sizes
original_size = os.stat("examples/memo.pdf").st_size
print(f"Size of original file: {original_size}")
compressed_size = os.stat("pdf_encoded.bin").st_size
print(f"Size of compressed file: {compressed_size}")

# Calculate compression ratio
compression_ratio = original_size / compressed_size
print(f"Data compression ratio: {compression_ratio}")