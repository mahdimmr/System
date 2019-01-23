from Sys import mail
from flask_mail import Message
from flask import url_for
import shutil
import urllib.request
import socket
import multiprocessing
import psutil
import platform



#Calculate the System Storage of address that 'drive' value take that
def get_system_storage(drive):
    total, used, free = shutil.disk_usage(drive)
    totaldisk = total // (2 ** 30)
    Used = used // (2 ** 30)
    Free = free // (2 ** 30)
    return f"Total: {totaldisk}GB Used Memory: {Used}GB Free: {Free}GB"


#view source any site you want
def view_source_any_site():
    with urllib.request.urlopen('http://198.143.180.66:5000') as response:
        html = response.read()
    return html


#get local IP with using socket library
def local_ip():
    loc_ip = socket.gethostbyname(socket.gethostname())
    return loc_ip



def get_hostname_ip(hostname):
    ip = socket.gethostbyname(hostname)
    answer = f"('Hostname: ', {hostname}, '\n' 'IP: ', {ip})"
    return answer


#send token for reset password
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='flask.sup@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link: {url_for('reset_token', token=token,
                                                                              _external=True)}"

If you not make this request then simply ignore this email and no change will be made.'''

    mail.send(msg)


#see battery status and percent charge have
def get_battery():
    battery = psutil.sensors_battery()
    if not battery:
        return 'No Battery!'
    plugged = battery.power_plugged
    percent = str(battery.percent)
    if plugged:
        return f'{percent}% Charging!'
    else:
        return f'{percent}% Cable Not Plugged In!'


#get battery percent charge
def get_battery_percent():
    battery = psutil.sensors_battery()

    if not battery:
        return None
    plugged = battery.power_plugged
    percent = str(battery.percent)
    if plugged:
        return percent


#show distro if OS was Linux
def linux_distru():
    if platform.system() == 'linux':
        distro_linux = platform.linux_distribution()
        return distro_linux
    return '.'


#show core of cpu
def cpu_core_count():
    num_of_core = multiprocessing.cpu_count()
    return num_of_core


#get connection network Port and IP
def connection_list():
    conn_lists = psutil.net_connections()
    return conn_lists


#show disk partition
def disk_partition():
    disk_part = psutil.disk_partitions()
    return disk_part


#show task runnig
#def running_task():



#get phsical Ram usage
def ram_usage():
    ram = psutil.virtual_memory()
    total = ram.total
    free = ram.free
    available = ram.available
    return f"Total Ram Usage: {total} Free:{free} Available: {available}"
