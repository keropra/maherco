from flask import Flask, request, jsonify, send_from_directory
import requests
import time
import threading
import random

app = Flask(__name__)

#room_id = '11677377'
room_id = '29832488'
running = False
log_messages = []
last_cycle_time = 0
round_count = 0

accounts = [
    {"name": "Omar_Youssef12", 
    "cookies": {
    'USER_LOCALE': 'en',
    'cookie_preferences_set_v1': '%7B%22state%22%3A%7B%22preferences%22%3A%7B%22necessary%22%3Atrue%2C%22functional%22%3Afalse%2C%22performance%22%3Afalse%2C%22targeting%22%3Afalse%2C%22userHasMadeChoice%22%3Atrue%7D%2C%22functionalEnabled%22%3Afalse%2C%22performanceEnabled%22%3Afalse%2C%22targetingEnabled%22%3Afalse%7D%2C%22version%22%3A0%7D',
    'XSRF-TOKEN': 'eyJpdiI6IlR6czJNUndTMW5QcWNlMjh4Y0pnd0E9PSIsInZhbHVlIjoiM091blN3Y1RmL000ekY0RU9vU2J2dWpyaGxqSDFGOXhubmV4alkyUk5XSDk0SyttcUFESERwb245d0o1VkVSc0ltYzV0NHNEbjFVN0hIK3NkdzNnZGxRSzFWZC9Ud292RURiNUUvWHIvZmh1cFZEa1dYNU5WME52aEFNSkdRN3AiLCJtYWMiOiI0YTZlNTk1OTZhNmI3NGI3ZDNmNjQ3YWY0YWY1YmY4MmU4YTE0NjdiMDk5ZTM3MGYzNDgzYTU2NzgwMmYwYjcxIiwidGFnIjoiIn0%3D',
    'kick_session': 'eyJpdiI6IjBSVzNncDZFU3NOYUZYV2t0ZmNrVWc9PSIsInZhbHVlIjoiVDd0QW9ldnIwenpBQURZaG52Q2JDdGtoVXVYdUYxUVJwRGlPbVFzVmZaaUo1UU1KM2Vhc0paMndTcW84THBSMW5hNTB6enkyVnYrZ3JPNU9zT3ZVRUxnYjZqNWtTRjZVekVGVzA5NGM1eEhlUzkwTGdEMC9Rblo5dXdMeDhON0wiLCJtYWMiOiI0OGRmYzVjNjljODIxYjExZmNkOTlkZjMzZTViMTM2ODFiYTYyNGY0Njc1ZDA1OWM1MWIwMmY1NTkxNzc0N2MwIiwidGFnIjoiIn0%3D',
    'YNK0ut5c0SgF87MuVFGvoYRFX3JSQcUWUmWorNp6': 'eyJpdiI6IkJWc3NyRnFKTHNTdC9nRHhWVUFjQ3c9PSIsInZhbHVlIjoiRHZscjZaY1FVRTZaY1VjbnNoZERldFpHVEFTU09aR0hEdjh2YmVicVVETE9UTzRzT2puanE1a1p1QS9iU2lZNDJhNTM1dW43Tk05VlpCWFdGM1krWmF2TkUxV0RQNzhLeUpxT1dJRzM5dnM4K3c2WHdjalJkdFhXQ2VlbmErWU5GUEVIVm9Mc2lEVDdXZjhETjFBcWN3R2tTNUJEb2p6TmZGak9LSkx5SllublZ2ZHBsdWdHLzBrV0cwdURPYjZNVEFEOGdoaXFaVUN2NUpqYitkTC9ibGUwUWpOYjFqQzcxcTMwaG1qQi9PSUZhQUx2cS8xazNzNng5Y1VBMmZXM0tvWGNTUmVLY2IxclFZU3NXaXBGekMyYUViWGR6YjBRZllaUU1sYmpBOTJBM1lTS0I5dVk0THFDclg0VjIxYzkvbkhsWlRjZ2k3YUpIM0lOYnZoMVRlaElqdm1XSUo0VzZ4SHU1Tm4zUGIxNGJLRisrejQ1ZDRHR2t3NWh1bkhiNFBWRWs0RlljdzVmendCM09UMktPYnJBZ2Q2VHJHREhpVUQ4KzdBTU5KTVdMb1pqbFFKL0NwTzVhMVNKUnFBUG9GWXdqNlJ5V2o2NkZzU2ppclhZV0M0V0wzNlpUZzEzQ2Vud1E2OFU1bUIyeC9naVNCT0xkRWFFQjFQYzM0UTkwRXRnejk4WWpId0Y0bWl6ZWhTMlVTRC8vUDRHaE02MmxCMGlBR3BmcURzZ1AwelFHbExOYVJoVFFSc3EzclFYcFFKeXJLSURoZ1hSd1d5NVZCMTJXdz09IiwibWFjIjoiNzgyZWZmN2JjZDc2N2RhMjkzOTUwMDJkYjVjZDQ2NjM0NTA1Y2VkODU4Y2IzNjUxNmNiNmNmOTQzOWY2M2FkNyIsInRhZyI6IiJ9',
    'session_token': '235310106%7CFdbCzOjHD4SRQFUnzuVxAFxgx3OqsyvOIZeU7QSL',
    '_cfuvid': 'BopRy5T38c6du5RsSvvto.QFHirN1FmX29xIbMEoE90-1751488029663-0.0.1.1-604800000',
    'KP_UIDz-ssn': '0bO3OaghiKmdXeV8m4yDozaEb7UByHskAaVacqZX3LVy3XERCSvxs2yKXIOMZRzgFz8xZCBPZIA8TUeee3SjUsoCJhFiWwDK1ngvu9OEct2QJAMKjGu5PXcD2uNN20bsAsHu4wLU1JzOO3e9nVkLYrYBR7TgWk9rsGsvzcRCwZE',
    'KP_UIDz': '0bO3OaghiKmdXeV8m4yDozaEb7UByHskAaVacqZX3LVy3XERCSvxs2yKXIOMZRzgFz8xZCBPZIA8TUeee3SjUsoCJhFiWwDK1ngvu9OEct2QJAMKjGu5PXcD2uNN20bsAsHu4wLU1JzOO3e9nVkLYrYBR7TgWk9rsGsvzcRCwZE',
    '__cf_bm': 'BmQ_UJFZTMjnujtPmdaw0OE9CeKF6Pb4mzR38QrFZ.Y-1751505602-1.0.1.1-XpHXgq2Nj1wnX2ncByCDUUv0fpDyj0i9BjAnEiyoS3r0FNCLo0Ei1.sSPXdrtiAnhFOXeD8FLdPCbJc6vWpsDQISPvvWCoc3ozIJoBdmiAo',
    'cf_clearance': 'IIpLQVRSXn94DLgPCaDrv4VDvhsQMHq9x.F57Ddz.Ck-1751505602-1.2.1.1-2DPa.LepSI.1Q8DG7kr1vKK0cr3Ua04hITUxmz2mmeWJ2uGD1itC.AfB8UqA3dIHaEMAJtimCeIZ42d0c_o_N3X8lJkTDQ6BSe8V1uir6.Q5UHadR0K5XcHLCZk4f.w642EXjAS2z_uPPqs444FCG7.G0R1CaTyMTQKALHDNCnx7JIMByoHr2SWAe27kNqeLIJhRsHG_MDJ3k_Cb7tgtCDYpo25XPOy6yS2XL2hvqkQ',
    '__stripe_mid': '851c182b-24ac-4cec-9ff2-b7e8beab7b3a0efb5f',
    '__stripe_sid': '18534c40-a4d5-4353-9ec2-3283d1411a8bffa97e',
    }, 
    "headers": {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': 'Bearer 235310106|FdbCzOjHD4SRQFUnzuVxAFxgx3OqsyvOIZeU7QSL',
    'cluster': 'v2',
    'content-type': 'application/json',
    'origin': 'https://kick.com',
    'priority': 'u=1, i',
    'referer': 'https://kick.com/maherco',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    }},
    {"name": "Tariq_Hassan845",
    "cookies": {
    'cookie_preferences_set_v1': '%7B%22state%22%3A%7B%22preferences%22%3A%7B%22necessary%22%3Atrue%2C%22functional%22%3Afalse%2C%22performance%22%3Afalse%2C%22targeting%22%3Afalse%2C%22userHasMadeChoice%22%3Atrue%7D%2C%22functionalEnabled%22%3Afalse%2C%22performanceEnabled%22%3Afalse%2C%22targetingEnabled%22%3Afalse%7D%2C%22version%22%3A0%7D',
    'XSRF-TOKEN': 'eyJpdiI6IiticVVDdEJNbTVITWZzS2VRVWl0MWc9PSIsInZhbHVlIjoiUlNOK0NkNUhPV3FGOHQ1YlhuNVdUb2Y5M3p6ZiszZHpNOW5jdVNIOHJyNUE1QU5qY2lMQlpJOUljMEFzQ2J1dkpycm5wKzVnZnFVMnhPM0lRbGZDOSt3Y1V5bEpSTUVxS3BIRG5BeTZGVmR0dWRlUWFHbFZXenBkYUs4K1ErRVIiLCJtYWMiOiI1N2YyMzg2ZjZiZWFkNDg5ZDYwZTEzZGNkNWQzNGU4NWRmYzkwMWIyMGQxNjlkNDRkODRhMDBmMmYwNzFmNjc0IiwidGFnIjoiIn0%3D',
    'kick_session': 'eyJpdiI6InNwSTVNaGlNMWRDczlBM3RTL3BvT0E9PSIsInZhbHVlIjoicGoxZ3RYMm1WQTNycGprejNSZ3hTeWJpd2tqZ3liS1BSTHZZMG9RbG5yUU5SVDVIOS9sKzVVTFAwVUhTTEpVdlg1Ym80NTlOUmhYa1p4ZnBOTndjYmdOV210UHR1YWdTNk5jOGNVa0szaEZRTnU2cWYxdzZMSlcxQ0NhNXgrKzUiLCJtYWMiOiJlMDMxYjE2NDM2YmYwY2E0YjY0MTY5MTQxYzYxOWE0OGZiZjNjN2I3YTNjMDMwY2M1ZTUzNjc5MDBjODZlZTQ5IiwidGFnIjoiIn0%3D',
    'LP2DqIFNGyxRZxPk80IRtFPdKu3jVm1UdQEhBTxW': 'eyJpdiI6InIwZGlueHBSbXlBQ3dSL1N5bVlaZmc9PSIsInZhbHVlIjoiRkIvL3pNdGZlbWFMd3hXcFBEeW15VFZuNmlmN3Joa1AwaXMrSk9SL3lyemFlNWxsQm5uZjlZeVpaMnp0SExYUVVpWkwxenFkOGllRkFnUlhQdlVQUGl2OTNFaUFJNG5JRXZiL1lsQmZvY1I2ejV2dm8yVllyZDVXYkQ5YjNKejZIaVdRaGZBclgvSzBJbG9tMzhGT3VrbFlOQlFsM2ppRDRZYXV3K1Axa1pEL3NkTGxpUDN1NXZzaStQQ1lnaXZCODdOWXgwdDV4THpxZWhRRjYvME1XbWNNOGZuQ0I3dUlOUUF5cTVvWU91UEw1aS9NRC9pM3JGdjJITjBadVRJT2syUTRuTjZKWDIxa0J4RFlvUGJkd3kvOThPVmJ6K3NuRXc0eVNiWnZCdU0zOHBmYmhqRHZ1M1dZMzBPZTNoQTF1Si9IamNab05hWjk1TzBXWnZDV0xFZTNBK1FaRXgyQXNrNVJtL2hMM3Z1SkF2ZE1nRWc4eGhSQ2xWSXZVVkUwbHJ6QmV2MmIxWWtVV1creE1hVjViZ09USTg1YmxtaDV0REY2UmtMcDY2NzlrQTB0T3JMb1E4TGozbjNVcW11MHVNSTBLTG40WjFoRlBDNUZkd1F1NUVKdUpBNVZIS0xwZmN3b2RJTzBROGllY3NCSzVJd0JIQkp0RTNVTW4waW5mMEtwN3pCbUVUYUJpL1hMWjJXcE9STVhBL2Nod0NDdFdoUVNWTmpjWERDWHZrYWtzS2w0MklEZnp3dkNaYUJWV1dvVlNiNHB1QkNhVXJjRnZRR0gyQT09IiwibWFjIjoiNWU3ZWFmZDVjYjQ4MTE3MjQ2MWRlZWI5NTBlOTYyZTZlNmFlN2ZkMDRiNDdiYWJkMjBmYmQ0YTQ3ZjM5MmJkNyIsInRhZyI6IiJ9',
    'session_token': '234776962%7CvyPEvA1h35fX5WTTrFF9nJxFolzeByJuEuKYjnOa',
    '_cfuvid': '11Yl8VqU5M5oKxTs050TmEWs31gH3vAlOHsGx_p1adg-1751487759705-0.0.1.1-604800000',
    'KP_UIDz-ssn': '0bWCKLX83mciDBcTW0icJtXVEsnLXLA4Cg0IhXeBVBvh67TsnkfKvoCIGAGAn6FjTATRwp64caWNEc93zG2aj9L5Dt4JEE1NpzQDTdfoV8ZLc0pVngOPkupBfInfMcRzZDMVEXbXnDCG3YmSVWSDdDmfo1A4D3ChCsNdi17pkJA',
    'KP_UIDz': '0bWCKLX83mciDBcTW0icJtXVEsnLXLA4Cg0IhXeBVBvh67TsnkfKvoCIGAGAn6FjTATRwp64caWNEc93zG2aj9L5Dt4JEE1NpzQDTdfoV8ZLc0pVngOPkupBfInfMcRzZDMVEXbXnDCG3YmSVWSDdDmfo1A4D3ChCsNdi17pkJA',
    '__cf_bm': 'guWoEEa4cusFmI.UtBc8z6QuhQbl8UE3GzyF9.hhtGI-1751505393-1.0.1.1-__q8axnvw_zw1EhXeBk2xIqk5n9KvPnRGaNmhXncVuSpQ8kpXQM0bNag1QhhTFaqt0FWhBub2do8KBgFWQmUtXEwuPGj3rXntjTqX9rnCIM',
    'cf_clearance': 'm5u4lKyqdmfRiBvLJ7ARXwDxlCWOHusULNJu0kxM2Wc-1751505393-1.2.1.1-rSjZcYrTJndYuesUUIhtYZ17PlZIBAV1sojEh.4PMapGjIPrXb7rYaj5wfD7GKljb0kn6_fsdnwvfqdoLOgkoSaTK36U9JZZt5zgIbqWRxeE.DpHEOTrw4gLpq_g7RCGVb4FGJf3mz5221SD52M4p51.U9Cmi89MNaPvkgFs3J2PtCPyBuwVW28QJVqv2VLIZoAyJgh_GUqA.lOzoCRJwH8A8KwrtAERESHur8CZhgM',
    'USER_LOCALE': 'en',
    '__stripe_mid': 'c9f8e6e0-1ba5-4e9c-8caf-785f03c343f7772066',
    '__stripe_sid': 'e72cfee4-5813-4986-8b1f-79db2457bd103bfe75',
    },
    "headers": {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': 'Bearer 234776962|vyPEvA1h35fX5WTTrFF9nJxFolzeByJuEuKYjnOa',
    'cache-control': 'max-age=0',
    'cluster': 'v2',
    'content-type': 'application/json',
    'origin': 'https://kick.com',
    'priority': 'u=1, i',
    'referer': 'https://kick.com/maherco',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    }},
    {"name": "Medo_com10", 
    "cookies": {
    'cookie_preferences_set_v1': '%7B%22state%22%3A%7B%22preferences%22%3A%7B%22necessary%22%3Atrue%2C%22functional%22%3Afalse%2C%22performance%22%3Afalse%2C%22targeting%22%3Afalse%2C%22userHasMadeChoice%22%3Atrue%7D%2C%22functionalEnabled%22%3Afalse%2C%22performanceEnabled%22%3Afalse%2C%22targetingEnabled%22%3Afalse%7D%2C%22version%22%3A0%7D',
    'XSRF-TOKEN': 'eyJpdiI6ImJ0MFAzNXBBM01sMjIxMFB3T0pPbnc9PSIsInZhbHVlIjoiTzVNakd3WEcxYnVRY2RlbHBBc2JhaHo2YU1ObjlOdDFvcUNlMVZheGpOOW1PbEZZcGdiL3oraGtIOWFIYURnRkthV2VuOVVEWTN2MmJvd3BQZlV4TnJBSVdjSi84SFIxSVdXS293NlBZeTdpeVpralI1M0pTOGtUQk1YMW1Cd1giLCJtYWMiOiI3MzU5MmQ5NWQ1NTM4MmMwMWUyMzg0MDc5ZjA1NWNmNWZlZjU3YTc0NTZhZjVjMGVmODg2ZTBmZTAyMTg1MTA5IiwidGFnIjoiIn0%3D',
    'kick_session': 'eyJpdiI6Im9uaHZLWEJRMVlNNm5OR1V2dzQwTFE9PSIsInZhbHVlIjoibFZMZVJkTWpVcjB2VDU5NitFSmRuUUxKNjZLUEo5a28vMFQxSmpEUlNTcEFYeTNEWUlYZ0pjSm9QY211dEZlZmlqdms1L3dXa3FoMmFWWnJHQkZoTDlwQnVLcHFrRDJZb3duOEp6SGZGdjZORVNpRmgwL1ZJajZnVWtDUk5iR1giLCJtYWMiOiIwYzczYzM2Yzg5NTQyMjNhYjk0MjkzZjllYWE3MjMwNDU1NjRhZGM5MmE5YWI5MzMwYmY3NjFmY2QzYmUwYmI1IiwidGFnIjoiIn0%3D',
    'LJuyNuCS3AlXmYeLDodyl4wXVZa4Ls1rCuKILPVd': 'eyJpdiI6IlNZckd1RHpyU0t2c1JtUXNRSmJRQWc9PSIsInZhbHVlIjoiWElLK0tWbzRHbGdqdCtNQmI1UTg1dFU2MVdrRU9ISEw3SXlHRklvT2tpWGtJelQyVnN4am0vUDB0enhyY0xZUnk4KzFQSm9lbVVEa241QWVkK1JnVEJNY3I2bXRhVEFPWS9STVdoM1NEekJSa3cxL2FXRkI1WS85WFMvalcrVDFDQkcvejAwT2xFNmpWaVZDU1hjN2hXSDl1UjFGaXJXUXhIcng1R09ZQkhHNDRhbFp1eVdyTGZheEd2TEFQN25pSEV3emdrUGEvYVlKR3ducDJnRUxzbmJDQjRTd2dJaWdtbmNHY0NreTM3VGJYdlluOUtqYm1wK2pGQkJpcjNpdzJ4SXl4aWRwajJjd3lFcnJRekNHVmo5cTg0NnJXVmluM3QzbllMSzFFb1VXQzdPTnFRVXF3dndjTXlyMUQxT1RlUHA4KytSaFFlVFVjazZDSlA0QjZEdFNrN2gzS3RXMUdaMjJzbHNnN3BkeTZjbk9Gb2hXZUg3Z29qODlqbGczZHdJK2oxNWU2V05hNktsbWI2KzFqNWJiRXhEWU1FeUxxTkU1bkZTRUNQaU9wekticzlFWEtxOTdCNk1qS2NaWUw3Y0FRYXMrVjhZQ21Xa0ZpUTdkN281RmNjOGRPNk4zcmhmelM0UmliQ0lzR0hBMkp5UXhRWVNveE1KREd1bjhqdGpZYnl5V2tmNi9MQkZnMEtabW9uOXB6bWpqQmFtSWFsRVNrbU5NNXBFZWFRZE1xeml2d010eXpvRnZJNlU1WWFXMXBnRjZRUnVEakN5cUZlNXh4Zz09IiwibWFjIjoiZTIxMmU5ZDg1MDNmOTM5Y2JmNzFjZDhmNTM4Mzc0Y2NkZWY4ZjZjOTgzM2RhNTk3ZTJhN2I5NjQ2M2FlNzY2OSIsInRhZyI6IiJ9',
    'session_token': '235312501%7Cu3BFTAtC42RNzcth9B7e3mGxvgTUTZLbSIoykHpF',
    '_cfuvid': '5z_D2TGUBw4E4PLE83EIhrcGMyxXwynGHwjYsAZWIyQ-1751488317280-0.0.1.1-604800000',
    'USER_LOCALE': 'en',
    'KP_UIDz-ssn': '0J0JFlcvSH2nWYQLCfjPJ3db2q479GPhvkGeZ6MQGbPNUCuIhwLDUXrQPuropwpvQcTvVxy7yvu86Rv8AKNs4otcYlGUop5KecexFTYS7OOoYISZYySvrOC8401p7PcyZHtOIkGidE8c1lwVvPFI5klhZTmlBSU8aHYYX8P5',
    'KP_UIDz': '0J0JFlcvSH2nWYQLCfjPJ3db2q479GPhvkGeZ6MQGbPNUCuIhwLDUXrQPuropwpvQcTvVxy7yvu86Rv8AKNs4otcYlGUop5KecexFTYS7OOoYISZYySvrOC8401p7PcyZHtOIkGidE8c1lwVvPFI5klhZTmlBSU8aHYYX8P5',
    '__cf_bm': 'ITijiLCzlGbvKPCg0307nBDUGfvLZw1168r9RG4xl6U-1751505664-1.0.1.1-11urAVrV9yNcolGnFCXf_9yeDDly_rVJK5FAEEqzYOnymlEYZWUwP.QS9PT8Yj2cD2zkn0_XZJcMI7CgiLIakv38VTAE4jhM6iy.H.TNTlI',
    'cf_clearance': 'g4aVg6K4EqqGKC1wcvUrToT4cycBpdDAkBP4fL9qSu0-1751505664-1.2.1.1-3xO_a4XlM8DKz.wqQ_J0me60WOSqiWkF3WCXAWkXM.klQbJnpK_MKYRvBJIS5W0AWgAYA3BoOKJWW7e2QuUozFf54XhkadFWOO690f1sThI9rYb38MMjGE0ixN6YUpV9nbKHgQfVIpoeGVNHWds7Ub8LOlWBvUFFZH.200WeJYmTSH_k4aph_PJmcKGv0vP1wr.b0dsBCiXbpfTjrav9wqud6i.nUvPxnDdYM3bgJs8',
    '__stripe_mid': '95b42b75-9422-40dc-b591-ebcd4042cc22540002',
    '__stripe_sid': '971429af-83ec-4138-bc12-786ef4376564e2650b',
    }, 
    "headers": {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.6',
    'authorization': 'Bearer 235312501|u3BFTAtC42RNzcth9B7e3mGxvgTUTZLbSIoykHpF',
    'cluster': 'v2',
    'content-type': 'application/json',
    'origin': 'https://kick.com',
    'priority': 'u=1, i',
    'referer': 'https://kick.com/maherco',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    }},
    {"name": "egypt12", 
    "cookies": {
    'cookie_preferences_set_v1': '%7B%22state%22%3A%7B%22preferences%22%3A%7B%22necessary%22%3Atrue%2C%22functional%22%3Afalse%2C%22performance%22%3Afalse%2C%22targeting%22%3Afalse%2C%22userHasMadeChoice%22%3Atrue%7D%2C%22functionalEnabled%22%3Afalse%2C%22performanceEnabled%22%3Afalse%2C%22targetingEnabled%22%3Afalse%7D%2C%22version%22%3A0%7D',
    'XSRF-TOKEN': 'eyJpdiI6IjR1RlUzbEJYN1dqTW84ZnlDZU1acHc9PSIsInZhbHVlIjoidHFsb1pTeXpYVjQrS3cxTUFyS0l3MUZWVzg2Wnh5OGovb1FDQlFDa25Ibkh0VEVzbXdia0dPa01CLzJJZ0N2V3RtWlEzbnRPYUR0Z3hLM1N5Y2tUeW4yWFRJSmtjbFgybDU5bmZNa3lQZVIxYlFxWlNFOWduSW1LRWtFNko0VnoiLCJtYWMiOiI5Mzg5NTJkZGYzYWNiYzFlZjgzMzA5NDIyY2I0YmUyMzMyMDlhMTQyOWJhYzE2ODkzYWIyNDdhNzg5YTEwNDkxIiwidGFnIjoiIn0%3D',
    'kick_session': 'eyJpdiI6Ik5KMzNwSzRmVzNTVFZPZS9MR0hNaVE9PSIsInZhbHVlIjoiVktnaWFLaS82bEZCenZiMkUrdVhmOU9CMDFISm1Ndjc4Y3prRW5tUkFhR1grWGc3bS9xQ2xOTXhYODYzRndsSmdQdHFxQTJ1ZnNJenRud0g1TmorWW04MlduNytZZWJPRytCaklsd2ozQWxHZmF6RjErdTI1V0l3UEJsWGNhczYiLCJtYWMiOiJlYjg2ZjhlM2U0ZTlkNjc4OGZhY2ZmZTI3ZTJhYzg1OTg5MmFjYjFkZTZkNDllZmY1ODVlNzYzODc4YjEyMjY3IiwidGFnIjoiIn0%3D',
    'QVkdaApGhxMBt4ANKRSAOJlSaPWZPqFhpabzUwsY': 'eyJpdiI6IkdXVGJlQVF3MGM3UG1wYTZMemhjRWc9PSIsInZhbHVlIjoiOGY4WXBUU05Ca3U4NlJWVWg5OHluTFlnQU9ET2hyek9RSERvN2NNRUtWbUZVaFBSK0ZjeTlYeHZGcmNLNWdvb2ViSExrOTV2NFpHTTRYKzBYYjhoSndQc3RwM2p4ZVArNmMwa25FRkprMXA3R2ZlaUF2V1hTZTdEdXFyMTd2M01QRGtwVGFJeThJWDFzRE83ZlF2RE9uQXdEU1MwOWdqVTlqSTV6bWlJU0V4VmtXRjN1bFpaelNpNTdSbkFPRE9wbFFSbVMzQVFqNlZ5cWhEcFJaVkdHTnNwWEI0bk9CWG5YazBSZWpjZFV1Vmt1bk5QVVhScytuQ1FnLzhDTXd3Q1p1RDV1N0p1WWZCa0sza2tQRk50UDN5WDAwejRLZUw2aW41THNUbGhvZUJPSkxBUi91UXNENGhId2Rra0R3QzIwU0J3Z2hickMvNytMU2ZaL3YvYlV3dk54aFJySUNmbmVET1VKNW5QbDY0UUtzVW50UnpEZCtWL0Q5Zi9oV1dhTHFrV0RZN0RCRzNrOHd6ZytJMUJIOTVBeXlDK2pqOEVyNzN3TUNZRnV4cz0iLCJtYWMiOiJiNDM2ZThlMzI5MzVhMmNkOGMwMGVkNjUxNTA1MDg5MDg0YzYwZWUwZWY4ZjBhZGZhNmFmMTMyOGFjNjg0ZDFjIiwidGFnIjoiIn0%3D',
    'session_token': '235314486%7CoK9VKHl8iiImnsnRWOG2EeyrAptitpyaB0XI0g48',
    '_cfuvid': 'ROcNEdyQzeyiNRo.KjvubQIjFU3APecaCqKL_zlsfbM-1751488498065-0.0.1.1-604800000',
    'KP_UIDz-ssn': '0GxvMZB1NYowisLcyxzaJEub1f4qUpFttM3mYNtqnDd7HXdANUHK39uOl1cXOZ3s6BkbEhpxhMWg7u5vqEND4j8FFf4UZGYGTP7ahMJvRZ5czVnE0sRlEStTDhgtW7A16VF2XyLk92USHUMELrKFtSsjpS1JxpVixnFtL75s',
    'KP_UIDz': '0GxvMZB1NYowisLcyxzaJEub1f4qUpFttM3mYNtqnDd7HXdANUHK39uOl1cXOZ3s6BkbEhpxhMWg7u5vqEND4j8FFf4UZGYGTP7ahMJvRZ5czVnE0sRlEStTDhgtW7A16VF2XyLk92USHUMELrKFtSsjpS1JxpVixnFtL75s',
    '__cf_bm': '_ldecs46BjaBDwkh2gva.hrl6C8badGXQUVYcBFZ_NE-1751505735-1.0.1.1-by4aI_5O_mXzhdDh8h375H429WKwOngjhQkIc5nbCUS3XBmQh7WlCNkLLlZ8W8KnAobn93.49_ThiHZnzB6sIVMVdNJ59FrTpr5xZmyV5Sw',
    'cf_clearance': 'W.4Em.bkO2wd0v9pgTlOxOKWtNMPaGM4WdZad0TKKYc-1751505735-1.2.1.1-n84F49CvZeO8ioKQgIZ3_0_03HgYge151khEvbt9nj2QsIm0pMXOZPw_DGQNNmAWcinWqljdIU2K_gDFwalOWLm7ebvX.MOfLAWk2OMw0RKjL7N_WUMwId3BAcab7uVp1SMQP_9uRKST.OFbTWpjvJRu7TsKD8OFm44l75Q9WiRUIIHiKbph13sRVz7EVpn8RnO2x5Eh3BLkD_bxD.iDU9WZ7U_Wo0jBru7Ep8VM.vM',
    '__stripe_mid': '7f2d1191-3fb9-4f20-bae9-fb04b333d834167be5',
    '__stripe_sid': '40b4c380-eb56-480e-95bc-df98033661d24ccd82',
    }, 
    "headers": {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.7',
    'authorization': 'Bearer 235314486|oK9VKHl8iiImnsnRWOG2EeyrAptitpyaB0XI0g48',
    'cluster': 'v2',
    'content-type': 'application/json',
    'origin': 'https://kick.com',
    'priority': 'u=1, i',
    'referer': 'https://kick.com/maherco',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    }},
    {"name": "Zaid_Khalil023", 
    "cookies": {
     'XSRF-TOKEN': 'eyJpdiI6InhHSEtkd2FZdFpRMXZzNkhNUy9iaFE9PSIsInZhbHVlIjoiMU9FQXppTVR0Y0lZKzM3QW12RU1aZ25mWGxzUkxZUkRpS2V5KzJhTk9hYXRndS84SkxzbCsvOWFkQmo2V2ZlTHFGRGhmdzFXdEtHZVZNYzNlQUFPREZyRSt5RWQ0UEZYZVJDUnE3ckJZbmhpTG15ZXR2MDMrRHlnUEhJazg4VDMiLCJtYWMiOiIzYmFiMGZlZTMzOTA0NjQ3NDE5ZjA0MTAzZGJmOTkzODcxYzI3ZmQxYzZlY2Y2MDA4ZjVhNWVkNmE3Y2JkN2ZkIiwidGFnIjoiIn0%3D',
    'kick_session': 'eyJpdiI6InN1NU9MYzMwVGR5eXJjd3RuNGZYQ2c9PSIsInZhbHVlIjoiOVFBT3lveThseVhqZE1STzdiY0FIMW16NGZwUC9Na0dXVUlpdHpWclFNN3VHSFpRRzIxWTJWcXNQL0xBNldSaHJSU0c2Q1J4ZUZVR0tadHYrN3BlazhqZlV5SlFlYm5Ib2pNb2hNUlMzMWFNSVMyV0N2a1hXNTRWOWhZN0JxV0kiLCJtYWMiOiI2YTc0NzE4ZWFmYjdmZjE3MDc2YzY5OTU3ZmQ4M2VkYzkzYmFhNThiODM1ZjdmODE3YTM0YmYxYjhiNzEzMjYyIiwidGFnIjoiIn0%3D',
    'Y4JpLyp4XlH8YqGuLDmJ3PGqMf1bZXR0S1MY6nzn': 'eyJpdiI6IkVYQVZmR1FRNXlLZnZDUFd0R0EzRWc9PSIsInZhbHVlIjoiNElSWHdLVC93UHFrWlhHQStBeVNNNlMyYUkrNmtTcEE1UlBmTXRuMUhsRmFsZ25oM1p4bUhoRC9TK3dway84cEF2QzY0RDNsM0Y4d3ZsbmlqazRiOG92MzVrV1dlTHZJSXd1cE5VNjhRQW9nSGFqcEQyZWJiTVY2TjB6czIzSGk2KzZpL2lRRlUyeURMU1dxZlZEZG42eW9QdndWbGhWUVdvWGJ1c1pqL2Nza3JTT1IwSFFHNHZJRUNxWlZlSFFsTlJxTWJKQUtrSExDbkRtMlFGTUhqdWovTWNGbXVhMmxZOHdDVVk0Z1VheDF0VlBwanFBY2JhUnh2RFYzOEpFWUpNWnRFTGxJMm14bGx3cmg3WXhUNzJsZURFcU1WT1A5MFZBTDNkc1Zydnl2aUF3MnEzeDMwZDY5NXZkYWZWcW1ORXFWTXpSUFRVVDJLWlhjWWlHL2ZHMFprSG52NEJsSFdFUlJTZ1MwU0EwZ2dKSlcvRHVaQzJVWXl5LzBydE5hQjR6cTgyNHpmdzRONTNWWGo4aHgwOG5oNVpOSmVHR2UxRU5PNnJXZzRhYz0iLCJtYWMiOiJmMTMwNzA3YmZiYTUxYmMzZmIzOTEyZTY0NWIwYjk3MGFjMDE0Y2UyYjJhODVkMjgxY2JlYjFiZDFlMjdmYjI0IiwidGFnIjoiIn0%3D',
    'session_token': '235316560%7CkvuxrZ9pom6MdP9UqnpU6vD15x6oRB83RVRT163R',
    '_cfuvid': '6VtP6fT3273A.tFSjVIw9GH5jZKYDOTqIVEeq4L0QrA-1751488411641-0.0.1.1-604800000',
    'cookie_preferences_set_v1': '%7B%22state%22%3A%7B%22preferences%22%3A%7B%22necessary%22%3Atrue%2C%22functional%22%3Afalse%2C%22performance%22%3Afalse%2C%22targeting%22%3Afalse%2C%22userHasMadeChoice%22%3Atrue%7D%2C%22functionalEnabled%22%3Afalse%2C%22performanceEnabled%22%3Afalse%2C%22targetingEnabled%22%3Afalse%7D%2C%22version%22%3A0%7D',
    'KP_UIDz-ssn': '0KT4BnwFW2xAJQhMcAGV3o4r8SwzxuYGPQlENeczFaGSKctFtaBAqj8lExc93CHSEdBpv7rNx6Q3GVXS8AHKkpmae1IKSp7pyIglosvF2Ob2BG7z4k0bRyofX7mTGikCKeZx5dFbiXI6qYEzRGQktQySzmJMoJx4ftHKhwBG',
    'KP_UIDz': '0KT4BnwFW2xAJQhMcAGV3o4r8SwzxuYGPQlENeczFaGSKctFtaBAqj8lExc93CHSEdBpv7rNx6Q3GVXS8AHKkpmae1IKSp7pyIglosvF2Ob2BG7z4k0bRyofX7mTGikCKeZx5dFbiXI6qYEzRGQktQySzmJMoJx4ftHKhwBG',
    '__cf_bm': 'IWIX_MMZVmn4zcWcoViFNOMDDuLEP4d1UdXza9.dNqE-1751505793-1.0.1.1-8x0s3PEE36QLfgaWt60jExMOVC2hUAJbOsM_apyNZnu3zuAHPxYQuCDevJ3MtKZFvteymbmaBYc4.PEKDws3nkNw3cuW1FsuyYv6BsNMkzQ',
    'cf_clearance': 'y6jgxryk7BwlEpxkYYWHYP1looJ9kmocaJlB2YI8shY-1751505794-1.2.1.1-GK_PPNZ9i7phjh5gPkyvzzgTK6IALUAIkaOxFOPYePDl_ELU1nsRlYhqeovl5TFAM88rCgTPygPTeI6N17iXXhMpsBwYZUTDz1sdLlq4GjQKdWtN47.dWfScU6iN.S_C.bBM.fO_J6.QpEgRmUXtXYVywfR4AeKbwAe7E0VdmvsA3yWTSLBm.pjXGSVEO3xY7q4xZmz42rRawEBpf.bMNdVDNGlRLQci8ATY0vWaQHA',
    }, 
    "headers": {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.7',
    'authorization': 'Bearer 235316560|kvuxrZ9pom6MdP9UqnpU6vD15x6oRB83RVRT163R',
    'cluster': 'v2',
    'content-type': 'application/json',
    'origin': 'https://kick.com',
    'priority': 'u=1, i',
    'referer': 'https://kick.com/maherco',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    }},
    {"name": "ahmed_maher48", 
    "cookies": {
    'XSRF-TOKEN': 'eyJpdiI6IkRaZXY4MExTN3JKVzZ2Y1R1dndhYlE9PSIsInZhbHVlIjoieTR0QUQyenl5UWErVmNKL21NYnl4ZDdRSFVDaWdiblhVVys0OFZNdDNTNkhWYmk0S3E4TFE2RW1EOG1iR2M5WkZtOWJTYldLU0MyZUpHNGhiMnlrYzlWbHA0bjh1RXVueGUrMkpOY3QwWVo5ZG04OFVVZitORlRLWFhmNi9Oam0iLCJtYWMiOiI1NzY4MjI3MTVkMzQ3NTJlYzVkMWQ0OWY4ZWQyOWQ1YjQxYzA2Zjg1NTEwZWFmY2U0MDAyY2NiYzgyNTFkNGU3IiwidGFnIjoiIn0%3D',
    'kick_session': 'eyJpdiI6Ijg4Tk5OMTg3YlJ0Nk9TVzhORHBxZmc9PSIsInZhbHVlIjoiR2UwNncyaVFQNVNUMlNocTk2U1U0MkMzWU42YURmUUl6L2Z5Zk8yQWwzRzhLU3lDdGJ1RGpiTTdJVkxWVHZBMVJZZ3pLYVlxUGR5UWxpUUZPYzNCNnoxQVMwY2tpaHI4RHo1RmFsMS8raEpRcWlaR3VZSGRRTEtVbGZqK1hxWTEiLCJtYWMiOiI4Y2I4YjRlYjZiMzM2ZWFjOTRkNjA3MDM2ZjdiOGMwNWQ4NGRlYTRkZDI1MDkxZjlhMzEwMDMxZGJjYzJiMDkzIiwidGFnIjoiIn0%3D',
    'KYOgJF2RzRnqUoLKLTE7B6w8mCc1fU5ZSKailYF6': 'eyJpdiI6IlR6UTBpTi80d2pBWlYzYStkVk5jc1E9PSIsInZhbHVlIjoiSENXdktQYnpHMHRKczk4WFhRSnVqOGlscmV6SFhvWlVLd0hhaDNiMm5OQU5vWGJ4Tk9uNEFrUnM3SXN3dkx4eXFmS0cwNDJIczJsOUhZRHZRazkzZEdHdWk3by9tMVYxTnRsSTJBeExURmEzZzFub2gwZ2hzcGpEZy9FeVluZHhHYVBidjViMis3ajQxWVFxTlQxMEFMVWxaL2tyVmpyU1NxNHV2a21Sdno4UkFOUjNhN3lDTEs4Vlg2QUw0ZjlaVWpqb3AxK3NnelQwa1FLbE1wa2MyVXYvaFJneTFSYUxuSndmdDFYamlQdzJxS2pHblBFd085ei9zeFNUOURxWlk4elI5ejUxb3gyZjJrbGIxV1dGd1Ivd3IxRkZqcGhJcHlBRHhiM0ZlMjlFZnk1Q0xuQWJVdjZtS0pYdFBONjZ6NU4vMjdJeTJObm1ZeVk0akNuSzd3ZmRPNW5KWnUxc09jTWMvZEY1a3lReDNlSWo1aktsVDBTVk1oRERNNnJrSDA3RGdVbm1IdUtmNE1uVUlmOCtKVng0bFpIVWFJVTA3TlYxbUFidjRsST0iLCJtYWMiOiJkOWI4YmViOGQzNmI1ZTc4ZDU5MmU2YjE4MTQ3NTRlMDM4OWQ5YjdmNGNkYmM0MjE0YzZiNjEyOGYzZDE2ODdjIiwidGFnIjoiIn0%3D',
    'session_token': '235319090%7C1UyBnyjTHLGn8R8JPmnV2oWos7qjQyKLvP623XZP',
    '_cfuvid': 'ybyz3oG4n.HW7aXK_htuDSimg9sxRukUkuGhANBwtwU-1751488586456-0.0.1.1-604800000',
    'cookie_preferences_set_v1': '%7B%22state%22%3A%7B%22preferences%22%3A%7B%22necessary%22%3Atrue%2C%22functional%22%3Afalse%2C%22performance%22%3Afalse%2C%22targeting%22%3Afalse%2C%22userHasMadeChoice%22%3Atrue%7D%2C%22functionalEnabled%22%3Afalse%2C%22performanceEnabled%22%3Afalse%2C%22targetingEnabled%22%3Afalse%7D%2C%22version%22%3A0%7D',
    'KP_UIDz-ssn': '0BI8F0lZjIJwAZa6GR6eiFMBkKjtl3mKqxbeYgx1NwWDIqiIqrGZPV4Mztd6xVDz52s3RHNBUvOkkd0Dd6eyCOrFlJkLiyssDgTktWm1lKIkiqthtLp0duzKx0Je9Yx0JivNYuhgj0bwLiZ5FZCSjdHmvn7BQmstgq11r2py',
    'KP_UIDz': '0BI8F0lZjIJwAZa6GR6eiFMBkKjtl3mKqxbeYgx1NwWDIqiIqrGZPV4Mztd6xVDz52s3RHNBUvOkkd0Dd6eyCOrFlJkLiyssDgTktWm1lKIkiqthtLp0duzKx0Je9Yx0JivNYuhgj0bwLiZ5FZCSjdHmvn7BQmstgq11r2py',
    '__cf_bm': 'J8XOcq_J9wBalNOROCy.KuoUgxVce7sBvSfAW3GmavU-1751505865-1.0.1.1-.EBjcE6b1wTg3R19BEgSKSeRZQR.a8HCyJF8Bf6zkO8aRKQsiUoL08ai_Le3mnGHckmM_xsaqSCL9Db_uaNKy8jY0TLOVt1Mt4Y.gFd9R84',
    'cf_clearance': 'SPKqm8QY.MUGV2PSrszmR1z7tIX9t3cG9DoF1w_dRGM-1751505865-1.2.1.1-vdC9xKsk3BmZGL1MgSFhGZXIxi.uXrps0RsCWujIEPJG.JB2SkVpLw3.Uuihkg31PAQfMK5N0hpxZkONutUYAkyS72cB_OREpXtsUUN08nTt_6GlrMrFYKDnX8JH80H77_0emfvGgDr2agZgzJLPN2wmMrtUcIkuoEsDj7cNUKZkW0M0HeAqs6y4sCW6jp2QMD4b9iYuXCbtL7tdMhaidk5SIqgr5EKsYTG.2i1wg08',
    '__stripe_mid': '9cce4326-7bc3-450a-89e5-105297c9e67382a75c',
    '__stripe_sid': 'a4d0e1b9-aa2e-450c-85e0-db55fdb94217940851',
    }, 
    "headers": {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.8',
    'authorization': 'Bearer 235319090|1UyBnyjTHLGn8R8JPmnV2oWos7qjQyKLvP623XZP',
    'cluster': 'v2',
    'content-type': 'application/json',
    'origin': 'https://kick.com',
    'priority': 'u=1, i',
    'referer': 'https://kick.com/maherco',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    }}
]


