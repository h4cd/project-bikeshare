import pandas as pd
import numpy as np
import time

data_ciudades = { 'chicago': 'chicago.csv',
                  'new york city':'new_york_ciudad.csv',
                  'washington': 'washington.csv' }

meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio']

dias_semana = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']

# Crea una linea para separar las partes de que se ejecutan.

separador = 100
linea_separador = lambda char: print(char[0] * separador)

def tiempo_proceso(inicio):
    mensaje_tiempo = "Tiempo de ejecución: %s segundos..." % round((time.time() - inicio), 3)
    print(mensaje_tiempo.rjust(separador))
    linea_separador('//')


def filtro_ciudad():
    """Solicita al usuario la ciudad (número)"""
    # Crea un lista de las ciudades en la base y define la cantidad inicial.
    lista_ciudades = []
    cantidad_ciudades = 0

    for ciudad in data_ciudades:
        lista_ciudades.append(ciudad)
        cantidad_ciudades += 1
        print('{0:30}.{1}'.format(cantidad_ciudades, ciudad.title()))

   # Solicita elegir el numero correspondiente a la ciudad.
    while True:
        try:
            opcion_ciudad = int(input("\nIngrese el número de la ciudad que desea consultar (1 - {}):  ".format(len(lista_ciudades))))
        except:
            continue

        if opcion_ciudad in range(1, len(lista_ciudades)+1):
            break

    # Obtiene el nombre de las ciudades
    ciudad = lista_ciudades[opcion_ciudad - 1]
    return ciudad

# crea el filtro por mes teniendo en cuenta la información de la base.
def filtro_mes():
    """Solicita al usuario que espesifique el mes (número)"""
    while True:
        try:
            mes = input("Indique el mes (número) que desea consultar ejemplo: Enero = 1, Febrero = 2 o 'a' para seleccionar todos:  ")
        except:
            print("Valores aceptados:  1 - 6, a")
            continue

        if mes == 'a':
            mes = 'all'
            break
        elif mes in {'1', '2', '3', '4', '5', '6'}:
            mes = meses[int(mes) - 1]
            break
        else:
            continue
    
    return mes

# crea el filtro por día teniendo en cuenta la información de la base.
def filtro_dia():
    """Solicita al usuario que espesifique el día (número)"""
    while True:
        try:
            dia = input("Indique el día (número) que desea consultar ejemplo: Lunes = 1, Martes = 2 o 'a' para seleccionar todos:  ")
        except:
            print("Valores aceptados:  1 - 7, a")
            continue

        if dia == 'a':
            dia = 'all'
            break
        elif dia in {'1', '2', '3', '4', '5', '6', '7'}:
            dia = dias_semana[int(dia) - 1]
            break
        else:
            continue

    return dia


def filtros():
    """Solicita al usuario los datos de ciudad, mes y día a analizar"""
    
    #Linea que separa las partes del proyecto
    linea_separador('//')
    
    #Titulo del proyecto
    print('\n Explorador base de datos de US bikeshare\n')
  
    ciudad = filtro_ciudad()

    # Obtiene el valor de mes seleccionado por el usuario
    mes = filtro_mes()

    # Obtiene el valor de día seleccionado por el usuario
    dia = filtro_dia()
    
    # Devuelve el valor de las variables.
    return ciudad, mes, dia


def filtros_seleccionados(ciudad, mes, dia, total_viajes, df):
    """
    Se muestra los filtros selecionados de ciudad, mes y dia.

    tipo variables:
   
    ciudad es de tipo (str) 
    mes es de tipo (str)
    dia es de tipo (str)
    total_viajes es de tipo (int) 
    df es de tipo (dataframe) - Este se encarga de filtrar la base.
    """
    inicio = time.time()

    #Recupera la información de las estaciones de incio y final de los viajes contenidos en las bases de datos.
    
    filtro_viajes = len(df)
    estaciones_inicio = len(df['Start Station'].unique())
    estaciones_final = len(df['End Station'].unique())

    print('Estadisticas de la ciudad de: ', ciudad)    
    print('Filtros selecionados (mes, dia): ', mes, ', ', dia)
    print('Total viajes: ', total_viajes)
    print('Viajes filtrados: ', filtro_viajes)
    print('Cantidad de estaciones de inicio del viaje: ', estaciones_inicio)
    print('Cantidad de estaciones final del viaje: ', estaciones_final)

    tiempo_proceso(inicio)


