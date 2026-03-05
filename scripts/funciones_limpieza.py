# Librerías estándar
import os
import warnings

# Manipulación de datos
import pandas as pd
import numpy as np

# Visualización de datos
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.colors as mcolors
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Análisis de nulos
import missingno as msno

# Estadística
import scipy.stats as stats

# Configuración de warnings
warnings.filterwarnings('ignore')

def leer_archivo(ruta_completa):
    try:

        _, extension = os.path.splitext(ruta_completa.lower())


        if extension == '.csv':
            df = pd.read_csv(ruta_completa)
        elif extension in ('.xlsx', '.xls'):
            df = pd.read_excel(ruta_completa)
        else:
            print("Error: Formato no compatible")
            return None

        return df

    except FileNotFoundError:
        print(f"Error: Archivo no encontrado en la ruta '{ruta_completa}'.")
        return None

    except Exception as e:
        print(f"Error inesperado: {e}")
        return None




def exploracion_inicial(df, nombre=None, tipo=None):
    """
    Realiza una exploración inicial de un DataFrame y muestra información clave.

    Parámetros:
    df (pd.DataFrame): El DataFrame a explorar.
    tipo (str, opcional): El tipo de exploración. 'simple' muestra menos detalles.

    Imprime:
    Información relevante sobre el DataFrame, incluyendo filas, columnas, tipos de datos,
    estadísticas descriptivas, y valores nulos.
    """
    if nombre:
      print(nombre.upper().center(90, ' # '))
      print('\n\n')

    # Información básica sobre el DataFrame
    num_filas, num_columnas = df.shape
    print(f"¿Cuántas filas y columnas hay en el conjunto de datos?")
    print(f"\tHay {num_filas:,} filas y {num_columnas:,} columnas.")
    print('#' * 90)

    # Exploración simple
    if tipo == 'simple':
        print("¿Cuáles son las primeras dos filas del conjunto de datos?")
        display(df.head(2))
    else:
        # Exploración completa
        print("¿Cuáles son las primeras cinco filas del conjunto de datos?")
        display(df.head())
        print('-' * 100)

        print("¿Cuáles son las últimas cinco filas del conjunto de datos?")
        display(df.tail())
        print('-' * 100)

        print("¿Cómo puedes obtener una muestra aleatoria de filas del conjunto de datos?")
        display(df.sample(n=5))
        print('-' * 100)

        print("¿Cuáles son las columnas del conjunto de datos?")
        print("\n".join(f"\t- {col}" for col in df.columns))
        print('-' * 100)

        print("¿Cuál es el tipo de datos de cada columna?")
        print(df.dtypes)
        print('-' * 100)

        print("¿Cuántas columnas hay de cada tipo de datos?")
        print(df.dtypes.value_counts())
        print('-' * 100)

        print("¿Cómo podríamos obtener información más completa sobre la estructura y el contenido del DataFrame?")
        print(df.info())
        print('-' * 100)

        print("¿Cuántos valores únicos tiene cada columna?")
        print(df.nunique())
        print('-' * 100)

        print("¿Cuáles son los valores únicos de cada columna?")
        df_valores_unicos = pd.DataFrame(df.apply(lambda x: x.unique()))
        display(df_valores_unicos)
        print('-' * 100)

        print("¿Cuáles son las estadísticas descriptivas básicas de todas las columnas?")
        display(df.describe(include='all').fillna(''))
        print('-' * 100)

        print("¿Cuántos valores nulos hay en cada columna del DataFrame?")
        display(df.isnull().sum())
        print('-' * 100)

        print("¿Cuál es el porcentaje de valores nulos por columna, ordenado de mayor a menor?")
        df_nulos = df.isnull().sum().div(len(df)).mul(100).round(2).reset_index().rename(columns = {'index': 'Col', 0: 'pct'})
        df_nulos = df_nulos.sort_values(by = 'pct', ascending=False).reset_index(drop = True)
        display(df_nulos)
        print('-' * 100)

        print("## Valores nulos: Visualización")
        msno.bar(df, figsize = (6, 3), fontsize= 9)
        plt.show()
        print('-' * 100)

        print("## Visualización de patrones en valores nulos")
        msno.matrix(df, figsize = (6, 3), fontsize= 9, sparkline = False)
        plt.show()
        print('-' * 100)

        msno.heatmap(df, figsize = (6, 3), fontsize= 9)
        plt.show()
        print('-' * 100)

    print('#' * 90)


import pandas as pd
import re

