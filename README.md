# syncDEI

Este programa sincroniza algunos campos de una tabla entre dos sistemas a los cuales se accede mediante http APIs.

La sincronización se hace en forma unidireccional. Todo cambio en el sistema en EVA debe verse reflejado en una lista de sharepoint de Microsoft 365 en la nube.

Los accesos a la lista de sharepoint se hace mediante el ID único de cada registro, el cual es devuelto por la API al momento de crear dicho registro. Solo es posible agregar, modificar o borrar un registro por cada llamada a la API de MSGraph de la lista de sharepoint. Los ID de cada registro se almacenan localmente en una base sqlite.

Cada operación realizada en la lista de sharepoint a través de llamadas a la API demora entre 1 a 2 segundos, por lo tanto por eficiencia solo se agregan, modifican o borran en la lista de sharepoint los registros que fueron agregados, modificados o borrados en la tabla de EVA desde la consulta anterior.

Como al sistema EVA se accede localmente es posible, mediante la ejecución de una API, traer todos los registros de la tabla a sincronizar, los cuales se comparan uno a uno con los registros de una base local en sqlite que mantiene el estado de los campos al momento la consulta anterior. Cada diferencia da lugar a un cambio en la lista de sharepoint el cual también se refleja en la base local de sqlite.

Las sincronizaciones se realizan periódicamente ejecutando el programa mediante un crontab.