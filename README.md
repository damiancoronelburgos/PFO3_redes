# PFO 3: Rediseño como Sistema Distribuido (Cliente-Servidor)

Este proyecto fue desarrollado como parte de la **Practica Formativa Obligatoria N° 3** de la **Tecnicatura en Programación**.

---

##  Objetivo del Proyecto

En este proyecto se realizó una aplicación cliente-servidor en **Python** donde:

- El **servidor** reciba tareas mediante sockets y las distribuya a **workers**.
- Los **clientes** envíen operaciones aritméticas y reciban los resultados procesados.
- Se utilice **Flask** para ofrecer una interfaz web simple que permita interactuar con el sistema.

---

##  Descripción General

El sistema está compuesto por:

- **Servidor (Flask)** → Recibe tareas desde el cliente, las guarda en una base de datos SQLite y las envía a una cola.
- **Workers** → Hilos (`threading`) que procesan las operaciones aritméticas en segundo plano.
- **Cliente (Web)** → Interfaz HTML para registrar usuarios, iniciar sesión y enviar operaciones.

---

##  Estructura del Proyecto

project/
│
├── app.py # Punto de inicio del servidor Flask
├── auth.py # Registro e inicio de sesión de usuarios
├── db.py # Creación y conexión a la base de datos SQLite
├── routes.py # Definición de rutas y lógica de interacción
├── tasks.py # Procesamiento en segundo plano con hilos
│
├── templates/ # Páginas HTML (Frontend)
│ ├── index.html
│ ├── login.html
│ ├── register.html
│ └── task.html
│
├── static/ # Archivos estáticos (CSS)
│ └── style.css
│
└── app.db # Base de datos (se genera automáticamente)




---

##  Flujo de Funcionamiento

a. El usuario se registra o inicia sesión
b. Envía una operación aritmética (por ejemplo `5 + 3`).
c. La operación se almacena en la base de datos y se coloca en una cola de tareas
d. Los workers en segundo plano procesan la tarea.
e. El resultado se guarda y se muestra en la interfaz web.

---

##  Instalación y Ejecución

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tuusuario/pfo3_redes.git
   cd pfo3_redes
   

2. **Crear un entorno virtual (opcional)**

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows


3. **Instalar dependencias**

pip install flask

4. **Ejecutar la aplicación**

python app.py


5. **Abrir el navegador en:**
http://127.0.0.1:5000


**Tecnologías Utilizadas:**

*Python 3*

*Flask*

*SQLite3*

*Threading / Queue*

*HTML + CSS*


 
 Autor

Damian CORONEL BURGOS 
Tecnicatura en Programación – PFO 3
danielcoronelburgos1993@gmail.com


