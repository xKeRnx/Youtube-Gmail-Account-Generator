# Youtube/Gmail Account Generator
<br/>
<br/>
# Windows / Linux / Mac
* ## Installation 
  * $ py pip install -r requirements.txt
  * OR
  * $ py -m pip install -r requirements.txt
  ```
  If something goes wrong, try again after installing latest version pip.
  ```
* ## Usage
   * Open command prompt in Youtube-Gmail-Account-Generator folder and run
        ```
        $ py GmailBot.py
        ```
   * Rest is self explanatory.


# Requirements
 * Python 3.6+
 * High speed Internet Connection
 * Good proxy list (http, https, socks4, socks5)
 * Google Chrome installed on your OS (not Chromium)
 * sms-activate.ru account


# Important Settings
 ```
 ############################# SMS API ##################################### 
 api_key = ''
 country = '0' #0=Russia, 1=Ukraine, 12=USA, , 43=Germany, 32=Romania, 36=Canada : MORE -> https://sms-activate.ru/en/price

 ######################## Proxy settings ###################################  
 #Start with proxy number
 num = 0
 category = "rp" #f=free / r=residential / rp=residential pool - If you use residential pool proxies we will always use the first proxy from file
 background = False
 auth_required = False
 proxyfile = 'proxy.txt'
 proxy_type = 'socks4' # -> https://github.com/TheSpeedX/PROXY-List -> proxy.txt
 ```


# Proxies
 *[IPRoyal](https://iproyal.com) offers datacenter and residential proxies. The Royal Residential proxies have a large pool with addresses in over 160 countries all over the world, so they can generate a massive number of views. IPRoyal agreed to provide a huge discount for my script users, so the price will be as low as 0.60USD/GB! To get this incredible 80% discount for Royal Residential proxies, use the discount code: `youtube80`*


* ## Important Information
   Of course, google also knows all the free proxy server and the created account will be blocked again after a few hours!

* ## Free Proxy
   Try not to use free proxies. But if you have a paid subscription and you want to use authenticated IP feature, then you can use the free proxy category. Provide your text file path (where you saved the proxies) when the script asks for a proxy file name or a proxy API.
   N.B: Available for **http(s)/socks4/socks5**
   
* ## Premium Proxy
   Proxies with authentication can also be done. To do so put your proxies in this format `username:password@ipaddress:port`or `ipaddress:port:username:password` in a text file. Every single line will contain a single proxy. Provide your text file path when the script asks for a proxy file name or a proxy API.
   
   N.B: Only available for **http** type proxy.

* ## Rotating Proxy
   You can also use the rotating proxies service. You can either authenticate your IP on your proxy provider service and use `ipaddress:port` as Main Gateway. 
   N.B: Available for **http(s)/socks4/socks5**

   Or direct use username:password combo like this `username:password@ipaddress:port` or `ipaddress:port:username:password` as Main Gateway.

   N.B: Only available for **http** type proxy.
   You can use proxy API too.


# Big Thanks to:
* I have used these projects as code reference
  <br/>
  https://github.com/MShawon/YouTube-Viewer
  <br/>
  https://github.com/temadol/gmail_generator


# License

The MIT License (MIT) Copyright (c)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
