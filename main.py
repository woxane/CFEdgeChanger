#!/usr/bin/python3


from os import path , system , stat
from sys import argv


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
        File.write(f'\nZone = {Zone}')
        File.write(f'\nDnsRecord = {DnsRecord}')
        File.write(f'\nEmail = {Email}')
        File.write(f'\nAuthKey = {AuthKey}')


def ScannIp() :
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
    
    print(f'The best ip for this network is : \nPing : {Ping} , Ip : {Ip}')    


if __name__ == '__main__' :
    CreateConfig()
    ScannIp()
