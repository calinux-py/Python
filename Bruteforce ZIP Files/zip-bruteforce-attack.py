import zipfile

password_file = "pass.txt"
zip_folder = "loltest.zip"

def unlock_zip(password):
    try:
        with zipfile.ZipFile(zip_folder, 'r') as zip_ref:
            zip_ref.extractall(pwd=password.encode())
        return True
    except zipfile.BadZipFile:
        print("Invalid zip file.")
    except RuntimeError as e:
        if str(e) == "Bad password for file":
            return False
        else:
            print(f"An error occurred: {e}")
    return False

def read_passwords(file):
    with open(file, 'r') as pass_file:
        passwords = pass_file.readlines()
    return [password.strip().strip('"') for password in passwords]

def main():
    passwords = read_passwords(password_file)
    for password in passwords:
        print(f"Trying password: {password}")
        if unlock_zip(password):
            print(f"\nFolder unlocked. Password: {password}")
            break
    else:
        print("\nUnable to unlock the folder.")

if __name__ == "__main__":
    main()
