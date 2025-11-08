from . import utils

#Symetric Ciphers
def caesar_cipher(text, shift):
	result = ""
	for char in text:
		if char.isalpha():
			shift_base = ord('A') if char.isupper() else ord('a')
			result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
		else:
			result += char
	return result

def run():
	# Example usage
	plaintext = "Hello, World!"
	shift = 3
	ciphertext = caesar_cipher(plaintext, shift)
	print(f"Ciphertext: {ciphertext}")
	decrypted_text = caesar_cipher(ciphertext, -shift)
	print(f"Decrypted Text: {decrypted_text}")	# Example usage
	plaintext = "Hello, World!"
	shift = 3
	ciphertext = caesar_cipher(plaintext, shift)
	print(f"Ciphertext: {ciphertext}")
	decrypted_text = caesar_cipher(ciphertext, -shift)
	print(f"Decrypted Text: {decrypted_text}")
	print(utils.parse_data("Hola"))
	print(utils.factorise(1232385274095812))

if __name__ == "__main__":
	run()