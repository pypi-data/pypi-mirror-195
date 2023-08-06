import datetime
import time 
import sys, os
import requests
import logging
import socket
from tabulate import tabulate
from pathlib import Path
from pprint import pprint
from ..utils import dumps, abort, get_datafile
from subprocess import check_call, call
from P4 import P4, P4Exception
import shutil

log = logging.getLogger(__name__)

from typer import Context, launch, echo, secho, Option, Typer, confirm, prompt, style, progressbar

app = Typer()
task_app = Typer(name="task")


hostname = socket.gethostname().lower()
SUBST_DRIVE = "S:"
path = f"{SUBST_DRIVE}\\sn2-main\\"
BASE_STREAM = "//Project/SN2-Main"
UE_STREAM = "//project/sn2-main-ue"

p4 = None

def connect_p4():
    p4_conn = P4()
    try:
        p4_conn.connect()
    except Exception as e:
        abort(f"Cannot establish connection with Perforce server: {e}...")
    return p4_conn


@task_app.callback()
def main():
    """
    Manage task streams.
    
    This tool is highly opinionated and expects you to be using the //Project/SN2-Main-UE stream and be working in a workspace called <username>_<label>_sn2-main
    """
    global p4
    p4 = connect_p4()
    ret = get_current_stream()
    client = get_current_client()
    
    if "Stream" not in ret:
        abort("Invalid workspace. You must be working in Streams to use this tool")
    stream_name = ret["Stream"]
    parent = ret["Parent"]
    secho(f"You are currently working in client {client['Client']} - stream: {stream_name}, root: {client['Root']}", fg="blue")
    if parent.lower() != UE_STREAM and stream_name.lower() != UE_STREAM:
        abort(f"To use this tool you must be working in the {UE_STREAM} stream while your workspace is set on {stream_name}. Please change your workspace with 'p4 set P4CLIENT <username>_<label>_sn2-main'")

def get_task_streams():
    lst = p4.run_streams("-F", f"Owner=jonb Type=task baseParent={BASE_STREAM}")
    return lst

def get_current_stream():
    ret = p4.run_stream("-o")[0]
    return ret

def get_current_client():
    ret = p4.run_client("-o")[0]
    return ret

def get_clients():
    try:
        specs = p4.run_clients("-u", p4.user)
    except Exception as e:
        abort(str(e))
    ret = {}
    for s in specs:
        host = s["Host"].lower()
        if host == hostname or not host:
            ret[s["Stream"].lower()] = s
    return ret

def sync():
    s = confirm("Sync latest?")

    if not s:
        return

    secho(f"Syncing all (this will take a while)...")
    try:
        ret = p4.run_sync("-q", f"{path}...")
    except P4Exception as e:
        print(e)

@task_app.command()
def create(label: str = Option(None, prompt="Task branch label")):
    """
    Create a new task branch
    """
    if not label:
        abort("Aborted.")
    clients = get_clients()

    ue_stream_client = None
    for k, c in clients.items():
        if k == UE_STREAM:
            ue_stream_client = c
    if not ue_stream_client:
        abort(f"You have no workspace mapped to the {UE_STREAM} stream. Please set one up.")
    print(ue_stream_client)
    task_client_name = ue_stream_client["client"] + "_task"
    task_client = None
    for k, c in clients.items():
        if c["client"] == task_client_name:
            echo(f"Reusing existing task workspace {k}")
            task_client = c
            break


    d = datetime.datetime.utcnow().isoformat().split("T")[0]
    label = label.replace(" ", "_").lower()
    stream_name = f"{p4.user}-{d}-{label}"
    full_stream_name = f"//Project/{stream_name}"
    secho(f"Creating task stream {stream_name} from {UE_STREAM}...")
    args = f"""
Stream: {full_stream_name}
Owner:  {p4.user}
Name:   {stream_name}
Parent: {UE_STREAM}
Type:   task
Description:
    Created by {p4.user}.
Options:        allsubmit unlocked toparent fromparent mergedown
ParentView:     inherit
Paths:
    share ...
"""
    p4.input = args
    ret = p4.run_stream("-i", "-t", "task")
    print(ret[0])

    secho(f"Populating stream {full_stream_name}...")
    try:
        ret = p4.run_populate("-o", "-S", full_stream_name, "-r", "-d", "Initial branch")
    except P4Exception as e:
        if e.errors:
            secho(e.errors[0], fg="yellow")


    if not task_client and 0:
        root = f"{ue_stream_client['Root']}_task"
        echo("Creating new workspace {task_client_name} -> {root}...")
        client_spec = f"""
Client: {task_client_name}
Owner:  {ue_stream_client['Owner']}
Host:   {ue_stream_client['Host']}
Description:
    Automatically created task workspace for {ue_stream_client['Owner']}

Root:   {root}
Options:        noallwrite noclobber nocompress unlocked nomodtime normdir
SubmitOptions:  submitunchanged
LineEnd:        local
Stream: {full_stream_name}"""
        p4.input = client_spec
        p4.run_client("-i")

    p4.client = task_client_name
    secho(f"Switching current workspace to {full_stream_name}...")
    p4.run_client("-s", "-S", full_stream_name)
    ret = p4.run_client("-o")[0]
    root_path = ret["Root"]

