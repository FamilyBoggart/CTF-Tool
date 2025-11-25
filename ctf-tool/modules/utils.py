#from factordb.factordb import FactorDB
#PARSING TOOLS
def parse_data(data):
    if isinstance(data, str):
        return data.encode('utf-8').decode('unicode_escape').encode('latin1')
    elif isinstance(data, bytes):
        return data
    elif isinstance(data, int):
        length = (data.bit_length() + 7) // 8 or 1
        return data.to_bytes(length, byteorder = 'big')
    elif isinstance(data, bytearray):
        return bytes(data)
    else:
        raise TypeError(f"Tipo de dato no soportado : {type(data)}")

def matrix2bytes(matrix):
    """ Converts a 4x4 matrix into a 16-byte array.  """
    return bytes([matrix[row][col] for row in range(4) for col in range(4)])

#FACTORING TOOL
def factorise(number):
    f = FactorDB(number)
    f.connect()
    factors = f.get_factor_list()
    return factors

# Read file
def read_headers_file(archivo):
    """
    Lee y procesa un archivo de headers para usar en peticiones HTTP
    """
    headers = {}
    try:
        with open(archivo, 'r') as f:
            lines = f.readlines()
            
            # Procesamos la primera línea si existe
            if lines and not lines[0].strip().startswith('#'):
                first_line = lines[0].strip()
                if ':' not in first_line:
                    # Si no tiene dos puntos, es probablemente el método HTTP
                    headers['Method'] = first_line
                else:
                    # Si tiene dos puntos, lo procesamos como cualquier otra línea
                    key, value = first_line.split(':', 1)
                    headers[key.strip()] = value.strip()
            
            # Procesamos el resto de líneas
            for line in lines[1:]:
                line = line.strip()
                
                # Saltamos líneas vacías o comentarios
                if not line or line.startswith('#'):
                    continue
                    
                # Dividimos en clave:valor
                parts = line.split(':', 1)
                if len(parts) != 2:
                    print(f"Advertencia: Línea ignorada por formato incorrecto: {line}")
                    continue
                
                key, value = parts
                headers[key.strip()] = value.strip()
        
        return headers
    except FileNotFoundError:
        print(f"No se encontró el archivo {archivo}")
        return None
    except Exception as e:
        print(f"Error leyendo el archivo: {e}")
        return None
