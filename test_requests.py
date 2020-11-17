import requests
import json
tz = {'tz' : 'Asia/Tokyo'}
data = json.dumps({'start':{"date":'12.20.2020 22:26:05'},
                    'end' :{"date":'12.20.2020 22:23:05'},
                   })


print('1:')
url = 'http://localhost:8080/'
post = requests.get(url)
print(post.text)

print('2:')
url = 'http://localhost:8080/Asia/Tokyo'
post = requests.get(url)
print(post.text)

print('3-TEST1:')
url = 'http://localhost:8080/api/v1/time'
post = requests.post(url)
print(post.text)

print('3-TEST2:')
url = 'http://localhost:8080/api/v1/time'
data = json.dumps({'tz' : 'Asia/Tokyo'})
post = requests.post(url,data)
print(post.text)

print('3-TEST3:')
url = 'http://localhost:8080/api/v1/time'
data = json.dumps({'tz' : 'Wrong/Tz'})
post = requests.post(url,data)
print(post.text)

print('4-TEST1:')
url = 'http://localhost:8080/api/v1/date'
post = requests.post(url)
print(post.text)

print('4-TEST2:')
url = 'http://localhost:8080/api/v1/date'
data = json.dumps({'tz' : 'Asia/Tokyo'})
post = requests.post(url,data)
print(post.text)

print('4-TEST3:')
url = 'http://localhost:8080/api/v1/date'
data = json.dumps({'tz' : 'Wrong/Tz'})
post = requests.post(url,data)
print(post.text)

print('5-TEST1:')
url = 'http://localhost:8080/api/v1/datediff'
data = json.dumps({'start':{"date":'12.20.2020 22:26:05'},
                    'end' :{"date":'12.20.2020 22:23:05'},
                   })
post = requests.post(url,data)
print(post.text)

print('5-TEST2:')
url = 'http://localhost:8080/api/v1/datediff'
data = json.dumps({'start':{"date":'12.20.2020 22:26:05', 'tz':'Asia/Tomsk'},
                    'end' :{"date":'12.20.2020 22:26:05', 'tz':'Asia/Tokyo'},
                   })
post = requests.post(url,data)
print(post.text)


print('5-TEST3:')
url = 'http://localhost:8080/api/v1/datediff'
data = json.dumps({'start':{"date":'WITHOUT START TIME', 'tz':'Asia/Tomsk'},
                    'end' :{"date":'12.20.2020 22:26:05', 'tz':'Asia/Tokyo'},
                   })
post = requests.post(url,data)
print(post.text)
