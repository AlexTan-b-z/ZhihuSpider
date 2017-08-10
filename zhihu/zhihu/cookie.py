#encoding=utf8
import pdb
import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging
from .yumdama import identify

# ------------------------------------------
#   版本：1.0
#   日期：2017-8-06
#   作者：AlexTan
#   <CSDN:   http://blog.csdn.net/alextan_>  
#   <e-mail: alextanbz@gmail.com>
# ------------------------------------------

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"
)
logger = logging.getLogger(__name__)
logging.getLogger("selenium").setLevel(logging.WARNING) # 将selenium的日志级别设成WARNING，太烦人

METHOD = 0 #0代表手动输入验证码，1代表云打码

myZhiHu = [
    ('这里填写账号','这里填写密码',0),  #0代表账号为手机，1代表账号为邮箱
]

def getCookie(account,password,way):
    if way == 0:
        loginURL = "https://www.zhihu.com/login/phone_num"
        username = 'phone_num'
    else:
        loginURL = "https://www.zhihu.com/login/email"
        username = 'email'
    try:
        browser = webdriver.PhantomJS(desired_capabilities=dcap)
        #browser = webdriver.Firefox()
        browser.set_window_size(1920, 1080)
        browser.get("https://www.zhihu.com/explore")
        time.sleep(1)
        #pdb.set_trace()
        browser.find_element_by_class_name('switch-to-login').click()
        loginDIV = browser.find_element_by_id('SidebarSignFlow').find_element_by_class_name('LoginForm')
        loginDIV.find_element_by_name('account').send_keys(account)
        loginDIV.find_element_by_name('password').send_keys(password)
        time.sleep(1)
        browser.save_screenshot("zhihu.png")
        if loginDIV.find_element_by_class_name('captcha-module').get_attribute('style') != '':
            if METHOD == 0:
                code_txt = input("请查看路径下新生成的zhihu.png，然后输入验证码:")
            else:
                img = loginDIV.find_element_by_class_name('captcha')
                x = img.location["x"]
                y = img.location["y"]
                from PIL import Image
                im = Image.open("zhihu.png")
                im.crop((x, y, 85 + x, y + 30)).save("captcha.png")
                #pdb.set_trace()
                code_txt = identify()
            loginDIV.find_element_by_name('captcha').send_keys(code_txt)
        loginDIV.find_element_by_class_name('zg-btn-blue').click()
        time.sleep(3)
        try:
            loginDIV.find_element_by_class_name('error')
            logger.warning("验证码或账号密码错误 %s!" % account)
        except:
            try:
                #pdb.set_trace()
                browser.find_element_by_class_name('top-nav-profile')
                cookie = {}
                for elem in browser.get_cookies():
                    cookie[elem["name"]] = elem["value"]
                logger.warning("Get Cookie Success!( Account:%s )" % account)
                #pdb.set_trace()
                return json.dumps(cookie)
            except Exception:
                logger.warning("Failed %s!" % account)
                return ""
    except Exception:
        logger.warning("Failed %s!" % account)
        return ""
    finally:
        try:
            browser.quit()
        except Exception:
            pass

