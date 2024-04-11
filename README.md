# data_for_sunburst project
## Descripción
Este proyecto permite generar el conjunto de datos para generar la visualización en formato Sunburts propuesta como solución a la PEC2 de la asignatura Visualización de Datos correspondiente al plan de estudios del Máster de Ciencia de Datos en la Universitat Oberta de Catalunya.
<br><br>
El proyecto contiene los siguientes ficheros:
- dataset\NBA_game_data.xlsx: se trata de un fichero generado por el autor del repositorio a partir de la captura manual en la web www.nba.com de las estadísticas de un partido entre los Indiana Pacers y los Toronto Raptors el 9 de Abril de 2024. Se ha copiado también información de la plantilla de los dos equipos para determinar la posición principal de cada jugador y poder distinguir en el Sunburst las puntuaciones obtenidas por los jugadores en cada posición.
<br>  https://www.nba.com/game/ind-vs-tor-0022301146/box-score
<br>  https://www.nba.com/team/1610612761/raptors
<br>  https://www.nba.com/team/1610612754/pacers
<br>
<br>
- dataset\game_scorebox.csv: fichero de salida generado al ejecutar main.py con los datos para el Sunburts en formato requerido por Infogram.
<br>
<br>
- main.py: código principal para generar el dataset de salida game_scorebox.csv

<br>

La visualización resultante generada en Infogram se puede encontrar en el siguiente link:
https://infogram.com/nba-game-score-box-sunburst-1hxj48mpvxxy52v?live

## Autores
El autor del proyecto es:
- Alvaro Campion Mezquiriz (acampion@uoc.edu)

## Instalación
Clonar el repositorio para su instalación <br>

'''
git clone https://github.com/jferraguta/pythonProject1.git
'''

# Ejecución
La ejecución del código se puede hacer mediante la siguiente expresión:
<br>
'''
python main.py
'''
<br>
