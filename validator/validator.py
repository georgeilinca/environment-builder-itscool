import sys
from pathlib import Path

import yaml


SUPPORTED_FILE = Path(__file__).parent / "tehnologii-suportate.yml"
DEFAULT_CONFIG_FILE = Path(__file__).parent.parent / "config" / "config.yml"
DEFAULT_OUTPUT_FILE = Path(__file__).parent.parent / "generated" / "generated.yml"

def load_yaml(file_path):
    """Incarca si returneaza YAML data dintr-un fisier."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"ERROR: Fisierul nu a fost gasit: {file_path}")
        return None
    except yaml.YAMLError as error:
        print(f"ERROR: Format YAML invalid {file_path}")
        print(error)
        return None


def validate_configuration(config, supported):
    """Valideaza tehnoloiile si versiunile cerute."""
    errors = []

    if not isinstance(config, dict):
        errors.append("Configuratia trebuie sa fie in format YAML valid.")
        return errors

    if "technologies" not in config:
        errors.append("Lipseste campul: technologies")
        return errors

    technologies = config["technologies"]

    if not isinstance(technologies, list):
        errors.append("Campul 'technologies' trebuie sa fie o lista.")
        return errors

    supported_technologies = supported.get("technologies", {})

    seen = set()

    for index, technology in enumerate(technologies, start=1):

        if not isinstance(technology, dict):
            errors.append(
                f"Tehnologia #{index} trebuie sa contina campurile 'name' si 'version'."
            )
            continue

        name = technology.get("name")
        version = technology.get("version")

        if not name:
            errors.append(f"Tehnologia #{index}: lipseste campul 'name'.")
            continue

        if name in seen:
            errors.append(f"Tehnologie duplicata: {name}")
            continue

        seen.add(name)

        if name not in supported_technologies:
            errors.append(f"Tehnologie nesuportata: {name}")
            continue

        if not version:
            errors.append(
                f"Versionea e necesara pentru tehnologia: {name}"
            )
            continue

        supported_versions = supported_technologies[name].get("versions", [])

        if version not in supported_versions:
            errors.append(
                f"Versiune nesuportata pentru tehnologia {name}: {version}. "
                f"Versiuni suportate: {', '.join(supported_versions)}"
            )

    return errors


def generate_variables(config, supported, output_file):
    """Genereaza variabilele folosite ulterior ca input in Ansible."""
    requested = {
        technology["name"]: technology["version"]
        for technology in config["technologies"]
    }

    generated = {
        "technologies": {}
    }

    for name, details in supported["technologies"].items():
        technology_data = {
            "enabled": name in requested
        }

        if name in requested:
            technology_data["version"] = requested[name]

        technology_data["command"] = details["command"]

        generated["technologies"][name] = technology_data

    with open(output_file, "w", encoding="utf-8") as file:
        yaml.safe_dump(
            generated,
            file,
            sort_keys=False
        )


def main():
    config_file = DEFAULT_CONFIG_FILE
    output_file = DEFAULT_OUTPUT_FILE

    args = sys.argv[1:]

    if "--config" in args:
        config_index = args.index("--config")

        if config_index + 1 >= len(args):
            print("ERROR: Optiunea --config necesita o cale catre fisier.")
            return 1

        config_file = Path(args[config_index + 1])

    elif args:
        config_file = Path(args[0])

    if "--output" in args:
        output_index = args.index("--output")

        if output_index + 1 >= len(args):
            print("ERROR: Optiunea --output necesita o cale catre fisier.")
            return 1

        output_file = Path(args[output_index + 1])

    print("============================================")
    print(" Environment Builder - Validare configuratie")
    print("============================================")
    print()
    print(f"Configuratie ceruta: {config_file}")
    print(f"Tehnologii suportate: {SUPPORTED_FILE}")
    print()

    config = load_yaml(config_file)

    if config is None:
        return 1

    supported = load_yaml(SUPPORTED_FILE)

    if supported is None:
        return 1

    errors = validate_configuration(config, supported)

    if errors:
        print("Validarea configurarii a esuat - FAILED.")
        print()

        for error in errors:
            print(f"ERROR: {error}")

        print()
        print("Instalarea nu va porni.")
        return 1

    print("Validarea configurarii a reusit - PASSED.")
    print()

    generate_variables(
        config,
        supported,
        output_file
    )

    print(f"Variabile generate in fisierul: {output_file}")
    print()
    print("Validarea s-a finalizat cu SUCCES.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
