course_config = {
    'schedule_page_url': 'https://my.gwu.edu/mod/pws/subjects.cfm',
    'campus_id': '1', # Main Campus
    'term_id': '202302',
    'course_page_url': 'https://my.gwu.edu/mod/pws/courses.cfm?'
}
bkstr_config = {
    'base_url': 'https://svc.bkstr.com/courseMaterial/results',
    'params': {
        'storeId': '10370',
        'langId': '-1',
        'catalogId': '11077',
        'requestType': 'BookLook'
    },
    'json_data': {
        'bookstoreId': '122',
        'courses': [
            {
                'courseDisplayName': '6190',
                'departmentDisplayName': 'AMST',
                'divisionDisplayName': '',
                'sectionDisplayName': '10',
                'courseRefId': '',
            },
        ],
        'termId': '202302',
    }
}

bkstr_headers = {
    'chrome': {
        'authority': 'svc.bkstr.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'cookie': '_pxvid=08d399a9-169b-11ee-b61c-5e1e9bb8bc21; __pxvid=08f4be25-169b-11ee-b875-0242ac120004; _gid=GA1.2.1626338468.1688056562; RES_TRACKINGID=86193645346565088; dtm_token=AQEHHLXJHpiBEwFdekJ3AQEI-wE; _gcl_au=1.1.1997146795.1688056565; _pubcid=05fe4ba7-88f3-47cc-be01-5bf0eddd15fd; _cc_id=dba6712c988741c00f321a3fca261d15; panoramaId_expiry=1688661369985; panoramaId=6486a2ca1575c00603f8092e44c34945a7022ecb1dd94a87cfde2079ae2012f7; panoramaIdType=panoIndiv; dtm_token_sc=AAAGHbTIH5mAEgBce0N2AAAAAAE; _fbp=fb.1.1688056581979.834552966; _scid=b356fe70-42ea-4140-b5b1-49690f6e6d1e; _sctr=1%7C1688011200000; dtCookie=v_4_srv_4_sn_4DC101229CEA7076494042875659372D_perc_100000_ol_0_mul_1_app-3A45f2676e29f53eb9_1; rxVisitor=1688137129423KST3CEGCKNGM2M6P23VGI8FJ62N4SH9Q; dtSa=-; pxcts=9f6348ef-1756-11ee-89d6-4e70424e756a; TLTSID=47630579596919552967464083165774; GCLB=CNfPuqGIp5eDEA; efollett_rt=G; AMCVS_712B7B2A53ABFF670A490D45%40AdobeOrg=1; AMCV_712B7B2A53ABFF670A490D45%40AdobeOrg=1176715910%7CMCMID%7C58509804920714268402846530781579044103%7CMCAAMLH-1688741932%7C7%7CMCAAMB-1688741932%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1688144332s%7CNONE%7CvVersion%7C5.4.0%7CMCIDTS%7C19538; s_ips=944; s_tp=2253; s_ppv=122%253ACourse%2520Materials%2520Results%2520Page%2C42%2C42%2C944%2C1%2C2; s_cc=true; productnum=12; IR_gbd=bkstr.com; IR_2379=1688137130385%7C217066%7C1688137130385%7C%7C; IR_PI=14c1c8a1-169b-11ee-92ea-c3baa5af2bf3%7C1688223530385; OptanonConsent=isIABGlobal=false&datestamp=Fri+Jun+30+2023+10%3A58%3A53+GMT-0400+(Eastern+Daylight+Time)&version=6.13.0&hosts=&consentId=bd933f78-c331-4935-9444-159d79391118&interactionCount=1&landingPath=NotLandingPage&groups=1%3A1%2C2%3A1%2C3%3A1%2C4%3A1&AwaitingReconsent=false; _uetsid=14ffa2e0169b11eeb39e3f52d3854ca3; _uetvid=14ffc950169b11ee9b47df5cb4bb5ee8; _scid_r=b356fe70-42ea-4140-b5b1-49690f6e6d1e; __gads=ID=45cb723813a57d23:T=1688056567:RT=1688137136:S=ALNI_MZK-wmFVfN6b451L2Z1Ph46rl2jnQ; __gpi=UID=0000099f805e6037:T=1688056567:RT=1688137136:S=ALNI_MZcU8fzg4S8_b8Bh9vz1ML0-dIcig; __qca=P0-1058319018-1688137134777; _ga_KEQCWK2159=GS1.1.1688137300.1.0.1688137300.0.0.0; _ga_8YK08B82BK=GS1.1.1688137132.1.0.1688137300.0.0.0; _ga=GA1.2.1418270828.1688056562; efollett_puid=1688137302801-1567870; rxvt=1688139102480|1688137129424; _px3=3721db3aefcfff4f7ddaaf6a9a968ef33fb0e7625ac0f2d2ffac9a4c55e1dd72:MFJMVHHvwNbbh9TRDF40jFU55mTHHwOPJSCGqewELCgnn1MQBnMKBFkmcnXGJ1AzY2Rv1ISQHOPpmAQweJvwUg==:1000:giB1WlUPmlULuJgsWDXx/6jx58kEcD49s7+tTxOzNcZ0W+EChMaYQaQ5blIeB7P1k4uSv3CUKb5KXlxGtHuO8IfEpAamyjoOq9TlEbpgayZzWzNurWxbSNAfVfox7ttDxcmh5wudNunXezczdoMiMho+8HnJXKR2Zb3ayR/Qv/NDYg/D5Zdz8y38FAqlhpZ7eyc+5/0f4PexUfy08LXcVA==; dtPC=4$337301124_90h16vHPLWBSPPPPFKCPHEAIRLPMBDRATAETTF-0e0',
        'origin': 'https://www.bkstr.com',
        'pragma': 'no-cache',
        'referer': 'https://www.bkstr.com/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    },
    'firefox': {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/114.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'Origin': 'https://www.bkstr.com',
        'Connection': 'keep-alive',
        'Referer': 'https://www.bkstr.com/',
        'Cookie': '_pxvid=26c7697b-f993-11ed-af20-fc53f410491e; __pxvid=2732ee53-f993-11ed-930f-0242ac120004; _pxhd=IocdjTygYAG9o3Kxwq1jiOyR42gLP7AJrC4qyvGMoe2/bPXXXHlBlJNlSt/qmOZ5Rq9TCZeO2UFRDl/plSmSYg==:dqKIAIArGuR7IXR7zUqHaqminMP3D1jeiYO3BwJl4nv59JJ8Wq-RD6MebZcgca7yh9ohv2EhgdJM9JOS2EjnLUp3qTMi8-XwpgHJCuU14Eaw71qYMMSet9LY1S7owypv12gqcfkCkfX/dB5w1MV/kg==; OptanonConsent=isIABGlobal=false&datestamp=Fri+Jun+30+2023+13%3A21%3A27+GMT-0400+(Eastern+Daylight+Time)&version=6.13.0&hosts=&consentId=e2038ae1-5469-4fc6-b156-1bbb40bb98b9&interactionCount=1&landingPath=NotLandingPage&groups=1%3A1%2C2%3A1%2C3%3A1%2C4%3A1&AwaitingReconsent=false; _ga=GA1.2.1942408775.1684864593; _gcl_au=1.1.1744189819.1684864595; AMCV_712B7B2A53ABFF670A490D45%40AdobeOrg=1176715910%7CMCMID%7C25084496015473590822373679261827398831%7CMCAAMLH-1688750442%7C7%7CMCAAMB-1688750442%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1688152842s%7CNONE%7CvVersion%7C5.4.0%7CMCIDTS%7C19538%7CMCSYNCSOP%7C411-19542; productnum=39; dtm_token_sc=AAACUmThyIodowBuJ5AcAAAAAAE; dtm_token=AQEGOYEvzTjHOQFQ8DFMAQEBAQA; RES_TRACKINGID=19505824359546848; _pubcid=c6d127f8-af88-4d5c-a7d0-76dac284e72c; _cc_id=7fedcb8385c63485cb6f5a2bad60aa5e; __gads=ID=1ac9c514aa44fd7f:T=1684864596:RT=1688145690:S=ALNI_MajSrcsVE-nbQp5b6XhvNj0ja61UA; __gpi=UID=00000c283d30545e:T=1684864596:RT=1688145690:S=ALNI_MZxOZpF8WiEmRdvG4b9YddaRbg0EQ; _scid=206b9a8c-6731-4f9c-a58a-973a0112461b; IR_PI=446f0af2-f993-11ed-affa-af74c34ebb15%7C1688232083408; _fbp=fb.1.1684864642450.1364069069; _sctr=1%7C1687752000000; panoramaId_expiry=1688407165524; panoramaId=5669b98fe44dfc45c89192632ce216d53938c47d60a7b4873efcd6a007e88464; panoramaIdType=panoIndiv; dtCookie=v_4_srv_7_sn_5869A837395A4D5C8C7A01F84384B6F1_perc_100000_ol_0_mul_1_app-3A45f2676e29f53eb9_1; rxVisitor=1688145636722EMODN1FG7OJOOFLN7HMQAQDKVCDJHO8A; dtPC=7$345729672_875h16vCUHVTOCLJAPRKWUAAHKJAWUUFSPOVJRO-0e0; rxvt=1688147530646|1688145636723; dtSa=-; pxcts=6dbe8b3d-176a-11ee-a434-786b4e65596c; TLTSID=11825141073730440941506231799703; GCLB=CISxj4nqhtP1EA; _px3=9448f8a7c6bf5f08475876c79c06aee9006137d05fc30a9b6d6c2c04370c6eeb:25C26Z3p6upKbRG16VsMVOtEGX0yr9mI7ITi9hgGlZ3dE9DZSm8JEBySL/dZDqctsXMGbeYPriNxth+TDgtR0A==:1000:NdYEPHdMgihDzZ40+iouQ3+Sg2bGg9TjnKCXt52psvd28EfVcQ9HIPrLINdXV6WVy0iXoqRol8DzCSpODL7Ggon0FXgGzFIsyT7ZuemMKXstir3PH8ZtJEapXE1FENqbrxqSBFcC4rgKX22k2AeYSyKN3P+ZmHL7c3ngN7qSwxGt8vp1aFFJiAqNP3njD9UpwQ9J/DLcIeyayVyfgn7uJA==; _gid=GA1.2.2107757603.1688145640; efollett_puid=1688145730664-1574640; efollett_rt=G; AMCVS_712B7B2A53ABFF670A490D45%40AdobeOrg=1; s_ppv=122%253ACourse%2520Materials%2520Results%2520Page%2C29%2C29%2C669%2C1%2C3; s_ips=669; s_tp=2347; s_cc=true; IR_gbd=bkstr.com; IR_2379=1688145683408%7C127923%7C1688145683408%7C%7C; _uetsid=5019ff60169b11eea2d3c38e141e2672; _uetvid=831488b0344f11eda2a6832312469d81; _scid_r=206b9a8c-6731-4f9c-a58a-973a0112461b; __qca=P0-1367091946-1688145688918; _ga_KEQCWK2159=GS1.1.1688145653.1.0.1688145729.0.0.0; _ga_8YK08B82BK=GS1.1.1688145642.1.1.1688145729.0.0.0',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'trailers',
    }

}