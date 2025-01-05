# Pruebas Automatizadas para Rutas Urbanas

Este proyecto contiene un conjunto de pruebas automatizadas para la funcionalidad de solicitud de taxis en una aplicación de rutas urbanas. Utiliza Selenium para interactuar con la interfaz de usuario y verificar que los diferentes componentes de la aplicación funcionen correctamente.

## Requisitos Previos

Antes de ejecutar las pruebas, asegúrate de tener instalados los siguientes paquetes:

- `pytest`
- `selenium`

Puedes instalar estos paquetes utilizando pip:

```bash
pip install pytest selenium
```

Además, asegúrate de tener el controlador de Chrome (ChromeDriver) instalado y que sea compatible con la versión de tu navegador Chrome. Puedes descargarlo desde [aquí](https://sites.google.com/chromium.org/driver/).

## Ejecución de Pruebas

Para ejecutar todas las pruebas, usa el siguiente comando en la terminal:

```bash
pytest test_urban_routes.py
```

Este comando ejecutará todas las pruebas definidas en el archivo `test_urban_routes.py`.

## Descripción de las Pruebas

Este conjunto de pruebas verifica el comportamiento de la funcionalidad de solicitud de taxis a través de la interfaz de usuario. Las pruebas cubren los siguientes escenarios:

- **test_set_route:** 
  - Verifica que los campos de origen y destino se llenen correctamente.

- **test_select_plan:** 
  - Prueba la selección del modo de transporte y la solicitud de un taxi.

- **test_fill_phone_number:** 
  - Verifica que se pueda ingresar un número de teléfono y recuperar el código de confirmación.

- **test_fill_card:** 
  - Prueba la funcionalidad para agregar un método de pago.

- **test_comment_for_driver:** 
  - Verifica que se pueda enviar un mensaje al conductor.

- **test_order_blanket_and_handkerchiefs:** 
  - Prueba la opción de solicitar comodidades adicionales durante la solicitud del taxi.

- **test_order_2_ice_creams:** 
  - Prueba la opción de solicitar helados adicionales durante la solicitud del taxi.

## Estructura del Código

El código está organizado en clases que representan diferentes páginas y componentes de la aplicación. Cada prueba se define como un método dentro de la clase **TestUrbanRoutes**, que utiliza el controlador de Selenium para interactuar con la aplicación.

### Clases Principales

- **`UrbanRoutesPage:`** Maneja la interacción con la página de rutas urbanas.

## Información Adicional

Si encuentras errores o tienes sugerencias para mejorar las pruebas, por favor abre un `issue` en este repositorio.

## Información del Autor

**Nombre:** Eduardo Reyna Hernández  
**Cohorte:** 19
