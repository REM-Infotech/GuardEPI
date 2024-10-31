from app import app
from configs import debugmode


if __name__ == "__main__":

    app.run("0.0.0.0", 5002, debugmode())
