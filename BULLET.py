import os
import requests
from bs4 import BeautifulSoup
import time
import re

# ===== Color codes =====
R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
P = '\033[95m'
W = '\033[0m'

# ===== Banner Function =====
def show_banner():
    print(f"""{G}
██████╗ ██╗   ██╗██╗     ██╗     ███████╗████████╗
██╔══██╗██║   ██║██║     ██║     ██╔════╝╚══██╔══╝
██████╔╝██║   ██║██║     ██║     █████╗     ██║   
██╔══██╗██║   ██║██║     ██║     ██╔══╝     ██║   
██████║  ██████╔╝███████╗███████╗███████╗   ██║   
╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚══════╝   ╚═╝   

{R}                      TEAM{W}

{P}FaceBook Auto Reporting Tool{W}

{Y}Author : Pravas Bera
Version : 1.3.1
Country : India{W}

{R}Indian Danger Of Bullet Team{W}
""")

# ===== Reason menus =====
PROFILE_REASONS = {
    "1": ("fake_profile", "Fake Account"),
    "2": ("spam", "Spam or Scam"),
    "3": ("harassment", "Harassment or Hate"),
    "4": ("nudity", "Nudity or Sexual Content"),
    "5": ("violence", "Violence")
}

POST_REASONS = {
    "1": ("nudity", "Nudity / Sexual"),
    "2": ("hate_speech", "Hate Speech / Symbols"),
    "3": ("violence", "Violence / Bloody"),
    "4": ("false_info", "False Information"),
    "5": ("spam", "Spam or Scam")
}

# ===== Convert Link to Numeric ID =====
def extract_id(text, cookie):
    text = text.strip()
    if text.isdigit():
        return text
    elif "facebook.com" in text:
        try:
            headers = {"Cookie": cookie, "User-Agent": "Mozilla/5.0"}
            res = requests.get(text, headers=headers)
            html = res.text
            # Try 3 different patterns
            m = re.search(r'profile_id":"(\d+)"', html)
            if not m:
                m = re.search(r'entity_id":"(\d+)"', html)
            if not m:
                m = re.search(r'userID":"(\d+)"', html)
            if m:
                return m.group(1)
        except:
            return None
    return None

# ===== mbasic GET token =====
def get_tokens(cookie, target_id, what="profile"):
    url = f"https://mbasic.facebook.com/a/report/?subject={target_id}&what={what}"
    headers = {"Cookie": cookie, "User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        fb_dtsg = soup.find("input", {"name": "fb_dtsg"})["value"]
        jazoest = soup.find("input", {"name": "jazoest"})["value"]
        return fb_dtsg, jazoest
    except:
        return None, None

def send_report(cookie, target_id, fb_dtsg, jazoest, reason_code, what="profile"):
    url = f"https://mbasic.facebook.com/a/report/?subject={target_id}&what={what}"
    data = {
        "fb_dtsg": fb_dtsg,
        "jazoest": jazoest,
        "report_type": reason_code,
        "source": what,
        "submit": "Submit"
    }
    headers = {"Cookie": cookie, "User-Agent": "Mozilla/5.0"}
    return requests.post(url, data=data, headers=headers)

# ===== MAIN =====
def main():
    os.system("clear")
    show_banner()

    # Main Menu
    print(f"{Y}1) Report Profile   2) Report Post   3) Report Page{W}")
    choice = input("Choose option (1/2/3): ").strip()
    if choice == "1":
        what = "profile"
        reasons = PROFILE_REASONS
    elif choice == "2":
        what = "post"
        reasons = POST_REASONS
    elif choice == "3":
        what = "page"
        reasons = PROFILE_REASONS
    else:
        print("Invalid option.")
        return

    # Clear wrapper
    os.system("clear")
    show_banner()

    # Reason menu
    print(f"{P}---- Select Report Reason ----{W}")
    for key, val in reasons.items():
        print(f"{key}) {val[1]}")
    rc = input("Select Reason: ").strip()
    if rc not in reasons:
        print("Invalid reason.")
        return
    reason_code = reasons[rc][0]

    # Load cookies from file
    try:
        with open("cookies.txt", "r") as f:
            cookies = [i.strip() for i in f if i.strip()]
    except:
        print("cookies.txt not found!")
        return

    if not cookies:
        print("No cookies in file!")
        return

    # Ask ID or link, validate
    while True:
        user_input = input(f"{G}Enter Target ID or FB Link: {W}")
        # use first cookie to convert if needed
        target_id = extract_id(user_input, cookies[0])
        if target_id:
            break
        else:
            print(f"{R}Invalid ID or link, try again...{W}")

    print(f"\n{G}[+] Loaded {len(cookies)} cookies. Starting report...{W}")
    success = 0
    failed = 0
    bad_list = []

    # Loop through cookies
    for ck in cookies:
        print(f"{Y}[*] Using cookie: {ck[:20]}...{W}")
        fb_dtsg, jazoest = get_tokens(ck, target_id, what)
        if not fb_dtsg:
            print(f"{R}   [-] Invalid / checkpoint cookie{W}")
            bad_list.append(ck)
            failed += 1
            continue
        resp = send_report(ck, target_id, fb_dtsg, jazoest, reason_code, what)
        if resp.status_code == 200:
            success += 1
            print(f"{G}   [+] Report sent!{W}")
        else:
            failed += 1
            print(f"{R}   [-] HTTP {resp.status_code}{W}")
        time.sleep(5)

    if bad_list:
        with open("failed.txt", "w") as f:
            for b in bad_list:
                f.write(b+"\n")

    print(f"\n==== DONE ====")
    print(f"{G}Success : {success}{W}")
    print(f"{R}Failed  : {failed}{W}")
    if bad_list:
        print(f"{Y}Invalid cookies saved in failed.txt{W}")

if __name__ == "__main__":
    main()
