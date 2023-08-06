"""
This module will contain all the sdk functions for the iris command sdk, including login, logout, get, post, pull.
"""
import hashlib

# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #

import logging
import pathlib
import tarfile
from pathlib import Path
from typing import Optional, Union
from urllib.parse import urljoin, urlparse
import os
import io
import json

# for iris pull
import requests
from rich import print
import wget
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper

# internal imports
from .auth_utils import auth, handle_bad_response
from .conf_manager import conf_mgr
from .exception import (
    ArtefactNotFoundError,
    ArtefactTypeInvalidError,
    BadRequestError,
    DownloadLinkExpiredError,
    DownloadLinkNotFoundError,
    InvalidCommandError,
    ArtefactNotFoundError,
    UnsafeTensorsError,
    MissingTokenizerError,
)
from .utils import pull_image, tarify, dump, upload_from_file

# Whether to use tqdm for progress bars
TQDM = True

# ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                  IRIS USERS SDK                                                     #
# ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


# ------------------------------------      Setup Logger      ------------------------------------ #
# Logger config
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
)
logger = logging.getLogger(__name__)
logger.setLevel(conf_mgr.LOG_LEVEL)


# --------------------------------------      iris login    -------------------------------------- #
@auth
def login():
    logger.debug("logging in")
    return conf_mgr.current_user["name"]


# --------------------------------------     iris logout    -------------------------------------- #


def logout():
    logger.info("logging out")
    path = Path.home() / Path(conf_mgr.config.keyfile_name)
    if path.exists():
        path.unlink()
    if not path.exists():
        return True
    else:
        return False


# --------------------------------------      iris post     -------------------------------------- #


@auth
def post(**flags):
    endpoint = "experiment"
    # detype the flags, so we can send them
    payload = {k: str(val) for k, val in flags.items()}
    logger.debug(f"Dispatching job with payload {payload}")
    url = urljoin(conf_mgr.runner_url, f"{endpoint}/")
    headers = {"Authorization": f"Bearer {conf_mgr.access_token}"}
    response = requests.post(url=url, headers=headers, data=payload)
    if not response.ok:
        raise handle_bad_response(response, endpoint)
    else:
        print(dump(response))


# --------------------------------------       iris get     -------------------------------------- #


@auth
def get(
    object: str = "experiment",
    id: Optional[str] = None,
    query: Optional[str] = None,
    verbose=True,
):
    """Get objects from the titan API

    Args:
        object (str, optional): The object to get. Defaults to "experiment".
        id (Optional[str], optional): The id of the object. Defaults to None.
        query (Optional[str], optional): A JMESPath query to run against the returned json. Defaults to None, i.e. return everything.
    Returns:
        (str) A json response, formatted as: {"status": <http_response>, "response": <queried_json_response>}
    """
    logger.debug(f"Getting from ... {conf_mgr.base}, auth from {conf_mgr.AUTH0_DOMAIN}")
    endpoint = object + "/" + (str(id) if id is not None else "")
    url = urljoin(conf_mgr.runner_url, endpoint)
    headers = {"Authorization": f"Bearer {conf_mgr.access_token}"}

    response = requests.get(url=url, headers=headers)
    if not response.ok:
        raise handle_bad_response(response, endpoint)
    else:
        dumped_response = dump(response, query)
        if verbose:
            print(dumped_response)
        return dumped_response


# --------------------------------------      iris pull     -------------------------------------- #


@auth
def pull(experiment_cmd: str):
    logger.info("***Executing pull command***")

    Path("model_storage").mkdir(parents=True, exist_ok=True)

    args = experiment_cmd.split(":")
    if len(args) != 2:
        raise InvalidCommandError

    experiment_id = args[0]
    job_tag = args[1]
    endpoint = "experiment"
    url = urljoin(conf_mgr.runner_url, f"{endpoint}/{experiment_id}")
    headers = {"Authorization": f"Bearer {conf_mgr.access_token}"}

    response = requests.get(url=url, headers=headers)
    response_json = response.json()

    # check if the request was successful
    if response_json["status"] != "success":
        raise BadRequestError
    else:
        jobs_list = response_json["experiment"]["jobs"]
        model_uuid = None
        # loop through the jobs list and find the job with the same tag
        for i in range(len(jobs_list)):
            if job_tag == jobs_list[i]["name"].split("_")[-1]:
                model_uuid = jobs_list[i]["out_art_id"]
                model_name = jobs_list[i]["name"]
                task_name = jobs_list[i]["flags"]["task"]
                baseline_model_name = jobs_list[i]["flags"]["model.teacher"]

                if baseline_model_name is None:
                    baseline_model_name = jobs_list[i]["flags"]["model.student"]

                if task_name == "glue":
                    task_name = "sequence_classification"  # tranlate glue to sequence_classification

                # check if the download link is valid
                if model_uuid is None:
                    raise ArtefactNotFoundError
                else:
                    url = urljoin(
                        conf_mgr.runner_url,
                        "artefact/link/" + model_uuid + "/download",
                    )
                    response = requests.get(url=url, headers=headers)
                    response_json = response.json()
                    download_url = response_json["link"]["link"]
                break

        logger.info("Downloading model")
        try:
            tarfile_path = wget.download(
                download_url, "model_storage"
            )  # response is the path to the downloaded file
        except Exception as e:
            print(e)
            raise DownloadLinkExpiredError

        logger.info("Extracting model to model_storage folder")
        # Extract the tar file to a folder on the local file system
        with tarfile.open(tarfile_path) as tar:
            tar.extractall(path=f"model_storage/{model_name}/models")

        # delete the tar file
        Path(tarfile_path).unlink()

    logger.info("Pulling image from the server")
    pull_image(
        model_folder_path=f"model_storage/{model_name}/models",
        container_name=f"iris-triton-{experiment_id}",
        job_tag=job_tag,
        task_name=task_name,
        baseline_model_name=baseline_model_name,
    )
    logger.info("All done!")


