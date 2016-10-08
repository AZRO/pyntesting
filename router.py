import requests
from requests.auth import HTTPBasicAuth
from lxml import html
from bs4 import BeautifulSoup
import optparse

### this function extract and return the data from th router webpage

def extract_log(url,user,pwd):
    r =""
    response = requests.get(url, auth=HTTPBasicAuth(user, pwd))
    data = response.text
    soup = BeautifulSoup(data)
    for el in soup.find_all('textarea'):
        r+= el.text
    return r 

### because im using asus router at home and on this script i will connect to router via web interface.
### wed:"http://"+router_ip+"/Main_WStatus_Content.asp".
### extract MAC address from returned data ,check extracted Mac with the list of trusted MAC.
### router_ip,user,pwd provided on command line when running the script.

def Mac_verification(router_ip,user,pwd):

    url1 ="http://"+router_ip+"/Main_WStatus_Content.asp"
    url2="http://"+router_ip+"/Main_DHCPStatus_Content.asp"
        
    wifi_log =str(extract_log(url1,user,pwd))
    dhcp_log=str(extract_log(url2,user,pwd))
        
        
    wifi_mac=[]
    dhcp_mac =[]
    
    ### because in the router im using mac filtering options with allowed list of mac
    ### so trusted_mac = list of trusted device/mac address

    trusted_mac = ["00:11:22:33:44:55","00:11:22:33:44:55","00:11:22:33:44:55"]

    wifi_log = wifi_log.split()
    for i in range(28,len(wifi_log),9):
        wifi_mac.append(wifi_log[i])

    dhcp_log = dhcp_log.split()
    for i in range(8,len(dhcp_log),4):
        dhcp_mac.append(dhcp_log[i].upper())

    print"[+]number of connceted clients : ",len(wifi_mac)  
    print ("[-]clients MAC Address : ")
    for x in wifi_mac:
        print (">>>>>>"+ x )    


    for e in wifi_mac:
        if e not in trusted_mac :
            print ("\r\n[+]Intrusion detected >> MAC Address :"+e)
       


        else:print ("\r\n[+]no intrusion :"+e+ " >> trusted device\r\n") 

    return 




def main():

    ### to run the script : router.py -R ip_address -U router_admin -P password
    ### router.py -h for more information

    parser = optparse.OptionParser('%prog '+'-R <router_ip> -U <user> -P <password>')
    parser.add_option('-R', dest='router_ip', type='string',help='specify the router ip ')
    parser.add_option('-P', dest='password', type='string',help='specify admin password')
    parser.add_option('-U', dest='user', type='string',help='specify the admin  username')
    (options, args) = parser.parse_args()
    
    ### router_ip = router ip address
    ### user = router admin user
    ### pwd admin user's password

    router_ip = options.router_ip
    pwd = options.password
    user = options.user
    
    

    if router_ip == None or pwd == None or user == None:
        print parser.usage
        exit(0)
    else:

        Mac_verification(router_ip,user,pwd)
        
if __name__ == '__main__':
    main()