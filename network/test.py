from typing import Counter
import webbrowser
import time
try:
    #code
    print("No error")
except Exception as e:
    print("error: " + str(e))
    print("Opening the webbrowser...")
    time.sleep(1)
    webbrowser.open('https://www.stackoverflow/search?q=[python] ' + str(e))