# --------------------------------------      iris upload     -------------------------------------- #


@auth
def upload(name: str, src: Union[str, Path], art_type: str, description: str):
    """Upload an artefact to the titan hub

    Args:
        name (str): The name of the artefact
        src (Union[str, Path]): The source of the artefact on disk
        art_type (str): The artefact type. Should be either ['model', 'dataset']
        description (str): A short description of the artefact.

    Raises:
        ArtefactNotFoundError: If the path to the artefact doesn't exist.
        UnsafeTensorsError: If the artefact is a model, and the model has not been saved in safetensors format.
    """
    # cast from path to str.
    art_type = str(art_type)
    src = str(src)

    endpoint = "artefact"
    url = urljoin(conf_mgr.runner_url, f"{endpoint}/")
    headers = {"Authorization": f"Bearer {conf_mgr.access_token}"}
    logger.debug(f"Uploading {art_type} from {src} to {url}")

    # todo probably better way to parse filepaths
    # Catches if you accidentally put a tilde in quotes:
    if src[0] == "~":
        src = os.path.expanduser(src)

    if not Path(src).is_dir():
        raise ArtefactNotFoundError(details=src)

    ext = ".tar.gz"
    if art_type == "model":
        namelist = os.listdir(src)
        if False and not any(".safetensors" in Path(x).suffixes for x in namelist):
            raise UnsafeTensorsError()

        if not any("tokenizer" in x for x in namelist):
            raise MissingTokenizerError()

    elif art_type == "dataset":
        print("dataset validation goes here")  # todo
    else:
        raise ArtefactTypeInvalidError

    post_req_data = {
        "name": name,
        "artefact_type": art_type,
        "description": description,
        "ext": ext,
        "src": src,
    }
    logger.debug(f"posting {post_req_data} to {url}")
    post_req_response = requests.post(url=url, headers=headers, data=post_req_data)
    if not post_req_response.ok:
        logger.debug("post unsuccessful")
        raise handle_bad_response(post_req_response, endpoint)
    else:
        logger.debug("post successful")
        data = post_req_response.json()["artefact"]
        art_uuid = data["uuid"]
        endpoint = "artefact/link/" + art_uuid + "/upload"
        url = urljoin(conf_mgr.runner_url, f"{endpoint}")
        logger.debug(f"Getting link from {url}")
        get_link_resp = requests.get(url=url, headers=headers)
        upl_link = get_link_resp.json()["link"]["link"]
        logger.debug(f"got link {upl_link}")

        # todo this is where further format checking would go (e.g. no uploading 10GB files or jpegs...)
        print("Beginning upload...")

    if TQDM:
        hashval, upload_response = upload_from_file(src, upl_link)
    else:
        with tarify(src, mode="w:gz") as f:
            f.seek(0)
            upload_response = requests.put(upl_link, data=f)
            hashval = hashlib.md5(f.getbuffer()).hexdigest()

    if upload_response is not None and upload_response.status_code == 200:
        endpoint = "artefact"
        print(f"Upload Complete -  Validating {art_type} UUID: {art_uuid} ......")
        url = urljoin(conf_mgr.runner_url, f"{endpoint}/{art_uuid}")
        patch_req_response = requests.patch(
            url=url, headers=headers, data={"hashval": hashval}
        )
        if not patch_req_response.ok:
            raise handle_bad_response(patch_req_response, endpoint)
        else:
            print("Upload validated")
    else:
        print("Upload failed")
        print(dump(upload_response))