def transformar_medallas(df):
    """
    Transforma un DataFrame de resultados de medallas de formato ancho a largo.

    El DataFrame original debe tener las columnas:
        'Eventos', 'Oro', 'Plata', 'Bronce', 'Año', 'Genero'

    La función devuelve un nuevo DataFrame con columnas:
        'Eventos', 'Año', 'Genero', 'Medalla', 'Atleta'

    El campo 'Atleta' contendrá solo el nombre (primeras dos palabras) del atleta.

    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame original con resultados de medallas.

    Retorna:
    --------
    pd.DataFrame
        DataFrame transformado en formato largo.
    """

    filas = []

    for _, row in df.iterrows():
        eventos = ' '.join(row['Eventos'].split(' ')[0:1])
        for medalla, atleta in zip(["Oro", "Plata", "Bronce"],
                                   [row["Oro"], row["Plata"], row["Bronce"]]):
            
            # Extraer solo las primeras dos palabras como nombre del atleta
            nombre_pais = re.split(r"\d", atleta)[0].strip().split()
            nombre = " ".join(nombre_pais[:2])

            filas.append({
                "Eventos": row["Eventos"],
                "Año": row["Año"],
                "Genero": row["Genero"],
                "Medalla": medalla,
                "Atleta": nombre
            })

    # Crear el DataFrame final
    df_transformado = pd.DataFrame(filas)
    return df_transformado



def desagregar_resultados(df_merged):
    """
    Desagrega los resultados de competencias deportivas de un DataFrame consolidado.

    Esta función toma un DataFrame con información de eventos y medallistas
    (columnas: 'Eventos', 'Año', 'Oro', 'Plata', 'Bronce') y genera un DataFrame
    con los datos individuales de cada atleta, incluyendo su nombre, apellido, país
    y resultados en cada fase de la competencia.

    Parámetros:
    -----------
    df_merged : pandas.DataFrame
        DataFrame de entrada con los datos consolidados de los eventos y medallistas.

    Retorna:
    --------
    df_desagregado : pandas.DataFrame
        DataFrame desagregado con columnas:
        - 'Fecha': Fecha del evento en formato 'YYYY-MM-DD'.
        - 'Nombre': Nombre del atleta.
        - 'Apellido': Apellido del atleta.
        - 'Pais': País del atleta.
        - 'Resultados': Resultados concatenados como "arrancada + dos_tiempos = total".
        - 'Arrancada': Resultado de la arrancada.
        - 'Dos_Tiempos': Resultado de los dos tiempos.
        - 'Total': Total del resultado.
    """
    
    # Crear DataFrame vacío para almacenar los resultados desagregados
    df_desagregado = pd.DataFrame(columns=['Fecha', 'Nombre', 'Apellido', 'Pais', 
                                           'Resultados', 'Arrancada', 'Dos_Tiempos', 'Total'])

    # Iterar sobre cada fila del DataFrame original
    for _, row in df_merged.iterrows():
        # Extraer fecha del evento
        fecha_str = row['Eventos'].split('(')[1].split(')')[0]
        dia, mes = fecha_str.split('.')
        fecha = pd.to_datetime(f"{row['Año']}-{mes}-{dia}")

        # Iterar sobre los tres medallistas: Oro, Plata, Bronce
        for atleta in [row['Oro'], row['Plata'], row['Bronce']]:
            # Eliminar cualquier texto entre corchetes
            atleta = re.sub(r"\[.*?\]", '', atleta)

            # Extraer nombre, apellido y país
            fila_str = re.split(r'\d', atleta)[0].strip().split()
            nombre = fila_str[0]
            apellido = fila_str[1]
            pais = ' '.join(fila_str[2:])

            # Extraer resultados numéricos
            fila_digito = re.findall(r'\d+', atleta)
            resultados = ' = '.join([(' + '.join(fila_digito[0:2])), fila_digito[2]])
            arrancada = fila_digito[0]
            dos_tiempos = fila_digito[1]
            total = fila_digito[2]

            # Crear fila individual y agregarla al DataFrame
            fila = pd.DataFrame([{
                'Fecha': fecha,
                'Nombre': nombre,
                'Apellido': apellido,
                'Pais': pais,
                'Resultados': resultados,
                'Arrancada': arrancada,
                'Dos_Tiempos': dos_tiempos,
                'Total': total
            }])

            df_desagregado = pd.concat([df_desagregado, fila], ignore_index=True)

    return df_desagregado





