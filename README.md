# 🏦 Análisis de Marketing Bancario y Contexto Económico

Este proyecto consiste en el análisis de un dataset de marketing directo de una institución bancaria portuguesa. El objetivo es predecir si un cliente contratará un **depósito a plazo fijo** (variable `y`).

---

## 🎯 Variable Objetivo: `y` (Target)
Indica si el cliente se suscribió a un depósito a plazo como resultado de la campaña.

*   **`y = yes`**: Campaña exitosa para este cliente. ✅
*   **`y = no`**: El cliente no contrató el producto. ❌

### ¿Cómo medimos el éxito global?
La efectividad de la campaña no se mide de forma individual, sino mediante la **Tasa de Conversión**:

$$\text{Tasa de éxito} = \frac{\text{Número de "yes"}}{\text{Total de clientes contactados}}$$

---

## 📋 Diccionario de Datos Detallado

### 📊 Variables Demográficas
*   **`age`**: Edad del cliente (numérica).
*   **`job`**: Tipo de trabajo (categórica: administrativo, técnico, emprendedor, etc.).
*   **`marital`**: Estado civil (categórica).
*   **`education`**: Nivel educativo alcanzado (categórica).

### 💳 Información Financiera
*   **`default`**: ¿Tiene actualmente créditos en incumplimiento de pago?
*   **`housing`**: ¿Tiene un préstamo hipotecario activo?
*   **`loan`**: ¿Tiene un préstamo personal activo?

### 📞 Información del Último Contacto
*   **`contact`**: Tipo de comunicación (celular o teléfono fijo).
*   **`month`**: Mes del último contacto.
*   **`day_of_week`**: Día de la semana del último contacto.
*   **`duration`**: Duración de la llamada en segundos. *Nota: A mayor duración, suele haber mayor interés.*

### 📈 Información de la Campaña
*   **`campaign`**: Número de veces que se ha contactado al cliente durante esta campaña.
*   **`pdays`**: Días transcurridos desde que el cliente fue contactado en una campaña anterior (999 significa que no fue contactado antes).
*   **`previous`**: Número de contactos realizados antes de esta campaña.
*   **`poutcome`**: Resultado de la campaña de marketing anterior (éxito, fracaso o inexistente).

---

## 🌍 Análisis de Variables Macroeconómicas
El éxito de un producto financiero depende del entorno. Aquí explicamos cómo leer estos indicadores:

### 1️⃣ Tasa de Variación del Empleo (`emp.var.rate`)
Indica si el empleo está creciendo o bajando trimestralmente.
*   **Positivo:** Economía en expansión. Los clientes tienen más estabilidad para invertir.
*   **Negativo:** Contracción económica. Los clientes suelen ser más cautelosos.

### 2️⃣ Euribor a 3 meses (`euribor3m`)
Es la tasa de interés a la que los bancos se prestan dinero. 
> **Escala en dataset:** Los valores vienen multiplicados por 10,000.
> *Ejemplo: 4857.0 $\rightarrow$ 0.4857%*

*   **Si el Euribor baja:** El dinero es "barato". Los bancos necesitan atraer liquidez y suelen ofrecer mejores condiciones en depósitos.
*   **Si el Euribor sube:** El dinero es "caro". Los préstamos suben de precio, pero los depósitos podrían pagar más interés.

### 3️⃣ Índice de Precios al Consumidor (`cons.price.idx`)
Mide la **inflación**.
> **Escala en dataset:** Los valores vienen multiplicados por 1,000.
> *Ejemplo: 93994 $\rightarrow$ 93.994*

*   **Inflación alta:** La gente busca inversiones (como depósitos) para proteger su dinero de la pérdida de valor, o prefiere liquidez si hay mucha incertidumbre.

### 4️⃣ Índice de Confianza del Consumidor (`cons.conf.idx`)
Mide qué tan optimista se siente la gente respecto a la economía.
*   **Valores altos:** Optimismo. Más probabilidad de invertir a largo plazo.
*   **Valores bajos:** Pesimismo. Los clientes prefieren guardar su dinero y no comprometerlo.

### 5️⃣ Número de Empleados (`nr.employed`)
Indica el nivel total de empleo en la economía (en miles).
*   **Tendencia al alza:** Economía fuerte, mayor disposición al ahorro.
*   **Tendencia a la baja:** Desaceleración económica, menor contratación de productos.

---

## 📊 Tabla Resumen Macroeconómica

| Variable | Qué mide | Conversión Requerida | Impacto en el Cliente |
| :--- | :--- | :--- | :--- |
| **emp.var.rate** | Variación empleo | Ninguna (%) | (+) Estabilidad $\rightarrow$ (+) Inversión |
| **euribor3m** | Tasa interés | Dividir entre 10,000 | Define rentabilidad del depósito |
| **cons.price.idx**| Inflación (IPC) | Dividir entre 1,000 | Determina urgencia de proteger ahorros |
| **cons.conf.idx** | Confianza | Ninguna (índice) | (+) Confianza $\rightarrow$ (+) Disposición |
| **nr.employed** | Total empleados | Ninguna (miles) | Refleja solidez del mercado laboral |

---

## 🧠 Conclusión del Análisis Contextual
Para que el modelo de Machine Learning sea efectivo, no solo miramos al individuo, sino al **momento**. 

Por ejemplo, un cliente con buen trabajo (**job**) y sin deudas (**default**), podría rechazar un depósito si el **euribor3m** está muy bajo (poca rentabilidad) o si la confianza del consumidor (**cons.conf.idx**) está cayendo por una crisis.

---
*Análisis desarrollado para optimizar la captación de depósitos mediante modelos predictivos.*
