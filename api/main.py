import os

from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlmodel import *

from api.database import * # from .db import engine, SQLModel

# from api.models import *

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://eng-soft-proj.vercel.app",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def create_users():
    user_1 = User(email="test1@test.com",
                  password_hash="password1",
                  registered_at=datetime.now(),
                  name="Felipe Ribeiro",
                  bio="bio1"
                  )
    
    user_2 = User(email="test2@test.com",
                  password_hash="password2",
                  registered_at=datetime.now(),
                  name="Enzo Koji",
                  bio="bio2"
                  )
    user_3 = User(email="test3@test.com",
                  password_hash="password3",
                  registered_at=datetime.now(),
                  name="Yuri Nichimura",
                  bio="bio3"
                  )

    session = Session(engine)

    session.add(user_1)
    session.add(user_2)
    session.add(user_3)

    session.commit()

def create_groups():
    session = Session(engine)

    group_1 = Group(name="Compiladores",
                    description="Estudo e desenvolvimento de programas que traduzem código-fonte de linguagens de alto nível para código de máquina, envolvendo análise léxica, sintática, semântica e otimização de código.",
                    creation_date=datetime.now(),
                    created_by=session.exec(select(User).order_by(func.random())).first()
                    )
    group_2 = Group(name="Computação Distribuída",
                    description="Exploração de sistemas que dividem tarefas entre múltiplos computadores interconectados, visando aumentar o desempenho, a escalabilidade e a tolerância a falhas.",
                    creation_date=datetime.now(),
                    created_by=session.exec(select(User).order_by(func.random())).first()
                    )
    group_3 = Group(name="Interação Humano-Computador",
                    description="Foco no design, avaliação e implementação de interfaces e sistemas que facilitam a interação eficiente e agradável entre humanos e computadores.",
                    creation_date=datetime.now(),
                    created_by=session.exec(select(User).order_by(func.random())).first()
                    )
    group_4 = Group(name="Engenharia de Software",
                    description="Abordagem sistemática para o desenvolvimento, manutenção e evolução de software de alta qualidade, utilizando metodologias, técnicas e ferramentas específicas.",
                    creation_date=datetime.now(),
                    created_by=session.exec(select(User).order_by(func.random())).first()
                    )
    group_5 = Group(name="Metodologia de Pesquisa em Computação",
                    description="Estudo dos métodos e técnicas para a condução de pesquisas científicas na área de computação, incluindo a formulação de problemas, experimentação e análise de dados.",
                    creation_date=datetime.now(),
                    created_by=session.exec(select(User).order_by(func.random())).first()
                    )
    group_6 = Group(name="Projetos Empreendedores",
                    description="Disciplina voltada ao desenvolvimento de habilidades empreendedoras para a criação e gestão de startups e inovações tecnológicas.",
                    creation_date=datetime.now(),
                    created_by=session.exec(select(User).order_by(func.random())).first()
                    )
    group_7 = Group(name="Teoria dos Grafos",
                    description="Análise e aplicação de grafos como estruturas matemáticas, abordando problemas como caminhos mínimos, árvores geradoras e fluxos em redes.",
                    creation_date=datetime.now(),
                    created_by=session.exec(select(User).order_by(func.random())).first()
                    )

    session.add(group_1)
    session.add(group_2)
    session.add(group_3)
    session.add(group_4)
    session.add(group_5)
    session.add(group_6)
    session.add(group_7)

    session.commit()

# if __name__ == "main": # if __name__ == "__main__":
create_db_and_tables()
# create_users()
create_groups()

@app.get("/")
def healthcheck():
    return {"status": "ok"}