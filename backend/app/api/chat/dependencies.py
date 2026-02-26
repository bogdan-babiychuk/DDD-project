from typing_extensions import Annotated
from fastapi import Depends
from app.application.init import init_container
from app.application.mediator.base import Mediator
from punq import Container


def get_conteiner():
    container = init_container()
    return container

ConteinerDep = Annotated[Container, Depends(get_conteiner)]
