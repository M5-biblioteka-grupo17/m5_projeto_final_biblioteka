# <h1 align="center"> Projeto BiblioteKa </h1>

## Instruções de inicialização

### Crie o ambiente virtual
```
python -m venv venv
```
### Ative o venv
```bash
# linux:
source venv/bin/activate
# windows (powershell):
.\venv\Scripts\activate
# windows (git bash):
source venv/Scripts/activate
```

### Instale as dependências
```
pip install -r requirements.txt
```
### Execute as migrações
```
python manage.py migrate
```

## Principais Funcionalidades da Aplicação

1. **Empréstimo de Livros**: Cada livro só poderá ser emprestado por um período fixo de tempo.
2. **Devolução de Livros**: 
    * Todos os livros emprestados deverão ter uma data de retorno.
    * Se a data de retorno for sábado ou domingo, modificar para segunda-feira.
    * Caso o estudante não devolva o livro até o prazo estipulado, deverá ser impedido (bloqueado) de solicitar outros empréstimos.
3. **Bloqueio de Novos Empréstimos**: Após completar as devoluções pendentes, o bloqueio deve permanecer por alguns dias.
4. **Usuários**: Deve ser possível cadastrar dois tipos de usuário: *estudante* e *colaborador da biblioteca*. 
5. **Rotas não autenticadas**: Deve ser possível também usuários não autenticados acessarem a plataforma para visualizar informações sobre os livros.
6. **Funcionalidades permitidas aos estudantes**: 
    * Ver seu próprio histórico de livros emprestados.
    * "Seguir" um livro a fim de receber notificações no email conforme a disponibilidade/status do livro.
    * Emprestar livros.
7. **Funcionalidades permitidas aos colaboradores**: 
    * Cadastrar novos livros.
    * Emprestar livros.
    * Verificar o histórico de empréstimo de cada estudante.
    *Verificar status do estudante.

## Tecnologias
* Python/Django
* JWT
* Swagger

## Desenvolvedores
⭐ Maikol Santos 
 * [GitHub](https://github.com/MaikolSantos)
 * [LinkedIn](https://www.linkedin.com/in/maikol-lourencon/)

⭐ Isadora Perdigão 
 * [GitHub](https://github.com/IsadoraPerdigao)
 * [LinkedIn](https://www.linkedin.com/in/doris-perdigao/)

⭐ Paulo Moreno 
 * [GitHub](https://github.com/PauloMorenoD)
 * [LinkedIn](https://www.linkedin.com/in/paulo-moreno-dev-front-end/)

⭐ Joseph Cardoso Vriesman
 * [GitHub](https://github.com/Joseph18CV)
 * [LinkedIn](https://www.linkedin.com/in/joseph-cardoso-vriesman-711103246/)