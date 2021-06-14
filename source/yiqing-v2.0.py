#!/usr/bin/env python
# encoding:utf-8
import selenium
import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 网页验证码识别函数
import base64
import json
import requests
def base64_api(uname, pwd, img, typeid):
    with open(img, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        b64 = base64_data.decode()
    data = {"username": uname, "password": pwd, "typeid": typeid, "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]
    return ""

# 设置打卡网址及访问工具
url = 'https://cas.gzhu.edu.cn/cas_server/login;jsessionid=EF79AF3AE0584CE1D3391788B5EC17F9?service=http%3A%2F%2Fyqtb.gzhu.edu.cn%2Finfoplus%2Flogin%3FretUrl%3Dhttp%253A%252F%252Fyqtb.gzhu.edu.cn%252Finfoplus%252Foauth2%252Fauthorize%253Fx_redirected%253Dtrue%2526scope%253Dprofile%252Bprofile_edit%252Bapp%252Btask%252Bprocess%252Bsubmit%252Bprocess_edit%252Btriple%252Bstats%252Bsys_profile%252Bsys_enterprise%252Bsys_triple%252Bsys_stats%252Bsys_entrust%252Bsys_entrust_edit%2526response_type%253Dcode%2526redirect_uri%253Dhttp%25253A%25252F%25252Fyq.gzhu.edu.cn%25252Ftaskcenter%25252Fwall%25252Fendpoint%25253FretUrl%25253Dhttp%2525253A%2525252F%2525252Fyq.gzhu.edu.cn%2525252Ftaskcenter%2525252Fworkflow%2525252Findex%2526client_id%253D1640e2e4-f213-11e3-815d-fa163e9215bb'
chrome_options = Options()
try:
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--start-maxmized')
    chrome_options.add_argument('--lang=zh-CN')
    driver = webdriver.Chrome(options= chrome_options)
    print("打开自动测试浏览器！！")
except BaseException as e:
    print("自动测试浏览器打开失败？？")

driver.get(url)
driver.save_screenshot('./printscreen.png')
# 1080分辨率
# 验证码在1080分辨率的图像中，所在的位置
rangle = (1300, 
          314, 
          1300+90,
          314+40) 
i = Image.open("./printscreen.png")  # 打开截图
frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
frame4=frame4.convert('RGB')
frame4.save('./save.jpg') # 保存我们接下来的验证码图片 进行打码
img_path = "./save.jpg"

result = base64_api(uname='图鉴用户名', pwd='图鉴密码', img=img_path, typeid=1)
time.sleep(3)
username = "疫情网站的账户名"
password = "疫情网站的密码"
yzm = result
try:
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    print("账户名及密码成功输入！！")
    
    try:
        driver.find_element_by_name("captcha").send_keys(yzm)
        print("验证码成功输入！！")
    except BaseExcept:
        print("验证码输入失败？？")
        
    print("成功输入账户名、密码及验证码！！")
except BaseException:
    print("无法输入账户名、密码及验证码？？")

try:
    driver.find_element_by_class_name("btn-submit").click()
    print("成功登录！！")
except BaseExcept:
    print("登录失败？？")

time.sleep(3)
try:
    driver.find_element_by_link_text("学生健康状况申报").click()
    print("成功点击'学生健康状况申报'按钮！！")
except BaseException:
    print("无法点击'学生健康状况申报'按钮？？")
time.sleep(3)

try:
    windows = driver.window_handles   # 获取该会话所有的窗口
    driver.switch_to.window(windows[-1])  # 跳转到最新的窗口
    print("窗口切换成功！！")
except BaseExcept:
    print("窗口切换失败？？")
# 把触发事件跳转到最新界面

try:
    driver.find_element_by_id("preview_start_button").click()
    print("点击开始上报按钮！！")
except BaseException:
    print("点击上报按钮失败？？")

try:
    for i in driver.find_elements_by_xpath("//*[@id='V1_CTRL262']"): #//*[@id="V1_CTRL262"]
        i.click()
    print("勾选全部的radioButton！！")
except BaseException:
    print("无法勾选全部的radioButton？？")

# 进行确认勾选
time.sleep(3)
try:
    driver.find_element_by_xpath("//*[@id='V1_CTRL82']").click()
    print("勾选最后的确认按钮！！")
except BaseException:
    print("确认按钮勾选失败？？")

# 确认提交按钮
try:
    driver.find_element_by_class_name("command_button_content").click()
    print("提交表单！！")
except BaseException:
    print("表单提交失败？？")
time.sleep(3)

driver.close() # 关闭当前窗口
driver.quit()  # 退出Chrome浏览器
print("打卡成功")

