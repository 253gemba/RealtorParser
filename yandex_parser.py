import requests

print()
print("НАЧАЛО")
print()

def get_json():

    cookies = {
        'yandexuid': '8203806711658661592',
        'yuidss': '8203806711658661592',
        'i': 'ri1nmM4e4tharBCiFo9ufwhuX9yoIC6hFy/SCi6xqhJBivhqhaYQiLwwuyXU3S1J+qF6Y5gVyvkH5VHUnHWtX7TfUlI=',
        'ymex': '1974021592.yrts.1658661592#1974021592.yrtsi.1658661592',
        'suid': 'b3dffe55affd5bb23831d24467538a67.1fe465303c8c385a3b00f8cbcd779a7b',
        '_csrf_token': '9ebb2466726b8e8a081658346c035fbbc41eb6292efcc4f1',
        'font_loaded': 'YSv1',
        'gdpr': '0',
        '_ym_uid': '1659084317254038581',
        '_ym_d': '1659084317',
        'tmr_lvid': '39883661f7deb903c675a66db843d8a2',
        'tmr_lvidTS': '1659084395171',
        'is_gdpr': '0',
        'is_gdpr_b': 'CLryEBCTgQE=',
        'from': 'direct',
        'skid': '2832644081659428144',
        '_ym_isad': '1',
        'spravka': 'dD0xNjU5NDQ2NDkxO2k9NS4xOC4xNzkuMTUzO0Q9QzU5RkQwNkI3OEEwNzc1QkEyNjFBQ0U2ODQyMEU1MjU1ODU2N0UwMTFEMURFNDcwQUJCRDk4MzYwQjcwMDUzN0EyMzAzOTcwO3U9MTY1OTQ0NjQ5MTYxNjU3OTA1NTtoPTk0YzlkMDVmYzRjNTJkYTY5OWU3YjExYmQ0MTg5MjM4',
        'tmr_detect': '1%7C1659463491122',
        'tmr_reqNum': '56',
        'rgid': '741964',
        '_yasc': 'fr90J+TKw6c2blYBCuBwDaxtvSn1ywJXQCGNkidFIwc1PECiQOD8xk6k',
        'prev_uaas_data': '8203806711658661592%23530723%23498217%23621144%23610377%23613879%23595584%23611621%23610826%23603501%23545039%23361531%23213159',
        'prev_uaas_expcrypted': 'AlO7N79U3lJrxYzeZiqZ402hiS_4segqR4266p1-FFKnJ_OOG_Bzm7DjLKNHaCjna2GIGm9vqc3YH76sT5dDn-zcs9yqLOuATX-P_6vK1hYRpn-422yhJP4hPDWc49N-JyaGJVNdwzw9PmODOJJwDuGrw206jlIHTTRQgFjYFFqJ7CKr6WCI5LFS-h6bajVK',
        'from_lifetime': '1659477170822',
    }

    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Client-View-Type': 'desktop',
        'Connection': 'keep-alive',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'yandexuid=8203806711658661592; yuidss=8203806711658661592; i=ri1nmM4e4tharBCiFo9ufwhuX9yoIC6hFy/SCi6xqhJBivhqhaYQiLwwuyXU3S1J+qF6Y5gVyvkH5VHUnHWtX7TfUlI=; ymex=1974021592.yrts.1658661592#1974021592.yrtsi.1658661592; suid=b3dffe55affd5bb23831d24467538a67.1fe465303c8c385a3b00f8cbcd779a7b; _csrf_token=9ebb2466726b8e8a081658346c035fbbc41eb6292efcc4f1; font_loaded=YSv1; gdpr=0; _ym_uid=1659084317254038581; _ym_d=1659084317; tmr_lvid=39883661f7deb903c675a66db843d8a2; tmr_lvidTS=1659084395171; is_gdpr=0; is_gdpr_b=CLryEBCTgQE=; from=direct; skid=2832644081659428144; _ym_isad=1; spravka=dD0xNjU5NDQ2NDkxO2k9NS4xOC4xNzkuMTUzO0Q9QzU5RkQwNkI3OEEwNzc1QkEyNjFBQ0U2ODQyMEU1MjU1ODU2N0UwMTFEMURFNDcwQUJCRDk4MzYwQjcwMDUzN0EyMzAzOTcwO3U9MTY1OTQ0NjQ5MTYxNjU3OTA1NTtoPTk0YzlkMDVmYzRjNTJkYTY5OWU3YjExYmQ0MTg5MjM4; tmr_detect=1%7C1659463491122; tmr_reqNum=56; rgid=741964; _yasc=fr90J+TKw6c2blYBCuBwDaxtvSn1ywJXQCGNkidFIwc1PECiQOD8xk6k; prev_uaas_data=8203806711658661592%23530723%23498217%23621144%23610377%23613879%23595584%23611621%23610826%23603501%23545039%23361531%23213159; prev_uaas_expcrypted=AlO7N79U3lJrxYzeZiqZ402hiS_4segqR4266p1-FFKnJ_OOG_Bzm7DjLKNHaCjna2GIGm9vqc3YH76sT5dDn-zcs9yqLOuATX-P_6vK1hYRpn-422yhJP4hPDWc49N-JyaGJVNdwzw9PmODOJJwDuGrw206jlIHTTRQgFjYFFqJ7CKr6WCI5LFS-h6bajVK; from_lifetime=1659477170822',
        'Referer': 'https://realty.yandex.ru/moskva_i_moskovskaya_oblast/kupit/kvartira/bez-posrednikov/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'X-Retpath-Y': 'https://realty.yandex.ru/moskva_i_moskovskaya_oblast/kupit/kvartira/bez-posrednikov/',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    params = {
        'sort': 'DATE_DESC',
        'rgid': '741964',
        'type': 'SELL',
        'category': 'APARTMENT',
        'agents': 'NO',
        '_pageType': 'search',
        '_providers': [
            'seo',
            'queryId',
            'forms',
            'filters',
            'filtersParams',
            'mapsPromo',
            'newbuildingPromo',
            'refinements',
            'search',
            'react-search-data',
            'searchHistoryParams',
            'searchParams',
            'searchPresets',
            'showSurveyBanner',
            'seo-data-offers-count',
            'related-newbuildings',
            'breadcrumbs',
            'ads',
            'cache-footer-links',
            'site-special-projects',
            'offers-stats',
        ],
        'crc': 'y43d20c34e66b03b8457400edb0c5ad89',
    }

    response = requests.get('https://realty.yandex.ru/gate/react-page/get/', params=params, cookies=cookies, headers=headers)
    data = response.json()
    print(type(data))
    # print("price" in data["response"]["search"]["offers"]["entities"][0])
    # print(data["response"]["search"]["offers"]["entities"][0]["price"])
    return data



