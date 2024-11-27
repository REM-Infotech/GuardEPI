
from clear import clear

from app import create_app

clear()
flask_app = create_app()
celery_app = flask_app.extensions["celery"]

flask_app.app_context().push()

if __name__ == "__main__":
    flask_app.run(port=5000, debug=True)

# if __name__ == "__main__":

#     port = int(values().get("PORT", 5000))
#     debug = values().get("DEBUG", "False").lower() in ("true", "1", "t", "y", "yes")
#     clear()

#     celery.worker_main(argv=["worker", "--loglevel=info"])

#     if not debug:
#         # with open(".version", "w") as f:
#         #     from app.misc.checkout import checkout_release_tag

#         #     version = checkout_release_tag()
#         #     f.write(version)

#         print("=======================================================\n")
#         print("Executando servidor Flask")
#         # print(f" * Versão: {version}")
#         print(" * Porta: 8000")
#         print("\n=======================================================")

#         server(listen(("localhost", port)), flask_app, log=flask_app.logger)

#     elif debug:
#         print("=======================================================\n")
#         print("Executando servidor Flask")
#         print(" * Porta: 8000")
#         print("\n=======================================================")

#         flask_app.run(port=int(port), debug=debug)
