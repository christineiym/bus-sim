import requests

ALL_ROUTES = ['1', '11', '12', '13', '14', '15', '16', '17', '18', '19L', \
            '2', '20', '21', '22', '24', '26', '27', '28X', '29', \
            '31', '36', '38', '39', \
            '4', '40', '41', '43', '44', '48', \
            '51', '51L', '52L', '53', '53L', '54', '55', '56', '57', '58', '59', \
            '6', '60', '61A', '61B', '61C', '61D', '64', '65', '67', '68', '69', \
            '7', '71', '71A', '71B', '71C', '71D', '74', '75', '77', '79', \
            '8', '81', '82', '83', '86', '87', '88', '89', \
            '91', '93', \
            'G2', 'G3', 'G31', \
            'O1', 'O12', 'O5', \
            'P1', 'P10', 'P12', 'P13', 'P16', 'P17', 'P2', 'P3', 'P67', 'P68', 'P69', 'P7', 'P71', 'P76', 'P78', \
            'Y1', 'Y45', 'Y46', 'Y47', 'Y49']
ALL_DIRECTIONS = ['Inbound', 'Outbound', 'Both']

headers = {
    # 'Origin': 'http://fiddle.jshell.net',
    # 'Accept-Encoding': 'gzip, deflate',
    # 'Accept-Language': 'en-US,en;q=0.8',
    # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': '*/*',
    # 'Referer': 'http://fiddle.jshell.net/_display/',
    # 'X-Requested-With': 'XMLHttpRequest',
    # 'Connection': 'keep-alive',
}


def main():
    for route in ALL_ROUTES:
        data = {
            'route_name': route,
            'service_day': 'Weekday',
            'date': '202001',
            'direction': 'Both',
        }
        try:
            response = requests.post('http://127.0.0.1:5000', headers=headers, data=data)
            print(response)
        except:
            print(response)

if __name__ == "__main__":
    main()