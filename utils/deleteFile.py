import os

def delete_file(file_path):
    """
    Elimina el archivo en la ruta especificada.

    :param file_path: Ruta del archivo a eliminar.
    :return: Mensaje de éxito o error.
    """
    if os.path.isfile(file_path):
        try:
            os.remove(file_path)
            return f"Archivo '{file_path}' eliminado exitosamente."
        except Exception as e:
            return f"Error al eliminar el archivo: {e}"
    else:
        return f"El archivo '{file_path}' no existe."