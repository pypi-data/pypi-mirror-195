import logging
import os
import shutil
import subprocess
import sys
import time
import fileinput
import webbrowser

from datetime import datetime
from collections import defaultdict
# from json import dumps
from pathlib import WindowsPath, Path

import click
import psutil
import requests

from parse import parse
# from jinja2 import Environment, FileSystemLoader
from rich import print, print_json
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.traceback import install

# from sttool.app import App

install(show_locals=True)

if sys.stdout.isatty():
    # You're running in a real terminal
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
else:
    LOG_FORMAT = "%(name)s - %(levelname)s - %(message)s"

logging.basicConfig(
    level=getattr(logging, os.getenv("LOGLEVEL", "INFO").upper()),
    format=LOG_FORMAT,
    datefmt="%Y-%m-%dT%H:%M:%S"
)

logger = logging.getLogger("sttool")

# set levels for other modules
logging.getLogger("urllib3").setLevel(logging.WARNING)


def kill_process_tree_by_name(process_name):
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        current_proc_name = proc.info['name']
        # parent_pid = int(proc.info['pid'])
        if process_name in current_proc_name:
            logging.info(f'Killing parent and child process: {current_proc_name}')
            for child in proc.children(recursive=True):
                if child.status() == "running":
                    try:
                        child.kill()
                        logging.debug(f'Killed child process: {child.name()}')
                    except Exception as ex:
                        logging.debug(f'Unable to kill child process: {child.name()} \n {ex}')
            try:
                proc.kill()
                logging.debug(f'Killed process: {current_proc_name}')
            except Exception as ex:
                logging.debug(f'Unable to kill process: {current_proc_name} \n {ex}')


def get_kpit_user_licenses(env):
    license_folder = {"prod": "934583504",
                      "test": "2103178387"}
    env_url = {"prod": "https://techconnect.agcocorp.com",
               "test": "https://agcouat.m-ize.com/"}
    license_path = WindowsPath(r"C:\Users\Default\KPIT_Jlicense").joinpath(license_folder[env])
    licenses_strings = []
    license_return = ""
    if license_path.is_dir():
        licenses_strings = list(license_path.glob("*.bin"))
    else:
        click.secho(f"No folder {license_path} was found you must log into {env_url[env]} and press connect for a "
                    f"license to be present", fg='red')
        navigate_flag = Confirm.ask(f"Do you want to navigate to this site?")
        if navigate_flag:
            webbrowser.open(env_url[env])
    licenses_dict = [parse("license_{user_license}.xml.bin", license_string.parts[-1]).named for license_string in
                     licenses_strings]
    licenses = [x['user_license'] for x in licenses_dict]

    if len(licenses) > 1:
        enumerated_licenses_dict = {str(x): y for x, y in enumerate(licenses)}
        for num, lic in enumerate(licenses):
            print(f"{num} :  {lic}")
        license_choice = click.prompt(
            "Please enter the number next to the license you want to utilize: ",
            type=click.Choice(enumerated_licenses_dict))
        license_return = enumerated_licenses_dict[license_choice]

    elif len(licenses) == 1:
        license_return = licenses[0]
    else:
        print(f"No licenses found in {license_path}")
    return license_return


def execute_command(path_and_command):
    """
    Runs an inputted command. If the command returns a non-zero return code it will fail. This method is not for
    capturing the output
    """
    logging.debug(f'Attempting to execute: {path_and_command}')
    p1 = subprocess.run(path_and_command,
                        shell=True,
                        check=True,
                        capture_output=True,
                        text=True,
                        )
    logging.debug(f'Command: {path_and_command}')
    logging.debug(f'ReturnCode: {str(p1.returncode)}')


def save_to_downloads(url, filename):
    save_path = os.path.expanduser(f'~\\Downloads\\{filename}')
    try:
        r = requests.get(url, allow_redirects=True)
        try:
            with open(save_path, 'wb') as f:
                f.write(r.content)
                logging.info(f"{filename} saved to {save_path}")
        except Exception as ex:
            logging.info(f'Unable to download the {filename} \n {ex}')
    except Exception as ex:
        logging.info(f'The link to download the {filename} is down \n {ex}')


def copy2clip(txt):
    cmd = f'echo {txt.strip()}|clip'
    click.secho(f"{txt} copied to clipboard\n", fg='green')
    return subprocess.check_call(cmd, shell=True)


def rec_dd():
    return defaultdict(rec_dd)


