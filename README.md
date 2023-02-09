# CloudFlare Record Changer
This script scans cloudflare IP addresses and Gives you IPs which work with CDN and update your record that you want . 

Special thanks to [Morteza Bashsiz](https://github.com/MortezaBashsiz/CFScanner) that wrote the scanner . 

You have to install following packages for scanner .
```
git
bc
curl
nmap
parallel
```

## How to run
1. Clone

```shell
git clone https://github.com/woxane/CFEdgeChanger.git
```
2. Run it ,  
```shell
python main.py [process count] [NetworkIsp] [Addr of ip range]
```
For example  :
```shell
python main.py 16 Mci ip.txt
```
