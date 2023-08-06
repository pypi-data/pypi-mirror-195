from datetime import datetime

import uvicorn
from fastapi import FastAPI, APIRouter, Response, status, Query
from ldap3 import Connection, Server
from starlette.middleware.cors import CORSMiddleware

import config
from domain.switch_management import TypeSwitch
from domain.wifi import Wifi
from output.activity_logs_database import ActivityLogsData
from output.contact_database import Contacts
from output.contact_sheet import ContactSheet
from output.equipment_shell import EquipmentShell
from output.favorite_links_database import FavoriteLinksData
from output.label_database import Labels
from output.record_dns_bind9 import Bind9
from output.script_model_shell import ScriptModelShell
from output.site_database import Sites, SitesContacts
from output.switch_shell import SwitchShell
from output.wifi_ansible import WifiAnsible

app = FastAPI()
temp = APIRouter(prefix='/api/v1')
app.include_router(temp)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/user")
# Ok
async def retrieve_data_user(data: dict):
    name: str = data["name"]
    password: str = data["password"]
    organization_name = config.ldap_organization_name
    ldap_url_base = f"dc={config.ldap_url_prefix},dc={config.ldap_url_suffix}"
    server = Server(f"ldap://{config.ldap_host}:{config.ldap_port}")

    user_auth = False

    ldap_connection = Connection(server, user=f"cn={name},ou={organization_name},{ldap_url_base}", password=password)
    if ldap_connection.bind():
        user_auth = True

    print(f"\nUtilisateur : {name}")
    print(f"Mot de passe : {password}")
    print(f"Il existe ? {user_auth}")

    actvity = ActivityLogsData(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"), author=name, action="Connexion")
    actvity.create_activity_log()

    return user_auth


@app.post("/sessions")
# Ok : API NORM
async def user_logout(data: dict):
    actvity = ActivityLogsData(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"), author=data["user"],
                               action="Déconnexion")
    actvity.create_activity_log()


@app.get("/switches")
# Ok
async def save_all_configs():
    switch = SwitchShell()
    switch.versioning_configs_from_ftp()


@app.get("/contacts")
# Ok
async def get_contacts():
    return ContactSheet.get_all_contact_json()


@app.get("/switches/templates")
# Ok
async def get_list_templates():
    return ScriptModelShell.get_all_templates_content(templates_directory=config.templates_directory_path)


@app.post("/switches/template")
# Ok
async def retrieve_template(data: dict):
    name: str = data["type"]
    command: list = data["command"].split("\n")
    variables: dict = {}
    for variable in data["variables"]:
        variables[variable] = ""

    ScriptModelShell.create_provisioning_templates(name, command, variables)


@app.post("/templates/equipments")
# Ok
async def execution_template(data: dict):
    equipments_group: dict = data["equipments_group"]
    equipments_group_selected: list = data["selected_equipments_group"]
    file_for_commands: str = data["template_name"]
    data_template: dict = data["values_templates_selected"]
    script_exec = ScriptModelShell()
    list_eq = []

    for equipment_gr in equipments_group:
        if equipment_gr in equipments_group_selected:
            for eq in equipments_group[equipment_gr]:
                equipment = EquipmentShell(name=eq['name'], ip=eq['ip'])
                list_eq.append(equipment)

    script_exec.modify_template_before_execution(file_name=file_for_commands,
                                                 command_template=data_template['commands'],
                                                 variables_template=data_template['variables'])
    script_exec.exec_commands_on_equipments(file_name=file_for_commands, list_equipments=list_eq)


@app.get("/equipments")
# Ok
async def get_list_templates():
    inventory_path = config.inventory_local_directory
    inventory_name = config.inventory_file_name

    return EquipmentShell.load_all(f"{inventory_path}/{inventory_name}")


# sudo lsof -t -i tcp:8000 | xargs kill -9 : to stop the server
@app.post("/templates")
# Ok
async def remove_template(template_name: str):
    switch = SwitchShell(switch_type=TypeSwitch(name=template_name.split("_")[0]))

    date: str = f"{template_name.split('_')[1]}_{template_name.split('_')[2]}"

    return Response(status_code=status.HTTP_200_OK) if ScriptModelShell.remove_template(switch.switch_type.name,
                                                                                        date=date) == 0 else Response(
        status_code=status.HTTP_404_NOT_FOUND)


@app.post("/templates/edition")
# Ok
async def edit_template(data: dict):
    name: str = data["templateName"]
    command: list = data["cmd"]
    variables: dict = data["vars"]
    new_variables = {variable: "" for variable in data["newVars"]}
    variables.update(new_variables)

    ScriptModelShell.modify_template_before_execution(file_name=name,
                                                      command_template=command,
                                                      variables_template=variables)


@app.post("/equipments/creation")
# Ok
async def create_equipment(data: dict):
    new_equipment_group = data["new_equipment"]
    values: str = data["values"]
    list_equipment_group_values = values.split('\n')

    if new_equipment_group != '':
        new_group_of_equipments = EquipmentShell()
        new_group_of_equipments.create(name_group=new_equipment_group, list_values=list_equipment_group_values)


@app.post("/equipments/edition")
# Ok
async def edit_equipment(data: dict):
    equipment_group_selected = data["equipment_selected"]
    values: str = data["values"]
    list_equipment_group_values = values.split('\n')

    if equipment_group_selected != '':
        edit_group_of_equipments = EquipmentShell()
        edit_group_of_equipments.edit(name_group=equipment_group_selected, list_values=list_equipment_group_values)


@app.post("/equipments/suppression")
# Ok
async def remove_equipment(data: dict):
    equipment_group_to_remove = data["equipment_selected"]
    if equipment_group_to_remove != '':
        remove_group_of_equipments = EquipmentShell()
        remove_group_of_equipments.remove(name_group=equipment_group_to_remove)


@app.get("/annuaire")
# Ok
async def get_list_sites_contacts_labels():
    return {"Contacts": Contacts.get_all(), "Sites": Sites.get_all(), "Labels": Labels.get_all()}


@app.post("/annuaires/contacts")
# Ok : API NORM
async def create_contact(data: dict):
    contact = Contacts()

    contact.first_name = data["firstName"]
    contact.last_name = data["lastName"]
    contact.number = data["phone"]
    contact.mail = data["email"]
    contact.address = data["address"]
    contact.commentary = data["comment"]

    contact.create()


@app.put("/annuaires/contacts")
# Ok : API NORM
async def edit_contact(data: dict):
    contact = Contacts()

    contact.id = data["id"]
    contact.first_name = data["firstName"]
    contact.last_name = data["lastName"]
    contact.mail = data["mail"]
    contact.address = data["address"]
    contact.number = data["phone"]
    contact.commentary = data["comment"]

    contact.update()


@app.delete("/annuaires/contacts")
# Ok : API NORM
async def supp_contact(data: dict):
    contact = Contacts()

    contact.id = data["id"]

    contact.delete()


@app.post("/annuaires/sites")
# Ok : API NORM
async def create_sites(data: dict):
    site = Sites()

    if data["siteName"]:
        site.site_name = data["siteName"]
        site.create()


@app.delete("/annuaires/sites")
# Ok : API NORM
async def supp_site(data: dict):
    site = Sites()

    site.id = data["id"]

    site.delete()


@app.put("/annuaires/sites")
# Ok : API NORM
async def edit_site(data: dict):
    site = Sites()

    site.id = data["id"]
    site.site_name = data["siteName"]

    site.update()


@app.post("/annuaires/sites/contacts")
# Ok : API NORM
async def add_contact_in_site(data: dict):
    site = Sites(id=data["siteId"])
    previous_contacts = [ids for ids in site.get_contacts_by_site_id().keys()]
    new_contacts = [ids.get("id") for ids in data["contactsList"]]
    contacts_to_add = [contact for contact in new_contacts if contact not in previous_contacts]
    contacts_to_remove = [contact for contact in previous_contacts if contact not in new_contacts]

    for contact_id in contacts_to_add:
        site_contact = SitesContacts(site_id=site.id)
        site_contact.contact_id = contact_id
        site_contact.add_contact_into_site()

    for contact_id in contacts_to_remove:
        SitesContacts.remove_contact_from_site(id_site=site.id, id_contact=contact_id)


@app.get("/alias")
# Ok : API NORM
def check_alias(alias_name: str = Query(...)):
    # TODO récuperation liste des alias
    alias = Bind9()
    alias.open_data = ["alias", "switch", "montre", "sel", "souris"]
    alias.name = alias_name

    return alias.alias_is_available()


@app.get("/alias/hosts")
# Ok : API NORM
async def check_host(host_name: str = Query(...)):
    equipment = EquipmentShell()
    equipment.name = host_name

    return equipment.server_exists()


@app.post("/alias")
# Ok : API NORM
async def create_alias(data: dict):
    alias = Bind9()
    alias.name = data["alias_name"]
    alias.host = data["host_name"]
    # alias.create_alias()

    actvity = ActivityLogsData(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"), author=data["user"],
                               action=f"Création de l'alias {alias.name} vers {alias.host}")
    actvity.create_activity_log()


@app.get("/activities")
# Ok : API NORM
async def get_activities():
    return ActivityLogsData.get_all_activity_logs()


@app.get("/favorites")
# Ok : API NORM
async def get_favorites():
    return FavoriteLinksData.get_all_links()


@app.post("/favorites")
# Ok : API NORM
async def create_favorites(data: dict):
    favorite = FavoriteLinksData(name=data["name"], url=data["url"])
    favorite.add_favorite_link()


@app.delete("/favorites")
# Ok : API NORM
async def delete_favorites(data: dict):
    favorite = FavoriteLinksData(id=data["id"])
    favorite.delete_favorite_link()


@app.put("/favorites")
# Ok : API NORM
async def update_favorites(data: dict):
    favorite = FavoriteLinksData(id=data["id"], name=data["name"], url=data["url"])
    favorite.edit_favorite_link()


@app.get("/wifis")
# Ok : API NORM
async def get_wifis_buildings():
    return Wifi.get_buildings()


@app.post("/wifis")
# Ok : API NORM
async def enable_wifi(data: dict):
    wifi = WifiAnsible()
    wifi.building = data["building"]
    # wifi.execute("script_ansible")

    print(wifi.building)
    print(data["user"])

    actvity = ActivityLogsData(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"), author=data["user"],
                               action=f"Activiation du wifi dans le batiment {wifi.building}")
    actvity.create_activity_log()


if __name__ == "__main__":
    uvicorn.run("api.server:app", port=8000, reload=True)
