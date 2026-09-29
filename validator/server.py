from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json

from validator import (
    load_yaml,
    validate_configuration,
    generate_variables,
)


CONFIG_FILE = Path("/config/config.yml")
SUPPORTED_FILE = Path("/app/tehnologii-suportate.yml")
OUTPUT_FILE = Path("/output/generated.yml")


class EnvironmentBuilderHandler(BaseHTTPRequestHandler):

    def send_json(self, status_code, data):
        response = json.dumps(data, indent=2)

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response.encode())))
        self.end_headers()

        self.wfile.write(response.encode())

    def do_GET(self):

        if self.path == "/health":
            self.send_json(
                200,
                {
                    "status": "UP",
                    "service": "environment-builder-validator"
                }
            )
            return

        if self.path == "/validate":

            config = load_yaml(CONFIG_FILE)
            supported = load_yaml(SUPPORTED_FILE)

            if config is None or supported is None:
                self.send_json(
                    500,
                    {
                        "status": "FAILED",
                        "message": "Configuratia sau fisierul cu tehnologii suportate nu poate fi citit."
                    }
                )
                return

            errors = validate_configuration(config, supported)

            if errors:
                self.send_json(
                    400,
                    {
                        "status": "FAILED",
                        "errors": errors
                    }
                )
                return

            generate_variables(
                config,
                supported,
                OUTPUT_FILE
            )

            self.send_json(
                200,
                {
                    "status": "PASSED",
                    "message": "Validarea configurarii s-a finalizat cu succes.",
                    "generated_file": str(OUTPUT_FILE)
                }
            )

            return

        self.send_json(
            200,
            {
                "service": "environment-builder-validator",
                "endpoints": [
                    "/health",
                    "/validate"
                ]
            }
        )


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 80), EnvironmentBuilderHandler)

    print("Environment Builder Validator HTTP server started on port 80")

    server.serve_forever()
