# LetsGo

Aplicación web ligera para gestionar la plantilla, alineación y confirmaciones de un equipo de fútbol aficionado. Permite además registrar jugadores y mantener la información del próximo partido.

## Requisitos

- Python 3.11+
- Dependencias listadas en `requirements.txt`

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

## Uso

```bash
flask --app app run
```

Luego abre [http://localhost:5000](http://localhost:5000) en tu navegador para acceder a la interfaz.

## Funcionalidades

- Gestión de jugadores: alta, baja y edición de alineación titular o banca.
- Confirmación de asistencia de cada jugador.
- Registro de nuevos jugadores a través de un formulario dedicado.
- Configuración y consulta de la información del partido (rival, fecha, hora y lugar).