def tc_force_restart():
    uri = "http://127.0.0.1:9090/lifecycle"
    payload = {"force": "true",
               "restart": "true"}
    r = requests.post(uri, json=payload)
    if r.status_code == 200:
        click.secho("Force restart of TechConnect completed successfully")
    else:
        click.secho(f"The attempt to force restart of TechConnect returned a {r.status_code} return code.")


def check_service_tester_status():
    uri = "http://localhost:51711/api/DiagnosticServices"
    r = requests.get(uri)
    if r.status_code == 200:
        response = r.json()
        status = response['status']
    else:
        status = f"The api call to launch Service Tester returned a {r.status_code} return code."
        click.secho(f"The api call to launch Service Tester returned a {r.status_code} return code.")
    logging.info(f"Service Tester Status: {status}")
    return status


def get_auc_client_id():
    uri = "http://localhost:51712/ClientInfo"
    r = requests.get(uri)
    if r.status_code == 200:
        response = r.json()
        return response['ClientID']
    else:
        logging.info(f"The api call to get the AUC Client id returned a {r.status_code} return code.")


def launch_service_tester():
    uri = "http://localhost:51711/api/DiagnosticServices"
    r = requests.post(uri)
    if r.status_code == 200:
        logging.info("Launching Service Tester completed successfully")
    else:
        logging.debug(f"The attempt to launch Service Tester returned a {r.status_code} return code.")


def wait_till_st_starts():
    tc_status = check_service_tester_status()
    while tc_status not in ("ProcessStopped", "ProcessStarting", "STARTING", "RUNNING"):
        kill_process_tree_by_name("KPIT_Vehicle_Diagnostics.exe")
        tc_status = check_service_tester_status()
    try:
        tc_status = check_service_tester_status()
        counter = 1
        while counter < 10 and tc_status != "RUNNING":
            logging.debug(f"ServiceTester's status is {tc_status}")
            time.sleep(3)
            tc_status = check_service_tester_status()
            counter += 1
    except Exception as e:
        logging.warning(f"Service Tester did not launch. \n{e}")


def limas_license_status_is_active(limas_user):
    uri = f"http://127.0.0.1:8443/license/registration/{limas_user}"
    r = requests.get(uri)
    click.secho('\nLimas License Status:', fg="yellow")
    if r.status_code == 200:
        response_expiration_date = r.json()["expirationDate"]
        expiration_date = datetime.strptime(response_expiration_date, '%Y-%m-%dT%H:%M:%SZ')
        current_datetime = datetime.now()
        click.secho(f'{limas_user}: Expires in {str(expiration_date - current_datetime)}', fg="blue")
        return current_datetime > expiration_date
    else:
        print_json(r.text)
        return False


def sim_clean(organization):
    logging.info("Clearing folders of previous simulations")
    service_tester_path = WindowsPath(r"C:\Program Files\KPIT\K-DCP\KDCPServiceTester")

    config_path = WindowsPath(r"C:\ProgramData\KDCPServiceTester\config")
    data_path = WindowsPath(r"C:\ProgramData\KDCPServiceTester\data")
    if service_tester_path.joinpath("server").is_dir():
        tf2pdu = service_tester_path.joinpath('server', 'D-PDUAPI')
        if not tf2pdu.is_dir():
            tf2pdu.mkdir()
    else:
        tf2pdu = service_tester_path.joinpath('D-PDUAPI')
    if tf2pdu.joinpath("KPIT_simulation.txt").is_file():
        shutil.copy(tf2pdu.joinpath("KPIT_simulation.txt"), tf2pdu.joinpath("simulation.txt"))

    file_gen = tf2pdu.rglob("*_simulation.txt")
    for file in file_gen:
        try:
            os.remove(file)
        except Exception as e:
            logging.error(f"Error while deleting file : {file} \n{e}")
    if config_path.joinpath("KPIT_application.properties").is_file():
        shutil.copy(config_path.joinpath("KPIT_application.properties"),
                    config_path.joinpath("application.properties"))

    app_property_file_gen = config_path.rglob("*_application.properties")
    for file in app_property_file_gen:
        try:
            os.remove(file)
        except Exception as e:
            print(f"Error while deleting file : {file} \n{e}")
    new_data_folder = WindowsPath(f"{data_path}_{organization}")
    if new_data_folder.is_dir():
        shutil.rmtree(new_data_folder)


