from modules import crypto

def main():
    print("Welcome to the CTF Tool!")
    print("Available modules:")
    print("1. Crypto")
    choice = input("Select a module (1): ")
    if choice == '1':
        crypto.run()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()