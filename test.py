from msgraph_api import MSGraphAPI

msgraph = MSGraphAPI()
msgraph.get_token()

# data = {"numero_maquina": "100000", "serial_number": "SM-0000-000000"}
# sharepoint_machine_id = msgraph.insert_machine(data)
# print(sharepoint_machine_id)

msgraph.update_machine(1752, {"creditos_maximos": "90", "creditos_1": "0.05", "porcentaje_1": "92", "creditos_2": "0.1", "porcentaje_2": "92"}) 

# msgraph.update_machine(14, {"serial_number": "X124", "juego": "Otro juego"})

# maquina = msgraph.get_machine_by_id(14)
# print(maquina._data)

#msgraph.delete_machine(12)

# from database import Database
# database = Database()

#print(database.exist_machine("123457"))

data = {}
data["numero_maquina"] = "123456"
data["serial_number"] = "R1235"
data["fabricante"] = None
data["juego"] = "Piruo"
data["modelo"] = None
data["progresivo"] = None
data["tipo_progresivo"] = None
data["cantidad_lineas"] = None
data["creditos_maximos"] = None
data["main_program"] = None
data["pay_table"] = None
data["base_program"] = None
data["creditos_1"] = None
data["porcentaje_1"] = None
data["creditos_2"] = None
data["porcentaje_2"] = None
data["creditos_3"] = None
data["porcentaje_3"] = None
data["creditos_4"] = None
data["porcentaje_4"] = None
data["acepta_bill"] = None
data["marca_bill"] = None
data["modelo_bill"] = None 
data["version_bill"] = None
data["impresora"] = None
data["marca_printer"] = None
data["modelo_printer"] = None
data["version_printer"] = None
data["sala"] = None
data["area"] = None
data["gerencia"] = None
data["empresa"] = None
data["estado_maquina"] = None 
data["pais_fabricacion"] = None
data["fecha_fabricacion"] = None 
data["layout_x"] = "12"
data["layout_y"] = "23"
data["premio_maximo"] = "1"
#database.insert_machine(data, "13")

# print(database.get_machines_marked_for_delete())

# print(database.get_sharepoint_machine_id("123456"))

# database.delete_machine("123460")

# database.start_machine_sync()

# print(database.get_machine_data("123456"))

# numero_maquina = "123456"
# id, data_base = database.get_machine_data(numero_maquina)
# changed_fields = database.get_diferences(data, data_base)
# print(changed_fields)

# database.update_machine(numero_maquina, changed_fields)