def cargue_data(ciudad, mes, dia):
    """Carga la información de la ciudad seleccionada y aplica los filtros correspondientes"""
    inicio = time.time()    
    df = pd.read_csv(data_ciudades[ciudad])
    df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')
    df['mes'] = df['Start Time'].dt.month
    df['dia_semana'] = df['Start Time'].dt.dayofweek     
    df['hour'] = df['Start Time'].dt.hour

    total_viajes = len(df)
    filtro_viajes = total_viajes

    # Aplica el filtro por mes y dia si es correcto el valor.
    # Utiliza el index para determinar la posición de los datos
    # Filtra la información y crea un nuevo dataframe.
        
    if mes != 'all':
        mes_i = meses.index(mes) + 1   
        df = df[df.mes == mes_i]
        mes = mes.title()

 
    if dia != 'all':        
        dia_i = dias_semana.index(dia) 
        df = df[df.dia_semana == dia_i]
        dia = dia.title()

    tiempo_proceso(inicio)

    filtros_seleccionados(ciudad.title(), mes, dia, total_viajes, df )

    return df


def formato_hora(hora):
    """Convierte la hora en formaro AM o PM"""

    if hora == 0:
        f_hora = '12 AM'
    elif hora == 12:
        f_hora = '12 PM'
    else:
        f_hora = '{} AM'.format(hora) if hora < 12 else '{} PM'.format(hora - 12)

    return f_hora


def estadisticas_tiempo(df):
    """Muestra la información de las estadisticas sobre los viajes mas frecuentes"""

    print('El mes, día y hora mas frecuentes son: ')
    inicio = time.time()

    # Muestra los meses, día y mes mas frecuentes  
    
    mes = meses[df['mes'].mode()[0] - 1].title()
    print('Mes: ', mes)    
    common_dia = df['dia_semana'].mode()[0]       
    common_dia = dias_semana[common_dia].title()
    print('Día de la semana: ', common_dia)    
    hora = formato_hora(df['hour'].mode()[0])
    print('Hora de inicio: ', hora)

    tiempo_proceso(inicio)


def estadistica_estaciones(df):
    """Muestra las estadisticas de las estaciones mas frecuentes."""

    print('Las estaciones de uso mas frecuente son: ')
    inicio = time.time()
    filtro_viajes = len(df)

    # Estación de incio, final y viaje mas frecuente.
    
    estacion_de_inicio = df['Start Station'].mode()[0]
    estacion_inicio_viajes = df['Start Station'].value_counts()[estacion_de_inicio]

    print('Estación de inicio viaje: ', estacion_de_inicio)
    print('Con {1} de {2} viajes.'.format(' ', estacion_inicio_viajes, filtro_viajes))
    estacion_final = df['End Station'].mode()[0]
    estacion_final_viajes = df['End Station'].value_counts()[estacion_final]

    print('Estación de final viaje: ', estacion_final)
    print('Con {1} de {2} viajes.'.format(' ', estacion_final_viajes, filtro_viajes))

   #Busca el viajes realizado con mayor frecuencia

    estacion_inicio_final = df.groupby(['Start Station', 'End Station'])
    viaje_frecuente_cuenta = estacion_inicio_final['Trip Duration'].count().max()
    viaje_mas_frecuente = estacion_inicio_final['Trip Duration'].count().idxmax()

    print('Viaje mas frecuente: {}, {}'.format(viaje_mas_frecuente[0], viaje_mas_frecuente[1]))
    print('Con {1} viajes.'.format(' ', viaje_frecuente_cuenta))

    tiempo_proceso(inicio)


