"""
1. Will load all images for this quiz from MongoDB.
2. Will then upload images to Telegram /sendPhotos endpoint and get back a file_id
3. Will persist mapping of question file_id & answer file id in the Question Doc itself.
4. These will be copied into the Session object later
"""

import requests,time
sess = requests.Session()
# murl = "https://api.telegram.org/bot1135804192:AAEtfVu4MZJuqesF6Wsph6UU0mtmPJZM2hQ/sendPhoto?chat_id=-466732659&photo=AgACAgEAAxkDAAOLXrEAAW5ZATdy3AYDx-OhYjTTF87wAAI6qDEbdEmJRSIXicIXadlBKr9uBgAEAQADAgADeQAD6IACAAEZBA"
murl = "https://api.telegram.org/bot1135804192:AAEtfVu4MZJuqesF6Wsph6UU0mtmPJZM2hQ/sendPhoto"
#
# chat_id = ["-466732659","-451968446","-327877867","-416057415","-403339971","-418181859","-361520996"]
# files = {
#     "photo" : open("test_img_2.jpeg","rb")
# }
# # files = {
# #
# #     "photo" : "AgACAgEAAxkDAAOLXrEAAW5ZATdy3AYDx-OhYjTTF87wAAI6qDEbdEmJRSIXicIXadlBKr9uBgAEAQADAgADeQAD6IACAAEZBA"
# # }
#
# # res = requests.post(murl,files=files)


# start = time.time()
# for i in range(25):
#     params = {"chat_id" : chat_id[i%7],"photo":file_id}
#     res = sess.post(murl,params)
#     print(res.status_code)
#     # if i == 28:
#     #     print("taking a break")
#     #     time.sleep(2)
#
#
# print("{}".format(time.time()-start))
#

# file_id = "AgACAgEAAxkDAAOLXrEAAW5ZATdy3AYDx-OhYjTTF87wAAI6qDEbdEmJRSIXicIXadlBKr9uBgAEAQADAgADeQAD6IACAAEZBA"
# params = {"chat_id" : "1106388958","photo":file_id,"caption":"hello"}
# # body = {"caption" : "hello"}
#
# res = sess.post(murl,params)
# print(res.status_code)


import matplotlib.pyplot as plt

dictionary = {1: 27, 34: 1, 3: 72, 4: 62, 5: 33, 6: 36, 7: 20, 8: 12, 9: 9, 10: 6, 11: 5,
              12: 8, 2: 74, 14: 4, 15: 3, 16: 1, 17: 1, 18: 1, 19: 1, 21: 1, 27: 2}
plt.barh(list(dictionary.keys()), dictionary.values(), color='g')
# plt.show()

from io import BytesIO
figfile = BytesIO()
plt.savefig(figfile, format='png')
figfile.seek(0)  # rewind to beginning of file
import base64

# figdata_png = base64.b64encode(figfile.read())
figdata_png = base64.b64encode(figfile.getvalue())
params = {"chat_id" : "1106388958"}
files = {"photo" : figfile.getvalue()}
res = sess.post(murl,params=params,files=files)
print(res.content)