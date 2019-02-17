import click
import subprocess
import os


def pickup_config_files():
    user = os.path.expanduser('~')
    list = ['.bashrc', '.zshrc', '.vimrc', '.profile', '.gitconfig']
    for file in list:
        if (os.path.exists(user + '/' + file)):
            copy = user + '/' + file
            destination = './dotfile/' + file
            subprocess.call(['cp', copy, destination])


def pickup_python_packages():
    with open('./dotfile/requirement.pip', 'w') as f:
        subprocess.call(['pip', 'freeze', ], stdout=f)


def pickup_installed_packages():
    with subprocess.Popen(['sudo', 'dnf', 'history', 'userinstalled'],
                          stdout=subprocess.PIPE, ) as proc:
        file = proc.stdout.read()
        with open('./dotfile/packages.sh', 'wb') as f:
            f.write(file)
    with open('./dotfile/packages.sh', 'r') as fread:
        list_of_packages = fread.readlines()
    for i in range(len(list_of_packages)):
        list_of_packages[i] = "sudo dnf install -y " + list_of_packages[i]
    with open('./dotfile/packages.sh', 'w') as fwrite:
        for i in range(len(list_of_packages)):
            fwrite.write(list_of_packages[i])


def system_setup():
    pass


@click.command()
@click.option('--make', '-m', nargs=2, type=str,
              help="To make your oliv_dotfile setup")
@click.option('--setup', '-s', nargs=2, type=str,
              help="To configure your system with your oliv_dotfile setup")
def oliv(make, setup):
    if make:
        subprocess.call(['mkdir', './dotfile'])
        pickup_config_files()
        pickup_python_packages()
        pickup_installed_packages()
    elif setup and os.path.isdir('./oliv_dotfile'):
        system_setup()