def formato_segundos(total_segundos):
    """Da formato a los segundos"""

    minutos, segundos = divmod(total_segundos, 60)
    horas, minutos = divmod(minutos, 60)
    dias, horas = divmod(horas, 24)
    semanas, dias = divmod(dias, 7)
    
    dia_hour_str = ''
    if semanas > 0:
        dia_hour_str += '{} semanas, '.format(semanas)
    if dias > 0:
        dia_hour_str += '{} dias, '.format(dias)
    if horas > 0:
        dia_hour_str += '{} horas, '.format(horas)
    if minutos > 0:
        dia_hour_str += '{} minutos, '.format(minutos)
    if total_segundos > 59:
        dia_hour_str += '{} segundos'.format(segundos)

    return dia_hour_str


def estadisticas_viajes_duracion(df):
    """Muestra las estadisticas sobre la duración de los viajes"""

    print('Duración del viaje: ')
    inicio = time.time()
    tiempo_total_viaje = int(df['Trip Duration'].sum())
    print('Tiempo total viaje: ', tiempo_total_viaje, 'segundos')
    print(formato_segundos(tiempo_total_viaje))

    # display mean travel time
    tiempo_promedio_viaje = int(df['Trip Duration'].mean())
    print('Tiempo promedio de viaje: ', tiempo_promedio_viaje, 'segundos')
    print(formato_segundos(tiempo_promedio_viaje))

    tiempo_proceso(inicio)


def estadisticas_usuarios(df):
    """Muestra las estadisticas sobre los usuarios que usan el servicio"""

    print('Estadisticas de usuarios:')
    inicio = time.time()

    # Muestra la cantidad por cada tipo de usuario
    tipos_usuarios = df['User Type'].value_counts()
    for idx in range(len(tipos_usuarios)):
        val = tipos_usuarios[idx]
        tipo_usuario = tipos_usuarios.index[idx]
        print('{}'.format((tipo_usuario + ':')), val)

    # Genero y Fecha de naciemiento solo estan en las ciudades de  Chicago y New York 
    if 'Gender' in df.columns:
        generos = df['Gender'].value_counts()
        for idx in range(len(generos)):
            val = generos[idx]
            genero = generos.index[idx]
            print('{}'.format((genero + ':')), val)

    if 'Birth Year' in df.columns:
        
        print('Fecha de nacimiento')
        print('La fecha mas antigua: ', int(df['Birth Year'].min()))
        print('La fecha mas reciente: ', int(df['Birth Year'].max()))
        print('La fecha mas común: ', int(df['Birth Year'].mode()))

    tiempo_proceso(inicio)


def datos_puros(df):
    """Pregunta al usuarios si desea ver mas información contenida dentro de la base.
    """
    cantidad_filas = 10
    fila_inicial = 0
    fila_final = cantidad_filas - 1

    print('\n¿Desea ver datos adicionales?')
    while True:
        data_pura = input('Pulse "y" para Sí o "n" para No :  ')
        if data_pura.lower() == 'y':
     
            print('\nFila {} de {}:'.format(fila_inicial + 1, fila_final + 1))

            print('\n', df.iloc[fila_inicial : fila_final + 1])
            fila_inicial += cantidad_filas
            fila_final += cantidad_filas

            linea_separador('//')
            print('\nDesea ver las siguientes {} filas?'.format(cantidad_filas))
            continue
        else:
            break


def main():
    
    while True:
        ciudad, mes, dia = filtros()
        df = cargue_data(ciudad, mes, dia)

        estadisticas_tiempo(df)
        estadistica_estaciones(df)
        estadisticas_viajes_duracion(df)
        estadisticas_usuarios(df)
        datos_puros(df)

        reinicio = input('\n Desea reiniciar el programa "y" para Sí o "n" para No:  ')
        if reinicio.lower() != 'y':
            break


if __name__ == "__main__":
	main()
