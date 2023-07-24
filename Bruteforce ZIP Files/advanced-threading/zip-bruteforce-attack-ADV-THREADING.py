import zipfile
import shutil
import threading

password_file = "pass.txt"
zip_folder = "loltest.zip"
extract_folder = "extracted"
found_passwords_file = "found_passwords.txt"

def unlock_zip(password):
    try:
        with zipfile.ZipFile(zip_folder, 'r') as zip_ref:
            zip_ref.extractall(path=extract_folder, pwd=password.encode())
        return True
    except zipfile.BadZipFile:
        print("Invalid zip file.")
    except RuntimeError as e:
        if str(e) == "Bad password for file":
            return False
    except:
        return False

def read_passwords(file):
    with open(file, 'r') as pass_file:
        passwords = pass_file.readlines()
    return [password.strip().strip('"') for password in passwords]

def unlock_zip_thread(password):
    if unlock_zip(password):
        print(f"\nFolder unlocked. Password: {password}")
        with open(found_passwords_file, 'a') as f:
            f.write(f"Found password: {password}\n")
        return True
    return False

def main():
    passwords = read_passwords(password_file)
    threads = []
    for password in passwords:
        print(f"Trying password: {password}")
        thread = threading.Thread(target=unlock_zip_thread, args=(password,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("\nUnable to unlock the folder.")

if __name__ == "__main__":
    shutil.rmtree(extract_folder, ignore_errors=True)
    with open(found_passwords_file, 'w') as f:
        f.write("Found Passwords:\n")
    main()