def win_service(win_service, command):
    """
    Sets a Windows service's start-up type to start or stop
    :param win_service: string name of Windows service
    :param command: support start and stop
    """
    if command in {"start", "stop"}:

        logging.debug(f'Attempting to set the following service to {command}: {win_service}')

        p1 = subprocess.run(fr'net {command} "{win_service}"',
                            shell=True,
                            capture_output=True,
                            text=True,
                            # check=True,
                            )
        if "successfully" in p1.stdout:
            logging.info(f"The {command} command was executed successfully on {win_service}")
        if "already" in p1.stderr or "not started" in p1.stderr:
            logging.info(f"The {win_service} is already in the desired state")
    else:
        logging.info(f"{command} is not supported")


def replace_text_in_file(file, search_term, replace_term):
    file_path_and_name = WindowsPath(file)
    with fileinput.input(file_path_and_name, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace(search_term, replace_term), end='')


def disable_simulations():
    app_prop_path = WindowsPath(r"C:\ProgramData\KDCPServiceTester\config\application.properties")
    logging.info(f"Updating {app_prop_path} to disable simulations")
    replace_text_in_file(app_prop_path, "simulationEnabled=true",
                         "simulationEnabled=false")


@click.group()
@click.version_option()
def cli():
    """Command-line utility to perform common testing actions for ST122"""


@cli.group()
def install():
    """Allows for install of common testing tools"""
    pass


@install.command()
def auc_ast():
    """Downloads AUC_AST.exe from the permalink (gets the latest released version)"""
    save_to_downloads('https://dl.agco-ats.com/AUC_AST.exe', 'AUC_AST.exe')
    # run_auc_client()


@install.command()
def aucclean():
    """Saves the latest version of AUC without subscribing to any update groups"""
    save_to_downloads('https://agcoedtdyn.azurewebsites.net/AGCOUpdateClient', 'AGCOUpdateClient.exe')


@install.command()
def choco():
    """Installs chocolatey nuget to a windows host assuming that it meets the installation requirements"""
    subprocess.call(r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe Set-ExecutionPolicy Bypass -Scope '
                    r'Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = '
                    r'[System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iwr '
                    r'https://chocolatey.org/install.ps1 -UseBasicParsing | iex', shell=True)


@cli.command()
@click.option("-e", "--environment", default="test", type=click.Choice(['test', 'prod'], case_sensitive=False))
@click.option("-t", "--tool", default='both', type=click.Choice(['limas', 'crypto', 'both'], case_sensitive=False))
def change(environment, tool):
    """Changes the development environment of Limas Server and Krypto config.properties"""
    environment = str(environment).lower()
    tool = str(tool).lower()
    kill_process_tree_by_name("KPIT_Vehicle_Diagnostics.exe")
    time.sleep(4)
    env_urls = {"prod": "https://servicetool.agcocorp.com/limasserver",
                "test": "https://testtool.agcocorp.com/limasserver"}
    if tool in {"limas", "both"}:
        try:
            if environment == "test":
                replace_text_in_file(r"C:\Program Files\KPIT\K-DCP\KDCPServiceTester\limas.properties",
                                     env_urls['prod'],
                                     env_urls["test"])
            else:
                replace_text_in_file(r"C:\Program Files\KPIT\K-DCP\KDCPServiceTester\limas.properties",
                                     env_urls['test'],
                                     env_urls["prod"])
            logging.info(f"Changed limas properties to {environment}")
        except FileNotFoundError as e:
            logging.info(
                r"The File path C:\Program Files\KPIT\K-DCP\KDCPServiceTester\limas.properties was not found. Please "
                f"confirm that Service Tester is installed.\n{e}")

    if tool in {"crypto", "both"}:
        try:
            if environment == "test":
                replace_text_in_file(r"C:\Program Files\KPIT\K-DCP\KDCPServiceTester\krypto\config.properties",
                                     env_urls['prod'], env_urls["test"])
            else:
                replace_text_in_file(r"C:\Program Files\KPIT\K-DCP\KDCPServiceTester\krypto\config.properties",
                                     env_urls['test'], env_urls["prod"])
            logging.info(f"Changed crypto properties to {environment}")

        except FileNotFoundError:
            logging.info(
                r"The C:\Program Files\KPIT\K-DCP\KDCPServiceTester\krypto\config.properties file was not found. "
                r"Please confirm that Service Tester is installed.")

    launch_service_tester()
    wait_till_st_starts()


@cli.group()
def st():
    """Command line interface to common actions with service tester"""
    pass


@st.command()
def status():
    """Returns Service Tester version and status"""
    uri = "http://localhost:51711/api/DiagnosticServices"
    try:
        r = requests.get(uri)
        if r.status_code == 200:
            response = r.text
        else:
            response = f"The api call to launch Service Tester returned a {r.status_code} return code."
        print_json(response)
    except Exception as e:
        click.secho(f"Please confirm that \"ACGO TCDiagnostics\" Service is running \n{e}", fg="red")


