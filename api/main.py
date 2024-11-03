import os

from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlmodel import *

from .database import * # from .db import engine, SQLModel

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
    user_1 = User(email="felipe@mackenzista.com.br",
                  password_hash="password1",
                  registered_at=datetime(2024,9,23,19,20),
                  name="Felipe Ribeiro",
                  bio="Estudante do 6º semestre de Ciência da Computação",
                  )
    
    user_2 = User(email="koji@mackenzista.com.br",
                  password_hash="password2",
                  registered_at=datetime(2024,9,23,19,20),
                  name="Enzo Koji",
                  bio="Estudante do 6º semestre de Ciência da Computação"
                  )
    user_3 = User(email="yuri@mackenzista.com.br",
                  password_hash="password3",
                  registered_at=datetime(2024,9,23,19,20),
                  name="Yuri Nichimura",
                  bio="Estudante do 6º semestre de Ciência da Computação"
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

@app.post("/user/")
def create_user(user: User):
    with Session(engine) as session:
        # TODO: check for existing email

        session.add(user)
        session.commit()
        session.refresh(user)
        return user # TODO: check
    
@app.get("/user/{user_id}")
def get_user_by_id(user_id: int):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.id == user_id)).one()
        return user
    
@app.get("/user/{user_id}/groups/")
def get_groups_by_user_id(user_id: int):
    with Session(engine) as session:
        groups = session.exec(select(Group).where(User.id == user_id)).all() # TODO: fix
        return groups

@app.get("/user/")
def get_all_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users
    
@app.post("/group/")
def create_group(group: Group):
    with Session(engine) as session:
        session.add(group)
        session.commit()
        session.refresh(group)
        return group # TODO: check
    
@app.get("/group/{group_id}")
def get_group_by_id(group_id: int):
    with Session(engine) as session:
        group = session.exec(select(Group).where(Group.id == group_id)).one()
        return group
    
@app.post("/post/")
def create_post(post: Post):
    with Session(engine) as session:
        # TODO: check for existing email

        session.add(post)
        session.commit()
        session.refresh(post)
        return post # TODO: check

@app.get("/post/{post_id}")
def get_post_by_id(post_id: int):
    with Session(engine) as session:
        post = session.exec(select(Post).where(Post.id == post_id)).one()
        return post

@app.delete("/post/{post_id}")
def delete_post_by_id(post_id: int):
    with Session(engine) as session:
        post = session.get(Post, post_id)

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        session.delete(post)
        session.commit()

        return {"ok": True} # TODO: check

@app.post("/post/{post_id}/comment")
def create_comment(post_id: int, comment: Comment):
    comment.post_id = post_id # TODO: check

    with Session(engine) as session:
        session.add(comment)
        session.commit()
        session.refresh(comment)
        return comment
    
@app.get("/post/{post_id}/comment")
def get_comments_by_post_id(post_id: int):
    with Session(engine) as session:
        comments = session.exec(select(Comment).where(Comment.post_id == post_id)).all()
        return comments

@app.delete("/post/{post_id}/comment/{comment_id}") # TODO: check
def delete_comment_by_id(post_id: int, comment_id: int):
    with Session(engine) as session:
        comment = session.get(Comment, comment_id)

        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")

        session.delete(comment)
        session.commit()

        return {"ok": True} # TODO: check

@app.post("/post/{post_id}/like")
def like_post(post_id: int, like: Like):
    like.post_id = post_id # TODO: check

    with Session(engine) as session:
        session.add(like)
        session.commit()
        session.refresh(like)
        return like
    
@app.get("/post/{post_id}/like")
def get_likes_by_post_id(post_id: int):
    with Session(engine) as session:
        likes = session.exec(select(Like).where(Like.post_id == post_id)).all()
        return likes