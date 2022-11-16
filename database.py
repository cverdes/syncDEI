import sqlite3

class Database():

    def __init__(self):
        super().__init__()
        # abre la base de datos
        self.con = sqlite3.connect("syncDEI.db")
        self.cur = self.con.cursor()


    def start_machine_sync(self):
        # pone todos los campos en delete = True
        self.cur.execute("UPDATE base_maquinas SET [delete] = 1")
        self.con.commit()


    def exist_machine(self, eva_machine_number):
        res = self.cur.execute(f"SELECT * FROM base_maquinas WHERE numero_maquina='{eva_machine_number}'")
        return not(res.fetchone() is None)


    def get_machines_marked_for_delete(self):
        # devuelve una lista de tuples con la forma [(numero_maquina, msgraph_id), ..]
        # de las máquinas que tienen delete = true
        to_delete = []
        for row in self.cur.execute("SELECT numero_maquina FROM base_maquinas WHERE [delete] = 1"):
            to_delete.append(row[0])
        return to_delete


    def delete_machine(self, numero_maquina):
        # borra la máquina de la base de datos con el número de maáquina
        self.cur.execute(f"DELETE FROM base_maquinas WHERE numero_maquina = {numero_maquina}")
        self.con.commit()


    def insert_machine(self, id_sharepoint, data):
        # inserta la nueva máquina en la base de datos cargando el id y seteando delete = False
        record_to_add = [(str(id_sharepoint),
                          0,
                          data["numero_maquina"], 
                          data["serial_number"], 
                          data["fabricante"],
                          data["juego"], 
                          data["modelo"], 
                          data["progresivo"], 
                          data["tipo_progresivo"], 
                          data["cantidad_lineas"], 
                          data["creditos_maximos"], 
                          data["main_program"], 
                          data["pay_table"], 
                          data["base_program"], 
                          data["creditos_1"], 
                          data["porcentaje_1"], 
                          data["creditos_2"], 
                          data["porcentaje_2"], 
                          data["creditos_3"], 
                          data["porcentaje_3"], 
                          data["creditos_4"], 
                          data["porcentaje_4"], 
                          data["acepta_bill"], 
                          data["marca_bill"], 
                          data["modelo_bill"], 
                          data["version_bill"], 
                          data["impresora"], 
                          data["marca_printer"], 
                          data["modelo_printer"], 
                          data["version_printer"], 
                          data["sala"], 
                          data["area"], 
                          data["gerencia"], 
                          data["empresa"], 
                          data["estado_maquina"], 
                          data["pais_fabricacion"], 
                          data["fecha_fabricacion"], 
                          data["layout_x"], 
                          data["layout_y"],
                          data["premio_maximo"],
                          data["creditos_linea"],
                          data["transmision"],
                          data["modulo_asociado"]
                        )]

        Question_marks = "?"
        for n in range(len(record_to_add[0]) - 1):
            Question_marks = Question_marks + ", ?"

        self.cur.executemany(f"INSERT INTO base_maquinas VALUES({Question_marks})", record_to_add )
        self.con.commit()


    def get_sharepoint_machine_id(self, numero_maquina):
        # retorna el id de la máquina en la lista de sharepoint
        id = None
        for row in self.cur.execute(f"SELECT msgraph_machine_id FROM base_maquinas WHERE numero_maquina = {numero_maquina}"):
            id = row[0]
        return id


    def get_machine_data(self, numero_maquina):
        # obtiene los campos de una máquina dado su número de eva
        data = {}
        res = self.cur.execute(f"SELECT * FROM base_maquinas WHERE numero_maquina = {numero_maquina}")
        row = res.fetchone()
        data["numero_maquina"] = row[2]
        data["serial_number"] = row[3]
        data["fabricante"] = row[4]
        data["juego"] = row[5]
        data["modelo"] = row[6]
        data["progresivo"] = row[7]
        data["tipo_progresivo"] = row[8]
        data["cantidad_lineas"] = row[9]
        data["creditos_maximos"] = row[10]
        data["main_program"] = row[11]
        data["pay_table"] = row[12]
        data["base_program"] = row[13]
        data["creditos_1"] = row[14]
        data["porcentaje_1"] = row[15]
        data["creditos_2"] = row[16]
        data["porcentaje_2"] = row[17]
        data["creditos_3"] = row[18]
        data["porcentaje_3"] = row[19]
        data["creditos_4"] = row[20]
        data["porcentaje_4"] = row[21]
        data["acepta_bill"] = row[22]
        data["marca_bill"] = row[23]
        data["modelo_bill"] = row[24]
        data["version_bill"] = row[25]
        data["impresora"] = row[26]
        data["marca_printer"] = row[27]
        data["modelo_printer"] = row[28]
        data["version_printer"] = row[29]
        data["sala"] = row[30]
        data["area"] = row[31]
        data["gerencia"] = row[32]
        data["empresa"] = row[33]
        data["estado_maquina"] = row[34]
        data["pais_fabricacion"] = row[35]
        data["fecha_fabricacion"] = row[36]
        data["layout_x"] = row[37]
        data["layout_y"] = row[38]
        data["premio_maximo"] = row[39]
        data["creditos_linea"] = row[40]
        data["transmision"] = row[41]
        data["modulo_asociado"] = row[42]

        # desmarca esta máquina como para borrar
        self.cur.execute(f"UPDATE base_maquinas SET [delete] = 0 WHERE numero_maquina = {numero_maquina}")
        self.con.commit()
        return row[0], data


    def get_diferences(self, data_eva_machine, data_database_machine):
        # devuelve los campos que fueron cambiado en eva con respecto a la última consulta
        
        # verifica que sea la misma máquina
        if str(data_eva_machine["numero_maquina"]) != str(data_database_machine["numero_maquina"]):
            raise Exception('Error comparing eva with database. "numero_maquina" can\'t change.')
        
        changed_fields = {}
        for key in data_eva_machine.keys():
            if str(data_eva_machine[key]) != str(data_database_machine[key]):
                if data_eva_machine[key] == None:
                    if data_database_machine[key] != "":
                        changed_fields[key] = ""
                else:
                    changed_fields[key] = str(data_eva_machine[key])

        return changed_fields


    def update_machine(self, numero_maquina, changed_fields):
        # realiza los cambios en la base de datos en el registro del numero de máquina y seteando delete = False
        sql = "UPDATE base_maquinas SET [delete] = 0"

        for key in changed_fields.keys():
            sql = sql + ", " + str(key) + " = '" + str(changed_fields[key]) + "'"

        sql = sql + f" WHERE numero_maquina = '{numero_maquina}'"

        self.cur.execute(sql)
        self.con.commit()