@st.command()
def restart():
    """Kills and restarts Service Tester"""
    kill_process_tree_by_name("KPIT_Vehicle_Diagnostics.exe")
    launch_service_tester()
    wait_till_st_starts()


@st.command(name="license")
@click.option("-e", "--environment", required=True, type=click.Choice(["test", "prod"]),
              help="Choose between test and production environments")
def get_license(environment):
    """Retrieves Limas License ID from file structure"""
    user_license = get_kpit_user_licenses(environment)
    if user_license:
        copy2clip(user_license)
        limas_license_status_is_active(user_license)


@st.group()
def service():
    """CLI commands to start and stop the AGCO TCDiagnostics service"""
    pass


@service.command(name="start")
def start_service():
    """Starts the AGCO TCDiagnostics service"""
    win_service("AGCO TCDiagnostics", "start")


@service.command(name="stop")
def stop_service():
    """Stops the AGCO TCDiagnostics service"""
    win_service("AGCO TCDiagnostics", "stop")


@cli.group()
def simulate():
    """Command line interface to add the necessary files to the proper folders to simulate different machines. It
    leverages the """
    pass


@simulate.command()
def guide():
    """Prints available simulations"""
    print(Panel("C220A - for C2-20 Valtra VCI simulation\n"
                "C220B - for C2-20 Massey VCI simulation\n"
                "C320B - for C3-20 Massey DGW simulation\n"
                "C320C - for C3-20 Valtra VCI simulation\n"
                "C320D - for C3-20 Massey Global VCI simulation\n"
                "M219A - for M2-19V Valtra DGW simulation\n"
                "M219B - for M2-19V Massey DGW simulation\n"
                "M219P - for M2-19P Fendt DGW simulation\n"
                "M219P14 - for M2-19P Fendt DGW (14 character SN) simulation\n"
                "S219A - for S2-19V Valtra DGW simulation\n"
                "S220P - for S2-20P Fendt DGW simulation\n"
                "YYDGW - for New DGW simulation\n"
                "YYDSH - for New DashBoard simulation\n"
                "YYNVA - for New DGW but No Value available", title="Available Simulations"))


@simulate.command()
@click.option("-o", "--organization", default="AGCOCORP", help="Backward compatibility")
def clean(organization):
    """Removes simulation files from previously run simulations"""
    sim_clean(organization)


@simulate.command()
def disable():
    """Changes value of application.properties to disable simulation"""
    disable_simulations()


sim_files = Path(__file__).parent.joinpath('templates', 'simulation').glob("*_simulation.txt")
sims = [x.name.split("_")[0] for x in sim_files]


@simulate.command()
@click.option("-s", "--selection", required=True, type=click.Choice(sims, case_sensitive=False))
@click.option("-d", "--dirty", is_flag=True, help="Leaves past simulation files")
@click.option("-o", "--organization", default="AGCOCORP",
              help='Allows user to specify organization. Defaults to \"AGCOCORP\".')
