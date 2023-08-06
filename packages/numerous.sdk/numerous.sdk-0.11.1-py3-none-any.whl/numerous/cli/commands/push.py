import json
import sys
from datetime import datetime
from logging import Logger, getLogger
from pathlib import Path
from typing import Optional

import requests
from dirtools import Dir, DirState, filehash

from ..auth import AuthenticationError, login
from ..build_manager_client import (
    SnapshotAlreadyExistsError,
    SnapshotError,
    get_build_manager_client,
)
from ..repository import NumerousRepository
from ..utils import GzippedTarball, bold, cyan, green, red, yellow

log = getLogger(__name__)


def get_snapshot_id(path: Path) -> str:
    dir = Dir(str(path))
    return str(dir.hash(index_func=filehash))


def get_snapshot_state(path: Path) -> DirState:
    dir = Dir(str(path))
    state = DirState(dir, index_cmp=filehash).state.copy()
    del state["directory"]
    return state


def print_push_error(msg: str, help_text: Optional[str] = None) -> None:
    print(red(f"Cannot push: {msg}"))
    if help_text:
        print(help_text)


def upload_snapshot(path: Path, upload_url: str, snapshot_id: str) -> None:
    print("Uploading snapshot...")
    with GzippedTarball(path) as tar_path:
        log.debug(f"Created tarball {tar_path} for {path}")
        with open(tar_path, "rb") as tar_file:
            upload_response = requests.post(
                upload_url,
                data=tar_file,
                headers={"Content-Type": "multipart/related"},
                params={"name": snapshot_id, "mimeType": "application/octet-stream"},
            )
            if upload_response.ok:
                log.debug(
                    f"Uploaded snapshot {snapshot_id} got response: {upload_response.status_code} "
                    f"{upload_response.reason}"
                )
            else:
                log.debug(
                    f"Failed uploading {snapshot_id} {upload_response.status_code} {upload_response.reason}"
                )
                raise RuntimeError("An error occured during upload")


def command_push(log: Logger, repo_path: Optional[Path], comment: str) -> None:
    path = Path.cwd() if repo_path is None else repo_path

    if not path.exists():
        print_push_error(f"{bold(path)} does not exist")
        sys.exit(1)

    repo = NumerousRepository(path).load()

    if repo.scenario is None:
        print_push_error("A scenario must be checked out.")
        sys.exit(1)

    if repo.snapshot == Dir(str(path)).hash(index_func=filehash):
        print_push_error("Cannot push: There is nothing new to push.")
        sys.exit(1)

    if repo.remote is None:
        help_text = (
            f'Use the command {bold("numerous config --remote <REMOTE_URL>")} to configure a remote for the '
            "repository."
        )
        print_push_error("No remote is configured for the repository.", help_text)
        sys.exit(1)

    try:
        id_token = login(repo)
    except AuthenticationError:
        print_push_error("Login failed.")
        sys.exit(1)

    print(cyan(f"Pushing to remote repository {bold(repo.remote)}..."))
    print("Creating snapshot metadata...")
    snapshot_id = get_snapshot_id(repo.path)
    snapshot_state = json.dumps(get_snapshot_state(repo.path))

    if len(snapshot_state) > 4e6:
        print_push_error(
            "The snapshot contains too many files and directories - please use the .exclude file to "
            "exclude files that are not needed."
        )
        sys.exit(1)

    with get_build_manager_client(repo.remote.api_url, id_token) as build_manager:
        try:
            upload_url = build_manager.create_snapshot_get_upload_url(
                repo.remote.name, snapshot_id, snapshot_state
            )
        except SnapshotAlreadyExistsError:
            print(yellow(f"Snapshot {snapshot_id} already exists. Stopping."))
            sys.exit(0)
        except SnapshotError:
            print_push_error("An error occured during snapshot creation.")
            sys.exit(1)

        try:
            upload_snapshot(repo.path, upload_url, snapshot_id)
        except Exception as e:
            print_push_error(str(e))
            sys.exit(1)

        commit_id = build_manager.create_history_update(
            repo.remote.name,
            repo.scenario.project_id,
            repo.scenario.id,
            snapshot_id,
            repo.commit,
            comment,
            datetime.utcnow().timestamp(),
        )
    print(green(f"Pushed snapshot {bold(snapshot_id)} as commit {bold(commit_id)}."))

    repo.commit = commit_id
    repo.snapshot = snapshot_id
    repo.save()