def tabla_completa(df_merged):
    """
    Desagrega los resultados de competencias deportivas de un DataFrame consolidado.

    Esta función toma un DataFrame con información de eventos y medallistas
    (columnas: 'Eventos', 'Año', 'Oro', 'Plata', 'Bronce') y genera un DataFrame
    con los datos individuales de cada atleta, incluyendo su nombre, apellido, país
    y resultados en cada fase de la competencia.

    Parámetros:
    -----------
    df_merged : pandas.DataFrame
        DataFrame de entrada con los datos consolidados de los eventos y medallistas.

    Retorna:
    --------
    df_desagregado : pandas.DataFrame
        DataFrame desagregado con columnas:
        - 'Fecha': Fecha del evento en formato 'YYYY-MM-DD'.
        - 'Nombre': Nombre del atleta.
        - 'Apellido': Apellido del atleta.
        - 'Pais': País del atleta.
        - 'Resultados': Resultados concatenados como "arrancada + dos_tiempos = total".
        - 'Arrancada': Resultado de la arrancada.
        - 'Dos_Tiempos': Resultado de los dos tiempos.
        - 'Total': Total del resultado.
    """
    paises = {
        'España', 'Italia', 'Bulagria', 'Turquía', 'Bielorrusia', 'Francia',
        'Alemania', 'Georgia', 'Albania','Letonia', 'Armenia', 'Rusia', 'Ucrania', 
        'Rumania', 'Polonia', 'Reino Unido', 'Austria', 'Moldavia', 'Azerbaiyán',
        'Suecia', 'Bélgica', 'Serbia', 'Noruega', 'Irlanda', 'Finlandia', 'Israel'
    }

    # Crear DataFrame vacío para almacenar los resultados desagregados
    df_completo = pd.DataFrame(columns=['Genero', 'Categoria', 'Fecha', 'Medalla', 'Nombre', 'Apellido', 'Pais', 
                                           'Arrancada', 'Dos_Tiempos', 'Total'])

    # Iterar sobre cada fila del DataFrame original
    for _, row in df_merged.iterrows():
        
        eventos = ''.join(row['Eventos'].strip().split()[0])

        # Extraer fecha del evento
        fecha_str = row['Eventos'].split('(')[1].split(')')[0]
        dia, mes = fecha_str.split('.')
        fecha = pd.to_datetime(f"{row['Año']}-{mes}-{dia}")

        # Iterar sobre los tres medallistas: Oro, Plata, Bronce
        for medalla, atleta in zip(['Oro', 'Plata', 'Bronce'],
                               [row['Oro'], row['Plata'], row['Bronce']]):
            # Eliminar cualquier texto entre corchetes
            atleta = re.sub(r"\[.*?\]", '', atleta)

            # 🔹 TEXTO SIN NÚMEROS
            texto = re.split(r'\d', atleta)[0].strip()
            partes = texto.split()

            nombre = partes[0]

            # 🔹 DETECTAR PAÍS DESDE EL FINAL
            pais = None
            for i in range(1, len(partes)):
                posible_pais = ' '.join(partes[i:])
                if posible_pais in paises:
                    apellido = ' '.join(partes[1:i])
                    pais = posible_pais
                    break

            # 🔹 FALLBACK (por seguridad)
            if pais is None:
                apellido = ' '.join(partes[1:-1])
                pais = partes[-1]

            # 🔹 RESULTADOS NUMÉRICOS
            fila_digito = re.findall(r'\d+', atleta)
            arrancada, dos_tiempos, total = map(int, fila_digito[:3])

            # Crear fila individual y agregarla al DataFrame
            fila = pd.DataFrame([{
                'Genero' : row['Genero'],
                'Categoria' : eventos,
                'Fecha': fecha,
                'Medalla': medalla,
                'Nombre': nombre,
                'Apellido': apellido,
                'Pais': pais,
                'Arrancada': arrancada,
                'Dos_Tiempos': dos_tiempos,
                'Total': total
            }])

            df_completo = pd.concat([df_completo, fila], ignore_index=True)

            df_completo['Arrancada'] = df_completo['Arrancada'].astype(int)
            df_completo['Dos_Tiempos'] = df_completo['Dos_Tiempos'].astype(int)
            df_completo['Total'] = df_completo['Total'].astype(int)
            
            orden_medalla = ['Oro', 'Plata', 'Bronce']
            df_completo['Medalla'] = pd.Categorical(df_completo['Medalla'],
                                          categories= orden_medalla,
                                          ordered=True)

    return df_completo


