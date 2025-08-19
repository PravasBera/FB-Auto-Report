import os
import requests
from bs4 import BeautifulSoup
import time

# Clear terminal screen
os.system("clear")

# ===== Color codes =====
R = '\033[91m'   # Red
G = '\033[92m'   # Green
Y = '\033[93m'   # Yellow
P = '\033[95m'   # Pink/Magenta
W = '\033[0m'    # Reset

# ===== ASCII Banner =====
banner = f"""{G}
██████╗ ██╗   ██╗██╗     ██╗     ███████╗████████╗
██╔══██╗██║   ██║██║     ██║     ██╔════╝╚══██╔══╝
██████╔╝██║   ██║██║     ██║     █████╗     ██║   
██╔══██╗██║   ██║██║     ██║     ██╔══╝     ██║   
██║  ██║╚██████╔╝███████╗███████╗███████╗   ██║   
╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝   ╚═╝   

{R}                      TEAM{W}

{P}FaceBook Auto Reporting Tool{W}

{Y}Author : Pravas Bera
Version : 1.0
Country : India{W}

{R}Indian Danger Of Bullet Team{W}
"""

print(banner)

# ===== Reason codes =====
REASONS = {
    "1": ("fake_profile", "Fake Account"),
    "2": ("spam", "Spam or Scam"),
    "3": ("harassment", "Harassment or Hate"),
    "4": ("nudity", "Nudity or Sexual Content"),
    "5": ("violence", "Violence")
}

def get_tokens(cookie, target_id, what="profile"):
    url = f"https://mbasic.facebook.com/a/report/?subject={target_id}&what={what}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10)",
        "Cookie": cookie
    }
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
    headers = {"User-Agent": "Mozilla/5.0", "Cookie": cookie}
    return requests.post(url, data=data, headers=headers)

def main():
    print(f"{Y}1) Report Profile   2) Report Post   3) Report Page{W}")
    choice = input("Choose option (1/2/3): ").strip()

    if choice == "1":
        what = "profile"
    elif choice == "2":
        what = "post"
    elif choice == "3":
        what = "page"
    else:
        print("Invalid option.")
        return

    print(f"\n{P}---- Select Report Reason ----{W}")
    for key, (_, txt) in REASONS.items():
        print(f"{key}) {txt}")
    rchoice = input("Select Reason (1-5): ").strip()

    if rchoice not in REASONS:
        print("Invalid reason.")
        return

    reason_code = REASONS[rchoice][0]
    target_id = input(f"{G}Enter numeric Target ID: {W}").strip()

    try:
        with open("cookies.txt", "r") as f:
            cookies = [line.strip() for line in f if line.strip()]
    except:
        print("cookies.txt not found!")
        return

    print(f"\n{G}[+] Loaded {len(cookies)} cookies.{W}")
    count = 0

    for ck in cookies:
        print(f"{Y}[*] Using cookie: {ck[:20]}...{W}")
        fb_dtsg, jazoest = get_tokens(ck, target_id, what)
        if not fb_dtsg:
            print(f"{R}   [-] Token missing, skipping.{W}")
            continue

        res = send_report(ck, target_id, fb_dtsg, jazoest, reason_code, what)
        if res.status_code == 200:
            print(f"{G}   [+] Report sent!{W}")
            count += 1
        else:
            print(f"{R}   [-] HTTP {res.status_code}{W}")
        time.sleep(5)

    print(f"\n==== DONE ====")
    print(f"Reports done: {count}/{len(cookies)}")

if __name__ == "__main__":
    main()
