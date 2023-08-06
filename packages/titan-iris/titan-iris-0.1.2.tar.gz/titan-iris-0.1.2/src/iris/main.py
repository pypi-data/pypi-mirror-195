"""
This is the main file for the sdk cli. It is responsible for handling the cli commands and passing them to the sdk module.
"""

# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
from typing import List, Optional
from enum import Enum
from pathlib import Path

import typer

import iris.sdk as sdk

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                   sdk CLI Module                                                     #

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

# create the typer object
main = typer.Typer()


@main.command()
def login():
    """Login to the iris client."""
    try:
        user_name = sdk.login()
        print(f"Logged in as {user_name}")
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)


@main.command()
def logout():
    """Logout from the iris client."""
    try:
        logged_out = sdk.logout()
        if logged_out:
            print("Successfully logged out")
        else:
            raise Exception("Failed to logout")
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)


class Task(str, Enum):
    sequence_classification = "sequence_classification"
    glue = "glue"
    question_answering = "question_answering"


class Object(str, Enum):
    experiment = "experiment"
    artefact = "artefact"


class Artefact(str, Enum):
    model = "model"
    dataset = "dataset"


class Task(str, Enum):
    sequence_classification = "sequence_classification"
    glue = "glue"
    question_answering = "question_answering"


class Object(str, Enum):
    experiment = "experiment"
    artefact = "artefact"


class Artefact(str, Enum):
    model = "model"
    dataset = "dataset"


@main.command()
def post(
    model: str = typer.Option(..., "--model", "-m", help="The model to optimize."),
    dataset: str = typer.Option(
        ..., "--dataset", "-d", help="The dataset to optimize the model with."
    ),
    task: Task = typer.Option(
        ..., "--task", "-t", help="The task to optimize the model for."
    ),
    experiment_name: str = typer.Option(
        "",
        "--name",
        "-n",
        help="The name to use for this job. Visible in the titan web interface.",
    ),
    test: bool = typer.Option(
        False,
        "--short-run",
        "-s",
        help="Truncates the run after 1 batch and 1 epoch. Will provide bad results, but useful to check that the model and dataset choices are valid.",
    ),
    num_labels: int = typer.Option(
        None,
        "--num-labels",
        "-nl",
        help="Number of labels. Required for task sequence_classification",
    ),
    text_fields: Optional[List[str]] = typer.Option(
        None,
        "--text-fields",
        "-tf",
        help="Text fields. Required for task sequence_classification",
    ),
    with_negative: bool = typer.Option(
        False,
        "--with-negative",
        "-wn",
        help="With negative. Required for question_answering",
    ),
):
    """Dispatch a job to the titan platform"""
    # get the enum value as task
    task = task.value
    try:
        # baseline flags
        flags = {"model": model, "dataset": dataset, "task": task, "test": test}
        # lots of argument checking
        if experiment_name != "":
            flags.update({"name": experiment_name})
        if task == "sequence_classification":
            # sequence of task specific flags
            # if the flag shouldn't be accepted, set invalid_input=True
            # if it should be, and you want to warn, print, but don't set invalid_input
            invalid_input = False
            if num_labels is None:
                print("Please provide the number of labels (--num-labels, -nl)")
                invalid_input = True
            if text_fields is None:
                print("Please provide the text fields to tokenize (--text-fields, -tf)")
                invalid_input = True
            if with_negative:
                print(
                    "With negative is not necessary for sequence classification tasks"
                )
            if invalid_input:
                raise typer.Abort()
            else:
                flags.update({"num_labels": num_labels, "text_fields": text_fields})
        elif task == "question_answering":
            invalid_input = False
            # sequence of task specific flags
            # if the flag shouldn't be accepted, set invalid_input=True
            # if it should be, and you want to warn, print, but don't set invalid_input
            if num_labels is not None:
                print("num_labels is not necessary for question answering tasks")
            if text_fields is not None:
                print("text_fields is not necessary for question answering tasks")
            if invalid_input:
                raise typer.Abort()
            else:
                flags.update({"version_2_with_negative": with_negative})
        elif task == "glue":
            # sequence of task specific flags
            # if the flag shouldn't be accepted, set invalid_input=True
            # if it should be, and you want to warn, print, but don't set invalid_input
            invalid_input = False
            if num_labels is not None:
                print("num_labels is not necessary for glue tasks")
            if text_fields is not None and text_fields != []:
                print("text_fields is not necessary for glue tasks")
            if with_negative:
                print("With negative is not necessary for glue tasks")
            if invalid_input:
                raise typer.Abort()
            else:
                pass
        else:
            print(f"Unrecognised task {task}")
            raise typer.Abort()
        # post the resulting flags
        sdk.post(**flags)
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)


@main.command()
def get(
    object: Object = typer.Argument("experiment", help="What type of object to get"),
    id: Optional[str] = typer.Option(
        None,
        "--id",
        "-i",
        help="Which object to get. None, or '' correspond to getting all objects. Evaluated server-side.",
    ),
    query: Optional[str] = typer.Option(
        None,
        "--query",
        "-q",
        help="A JMESPath string, to filter the objects returned by the API. Evaluated client-side.",
    ),
):
    """Get objects from the TYTN api."""
    # get the string from the enum
    object = object.value
    try:
        sdk.get(object, id, query)
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)


@main.command()
def pull(
    image: str = typer.Argument(
        ..., help="The image to pull. Should be displayed in the titan web interface."
    )
):
    """Pull the titan-optimized server docker image."""
    try:
        sdk.pull(image)
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)


@main.command()
def upload(
    src: Path = typer.Argument(
        ...,
        help="The location of the artefact on disk. Should be a folder, containing either a model or a dataset. For more information on the supported formats, see the titan documentation.",
    ),
    artefact_type: Artefact = typer.Argument(
        ..., help="The type of artefact to upload."
    ),
    name: str = typer.Argument(
        None, help="The name of the artefact. Displayed in the titan web interface."
    ),
    description: str = typer.Argument(
        None,
        help="A short description of the artefact. Displayed in the titan web interface.",
    ),
):
    """Upload an artefact to the titan hub."""
    artefact_type = artefact_type.value
    try:
        sdk.upload(name, src, artefact_type, description)
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)


@main.command()
def status(
    id: int = typer.Option(
        ..., "--id", "-i", help="The id of the experiment to get the status of"
    )
):
    """Get the status of an experiment"""
    try:
        summary = sdk.get(
            "experiment",
            id,
            "experiment.jobs[*].{name:name, results:results}",
            verbose=False,
        )
        tag_from_name = (
            lambda name: name.partition("-")[0] + ":" + name.rpartition("_")[-1]
        )
        import json

        response = json.loads(summary)["response"]
        for i in range(len(response)):
            response[i]["name"] = tag_from_name(response[i]["name"])
        response = json.dumps(response, indent=4)
        print(response)
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    main()
