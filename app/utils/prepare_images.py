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

file_id = "AgACAgEAAxkDAAOLXrEAAW5ZATdy3AYDx-OhYjTTF87wAAI6qDEbdEmJRSIXicIXadlBKr9uBgAEAQADAgADeQAD6IACAAEZBA"
params = {"chat_id" : "1106388958","photo":file_id,"caption":"hello"}
# body = {"caption" : "hello"}

res = sess.post(murl,params)
print(res.status_code)