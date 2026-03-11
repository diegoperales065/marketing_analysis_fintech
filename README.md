Aquí tienes el documento actualizado incluyendo la nueva sección de **Ingeniería de Características** para las variables que has creado, manteniendo la estructura y los nombres de columnas anteriores.

---

# 🏦 Análisis de Marketing Bancario y Contexto Económico

Este proyecto consiste en el análisis de un dataset de marketing directo de una institución bancaria portuguesa. El objetivo es predecir si un cliente contratará un **depósito a plazo fijo** (variable `subscribed`).

---

## 🎯 Variable Objetivo: `subscribed` (Target)
Indica si el cliente se suscribió a un depósito a plazo como resultado de la campaña.

*   **`subscribed = yes`**: Campaña exitosa para este cliente. ✅
*   **`subscribed = no`**: El cliente no contrató el producto. ❌

### ¿Cómo medimos el éxito global?
La efectividad de la campaña no se mide de forma individual, sino mediante la **Tasa de Conversión**:

$$\text{Tasa de éxito} = \frac{\text{Número de "subscribed = yes"}}{\text{Total de clientes contactados}}$$

---

## 📋 Diccionario de Datos Detallado

### 📊 Variables Demográficas
*   **`age`**: Edad del cliente (numérica).
*   **`job_type`**: Tipo de ocupación del cliente (categórica).
*   **`marital_status`**: Estado civil del cliente (categórica).
*   **`education_level`**: Nivel educativo alcanzado (categórica).

### 💳 Información Financiera
*   **`credit_default`**: Indica si el cliente tiene actualmente créditos en incumplimiento de pago.
*   **`has_housing_loan`**: Indica si el cliente tiene una hipoteca activa.
*   **`has_personal_loan`**: Indica si el cliente tiene un préstamo personal activo.

### 📞 Información del Último Contacto
*   **`contact_method`**: Método de contacto utilizado (celular o teléfono fijo).
*   **`contact_month`**: Mes en que se realizó el último contacto.
*   **`contact_day`**: Día de la semana del último contacto.
*   **`call_duration`**: Duración de la llamada en segundos. *Nota: A mayor duración, suele haber mayor interés.*

### 📈 Información de la Campaña
*   **`contact_attempts`**: Número de contactos realizados al cliente durante esta campaña actual.
*   **`previously_contacted`**: Días transcurridos desde que el cliente fue contactado en una campaña anterior (999 significa que no fue contactado antes).
*   **`previous_contacts`**: Número de contactos realizados antes de esta campaña.
*   **`previous_campaign_outcome`**: Resultado de la campaña de marketing anterior (éxito, fracaso o inexistente).

### 🛠️ Ingeniería de Características (Variables Derivadas)
*   **`is_new_campaign_client`**: Identifica si un cliente participa por primera vez en la campaña. 
    *   **1**: Cliente nuevo (no contactado en campañas anteriores).
    *   **0**: Cliente recurrente.
    *   *Objetivo:* Diferenciar comportamientos entre perfiles nuevos y conocidos para mejorar la capacidad predictiva.
*   **`high_contact_attempts`**: Identifica una alta intensidad de contacto en la campaña actual.
    *   **1**: El cliente ha sido contactado más de 3 veces.
    *   **0**: El cliente ha sido contactado 3 veces o menos.
    *   *Objetivo:* Analizar si el exceso de insistencia influye positiva o negativamente en la suscripción.

---

## 🌍 Análisis de Variables Macroeconómicas
El éxito de un producto financiero depende del entorno económico en el que se encuentra el cliente:

### 1️⃣ Tasa de Variación del Empleo (`employment_variation_rate`)
Indica si el empleo está creciendo o bajando trimestralmente.
*   **Positivo:** Economía en expansión. Los clientes tienen más estabilidad para invertir.
*   **Negativo:** Contracción económica. Los clientes suelen ser más cautelosos.

### 2️⃣ Euribor a 3 meses (`euribor_3m_rate`)
Es la tasa de interés a la que los bancos se prestan dinero entre sí.
*   **Si el Euribor baja:** El dinero es más "barato". Los bancos buscan captar liquidez y suelen ofrecer condiciones competitivas en depósitos.
*   **Si el Euribor sube:** Aunque los préstamos suben de precio, los depósitos pueden volverse más atractivos por el interés pagado.

### 3️⃣ Índice de Precios al Consumidor (`consumer_price_index`)
Mide la **inflación** o el coste de la vida.
*   **Inflación alta:** Los clientes suelen buscar productos de inversión para intentar que sus ahorros no pierdan poder adquisitivo.

### 4️⃣ Índice de Confianza del Consumidor (`consumer_confidence_index`)
Mide el optimismo de los ciudadanos respecto a la situación económica.
*   **Valores altos:** Mayor optimismo y disposición a invertir a largo plazo.
*   **Valores bajos:** Pesimismo. Los clientes prefieren mantener liquidez y evitan riesgos.

### 5️⃣ Número de Empleados (`total_employment`)
Indica el volumen total de personas empleadas en la economía (en miles).
*   **Tendencia al alza:** Refleja una economía sólida y mayor capacidad de ahorro.
*   **Tendencia a la baja:** Señala una desaceleración económica.

---

## 📊 Tabla Resumen Macroeconómica

| Variable | Qué mide | Impacto en el Cliente |
| :--- | :--- | :--- |
| **employment_variation_rate** | Variación trimestral del empleo | (+) Estabilidad $\rightarrow$ (+) Inversión |
| **euribor_3m_rate** | Tasa de interés interbancaria | Define la rentabilidad esperada del depósito |
| **consumer_price_index**| Inflación (IPC) | Determina la urgencia de proteger los ahorros |
| **consumer_confidence_index** | Confianza del público | (+) Confianza $\rightarrow$ (+) Disposición a invertir |
| **total_employment** | Total de empleados | Refleja la solidez general del mercado laboral |

---

## 🧠 Conclusión del Análisis Contextual
Para que el modelo de Machine Learning sea efectivo, no solo analizamos el perfil individual del cliente, sino el **contexto macroeconómico** y su **historial de interacción**.

Variables como **`is_new_campaign_client`** nos permiten saber si estamos ante un contacto en frío, mientras que **`high_contact_attempts`** alerta sobre el posible agotamiento del cliente. Todo esto, cruzado con el nivel de confianza del consumidor (**`consumer_confidence_index`**) o la tasa de interés (**`euribor_3m_rate`**), define la probabilidad real de éxito de la campaña.

---
*Análisis desarrollado para optimizar la captación de depósitos mediante modelos predictivos.*
