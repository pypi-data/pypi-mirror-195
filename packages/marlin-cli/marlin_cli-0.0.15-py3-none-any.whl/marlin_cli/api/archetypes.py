import requests
import marlin_cli.constants as constants


def get_archetype(archetype_name):
    archetype = None
    error = None
    response = requests.get(url=f"{constants.API_URL}/archetypes/{archetype_name}")
    if response.ok:
        archetype = response.json()
    else:
        error = {"code": response.status_code, "message": response.content}
    return (archetype, error)


def list_archetypes():
    module_list = None
    error = None
    response = requests.get(url=f"{constants.API_URL}/archetypes/available")
    if response.ok:
        module_list = response.json()
    else:
        error = {"code": response.status_code, "message": response.content}
    return (module_list, error)
