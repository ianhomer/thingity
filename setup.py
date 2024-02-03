from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="thingity",
    version="0.0.1",
    description="Todo and thing management",
    packages=["thingity"],
    entry_points={
        "console_scripts": [
            "todo=thingity.cli.todo:run",
            "thing=thingity.cli.thing:run",
            "things=thingity.cli.things:run",
            "things-search=thingity.cli.search:run",
            "things-with-modified=thingity.cli.withModified:run",
        ]
    },
    install_requires=required
)
