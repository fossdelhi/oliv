import click
import subprocess
import os
import shutil
import glob


def pickup_dotconfig():
    user = os.path.expanduser('~')
    source = user + '/.config'
    destination = './oliv_dotfile/.config/'
    shutil.copytree(source, destination)


def search_config_files():
    list = ['.aliases', '.bashrc', '.cookiecutterrc',
            '.exports', '.extra', '.functions', '.gdbinit',
            '.gitattributes', '.gitconfig', '.gitignore',
            '.gitmessage', '.inputrc', '.linux', '.osx',
            '.profile', '.travis.yml', '.vimrc', '.wgetrc',
            '.zshrc']
    files = []
    for x in list:
        if (os.path.exists(os.path.expanduser('~') + '/' + x)):
            files.append(x)
    pickup_config_files(files)


def pickup_config_files(files):
    user = os.path.expanduser('~')
    for file in files:
        if (os.path.exists(user + '/' + file)):
            copy = user + '/' + file
            destination = './oliv_dotfile/' + file
            subprocess.call(['cp', copy, destination])


def pickup_python_packages():
    with open('./oliv_dotfile/requirement.pip', 'w') as f:
        subprocess.call(['pip', 'freeze', ], stdout=f)


def pickup_installed_packages():
    with subprocess.Popen(['sudo', 'dnf', 'history', 'userinstalled'],
                          stdout=subprocess.PIPE, ) as proc:
        file = proc.stdout.read()
        with open('./oliv_dotfile/packages.sh', 'wb') as f:
            f.write(file)
    with open('./oliv_dotfile/packages.sh', 'r') as fread:
        list_of_packages = fread.readlines()
    for i in range(len(list_of_packages)):
        list_of_packages[i] = "sudo dnf install -y " + list_of_packages[i]
    with open('./oliv_dotfile/packages.sh', 'w') as fwrite:
        for i in range(len(list_of_packages)):
            fwrite.write(list_of_packages[i])


def system_setup():
    user = os.path.expanduser('~')
    source = './oliv_dotfile/.*'
    files = glob.glob(source)
    destination = user + '/'
    subprocess.call(['cp', '-r', './oliv_dotfile/.config', destination])
    for file in files:
        subprocess.call(['cp', file, destination])
    subprocess.call(['pip', 'install', '-r', './oliv_dotfile/requirement.pip'])
    with subprocess.Popen(['sudo', 'bash', './oliv_dotfile/packages.sh']) as f:
        if False:
            f


@click.command()
@click.option('--make', '-m', is_flag=True,
              help="To make your oliv_dotfile setup")
@click.option('--setup', '-s', is_flag=True,
              help="To configure your system with your oliv_dotfile setup")
def oliv(make, setup):
    if make:
        subprocess.call(['mkdir', './oliv_dotfile'])
        pickup_dotconfig()
        search_config_files()
        pickup_python_packages()
        pickup_installed_packages()
    elif setup and os.path.isdir('./oliv_dotfile'):
        system_setup()


if __name__ == '__main__':
    oliv()
