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

        print("¿Cuáles son las estadísticas descriptivas básicas de las columnas numéricas?")
        display(df.describe(include='number').fillna(''))
        print('-' * 100)
        
        print("¿Cuáles son las estadísticas descriptivas básicas de las columnas categóricas?")
        display(df.describe(include='object'))
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

        print("##Número de filas duplicadas (considerando todas las columnas)")
        print(f"\tHay {df.duplicated().sum():,} filas duplicadas.")

        msno.heatmap(df, figsize = (6, 3), fontsize= 9)
        plt.show()
        print('-' * 100)

    print('#' * 90)




import pandas as pd

def limpieza_fintech(df_fintech):
    # 0. Copia para evitar avisos de memoria
    df_fintech = df_fintech.copy()
    
    # 1. Cambio de nombre de columnas
    df_fintech = df_fintech.rename(columns={
        'job':'job_type','marital':'marital_status','education':'education_level',
        'loan':'has_personal_loan','housing':'has_housing_loan','month':'contact_month',
        'day_of_week':'contact_day','contact':'contact_method','duration':'call_duration',
        'default':'credit_default','campaign':'contact_attempts','pdays':'previously_contacted',
        'previous':'previous_contacts','poutcome':'previous_campaign_outcome','y':'subscribed',
        'euribor3m':'euribor_3m_rate','nr.employed':'total_employment',
        'cons.price.idx':'consumer_price_index','emp.var.rate':'employment_variation_rate',
        'cons.conf.idx':'consumer_confidence_index'
    })

    # --- NUEVA PARTE: Reemplazar 'unknown' por 'undisclosed' ---
    cols_to_fix = ['job_type', 'marital_status', 'education_level', 'credit_default']
    df_fintech[cols_to_fix] = df_fintech[cols_to_fix].replace('unknown', 'undisclosed')
    # ----------------------------------------------------------

    
    # 2. Eliminar duplicados (excluyendo la variable objetivo)
    columnas_duplicados = [c for c in df_fintech.columns if c != 'subscribed']
    df_fintech = df_fintech.drop_duplicates(subset=columnas_duplicados)

    # 3. Agrupación de duración de llamadas
    df_fintech["call_duration_group"] = pd.cut(
        df_fintech["call_duration"], 
        bins=[-1, 60, 180, 300, 600, 1200, 10000],
        labels=["0-1 min", "2-3 min", "4-5 min", "6-10 min", "11-20 min", "21+ min"],
        right=True
    )
    
    # 4. Categorical ordenados
    orden_meses = ['mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    df_fintech['contact_month'] = pd.Categorical(df_fintech['contact_month'], categories=orden_meses, ordered=True)
    
    orden_dias = ['mon', 'tue', 'wed', 'thu', 'fri']
    df_fintech['contact_day'] = pd.Categorical(df_fintech['contact_day'], categories=orden_dias, ordered=True)
    
    # 5. Eliminar filas con 'unknown' en préstamos (estos se mantienen como 'unknown' para ser eliminados)
    df_fintech = df_fintech[(df_fintech["has_housing_loan"] != "unknown") & (df_fintech["has_personal_loan"] != "unknown")]
    
    # 6. Nuevas columnas
    df_fintech['is_new_campaign_client'] = (df_fintech['previous_contacts'] == 0).map({True: 'yes', False: 'no'})
    df_fintech['high_contact_attempts'] = (df_fintech['contact_attempts'] > 3).map({True: 'yes', False: 'no'})
    
    # 7. Reordenar columna objetivo al final
    if 'subscribed' in df_fintech.columns:
        col_subscribed = df_fintech.pop('subscribed')
        df_fintech['subscribed'] = col_subscribed

    return df_fintech


