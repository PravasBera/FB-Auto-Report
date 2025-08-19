import os
import requests
from bs4 import BeautifulSoup
import time

# ===== Color codes =====
R = '\033[91m'   # Red
G = '\033[92m'   # Green
Y = '\033[93m'   # Yellow
P = '\033[95m'   # Pink/Magenta
W = '\033[0m'    # Reset

# ===== ASCII Banner =====
def show_banner():
    print(f"""{G}
██████╗ ██╗   ██╗██╗     ██╗     ███████╗████████╗
██╔══██╗██║   ██║██║     ██║     ██╔════╝╚══██╔══╝
██████╔╝██║   ██║██║     ██║     █████╗     ██║   
██╔══██╗██║   ██║██║     ██║     ██╔══╝     ██║   
██████║╚██████╔╝███████╗███████╗███████╗██║   
╚═════╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝ ╚═╝         

{R}                      TEAM{W}

{P}FaceBook Auto Reporting Tool{W}

{Y}Author : Pravas Bera
Version : 1.2
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

# ===== Main Token Request =====
def get_tokens(cookie, target_id, what="profile"):
    url = f"https://mbasic.facebook.com/a/report/?subject={target_id}&what={what}"
    headers = {
        "User-Agent": "Mozilla/5.0",
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

# ===== Main Function =====
def main():
    os.system("clear")
    show_banner()

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

    # Clear and show banner again
    os.system("clear")
    show_banner()

    print(f"{P}---- Select Report Reason ----{W}")
    for key, (_, txt) in reasons.items():
        print(f"{key}) {txt}")
    rchoice = input("Select Reason: ").strip()

    if rchoice not in reasons:
        print("Invalid reason.")
        return

    reason_code = reasons[rchoice][0]
    target_id = input(f"{G}Enter numeric Target ID: {W}").strip()

    try:
        with open("cookies.txt", "r") as f:
            cookies = [line.strip() for line in f if line.strip()]
    except:
        print("cookies.txt not found!")
        return

    print(f"\n{G}[+] Loaded {len(cookies)} cookies.{W}")
    success = 0
    failed = 0
    failed_list = []

    for ck in cookies:
        print(f"{Y}[*] Using cookie: {ck[:20]}...{W}")
        fb_dtsg, jazoest = get_tokens(ck, target_id, what)
        if not fb_dtsg:
            print(f"{R}   [-] Invalid or checkpoint cookie, skipping.{W}")
            failed += 1
            failed_list.append(ck)
            continue

        response = send_report(ck, target_id, fb_dtsg, jazoest, reason_code, what)
        if response.status_code == 200:
            print(f"{G}   [+] Report Sent!{W}")
            success += 1
        else:
            print(f"{R}   [-] HTTP {response.status_code}{W}")
        time.sleep(5)

    # Save failed into file
    if failed_list:
        with open("failed.txt", "w") as fp:
            for x in failed_list:
                fp.write(x + "\n")

    print(f"\n==== DONE ====")
    print(f"{G}Successful: {success}{W}")
    print(f"{R}Failed/Invalid: {failed}{W}")
    if failed > 0:
        print(f"{Y}Failed cookies saved to failed.txt{W}")

if __name__ == "__main__":
    main()
