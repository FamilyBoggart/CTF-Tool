from factordb.factordb import FactorDB

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