def UpdateCookie(account,cookie):
    browser = webdriver.PhantomJS(desired_capabilities=dcap)
    #browser = webdriver.Firefox()
    browser.set_window_size(1920, 1080)
    browser.get('https://www.zhihu.com')
    browser.delete_all_cookies()
    send_cookie = []
    for key,value in cookie.items():
        one = {}
        one = {'domain':'.zhihu.com','name':key,'value':value,'path':'/','expiry':None}
        #pdb.set_trace()
        browser.add_cookie({k: one[k] for k in ('name', 'value', 'domain', 'path', 'expiry')})
        #one = {'domain':'.zhihu.com','name':key,'value':value}
        #send_cookie.append(one)
    #browser.add_cookie(send_cookie)
    browser.get('https://www.zhihu.com/account/unhuman?type=unhuman&message=%E7%B3%BB%E7%BB%9F%E6%A3%80%E6%B5%8B%E5%88%B0%E6%82%A8%E7%9A%84%E5%B8%90%E5%8F%B7%E6%88%96IP%E5%AD%98%E5%9C%A8%E5%BC%82%E5%B8%B8%E6%B5%81%E9%87%8F%EF%BC%8C%E8%AF%B7%E8%BE%93%E5%85%A5%E4%BB%A5%E4%B8%8B%E5%AD%97%E7%AC%A6%E7%94%A8%E4%BA%8E%E7%A1%AE%E8%AE%A4%E8%BF%99%E4%BA%9B%E8%AF%B7%E6%B1%82%E4%B8%8D%E6%98%AF%E8%87%AA%E5%8A%A8%E7%A8%8B%E5%BA%8F%E5%8F%91%E5%87%BA%E7%9A%84')
    time.sleep(1)
    browser.save_screenshot("update.png")
    if METHOD == 0:
        code_txt = input("请查看路径下新生成的update.png，然后输入验证码:")
    else:
        img = browser.find_element_by_class_name('Unhuman-captcha')
        x = img.location["x"]
        y = img.location["y"]
        from PIL import Image
        im = Image.open("zhihu.png")
        im.crop((x, y, 85 + x, y + 30)).save("captcha.png")
        #pdb.set_trace()
        code_txt = identify()
    browser.find_element_by_class_name('Input').send_keys(code_txt)
    browser.find_element_by_class_name('Button--blue').click()
    time.sleep(3)
    try:
        browser.find_element_by_class_name('AppHeader-profile')
        cookie = {}
        for elem in browser.get_cookies():
            cookie[elem["name"]] = elem["value"]
        logger.warning("Update Cookie Success!( Account:%s )" % account)
        #pdb.set_trace()
        return json.dumps(cookie)
    except Exception:
        logger.warning("Update Failed %s!" % account)
        return ""
    finally:
        try:
            browser.quit()
        except Exception:
            pass



def initCookie(rconn, spiderName):
    """ 获取所有账号的Cookies，存入Redis。如果Redis已有该账号的Cookie，则不再获取。 """
    for zhihu in myZhiHu:
        if rconn.get("%s:Cookies:%s--%s" % (spiderName, zhihu[0], zhihu[1])) is None:  # 'zhihuspider:Cookies:账号--密码'，为None即不存在。
            cookie = getCookie(zhihu[0], zhihu[1],zhihu[2])
            if len(cookie) > 0:
                rconn.set("%s:Cookies:%s--%s" % (spiderName, zhihu[0], zhihu[1]), cookie)
    cookieNum = str(rconn.keys()).count("zhihuspider:Cookies")
    logger.warning("The num of the cookies is %s" % cookieNum)
    if cookieNum == 0:
        logger.warning('Stopping...')
        os.system("pause")

def updateCookie(accountText, rconn, spiderName, cookie):
    """ 更新一个账号的Cookie """
    account = accountText.split("--")[0]
    #pdb.set_trace()
    new_cookie = UpdateCookie(account, cookie)
    if len(new_cookie) > 0:
        logger.warning("The cookie of %s has been updated successfully!" % account)
        rconn.set("%s:Cookies:%s" % (spiderName, accountText), new_cookie)
    else:
        logger.warning("The cookie of %s updated failed! Remove it!" % accountText)
        removeCookie(accountText, rconn, spiderName)

def removeCookie(accountText, rconn, spiderName):
    """ 删除某个账号的Cookie """
    rconn.delete("%s:Cookies:%s" % (spiderName, accountText))
    cookieNum = str(rconn.keys()).count("zhihuspider:Cookies")
    logger.warning("The num of the cookies left is %s" % cookieNum)
    if cookieNum == 0:
        logger.warning("Stopping...")
        os.system("pause")


if __name__ == '__main__':
    getCookie(myZhiHu[0][0],myZhiHu[0][1],myZhiHu[0][2])
