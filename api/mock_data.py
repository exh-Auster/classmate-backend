from .database import engine
from .models import *

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

def create_posts():
    session = Session(engine)

    bodies = [
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt.",
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip.",
        "Duis aute irure dolor in reprehenderit, in voluptate velit esse cillum dolore eu fugiat nulla.",
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt.",
        "Mollit anim id est laborum, sed ut perspiciatis unde omnis iste natus error sit voluptatem.",
        "Accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore.",
        "Veritatis et quasi architecto beatae vitae dicta sunt explicabo, nemo enim ipsam voluptatem.",
        "Nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit.",
        "Quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex.",
        "Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit."
    ]

    for i in range(1, 11):
        author_id = (i - 1) % 3 + 1
        group_id = (i - 1) % 7 + 1
        body = bodies[i % 10]

        post = Post(
            author_id=author_id,
            group_id=group_id,
            body=body,
            external_content_url="https://mackenzie.br",
            created_at=datetime.now()
        )

        session.add(post)

    session.commit()