def start(selection, dirty, organization):
    """
    Performs all necessary process to starts simulation for a given machine.
    """
    kill_process_tree_by_name("KPIT_Vehicle_Diagnostics.exe")
    sel = str(selection).upper()
    template_path = WindowsPath(__file__).parent.joinpath('templates', 'simulation')
    config_template_path = WindowsPath(__file__).parent.joinpath('templates', 'config')
    service_tester_path = WindowsPath(r"C:\Program Files\KPIT\K-DCP\KDCPServiceTester")
    config_path = WindowsPath(r"C:\ProgramData\KDCPServiceTester\config")
    # data_path = WindowsPath(r"C:\ProgramData\KDCPServiceTester\data")
    if service_tester_path.joinpath("server").is_dir():
        tf2pdu = service_tester_path.joinpath('server', 'D-PDUAPI')
        if not tf2pdu.is_dir():
            logging.info(f"Creating {tf2pdu.name}")
            tf2pdu.mkdir()
    else:
        tf2pdu = service_tester_path.joinpath('D-PDUAPI')
    if not dirty:
        sim_clean(organization)

    if not tf2pdu.joinpath("KPIT_simulation.txt").is_file():
        logging.info("Creating KPIT_simulation.txt")
        shutil.copy(tf2pdu.joinpath("simulation.txt"), tf2pdu.joinpath("KPIT_simulation.txt"))

    if not config_path.joinpath("KPIT_application.properties").is_file():
        logging.info("Creating KPIT_application.properties")
        shutil.copy(config_path.joinpath("application.properties"), config_path.joinpath("KPIT_application.properties"))

    if not tf2pdu.joinpath(f'{sel}_simulation.txt').is_file():
        logging.info(f"Creating {sel}_simulation.txt in {tf2pdu}")

        try:
            shutil.copy(template_path.joinpath(f"{sel}_simulation.txt"), tf2pdu.joinpath(f"{sel}_simulation.txt"))
            logging.info(f"Updating {tf2pdu.joinpath('simulation.txt')}")
            shutil.copy(tf2pdu.joinpath(f'{sel}_simulation.txt'),
                        tf2pdu.joinpath("simulation.txt"))
        except Exception as ex:
            logging.warning(f"Could not write to {tf2pdu.joinpath(f'{sel}_simulation.txt')}\n {ex}")

    if not config_path.joinpath(f'{organization}_application.properties').is_file():
        try:

            logging.info(f"Creating {organization}_application.properties file in {config_path}")
            shutil.copy(config_template_path.joinpath("application.properties"),
                        config_path.joinpath(f"{organization}_application.properties"))

        except Exception as ex:
            logging.warning(
                f"Could not write to {config_path.joinpath(f'{organization}_application.properties')}\n {ex}")

        logging.info(f"Updating {config_path.joinpath('application.properties')}")
        shutil.copy(config_path.joinpath(f'{organization}_application.properties'),
                    config_path.joinpath("application.properties"))

    try:
        logging.info("Attempting to restart ServiceTester")
        launch_service_tester()
        wait_till_st_starts()

    except Exception as e:
        logging.warning(f"Service Tester did not launch. \n{e}")


@cli.group()
def opensite():
    """CLI to open some common URLs"""
    pass


@opensite.command()
def api():
    """Opens the TCD API"""
    webbrowser.open("http://127.0.0.1:51711/swagger/index.html")


@opensite.command()
def testapp():
    """Opens the TCD Test Web Application"""
    webbrowser.open("https://tcdwebapphost.z13.web.core.windows.net/")

@opensite.command()
def tc():
    """Opens the Production Tech Connect site"""
    webbrowser.open("https://techconnect.agcocorp.com/")


@opensite.command()
def bct():
    """Opens Beta CAPI Test"""
    webbrowser.open("https://betacapitest.z19.web.core.windows.net/")


@opensite.command()
def aucapi():
    """Opens the AUC API"""
    webbrowser.open("http://localhost:51712/swagger/ui/index#")


@opensite.command()
def uat():
    """Opens the TC UAT"""
    webbrowser.open("https://agcouat.m-ize.com/")


@opensite.command()
def update_groups():
    """Opens the Update System window to with the host's client id"""
    client_id = get_auc_client_id()
    webbrowser.open(
        f"https://secure.agco-ats.com/EDTSupportPortal/updatesystem-subscriptions.aspx?clientid={client_id}")


# @cli.group()
# def vm():
#     """Provides easy interface to interact with Terraform to quickly spin up azure VMs."""
#     pass
#
#
# @vm.command()
# def create():
#     """Takes vm inputs and uses the inputs in Terraform templates to create Azure VMs"""
#     create_flag = True
#     vm_types = {"win7": "test1",
#                 "win10": "test2",
#                 "win11": "test3"}
#     vm_list = []
#     vms_dict = rec_dd()
#     vm_counter = 1
#     while create_flag:
#         print("\n")
#         image_input = Prompt.ask(f"For vm {vm_counter}, which of these images do you want?",
#                                  choices=vm_types.keys(), show_choices=True)
#         vms_dict[str(vm_counter)].update({"vm_image": vm_types[image_input]})
#         vms_dict[str(vm_counter)]["vm_hostname"] = click.prompt(
#             "What do you want the name/basename of this/these vm/vms to be?")
#         vms_dict[str(vm_counter)]["vm_username"] = click.prompt("What do you want the admin username to be?",
#                                                                 default="Testuser1")
#         vms_dict[str(vm_counter)]["vm_password"] = click.prompt("What do you want the admin password to be?",
#                                                                 default="Testuser1!11")
#         vms_dict[str(vm_counter)]["vm_instances"] = click.prompt("How many of this type of VM do you want created?",
#                                                                  default=1)
#         print('\n')
#         vm_list.append(dict(vms_dict[str(vm_counter)]))
#         vm_counter += 1
#         create_flag = Confirm.ask("Do you want to create another VM?")
#     output = (dumps(vms_dict, indent=4))
#     print(Panel(output, title="VMs to Create", highlight=True))
#     return vm_list


if __name__ == "__main__":
    cli()