# ============ قوائم الرسائل ============

message_groups = [
    [ "[emote:37243:gachiGASM]​" , "[emote:37226:KEKW]", "ههههههههههههه"],
    ["[emote:39250:BBooomer]" , "[emote:39262:duckPlz]" , "[emote:37227:LULW]"],
    ["[emote:43404:mericKat]" , "[emote:39261:kkHuh]" , "[emote:37230:POLICE]"],
    [ "[emote:37243:gachiGASM]​" , "[emote:37226:KEKW]", "ههههههههههههه"],
    ["[emote:39250:BBooomer]" , "[emote:39262:duckPlz]" , "[emote:37227:LULW]"],
    ["[emote:43404:mericKat]" , "[emote:39261:kkHuh]" , "[emote:37230:POLICE]"],
    [ "[emote:37243:gachiGASM]​" , "[emote:37226:KEKW]", "ههههههههههههه"],
    ["[emote:39250:BBooomer]" , "[emote:39262:duckPlz]" , "[emote:37227:LULW]"],
    ["[emote:43404:mericKat]" , "[emote:39261:kkHuh]" , "[emote:37230:POLICE]"],
    [ "خرب يومك ماهر", " خرب  يومك هههههههههههه" ," خرب يومك "],
    [ "ماهركو الحب" , "ابو محمود الحب" , " ماهركو القلب "],
    [" ماهر اللعب RISK مع الاسكواد" , "نبي Risk يا ابو محمود" , "حق ريسك"],
    ["ماهر اللعب Road Craft مع شباب الاسكواد او مع  ميو" , "نبي رود كرافت مع ميو يا ابو محمود" , "حق رود كرافت" ],
    ["نبي دمبله يا ابو محمود " , "امتي هترجع مالطا ؟"],
    ["ابو محمود اشتقنا للعبة المخدرات " , "متي هتلعب لعبة المخدرات ؟" , "مش هترجع تلعب لعبة المخدرات تاني ؟"],
    ["ماهر  لعبة جديدة اسمها محاكي الشاورما اللعبها مع الاسكواد" , "حق لعبة الشاورما" , "ليش ما تلعب لعبة الشاورما"]
]

