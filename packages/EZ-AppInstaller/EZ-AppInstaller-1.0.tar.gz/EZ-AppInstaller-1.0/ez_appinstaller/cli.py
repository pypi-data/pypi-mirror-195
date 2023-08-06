import os
import click
import shutil
import yaml
import rich_click as click

CONFIG_PATH = os.path.join(os.getenv('LOCALAPPDATA'), 'EZ-AppInstaller', 'config.yaml')



@click.group()
@click.version_option(version='1.0.0')
def cli():
    pass


@cli.command()
@click.argument('source', type=click.Path(exists=True))
@click.option('--name', help='Name of the shortcut to create')
@click.option('--all', is_flag=True, help='Install all files in the folder')
@click.option('--copy-parent', is_flag=True, help='Copy the parent folder of the chosen executable')
@click.option('--dir', '-d', default=None, help='Installation directory')
@click.option('--shortcut', is_flag=True, default=True, help='Create a shortcut in the Quick Start menu')
@click.help_option(help="Show this message and exit.")
def install(source, name, all, copy_parent, dir, shortcut):
    """
    Install a file or folder.

    Examples:

    \b
    $ ez-install install myfile.exe
    $ ez-install install myfolder --all --shortcut --name "My Program"
    """
    config = load_config()
    default_install_dir = config.get('default_install_dir')
    default_shortcut_dir = config.get('default_shortcut_dir')
    applications = config.get('applications', {})

    if dir is None:
        dir = default_install_dir

    if not os.path.exists(dir):
        os.makedirs(dir)

    if all:
        items = os.listdir(source)
    else:
        items = [os.path.basename(source)]

    for item in items:
        source_path = os.path.join(source, item)
        if os.path.isfile(source) and (all or item.endswith('.exe')):
            if copy_parent:
                install_dir = os.path.abspath(os.path.join(dir, os.path.pardir))
                shutil.copytree(os.path.dirname(source_path), install_dir)
            else:
                install_dir = os.path.join(dir, os.path.splitext(item)[0])
                os.makedirs(install_dir, exist_ok=True)
                shutil.copy(source, install_dir)

            if shortcut:
                if name is None:
                    name = os.path.splitext(item)[0]
                shortcut_dir = default_shortcut_dir or os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs')
                create_shortcut(install_dir, name, shortcut_dir)

            applications[name] = (install_dir, os.path.join(shortcut_dir, f'{name}.lnk') if shortcut else None)

    save_config('applications', applications)


@cli.command()
@click.argument('name')
@click.help_option(help="Show this message and exit.")
def uninstall(name):
    """
    Uninstall an application by name.

    Example:

    \b
    $ ez-install uninstall MyProgram
    """
    config = load_config()
    applications = config.get('applications', {})

    if name not in applications:
        raise click.BadParameter(f"{name} not found")

    install_dir, shortcut_path = applications[name]

    if os.path.exists(install_dir):
        shutil.rmtree(install_dir)
        click.echo(f'{install_dir} has been removed.')

    if shortcut_path is not None and os.path.exists(shortcut_path):
        os.remove(shortcut_path)
        click.echo(f'{shortcut_path} has been removed.')

    del applications[name]
    save_config('applications', applications)

@cli.command()
@click.option('--dir', '-d', default=None, help='Set default installation directory')
@click.option('--shortcut-dir', '-s', default=None, help='Set default shortcut directory')
@click.help_option(help="Show this message and exit.")
def config(dir, shortcut_dir):
    """
    Set default installation and shortcut directories.

    If no options are provided, displays the current values of the default installation and shortcut directories.
    """
    if dir is not None:
        save_config('default_install_dir', dir)
    if shortcut_dir is not None:
        save_config('default_shortcut_dir', shortcut_dir)

    if not dir and not shortcut_dir:
        config = load_config()
        default_install_dir = config.get('default_install_dir', "Not set")
        default_shortcut_dir = config.get('default_shortcut_dir', "Not set")
        click.echo(f"Default installation directory: {default_install_dir}")
        click.echo(f"Default shortcut directory: {default_shortcut_dir}")

@cli.command()
def list():
    click.echo('Installed Applications:')
    config = load_config()
    applications = config.get('applications', {})
    if not applications:
        click.echo('No applications installed.')
    else:
        for name, install_path in applications.items():
            click.echo(f'{name}: {install_path}')


def create_shortcut(target, name, shortcut_dir):
    click.echo('make shortcut')
    from win32com.client import Dispatch
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(os.path.join(shortcut_dir, f'{name}.lnk'))
    shortcut.TargetPath = os.path.join(target, f'{name}.exe')
    shortcut.WorkingDirectory = target
    shortcut.save()

def save_config(key, value):
    config = load_config()
    config[key] = value
    with open(CONFIG_PATH, 'w') as f:
        yaml.safe_dump(config, f)

def load_config():
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'w') as f:
            yaml.safe_dump({}, f)

    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f) or {}

if __name__ == "__main__":
    cli()