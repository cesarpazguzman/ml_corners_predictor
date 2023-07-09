import logging

# Definición del logger root
# -----------------------------------------------------------------------------
logging.basicConfig(
    format = '%(asctime)-5s %(name)-15s %(levelname)-8s %(message)s',
    level  = logging.INFO,
    filemode = "a"
    )

# Nuevos handlers
# -----------------------------------------------------------------------------
# Si el root logger ya tiene handlers, se eliminan antes de añadir los nuevos.
# Esto es importante para que los logs no empiezen a duplicarse.
if logging.getLogger('logs').hasHandlers():
    logging.getLogger('logs').handlers.clear()
    
# Se añaden dos nuevos handlers al root logger, uno para los niveles de debug o
# superiores y otro para que se muestre por pantalla los niveles de info o
# superiores.
file_debug_handler = logging.FileHandler('Logs/logs_debug.log')
file_debug_handler.setLevel(logging.DEBUG)
file_debug_format = logging.Formatter('%(asctime)-5s %(name)-15s %(levelname)-8s %(message)s')
file_debug_handler.setFormatter(file_debug_format)
logging.getLogger('logs').addHandler(file_debug_handler)

