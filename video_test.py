from ar_coding import ArithmeticCoding
import os

with open("examples/video_test.mp4", "rb") as f:
    raw_bytes = f.read()

# Input
bits = 256
encode_str = raw_bytes.decode("ISO-8859-1")

ar = ArithmeticCoding(bits, encode_str) # Set up
code = ar.arithmetic_encoder() # Encode
binary_sequence = ''.join(map(str, code)) # Turn list into binary sequence for displaying
decoded_str = ar.arithmetic_decoder() # Decode

# Convert decoded string back to bytes
decoded_bytes = decoded_str.encode("ISO-8859-1")
with open("decoded_video.mp4", "wb") as f:
    f.write(decoded_bytes)

# Display results
print(f"Encoded: {binary_sequence}")

# Save bitstream to file
with open("video_encoded.bin", "wb") as f:
    byte_array = bytearray()
    for i in range(0, len(code), 8):
        byte = 0
        for j in range(8):
            if i + j < len(code):
                byte = (byte << 1) | code[i + j]
            else:
                byte <<= 1  # pad
        byte_array.append(byte)
    f.write(byte_array)

# Sizes
original_size = os.stat("examples/video_test.mp4").st_size
print(f"Size of original video: {original_size}")
compressed_size = os.stat("video_encoded.bin").st_size
print(f"Size of compressed video: {compressed_size}")

# Calculate compression ratio
compression_ratio = original_size / compressed_size
print(f"Data compression ratio: {compression_ratio}")