def tabla_completa2(df_merged):
    import pandas as pd
    import re

    paises = {
        'España', 'Italia', 'Bulagria', 'Turquía', 'Bielorrusia', 'Francia',
        'Alemania', 'Georgia', 'Albania','Letonia', 'Armenia', 'Rusia', 'Ucrania', 
        'Rumania', 'Polonia', 'Reino Unido', 'Austria', 'Moldavia', 'Azerbaiyán',
        'Suecia', 'Bélgica', 'Serbia', 'Noruega', 'Irlanda', 'Finlandia', 'Israel'
    }

    df_completo = pd.DataFrame(columns=[
        'Genero', 'Categoria', 'Fecha', 'Medalla',
        'Nombre', 'Apellido', 'Pais',
        'Arrancada', 'Dos_Tiempos', 'Total'
    ])

    for _, row in df_merged.iterrows():

        eventos = ''.join(row['Eventos'].strip().split()[0])

        fecha_str = row['Eventos'].split('(')[1].split(')')[0]
        dia, mes = fecha_str.split('.')
        fecha = pd.to_datetime(f"{row['Año']}-{mes}-{dia}")

        for medalla, atleta in zip(
            ['Oro', 'Plata', 'Bronce'],
            [row['Oro'], row['Plata'], row['Bronce']]
        ):

            atleta = re.sub(r"\[.*?\]", '', atleta)

            # 🔹 TEXTO SIN NÚMEROS
            texto = re.split(r'\d', atleta)[0].strip()
            partes = texto.split()

            nombre = partes[0]

            # 🔹 DETECTAR PAÍS DESDE EL FINAL
            pais = None
            for i in range(1, len(partes)):
                posible_pais = ' '.join(partes[i:])
                if posible_pais in paises:
                    apellido = ' '.join(partes[1:i])
                    pais = posible_pais
                    break

            # 🔹 FALLBACK (por seguridad)
            if pais is None:
                apellido = ' '.join(partes[1:-1])
                pais = partes[-1]

            # 🔹 RESULTADOS NUMÉRICOS
            fila_digito = re.findall(r'\d+', atleta)
            arrancada, dos_tiempos, total = map(int, fila_digito[:3])

            fila = pd.DataFrame([{
                'Genero': row['Genero'],
                'Categoria': eventos,
                'Fecha': fecha,
                'Medalla': medalla,
                'Nombre': nombre,
                'Apellido': apellido,
                'Pais': pais,
                'Arrancada': arrancada,
                'Dos_Tiempos': dos_tiempos,
                'Total': total
            }])

            df_completo = pd.concat([df_completo, fila], ignore_index=True)

    orden_medalla = ['Oro', 'Plata', 'Bronce']
    df_completo['Medalla'] = pd.Categorical(
        df_completo['Medalla'],
        categories=orden_medalla,
        ordered=True
    )

    return df_completo


def px_box_with_pvalue(df, cat_var, num_var, title=None, color_palette=None):
    import plotly.express as px
    import statsmodels.stats.weightstats as ws
    import statsmodels.api as sm
    from statsmodels.formula.api import ols

    data = df[[cat_var, num_var]].dropna()
    grupos = data.groupby(cat_var)[num_var]

    if len(grupos) == 2:
        g1, g2 = [g for _, g in grupos]
        t_stat, p_value, _ = ws.ttest_ind(g1, g2, usevar="unequal")
        test_name = "t-test"
    else:
        modelo = ols(f"{num_var} ~ C({cat_var})", data=data).fit()
        anova = sm.stats.anova_lm(modelo, typ=2)
        p_value = anova["PR(>F)"][0]
        test_name = "ANOVA"

    fig = px.box(
        data, 
        x=cat_var, 
        y=num_var, 
        color=cat_var,
        color_discrete_sequence=color_palette,
        title=title or f"{num_var} por {cat_var}",
        points="outliers"
    )
    
    fig.add_annotation(
        x=0.5, y=data[num_var].max() * 0.95,
        text=f"{test_name} p-value = {p_value:.4f}",
        showarrow=False, font=dict(size=12, color="darkred"),
        bgcolor="rgba(255,255,255,0.8)", bordercolor="darkred", borderwidth=1
    )
    
    # Fondo blanco y cuadrículas suaves
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white"
    )
    fig.update_xaxes(showgrid=True, gridcolor="lightgray")
    fig.update_yaxes(showgrid=True, gridcolor="lightgray")
    
    return fig

