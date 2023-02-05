#!/usr/bin/python3


from os import path



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



if __name__ == '__main__' :
    CreateConfig()
