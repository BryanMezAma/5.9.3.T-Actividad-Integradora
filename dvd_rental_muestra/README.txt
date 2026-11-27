Muestra de DVD Rental (Sakila)

Se conservaron los seis CSV de hasta 1,000 filas sin cambios. Los cuatro CSV mayores tienen 500 filas cada uno. Se seleccionaron rentas con semilla 42, sus pagos asociados, el inventario necesario y registros adicionales de inventario hasta completar 500; las relaciones película-actor priorizan una relación por película rentada cuando existe y se completan con otras relaciones aleatorias. Los encabezados y nombres originales se conservan, incluidos paymnet.csv, inventroy_id y el espacio en film_id de film.csv.

La muestra es para pruebas y demostración. No representa el historial completo de cada cliente, película o actor. Para métricas de demanda, segmentación por comportamiento histórico o entrenamiento final, se recomienda utilizar los CSV originales. Los archivos originales no fueron modificados.

Reproducir con pandas instalado:
python sample_data.py data/raw data/sample
