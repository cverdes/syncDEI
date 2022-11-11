import json
from msal import PublicClientApplication
from web_api import WebAPI
import urllib3

class MSGraphAPI(WebAPI):

    def __init__(self):
        super().__init__()

        self.AUTH_SERVER_URL = "https://login.microsoftonline.com/gruposlots.com.ar"
        self.CLIENT_SECRET_VALUE = "d5Y8Q~oeNpbWtBvStAKlcX9YBFZv_gUs-rGNNcCH"
        self.TENANT_ID = "8b319dc4-7d8e-4d30-8869-3f64e6195ea3"
        self.CLIENT_ID = "3e0f7e19-287f-496d-bfb7-4e57941a65c2"
        self.USER = "dei.corp@gruposlots.com.ar"
        self.PASSWORD = "TallerDEI1357"
        self.GRAPH_USER_SCOPES = ["User.Read", "Sites.ReadWrite.All"]
        self.SITE_ID = "e259c24a-b216-4f05-b0b7-9e8f7908febe"
        self.LISTA_ID = "9b039016-2acb-49b8-9c2d-3211001dc010"
        self.FIELDS = ["Title", "serial_number", "fabricante", "juego", "modelo", "progresivo", "tipo_progresivo", "cantidad_lineas", "creditos_maximos", "main_program", "pay_table", "base_program", "creditos_1", "porcentaje_1", "creditos_2", "porcentaje_2", "creditos_3", "porcentaje_3", "creditos_4", "porcentaje_4", "acepta_bill", "marca_bil", "modelo_bill", "version_bill", "impresora", "marca_printer", "modelo_printer", "version_printer", "sala", "area", "gerencia", "empresa", "estado_maquina", "pais_fabricacion", "fecha_fabricacion", "layout_x", "layout_y", "premio_maximo", "creditos_linea", "transmision", "modulo_asociado"]

        # disable InsecureRequestWarning for HTTPS request maded to host 'graph.microsoft.com'
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


    def get_token(self):
        app = PublicClientApplication(self.CLIENT_ID, authority=self.AUTH_SERVER_URL)

        result = app.acquire_token_by_username_password(self.USER, self.PASSWORD, 
                        scopes=self.GRAPH_USER_SCOPES)

        if "access_token" in result:
            self._token = result['access_token']
            self._authorization = {'Authorization': 'Bearer ' + self._token}
        else:
            raise Exception('get token error')


    def get_machine_by_id(self, id):
        # Devuelve la máquina de la lista de sharepoint con ese id
        url = f"https://graph.microsoft.com/v1.0/sites/{self.SITE_ID}/lists/{self.LISTA_ID}/items/{id}/fields"

        head = self._authorization
        head["Content-Type"] = "application/json"
        head["Accept"] = 'application/json'

        response = self.get_request(url, head, {})

        if response.status_code != 200:
            raise Exception('Error getting a machine from the sharepoint list')
        else:
            json_response = json.loads(response.text)
            data = {}

            for key_sharepoint in self.FIELDS:
                if key_sharepoint == "Title":
                    # El campo Title es el índice principal de todas las listas de Sharepoint
                    # y no se puede renombrar
                    key = "numero_maquina"
                elif key_sharepoint == "marca_bil":
                    # El campo "marca_bill" se creó mal y no se puede renombrar en Sharepoint
                    key = "marca_bill"
                else:
                    key = key_sharepoint

                if key_sharepoint in json_response:
                    data[key] = json_response[key_sharepoint]

        return data


    def update_machine(self, id, changes):
        # Se reflejan los cambios en la lista de sharepoint dado un id

        if "numero_maquina" in changes:
            # no se permite cambiar el número de la máquina de eva asociado al id
            raise Exception('Error updating a machine in sharepoint list. "numero_maquina" can\'t change.')

        # El campo "marca_bill" se creó mal y no se puede renombrar en Sharepoint
        data = {}
        for key in changes.keys():
            if key == "marca_bill":
                data["marca_bil"] = changes[key]
            else:
                data[key] = changes[key]

        body =  json.dumps({"fields": data})
        url = f"https://graph.microsoft.com/v1.0/sites/{self.SITE_ID}/lists/{self.LISTA_ID}/items/{id}"

        head = self._authorization
        head["Content-Type"] = "application/json"
        head["Accept"] = 'application/json'

        response = self.patch_request(url, head, body)

        if response.status_code != 200:
            raise Exception('Error updating a machine in sharepoint list')

        return


    def insert_machine(self, data_eva_machine):
        # Agrega una máquina a la lista de sharepoint

        if not("numero_maquina" in data_eva_machine):
            raise Exception('Error inserting a machine in sharepoint list')

        # elimina los campos sin datos, convierte todo a string y renombra algunos campos
        data = {}
        for key in data_eva_machine.keys():
            if data_eva_machine[key] != None:
                if str(data_eva_machine[key]) != "":
                    # El campo "marca_bill" se creó mal y no se puede renombrar en Sharepoint
                    if key == "numero_maquina":
                        key_sharepoint = "Title"
                    elif key == "marca_bill":
                        key_sharepoint = "marca_bil"
                    else:
                        key_sharepoint = key
                    data[key_sharepoint] = str(data_eva_machine[key])

        body =  json.dumps({"fields": data})
        url = f"https://graph.microsoft.com/v1.0/sites/{self.SITE_ID}/lists/{self.LISTA_ID}/items"

        head = self._authorization
        head["Content-Type"] = "application/json"
        head["Accept"] = 'application/json'

        response = self.post_request(url, head, body)

        if response.status_code != 201:
            raise Exception('Error inserting a machine in sharepoint list')
        else:
            data = json.loads(response.text)
            list_id = data["id"]

        return list_id


    def delete_machine(self, id):
        # Borra una máquina de la lista de sharepoint dado un id
        url = f"https://graph.microsoft.com/v1.0/sites/{self.SITE_ID}/lists/{self.LISTA_ID}/items/{id}"

        head = self._authorization
        head["Content-Type"] = "application/json"
        head["Accept"] = 'application/json'

        response = self.delete_request(url, head, {})

        if response.status_code != 204:
            raise Exception('Error deleting a machine in sharepoint list')

        return