from eva_api import EVAAPI
from msgraph_api import MSGraphAPI
from database import Database
from logger import Logger

def main():
    try:
        log = Logger()
        log.info("Start")

        eva = EVAAPI()
        eva.get_token()
        eva.start_machine_sync()

        msgraph = MSGraphAPI()
        msgraph.get_token()

        database = Database()
        database.start_machine_sync()

        while eva.more_machines():
            data_eva_machine = eva.get_next_machine()
            numero_maquina = data_eva_machine["numero_maquina"]

            if database.exist_machine(numero_maquina):
                # Obtiene los datos de la última búsqueda en la base de datos
                sharepoint_machine_id, data_database_machine = database.get_machine_data(numero_maquina)
                # Verifica si hay que algún cambio en algún campo
                changed_fields = database.get_diferences(data_eva_machine, data_database_machine)
                
                if changed_fields:
                    log.info(f"UPDATE {numero_maquina} WITH {changed_fields}")
                    
                    # Se reflejan los cambios en la lista de sharepoint para ese id
                    msgraph.update_machine(sharepoint_machine_id, changed_fields)
                    # Se reflejan los cambios en la base de datos para ese número de máquina
                    database.update_machine(numero_maquina, changed_fields)
            else:
                log.info(f"ADD ID {sharepoint_machine_id} WITH {data_eva_machine}")

                # Inserta la nueva máquina en sharepoint y obtiene el id
                sharepoint_machine_id = msgraph.insert_machine(data_eva_machine)
                # Inserta la nueva máquina en la base de datos
                database.insert_machine(sharepoint_machine_id, data_eva_machine)

        marked_for_deletion_list = database.get_machines_marked_for_delete()

        for number_to_delete in marked_for_deletion_list:
            # Obtiene el id para ese número de máquina de la base de datos
            sharepoint_machine_id = database.get_sharepoint_machine_id(number_to_delete)
            # Borra la máquina de sharepoint con el id
            msgraph.delete_machine(sharepoint_machine_id)
            # Borra la máquina de a base de máquinas con el número de máquina
            database.delete_machine(number_to_delete)

            log.warning(f"DELETE {number_to_delete}")

    except:
        log.exception("An exception occurred")
    finally:
        log.info("Finish")

if __name__ == "__main__":
    main()