import argparse
import pathlib

from .logging import get_logger

logger = get_logger("cppygen command")

import toml

from cppygen.cppygen_parser import Parser


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config_file", required=True, type=str, help="Path to config file"
    )

    parser.add_argument(
        "--cwd", required=True, type=str, help="Current Working Directory"
    )

    parser.add_argument(
        "--include_directories",
        required=False,
        type=str,
        help="include_directories for cmake project",
    )

    parser.add_argument(
        "--flags", required=False, type=str, help="flags for cmake project"
    )

    args = parser.parse_args()

    configs = toml.load(args.config_file)
    cwd = pathlib.Path(args.cwd)

    sources = []
    if (config_sources := configs.get("sources")) is None:
        logger.error("Please Specify the sources field in config file")
        exit(1)
    for i in config_sources:
        sources.extend([j for j in cwd.glob(i)])

    headers = []
    if (config_headers := configs.get("headers")) is None:
        logger.error("Please Specify the headers field in config file")
        exit(1)
    for i in config_headers:
        headers.extend([j for j in cwd.glob(i)])

    if (config_output_dir := configs.get("output_dir")) is None:
        logger.error("Please Specify the output_dir field in config file")
        exit(1)
    output_dir = cwd.joinpath(config_output_dir)

    cppygen = Parser(
        namespace=configs.get("search_namespace"),
        library_file=configs.get("libclang_path"),
    )

    flags = configs.get("flags") or []

    for i in configs.get("include_directories") or []:
        flags.append(f"-I{str(cwd.joinpath(i).absolute())}")

    flags.extend([i for i in (args.flags or "").split(";")])
    flags.extend([f"-I{i}" for i in (args.include_directories or "").split(";")])

    for i in sources:
        cppygen.parse_from_file(i, lang="cpp", flags=configs.get("flags") or [])

    for i in headers:
        cppygen.parse_from_file(i, lang="hpp", flags=configs.get("flags") or [])

    for i in configs.get("include_headers") or []:
        cppygen.add_hpp_includes(i)

    with open(str(output_dir) + "/cppygen_generated.hpp", "w") as f:
        f.write(cppygen.hpp_generate())

    with open(str(output_dir) + "/cppygen_generated.cpp", "w") as f:
        f.write(cppygen.cpp_generate())


if __name__ == "__main__":
    run()
