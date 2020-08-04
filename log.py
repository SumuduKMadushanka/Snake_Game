## Created by : Sumudu Madushanka
## Last update : 8/4/2020

from datetime import datetime

## Log write ##
# write logs in log file
def log_write(log):
    log_file = open("Log/Snake_Game_Log.txt", "a")
    ts = datetime.fromtimestamp(datetime.now().timestamp()).isoformat()
    log_file.write(ts + "||" + log)
    log_file.close()

# Init the log file
def init_log_file():
    try:
        prev_log_file = open("Log/Snake_Game_Log.txt", "r")
        prev_log = prev_log_file.read()
        prev_log_file.close()
        prev_ts = prev_log.split("||")[0].replace(":", "-")
        prev_log_name = "Log/Snake_Game_Log_" + prev_ts + ".txt"
        prev_log_file = open(prev_log_name, "w")
        prev_log_file.write(prev_log)
    except FileNotFoundError:
        print ("Prev_log not found")
    finally:
        log_file = open("Log/Snake_Game_Log.txt", "w")
        log_file.close()
        log_write("Snake Game Log\n")
        log_write("Log File Created\n")
