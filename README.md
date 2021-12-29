# Apyron
Implementación en Python del generador de horarios [Apeiron](https://apeiron.sourceforge.net).

## Estado de desarrollo
**Esto es software ALFA**. Partes esenciales del programa no funcionan, así que es posible que algunas cosas no se vean como deberían, o puede hacer que tu computadora explote. _Los autores no se hacen responsables de horarios inexistentes, calentamiento global, profesores fantasmas, virus chinos, viajes en el tiempo, el fin del universo o cualquier otra clase de perjuicio por utilizar este programa._ _**QUEDA BAJO TU PROPIA RESPONSABILIDAD EL UTILIZAR ESTE PROGRAMA.**_

Aclarado el punto, el programa _debería_ de ser meta-estable, es decir, lo que funciona, debería de funcionar bien, aunque obviamente no hay garantías.

### ¿Y qué funciona?
Nada espectacular:
- Selección de horas de clase (aburrido)
- Agregar materias por clave
- Agregar materias por catálogo
  - Se regenerará el catálogo con la versión más reciente si no existe en la carpeta `data`, esto toma como  20 segundos + o -
- Ver horarios
- Ver profesores
- Marcar y desmarcar profesores y materias (qué emocionante...)
- Pantalla Acerca de (denle un vistazo, o mejor no)

### ¿Qué NO funciona?
Lo esencial:
- NO se pueden generar horarios
  - NO se puede configurar la generación de horarios (obviamente...)
- NO se pueden importar ni exportar los ajustes
- NO se pueden buscar actualizaciones
- NO sirve para nada útil (aún)

## Requisitos
Se requiere:
- Python 3 y las siguientes librerías
  - PySide2
  - requests
  - BeautifulSoup4
- Una pantalla de 1024x768px (no veo porqué alguien aun usaría una de 800x600px)
- Un buen ánimo (opcional)

## ¿Y dónde me puedo quejar?
Como señalé, es software ALFA, así que los errores serán de baja prioridad (si es siquiera les hago caso). Pero las ideas son bienvenidas en la sección de Issues de GitHub.

## Gran pérdida de tiempo, ¿dónde te puedo compensar?
No acepto donaciones, pero sería una gran ayuda difundir la palabra, aunque quizá deba cambiar el nombre del programa ;)
