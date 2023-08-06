# SPDX-FileCopyrightText: 2022 Freemelt AB <opensource@freemelt.com>
#
# SPDX-License-Identifier: Apache-2.0
# type: ignore
"""Command-line interface for obflib."""
import json
import pathlib
import traceback
import sys
from typing import List
import webbrowser
import zipfile

import click
import yaml

import obflib
from obflib.message_handler import MessageDict


@click.group()
@click.version_option()
@click.option("-q", "--quiet", is_flag=True, default=False, help="Suppress all output.")
@click.pass_context
def main(ctx: click.Context, quiet: bool) -> None:
    """Command-line interface for obflib."""
    ctx.ensure_object(dict)
    ctx.obj["quiet"] = quiet


def _present_human_readable(filename: click.Path, messages: obflib.OBFMessages) -> None:
    if messages.errors:
        click.secho(f"ERRORS in {filename}:", fg="red")
        _print_messages(messages.errors, "red")

    if messages.errors and messages.warnings:
        click.echo()

    if messages.warnings:
        click.secho(f"Warnings in {filename}:", fg="yellow")
        _print_messages(messages.warnings, "yellow")

    if messages.errors or messages.warnings:
        click.echo()
    if messages.is_valid():
        click.secho(f"The file {filename} appears to be a valid OBF file.", fg="green")
    else:
        click.secho(f"The file {filename} is not a valid OBF file.", fg="red")


def _print_messages(message_subset: MessageDict, color: str) -> None:
    for key, key_messages in message_subset.items():
        for message in key_messages:
            if key != "":
                click.secho(f"{key}: ", nl=False, fg=color)
            click.secho(message, fg=color)


@main.command()
@click.argument("filename", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "-j",
    "--json",
    "presentation",
    flag_value="json",
    help="Output summary in JSON format for machine consumption.",
)
@click.option(
    "-h",
    "--human",
    "presentation",
    flag_value="text",
    default=True,
    help="(Default) Output summary in text format for human consumption.",
)
@click.option("-q", "--quiet", is_flag=True, default=False, help="Suppress all output.")
@click.pass_context
def verify(ctx: click.Context, presentation: str, quiet: bool, filename: click.Path) -> None:
    """Verify an OBF file according to the specification."""
    try:
        messages = obflib.verify(str(filename))
    except Exception:  # pylint: disable=broad-except
        traceback.print_exc()
        ctx.exit(-1)

    if not (ctx.obj["quiet"] or quiet):
        if presentation == "json":
            click.echo(messages.to_json(indent=2))
        elif presentation == "text":
            _present_human_readable(filename, messages)

    if messages.is_valid():
        ctx.exit(0)
    else:
        ctx.exit(1)