def px_box(df, cat_var, num_var, title=None, color_palette=None):
    import plotly.express as px

    data = df[[cat_var, num_var]].dropna()

    fig = px.box(
        data,
        x=cat_var,
        y=num_var,
        color=cat_var,
        color_discrete_sequence=color_palette,
        title=title or f"{num_var} por {cat_var}",
        points="outliers"
    )

    # Fondo blanco y cuadrículas suaves
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white"
    )
    fig.update_xaxes(showgrid=True, gridcolor="lightgray")
    fig.update_yaxes(showgrid=True, gridcolor="lightgray")

    return fig


def px_countplot_by_category(df, cat_var, title=None, color_palette=None):
    import plotly.express as px

    # Conteo por categoría
    counts = df[cat_var].value_counts(ascending=True).reset_index()
    counts.columns = [cat_var, "Conteo"]

    fig = px.bar(
        counts,
        x="Conteo",
        y=cat_var,
        orientation="h",
        title=title or f"Total de medallas por {cat_var}",
        color_discrete_sequence=color_palette
    )

    # Hover limpio
    fig.update_traces(
        hovertemplate=f"{cat_var}: %{{y}}<br>Total: %{{x}}<extra></extra>",
        text=None
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False
    )

    fig.update_xaxes(title="Medallas", showgrid=True, gridcolor="lightgray")
    fig.update_yaxes(title="", showgrid=False)
    fig.update_layout(width=800, height=400)

    return fig




def px_total_por_fecha_por_año(df, fecha_col, total_col, genero_col, color_palette=None):
    """
    Crea gráficos de línea del total de 'total_col' por mes-día, separados por género.
    Cada línea corresponde a un año diferente.
    El eje X muestra solo mes y día (MM-DD), ordenadas correctamente.
    Retorna un diccionario de figuras con claves por género.
    """
    # Convertir columna de fecha a datetime
    df[fecha_col] = pd.to_datetime(df[fecha_col], errors='coerce')
    df = df.dropna(subset=[fecha_col])
    
    # Crear columna de Año
    df['Año'] = df[fecha_col].dt.year
    
    # Crear columna de Mes-Día como datetime con año fijo (2000)
    df['Mes-Día'] = df[fecha_col].apply(lambda x: pd.Timestamp(year=2000, month=x.month, day=x.day))
    
    figuras = []
    
    for genero in df[genero_col].unique():
        df_genero = df[df[genero_col] == genero]
        if df_genero.empty:
            continue
        
        # Agrupar por Mes-Día y Año sumando el total
        df_agrupado = df_genero.groupby(['Mes-Día', 'Año'], as_index=False)[total_col].sum()
        df_agrupado = df_agrupado.sort_values('Mes-Día')
        
        # Graficar
        fig = px.line(
            df_agrupado,
            x='Mes-Día',
            y=total_col,
            color='Año',
            markers=True,
            title=f'Total de puntos por Fecha - {genero}',
            color_discrete_sequence=color_palette
        )
        
        # Formatear eje X para mostrar solo MM-DD
        fig.update_xaxes(
            tickformat="%m-%d",
            showgrid=True,
            gridcolor='lightgray'
        )
        fig.update_yaxes(showgrid=True, gridcolor='lightgray')
        fig.update_layout(
            yaxis_title='Total (promedio)',
            xaxis_title='Mes-Día',
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        figuras.append(fig)
    
    return figuras


def top_n_bar(df, nombre_col, total_col, n=10, color_palette=None, titulo='Top N'):
    """
    Crea un gráfico de barras de los Top N valores de un DataFrame, con cada barra de un color distinto.
    
    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame con los datos.
    nombre_col : str
        Nombre de la columna que contiene los nombres.
    total_col : str
        Nombre de la columna que contiene los valores a graficar.
    n : int
        Número de top valores a mostrar.
    color_palette : list
        Paleta de colores para las barras.
    titulo : str
        Título del gráfico.
    """
    
    # Ordenar por total descendente y tomar top n
    df_top = df.groupby(nombre_col, as_index=False)[total_col].sum()
    df_top = df_top.sort_values(by=total_col, ascending=False).head(n)
    
    fig = px.bar(
        df_top,
        x=nombre_col,
        y=total_col,
        text=total_col,
        color=nombre_col,
        color_discrete_sequence=color_palette,
        title=titulo
    )
    
    fig.update_layout(
        yaxis_title=total_col,
        xaxis_title=nombre_col,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    fig.update_xaxes(showgrid=True, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridcolor='lightgray')
    
    fig.show()