# ============ إرسال رسالة واحدة ============

def send_message(account_index, message):
    account = accounts[account_index]
    json_data = {
        'content': message,
        'type': 'message',
        'message_ref': str(int(time.time() * 1000))
    }
    res = requests.post(
        f'https://kick.com/api/v2/messages/send/{room_id}',
        cookies=account['cookies'],
        headers=account['headers'],
        json=json_data
    )
    return f"{account['name']}: {res.status_code}"

# =================== حلقة التشغيل ===================
def loop_messages():
    global running, log_messages, last_cycle_time, round_count
    while running:
        round_count += 1
        group_indices = list(range(len(message_groups)))
        random.shuffle(group_indices)
        used_groups = set()
        round_log = [f"🔁 الدورة رقم {round_count}"]

        for i in range(len(accounts)):
            available = [g for g in group_indices if g not in used_groups]
            if not available:
                available = group_indices
            group_index = random.choice(available)
            used_groups.add(group_index)

            message = random.choice(message_groups[group_index])
            result = send_message(i, message)
            log_entry = f"{accounts[i]['name']} ⟶ {message}"
            round_log.append(log_entry)
            time.sleep(2)

        log_messages.append(round_log)
        if len(log_messages) > 3:
            log_messages.pop(0)

        last_cycle_time = int(time.time())
        time.sleep(60)

# =================== API Routes ===================
@app.route('/start_all', methods=['POST'])
def start_all():
    global running
    running = True
    threading.Thread(target=loop_messages).start()
    return jsonify({"status": "started"})

@app.route('/stop_all', methods=['POST'])
def stop_all():
    global running
    running = False
    return jsonify({"status": "stopped"})

@app.route('/logs')
def get_logs():
    return jsonify(log_messages)

@app.route('/last_cycle_time')
def get_last_cycle_time():
    return jsonify({"time": last_cycle_time})

@app.route('/round_count')
def get_round_count():
    return jsonify({"count": round_count})

@app.route('/send/<int:account>', methods=['POST'])
def send_custom(account):
    data = request.json
    message = data.get("message", "رسالة فارغة")
    result = send_message(account - 1, message)
    return jsonify({"status": result})

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')