@main.command()
@click.argument("input_dir", type=click.Path(exists=True, dir_okay=True))
@click.argument("output_obf", type=click.Path())
@click.option(
    "-b",
    "--bob-script",
    "bob_scripts",
    default=None,
    metavar="<name>=<path>",
    help="Specify lua file(s) to use as BOB script. Can be provided multiple times.",
    type=str,
    multiple=True,
)
@click.option(
    "-n",
    "--name",
    default=None,
    help="Specify the name to use for the generated OBF. "
    "Defaults to OUTPUT_OBF without file extension.",
    type=str,
)
@click.pass_context
def convert(  # noqa: C901
    ctx: click.Context, input_dir: str, output_obf: str, bob_scripts: List[str], name: str
):  # pylint: disable=too-many-locals,too-many-statements
    """Convert a directory of BOSS files to an OBF (PoC).

    PROOF OF CONCEPT -- NOT PRODUCTION READY.
    """
    # TODO: move this function to converter.py
    # TODO: validate input files

    try:
        input_path = pathlib.Path(input_dir)
        yaml_files = list(input_path.glob("*.yaml")) + list(input_path.glob("*.yml"))
        if len(yaml_files) != 1:
            raise ValueError(
                f"Expected exactly one yaml file in input directory, found {yaml_files}"
            )

        with open(yaml_files[0]) as build_yaml:
            boss_data = yaml.safe_load(build_yaml)

        obf_name = name or pathlib.Path(output_obf).stem
        click.echo(f"Using name '{obf_name}'")

        manifest = {
            "obfFormatVersion": "1.0",
            "name": obf_name,
            "version": "1.0",
            "author": "obftool",
            "description": "Converted from BOSS yaml with obftool",
            "buildInfo": "buildInfo.json",
            "buildProcessors": "buildProcessors/buildProcessors.json",
            "machineCapabilities": "machineCapabilities.json",
            "modules": {},
        }

        if bob_scripts:
            build_script_mapping = {}
            for bob_script in bob_scripts:
                script_name, path = bob_script.split("=")

                click.secho(f"Using build script '{path}' as '{script_name}'")
                build_script_mapping[script_name] = pathlib.Path(path)
        else:
            try:
                import luabob  # pylint: disable=import-outside-toplevel
            except ImportError:
                click.secho(
                    "ERROR: Lua-BOB example scripts were not found. "
                    "Please specify bob scripts manually with --bob-script.",
                    fg="red",
                )
                sys.exit(1)

            build_script_mapping = {
                "bob": pathlib.Path(luabob.__file__).parent / "example_scripts" / "bob.lua",
                "old-bob": pathlib.Path(luabob.__file__).parent / "example_scripts" / "old-bob.lua",
            }

        build_processors_info = {
            "buildProcessors": {
                script_name: {
                    "type": "lua-bob",
                    "version": "1.0",
                    "entryPoint": f"buildProcessors/bob/{script_name}.lua",
                }
                for script_name in build_script_mapping
            }
        }

        boss_start_heat = boss_data["build"]["start_heat"]
        boss_preheat = boss_data["build"]["preheat"]
        boss_postheat = boss_data["build"]["postheat"]
        build_info = {
            "files": {
                "startHeat": f"obp/{pathlib.PurePath(boss_start_heat['file']).name}",
                "layerPreHeat": f"obp/{pathlib.PurePath(boss_preheat['file']).name}",
                "layerPostHeat": f"obp/{pathlib.PurePath(boss_postheat['file']).name}",
            },
            "global": {
                "layerfeed": boss_data["build"]["layerfeed"],
                "startHeat": {
                    "file": "startHeat",
                    "temperatureSensor": boss_start_heat["temp_sensor"],
                    "targetTemperature": boss_start_heat["target_temperature"],
                    "timeout": boss_start_heat["timeout"],
                },
                "layerPreHeat": {
                    "file": "layerPreHeat",
                    "repetitions": boss_preheat["repetitions"],
                },
                "layerPostHeat": {
                    "file": "layerPostHeat",
                    "repetitions": boss_postheat["repetitions"],
                },
            },
            "layers": [],
        }

        while len(build_info["layers"]) < boss_data["build"]["build"]["layers"]:
            for boss_layer in boss_data["build"]["build"]["files"]:
                if len(build_info["layers"]) >= boss_data["build"]["build"]["layers"]:
                    break

                files = boss_layer if isinstance(boss_layer, list) else [boss_layer]
                layer = {"patternOrder": []}

                for file in files:
                    file_stem = pathlib.PurePath(file).stem
                    filename = pathlib.PurePath(file).name

                    # TODO: make this more robust. For now it will fail if the input points to
                    #  several files with the same name but in different directories,
                    #  or several files with the same name but different extension
                    build_info["files"][file_stem] = f"obp/{filename}"
                    layer["patternOrder"].append(file_stem)

                build_info["layers"].append(layer)

        machine_capabilities_info = {
            "buildModule": {"tankSize": 0, "platform": {}},
            "meltSystem": {"beamPower": 0, "beamSize": 0, "beamSpeed": 0},
            "software": {},
            "turnaroundStation": {},
        }

        obp_files = input_path.glob("*.obp")

        with zipfile.ZipFile(output_obf, "w", compression=zipfile.ZIP_DEFLATED) as obf:
            obf.writestr("manifest.json", json.dumps(manifest, indent=2))
            obf.writestr(
                "buildProcessors/buildProcessors.json", json.dumps(build_processors_info, indent=2)
            )

            for script_name, script_path in build_script_mapping.items():
                obf.writestr(f"buildProcessors/bob/{script_name}.lua", script_path.read_text())

            obf.writestr("buildInfo.json", json.dumps(build_info, indent=2))
            obf.writestr(
                "machineCapabilities.json", json.dumps(machine_capabilities_info, indent=2)
            )
            for obp in obp_files:
                click.echo(f"Adding obp: {obp}")
                with obf.open(f"obp/{obp.name}", "w") as output_obp, open(obp, "rb") as input_obp:
                    output_obp.write(input_obp.read())

        click.secho(f"Done! Wrote OBF to '{output_obf}'.", fg="green")

    except Exception:  # pylint: disable=broad-except
        traceback.print_exc()
        return ctx.exit(-1)


@main.command()
@click.pass_context
def api_docs(ctx: click.Context):
    """Open documentation for Python API in a browser."""
    api_docs_path = "/usr/share/doc/python3-obflib/index.html"
    if not pathlib.Path(api_docs_path).exists():
        click.echo("No API documentation seems to be installed.")
        ctx.exit(1)
    if not webbrowser.open(f"file://{api_docs_path}"):
        click.echo("Could not open browser.")
        ctx.exit(1)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
