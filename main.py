#!/usr/bin/python3


from os import path , system , stat
from sys import argv
import requests
from json import loads
import CONFIG
import subprocess

def CreateConfig() : 
    # Create cloudflare config file . 
    if path.exists('CONFIG.py') : 
        return 
       
    Zone = input('Enter your domain(zone) in CloudFlare : ') 
    DnsRecord = input('Enter your subdomain in CloudFlare : ')
    Email = input('Enter your CloudFlare email : ')
    AuthKey = input('Enter your CloudFlare Auth-Key : ')

    with open('CONFIG.py' , 'w') as File :    
        File.write('#Made With <3')
        File.write(f'\nZone = "{Zone}"')
        File.write(f'\nDnsRecord = "{DnsRecord}"')
        File.write(f'\nEmail = "{Email}"')
        File.write(f'\nAuthKey = "{AuthKey}"')


def ScanIp() :
    ScriptDir = path.abspath(path.dirname(argv[0]))
    Thread = argv[1]
    NetworkIsp = argv[2]
    IpRanges = argv[3]
    Output = f'result-{NetworkIsp}.cf'
    system(f'{ScriptDir}/FindIp.sh {Thread} {NetworkIsp} {IpRanges}')     

    if stat(Output).st_size == 1 : # means if file is empty 
        return 

    with open(Output , 'r') as File :
        Ping , Ip = File.readlines()[1].split()
    
    print(f'The best ip for this network is : \nIp : {Ip} , Ping : {Ping}')    

    return Ip

def ZoneIdGet() : 
    Zone = CONFIG.Zone
    Email = CONFIG.Email
    AuthKey = CONFIG.AuthKey
    DnsRecord = CONFIG.DnsRecord

    Header = {'X-Auth-Email' : Email , 'X-Auth-Key' : AuthKey , 'Content-Type' : 'application/json'}
    Url = f"https://api.cloudflare.com/client/v4/zones?name={Zone}&status=active"

    Req = requests.get(Url , headers=Header)
    Data = loads(Req.text)

    ZoneId = Data['result'][0]['id']
    
    return ZoneId

def DnsRecordGet() :
    Email = CONFIG.Email
    AuthKey = CONFIG.AuthKey
    DnsRecord = CONFIG.DnsRecord

    Header = {'X-Auth-Email' : Email , 'X-Auth-Key' : AuthKey , 'Content-Type' : 'application/json'}

    ZoneId = ZoneIdGet()

    Url = f'https://api.cloudflare.com/client/v4/zones/{ZoneId}/dns_records?type=A&name={DnsRecord}'
    Req = requests.get(Url , headers = Header)
    Data = loads(Req.text)

    ARecords = [[Data['content'] , Data['id']] for Data in Data['result']]  # get data in this format [ip , CloudFlare Dns Id]
    
    return ARecords

def GetPing() : # This Part of code came from this repo https://github.com/MortezaBashsiz/CFScanner    
    ARecords = DnsRecordGet()
    n = 1
    for Data in ARecords :  #Data[0] is ip
        Command = "timeout 2 curl -s -w 'TIME: %{time_total}\n' --tlsv1.2 -servername scan.sudoer.net -H 'Host: scan.sudoer.net'" + f" --resolve scan.sudoer.net:443:{Data[0]} https://scan.sudoer.net " + "| grep 'TIME' | tail -n 1 | awk '{print $2}' | xargs -I {} echo '{} * 1000 /1' | bc" 

        Ps = subprocess.Popen(Command , shell = True , stdout = subprocess.PIPE , stderr = subprocess.STDOUT)
        Ping = Ps.communicate()[0].decode().strip()
        print(f'{n}) Ip : {Data[0]} , Ping : {Ping if Ping else "FAILED"}')
        n += 1

    IndexOfIp = int(input('Enter the index of ip you want to change : ')) - 1

    return ARecords[IndexOfIp]
        

def RecordUpdate() :

    ZoneId = ZoneIdGet()
    DnsRecordId = GetPing()[1] 
    Ip = ScanIp() 
    Email = CONFIG.Email
    AuthKey = CONFIG.AuthKey
    DnsRecord = CONFIG.DnsRecord

    Header = {'X-Auth-Email' : Email , 'X-Auth-Key' : AuthKey , 'Content-Type' : 'application/json'}
#    Data = {'type' : 'A' , 'name' : DnsRecord , 'content' : Ip , 'ttl' : 1 , 'proxied' : 'false'}
    Data = "{\"type\":\"A\",\"name\":"+f"\"{DnsRecord}\""+",\"content\":"+f"\"{Ip}\""+",\"ttl\":1,\"proxied\":false}"
    Url = f"https://api.cloudflare.com/client/v4/zones/{ZoneId}/dns_records/{DnsRecordId}"

    Req = requests.put(Url , headers = Header , data = Data)
    print(Req)
    print(Req.text)




if __name__ == '__main__' :
#    CreateConfig()
#    ScannIp()
#    DnsRecordGet()
#    GetPing()
    RecordUpdate()