#    if not task_client:
#        secho("Force syncing your new workspace folder to latest")
#        ret = p4.run_sync(f"{root}...#head")
#    else:
#        sync()


    ret = p4.run_stream("-o")[0]
    stream_name = ret["Stream"]
    parent = ret["Parent"]

    if ret["Type"] != "task":
        abort(f"Something went wrong. Current stream {stream_name} is not a task stream")

    secho(f"You are now working in task stream {stream_name} from parent {parent}", bold=True, fg="green")


@task_app.command()
def switch():
    """
    Lists your current task streams and lets you switch between them
    """
    task_streams = get_task_streams()
    stream = get_current_stream()
    parent = None
    if stream["Type"] == "task":
        parent = stream["Parent"]
    for i, t in enumerate(task_streams):
        secho(f"{i+1} : {t['Stream']}")
    if parent:
        secho(f"0 : {parent}")
    
    if not task_streams:
        abort("You have no task streams. You can create one with the 'create' command")
    n = prompt("\nSelect a stream to work in")
    if n is None:
        abort("No stream selected")
    n = int(n)
    if n == 0:
        new_stream = parent
    else:
        new_stream = task_streams[n-1]["Stream"]
    
    secho(f"\nSwitching to stream {new_stream}", bold=True)
    try:
        p4.run_client("-s", "-S", new_stream)
    except P4Exception as e:
        abort(e)

    sync()



@task_app.command()
def update():
    """
    Merge from parent down to your current task branch
    """
    ret = p4.run_stream("-o")[0]
    stream_name = ret["Stream"]
    parent = ret["Parent"]
    if ret["Type"] != "task":
        abort(f"Current stream {stream_name} is not a task stream")

    ret = p4.run_client("-o")[0]
    root_path = ret["Root"]
    client = ret["Client"]

    ret = p4.run_opened()
    if (len(ret)):
        abort("Your default pending changelist must be empty.")

    secho(f"Integrating latest from parent {parent} to task stream {stream_name}...", bold=True)

    p4.input = f"""
Change: new
Client:	{client}
User:	{p4.user}

Description:
	Automatically merge {UE_STREAM} to {stream_name}

"""

    try:
        cmd = ["-Af", "-S", stream_name, "-r", f"{stream_name}/..."]
        ret = p4.run_merge(*cmd)
    except P4Exception as e:
        if e.errors:
            secho(e.errors[0], fg="red")
        if e.warnings:
            secho(e.warnings[0], fg="yellow")
        if "already integrated" in str(e):
            secho(f"Your task stream is already up to date with {UE_STREAM}", fg="green")
        return
    #ret = p4.run_opened()
    #for f in ret:
    ret = p4.run_resolve("-f", "-am", "-as", f"{root_path}/...")
    
    # p4 fstat -Olhp -Rco -e default //jonb_work_sn2-main/...
    ret = p4.run_fstat("-Olhp", "-Rco", "-e", "default", f"{root_path}/...")
    if not ret:
        abort("Your task stream is up to date.")

    unresolved = []
    for r in ret:
        if "unresolved" in r:
            unresolved.append(r)
            secho(f"  {r['clientFile']}... conflict", fg="yellow")
        else:
            secho(f"  {r['clientFile']}... ok", fg="green")
    
    if unresolved:
        y = confirm(f"\nOverwrite conflicting files in your task stream from {UE_STREAM}?")
        if not y:
            abort("Please resolve remaining files in p4v")
        for r in unresolved:
            ret = p4.run_resolve("-f", "-at", f"{r['clientFile']}")
        secho("Unresolved files have been overwritten by parent stream")

    ret = p4.run_fstat("-Olhp", "-Rco", "-e", "default", f"{root_path}/...")
    filelist = ""
    for r in ret:
        if "unresolved" in r:
            abort("There are still unresolved files in your pending changelist. Please resolve them in p4v")
        filelist += f"    {r['depotFile']}\n"

    mr = ""
    if unresolved:
        mr = f"{len(unresolved)} unresolvable files were overwritten."

    txt = f"""
Change: new
Client:	{client}
User:	{p4.user}

Description:
	Automatically merge {UE_STREAM} to {stream_name}. {mr}
Files:
{filelist}
"""
    p4.input = txt
    p4.run_submit('-i')

    ret = p4.run_resolve("-f", "-am", "-as", f"{root_path}...")
    ret = p4.run_fstat("-Olhp", "-Rco", "-e", "default", f"{root_path}/...")
    if not ret:
        secho(f"Your task stream is now up to date with {UE_STREAM}", fg="green")
    else:
        abort("Something is amiss. Your task stream is not up to date after the merge. Take a look at p4v")

@task_app.command()
def delete():
    """
    Permanently delete your current task stream"""
    ret = p4.run_stream("-o")[0]
    stream_name = ret["Stream"]
    parent = ret["Parent"]
    if ret["Type"] != "task":
        abort(f"Current stream {stream_name} is not a task stream")

    delete = confirm("Are you sure you want to delete the current task stream?")
    if delete:
        secho(f"Switching back to {parent}...")
        p4.run_client("-s", "-S", parent)

        secho(f"Deleting task stream {stream_name}...")
        p4.run_stream("--obliterate", "-y", stream_name)
    else:
        abort("Aborted")


app.add_typer(task_app)