def get_offers(data):
    offers = []

    entities = data["response"]["search"]["offers"]["entities"]
    print(len(entities))
    i = 0
    for item in entities:
        i += 1
        offer = {}

        price = item["price"]["value"]
        link = 'https:' + item["unsignedInternalUrl"]
        name = item["author"]["agentName"]
        if item.get("updateDate"):
            creat_date = item["updateDate"]
        else:
            creat_date = item["author"]["creationDate"]
        adress = item["location"]["address"]
        # offers.append(offer)
        print(i,price, name, creat_date, link, adress)

    return offers


def main():
    data = get_json()
    offers = get_offers(data)


if __name__ == '__main__':
    main()


'''
https://realty.yandex.ru/gate/offer-phones/get-new/?offerId=5859049218484004865&updateCalls=YES&crc=y8aa51498d1c7106541dbf3c76b5ef395&powB64=eyJoYXNoIjoiMDAwMDAxODI2NTBlMDNiN2Q3NzUyNDA4Y2YwOGVjMzkiLCJ0aW1lc3RhbXAiOjE2NTk1NTI3OTM0MjcsInBheWxvYWQiOiJvZmZlcklkPTU4NTkwNDkyMTg0ODQwMDQ4NjUmdXBkYXRlQ2FsbHM9WUVTJiIsInRpbWVUb0NvbXBsZXRlIjo3Nn0=
https://realty.yandex.ru/gate/offer-phones/get-new/?offerId=2981316173698520576&updateCalls=YES&crc=y8aa51498d1c7106541dbf3c76b5ef395&powB64=eyJoYXNoIjoiMDAwMDAxODI2NTE0YjkwZGY0MWI0MWMyOGY1YWI0MTAiLCJ0aW1lc3RhbXAiOjE2NTk1NTMyMzI5NjcsInBheWxvYWQiOiJvZmZlcklkPTI5ODEzMTYxNzM2OTg1MjA1NzYmdXBkYXRlQ2FsbHM9WUVTJiIsInRpbWVUb0NvbXBsZXRlIjoxODl9
https://realty.yandex.ru/gate/offer-phones/get-new/?offerId=6722184239095533313&updateCalls=YES&crc=y8aa51498d1c7106541dbf3c76b5ef395&powB64=eyJoYXNoIjoiMDAwMDAxODI2NTFkOTdlNzRiYjYyNTU1OGI5YWM2YmEiLCJ0aW1lc3RhbXAiOjE2NTk1NTM4MTQxOTEsInBheWxvYWQiOiJvZmZlcklkPTY3MjIxODQyMzkwOTU1MzMzMTMmdXBkYXRlQ2FsbHM9WUVTJiIsInRpbWVUb0NvbXBsZXRlIjoyOTJ9
                                                                                                                                             eyJoYXNoIjoiMDAwMDAxODI2NTBlMDNiN2Q3NzUyNDA4Y2YwOGVjMzkiLCJ0aW1lc3RhbXAiOjE2NTk1NTI3OTM0MjcsInBheWxvYWQiOiJvZmZlcklkPTU4NTkwNDkyMTg0ODQwMDQ4NjUmdXBkYXRlQ2FsbHM9WUVTJiIsInRpbWVUb0NvbXBsZXRlIjo3Nn0=
'''