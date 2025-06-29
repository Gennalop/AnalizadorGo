import os
import datetime

#Para generar logs automaticamnete en el formato prefix-githubUser-date-hour
def create_log_file(username="yourGitUser", base_dir="logs", prefix="semantico"):   #prefix: lexico, sintactico, semantico
    current_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.abspath(os.path.join(current_dir, "..", base_dir, username))
    os.makedirs(log_dir, exist_ok=True)
    now = datetime.datetime.now()
    date = now.strftime("%d-%m-%Y")
    time = now.strftime("%Hh%M")
    filename = f"{prefix}-{username}-{date}-{time}.txt"
    full_path = os.path.join(log_dir, filename)
    return open(full_path, "w", encoding="utf-8")
