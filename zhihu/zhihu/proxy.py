# encoding=utf-8
import telnetlib
import urllib
import logging

# ------------------------------------------
#   版本：1.0
#   日期：2017-8-06
#   作者：AlexTan
#   <CSDN:   http://blog.csdn.net/alextan_>  
#   <e-mail: alextanbz@gmail.com>
# ------------------------------------------

logger = logging.getLogger(__name__)
IPPOOLNUM=20 #一次性从网页获取的IP数量

def GetIPPOOLS(num):
    #大象代理买的ip,5元20000个，每十个差不多有一个能用
    IPPOOL=urllib.request.urlopen("http://tpv.daxiangdaili.com/ip/?tid=559480480576119&num="+str(num)+"&operator=1&filter=on&protocol=http&category=2&delay=1").read().decode("utf-8","ignore").split('\r\n')
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
                telnetlib.Telnet(ip,port=port,timeout=2) #检验代理ip是否有效
            except:
                logger.warning("The ip is not available !( IP:%s )" % ipall)
            else:
                logger.warning("Get ip Success!( IP:%s )" % ipall)
                rconn.set("IP:%s:10"%(ipall),ipall)     #10 is status
    else:
        logger.warning("The number of  the IP is %s!" % str(ipNum))

def updateIPPOOLS(rconn,ip,status,flag=0): # 0代表对status减一，-1代表减2，1代表加1
    if int(status) < 1:
        removeIPPOOLS(rconn,ip,status)
        return
    '''update status'''
    if flag == 1: #+status
        if int(status) < 10:
            rconn.delete('IP:'+ ip + ':' + status)
            status = int(status) + 1
            rconn.set("IP:%s:%s"%(ip,str(status)),ip)
    elif flag == -1:
        rconn.delete('IP:'+ ip + ':' + status)
        status = int(status) - 2
        rconn.set("IP:%s:%s"%(ip,str(status)),ip)
    else:
        rconn.delete('IP:'+ ip + ':' + status)
        status = int(status) - 1
        rconn.set("IP:%s:%s"%(ip,str(status)),ip)

def removeIPPOOLS(rconn,ip,status):
    logger.error("IP:%s not available ! System is deleting" % ip)
    try:
        rconn.delete('IP:' + ip + ':' + status)
    except:
        pass
    ipNum=len(rconn.keys('IP*'))
    logger.warning("The number of  the IP is %s!" % str(ipNum))
