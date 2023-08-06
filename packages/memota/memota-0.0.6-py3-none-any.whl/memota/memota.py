import resource
import sys
import daemon
import lockfile
import click
import traceback
import os
import time
import argparse
import logging
from daemon import pidfile
import psutil



debug_p = False

def get_memory():
    with open('/proc/meminfo', 'r') as mem:
        free_memory = 0
        for i in mem:
            sline = i.split()
            if str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:'):
                free_memory += int(sline[1])
    return free_memory


def get_ram_usage():
    """
    Obtains the absolute number of RAM bytes currently in use by the system.
    :returns: System RAM usage in bytes.
    :rtype: int
    """
    return int(psutil.virtual_memory().total - psutil.virtual_memory().available)


def get_ram_total():
    """
    Obtains the total amount of RAM in bytes available to the system.
    :returns: Total system RAM in bytes.
    :rtype: int
    """
    return int(psutil.virtual_memory().total)


def get_ram_usage_pct():
    """
    Obtains the system's current RAM usage.
    :returns: System RAM usage as a percentage.
    :rtype: float
    """
    return psutil.virtual_memory().percent


def do_something(logf):
    ### This does the "work" of the daemon

    logger = logging.getLogger('eg_daemon')
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(logf)
    fh.setLevel(logging.INFO)

    formatstr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(formatstr)

    fh.setFormatter(formatter)

    logger.addHandler(fh)

    while True:
        try:
            logger.info('RAM usage is {} %'.format(get_ram_usage_pct()))
            logger.info('RAM total is {} MB'.format(int(get_ram_total() / 1024 / 1024)))
            logger.info('RAM usage is {} MB'.format(int(get_ram_usage() / 1024 / 1024)))
            time.sleep(5)
        except MemoryError:
            sys.stderr.write('\n\nERROR: Memory Exception\n')
            sys.exit(1)


def start_daemon(pidf, logf):
    ### This launches the daemon in its context

    global debug_p

    if debug_p:
        print("eg_daemon: entered run()")
        print("eg_daemon: pidf = {}    logf = {}".format(pidf, logf))
        print("eg_daemon: about to start daemonization")

    ### XXX pidfile is a context
    with daemon.DaemonContext(
        working_directory='/home/bovdur/DocuSketch/memota',
        umask=0o002,
        pidfile=pidfile.TimeoutPIDLockFile(pidf),
        ) as context:
        do_something(logf)


@click.group(chain=True)
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    click.echo(f"Debug mode is {'on' if debug else 'off'}")
    global debug_p
    debug_p = debug


@cli.command()
def start():
    pid_file = '/home/bovdur/DocuSketch/memota/eg_daemon.pid'
    log_file = '/home/bovdur/DocuSketch/memota/eg_daemon.log'
    start_daemon(pid_file, log_file)
#test

@cli.command()
def stop():
    f = open("eg_daemon.pid","r")
    line = f.readlines()
    try:
        print(f'Killing processes {line[0]}')
        try:
                p = psutil.Process(int(line[0]))
                p.terminate()  #or p.kill()
        except Exception:
            print(f"{traceback.format_exc()}")
    except Exception:
        print(f"{traceback.format_exc()}")

    os.remove("eg_daemon.pid")
    os.remove("eg_daemon.log")


if __name__ == "__main__":
    cli()


