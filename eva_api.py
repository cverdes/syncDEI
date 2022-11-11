import json
from web_api import WebAPI

class EVAAPI(WebAPI):

    def __init__(self):
        super().__init__()
        self.SERVER = "http://10.119.10.90"
        self.CLIENT_ID = '2'
        self.CLIENT_SECRET = 'bUhxut4ma5HvobCuh2tlUAPIYkMAFewdM9taL7yO'
        self.SCOPES ='*'
        self.USERNAME = 'cesar.verdes@gruposlots.com.ar'
        self.PASSWORD = 'Slots2022'

        self._authorization = ""
        self._machines = {}
        self._machines_pointer = 0


    def get_token(self):
        AUTH_SERVER_URL = self.SERVER + "/authenticate/getToken"

        body = {'grant_type': 'password',
                'client_id': self.CLIENT_ID,
                'client_secret': self.CLIENT_SECRET,
                'scopes': self.SCOPES,
                'username': self.USERNAME,
                'password': self.PASSWORD}

        response = self.post_request(AUTH_SERVER_URL, {}, body)

        if response.status_code != 200:
            raise Exception('get tocken error')
        else:
            tokens = json.loads(response.text)
            self._token = tokens['data']['access_token']
            self._authorization = {'Authorization': 'Bearer ' + self._token}


    def start_machine_sync(self):
        url = self.SERVER + "/egmServices/v1/base-maquinas"
        response = self.get_request(url, self._authorization, {})

        if response.status_code != 200:
            raise Exception('get machine base')
        else:
            data = json.loads(response.text)
            self._machines = data["data"]
            self._machines_pointer = 0


    def more_machines(self):
        return self._machines_pointer < len(self._machines)


    def get_next_machine(self):
        data = {}
        data["numero_maquina"] = self._machines[self._machines_pointer]["idMaquina"]
        data["serial_number"] = self._machines[self._machines_pointer]["serialNumber"]
        data["fabricante"] = self._machines[self._machines_pointer]["fabricante"]
        data["juego"] = self._machines[self._machines_pointer]["juego"]
        data["modelo"] = self._machines[self._machines_pointer]["modelo"]
        data["progresivo"] = self._machines[self._machines_pointer]["progresivo"]
        data["tipo_progresivo"] = self._machines[self._machines_pointer]["tipoProgresivo"]
        data["cantidad_lineas"] = self._machines[self._machines_pointer]["cantidadLineas"]
        data["creditos_maximos"] = self._machines[self._machines_pointer]["maxCred"]
        data["premio_maximo"] = self._machines[self._machines_pointer]["premioMax"]
        data["main_program"] = self._machines[self._machines_pointer]["mainProgram"]
        data["pay_table"] = self._machines[self._machines_pointer]["payTable"]
        data["base_program"] = self._machines[self._machines_pointer]["baseProgram"]
        data["creditos_1"] = self._machines[self._machines_pointer]["creditos1"]
        data["porcentaje_1"] = self._machines[self._machines_pointer]["porcentaje1"]
        data["creditos_2"] = self._machines[self._machines_pointer]["creditos2"]
        data["porcentaje_2"] = self._machines[self._machines_pointer]["porcentaje2"]
        data["creditos_3"] = self._machines[self._machines_pointer]["creditos3"]
        data["porcentaje_3"] = self._machines[self._machines_pointer]["porcentaje3"]
        data["creditos_4"] = self._machines[self._machines_pointer]["creditos4"]
        data["porcentaje_4"] = self._machines[self._machines_pointer]["porcentaje4"]
        data["acepta_bill"] = self._machines[self._machines_pointer]["ba"]
        data["marca_bill"] = self._machines[self._machines_pointer]["modeloBillMarca"]
        data["modelo_bill"] = self._machines[self._machines_pointer]["modeloBill"]
        data["version_bill"] = self._machines[self._machines_pointer]["modeloBillVersion"]
        data["impresora"] = self._machines[self._machines_pointer]["impresora"]
        data["marca_printer"] = self._machines[self._machines_pointer]["modeloPrinterMarca"]
        data["modelo_printer"] = self._machines[self._machines_pointer]["modeloPrinter"]
        data["version_printer"] = self._machines[self._machines_pointer]["modeloPrinterVersion"]
        data["sala"] = self._machines[self._machines_pointer]["nombreSala"]
        data["area"] = self._machines[self._machines_pointer]["nombreArea"]
        data["gerencia"] = self._machines[self._machines_pointer]["nombreGerencia"]
        data["empresa"] = self._machines[self._machines_pointer]["nombreEmpresa"]
        data["estado_maquina"] = self._machines[self._machines_pointer]["estadoMaquina"]
        data["pais_fabricacion"] = self._machines[self._machines_pointer]["paisFabricacion"]
        data["fecha_fabricacion"] = self._machines[self._machines_pointer]["fechaFabricacion"]
        data["layout_x"] = self._machines[self._machines_pointer]["layoutx"]
        data["layout_y"] = self._machines[self._machines_pointer]["layouty"]
        data["premio_maximo"] = self._machines[self._machines_pointer]["premioMax"]
        data["creditos_linea"] = self._machines[self._machines_pointer]["creditosxLinea"]
        data["transmision"] = self._machines[self._machines_pointer]["transmision"]
        data["modulo_asociado"] = self._machines[self._machines_pointer]["macAddress"]
        
        self._machines_pointer = self._machines_pointer + 1
        return data
