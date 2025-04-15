'''
pip install requests
put usernames in a usernames.txt like so:
jack
joe
bob
'''
import requests
import time

def extract_username(line):
    line = line.strip()
    if not line:
        return None
    if line.startswith("https://github.com/"):
        return line.split("https://github.com/")[-1].strip("/")
    return line

def is_username_available(username):
    url = f"https://github.com/{username}"  # Using GitHub profile page instead of API
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        if response.status_code == 404:
            return True
        elif response.status_code == 200:
            return False
        else:
            print(f"[?] Unexpected status {response.status_code} for {username}")
            return False
    except requests.RequestException as e:
        print(f"[!] Error checking {username}: {e}")
        return False

def check_usernames_from_list(file_path, output_file="available.txt"):
    available_usernames = []

    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Input file not found.")
        return

    try:
        for line in lines:
            username = extract_username(line)
            if not username:
                continue
            available = is_username_available(username)
            status = "✅ Available" if available else "❌ Taken"
            print(f"{username}: {status}")
            if available:
                available_usernames.append(username)
            time.sleep(1)  # bad rate limit 
    except KeyboardInterrupt:
        print("\n[!] Interrupted. Saving progress...")

    finally:
        with open(output_file, "w") as out_file:
            for username in available_usernames:
                out_file.write(username + "\n")
        print(f"\nSaved {len(available_usernames)} available usernames to '{output_file}'.")

if __name__ == "__main__":
    check_usernames_from_list("usernames.txt")
