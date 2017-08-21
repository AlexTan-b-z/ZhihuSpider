# encoding=utf-8
import telnetlib
import urllib

# ------------------------------------------
#   版本：1.0
#   日期：2017-8-06
#   作者：AlexTan
#   <CSDN:   http://blog.csdn.net/alextan_>  
#   <e-mail: alextanbz@gmail.com>
# ------------------------------------------

IPPOOLNUM=20 #一次性从网页获取的IP数量

def GetIPPOOLS(num):
    #大象代理买的ip,5元20000个，每十个差不多有一个能用
    IPPOOL=urllib.request.urlopen("http://tpv.daxiangdaili.com/ip/?tid=YOUR PRODUCT ID&num="+str(num)+"&protocol=http&delay=1").read().decode("utf-8","ignore").split('\r\n')
    '''
    #自己获取的ip
    IPPOOLS1=urllib.request.urlopen("http://127.0.0.1:8000/?types=0&count=20&country=%E5%9B%BD%E5%86%85").read().decode("utf-8",'ignore')
    IPPOOLS2=re.findall('\"(\d+\.\d+\.\d+\.\d+\"\,\s*\d+)',IPPOOLS1)
    IPPOOL=[i.replace('", ',':') for i in IPPOOLS2]
    '''
    return IPPOOL

def initIPPOOLS(rconn):
    """把有效的IP存入	REDIS数据库"""

    ipNum=len(rconn.keys('IP*'))
    if ipNum<IPPOOLNUM:
        IPPOOLS=GetIPPOOLS(IPPOOLNUM)
        for ipall in IPPOOLS:
            try:
                ip=ipall.split(':')[0]
                port=ipall.split(':')[1]
                telnetlib.Telnet(ip,port=port,timeout=2)
            except:
                print('ip无效！')
            else:
                print('ip:%s 有效，正在存入数据库...'%(ipall))
                rconn.set("IP:%s"%(ipall),ipall)
    else:
        print('当前数据库中的IP数量为:'+str(ipNum))


def removeIPPOOLS(rconn,ip):
    print('IP:%s 已失效,正在删除...'%(ip))
    rconn.delete('IP:'+ip)
    ipNum=len(rconn.keys('IP*'))
    print('当前数据库中剩下的IP数量为:'+str(ipNum))
