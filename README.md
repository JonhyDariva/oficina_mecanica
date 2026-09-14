ac1 - oficina mecanica

nome: Joao marcos dariva lara
matricula: 202508025582

dominio escolhido

opcao b, oficina mecanica 


para rodar do 0

python -m venv .venv
.venv\Scripts\activate (windows) ou source .venv/bin/activate (linux/mac)
pip install -r requirements.txt
python dados_iniciais.py
python app.py

abrir http://127.0.0.1:5000 no navegador


rotas

GET / - lista todos os veiculos
GET /veiculo/<id> - mostra um veiculo e os servicos relacionados a ele, da 404 se o id nao existir
GET /novo - formulario de cadastro
POST /novo - grava o veiculo e redireciona
GET /veiculo/<id>/editar - formulario preenchido com os dados atuais
POST /veiculo/<id>/editar - GRAVA a alteracao e redireciona
POST /veiculo/<id>/excluir - EXCLUI o veiculo, e os servicos ligados a ele, e redireciona
GET /buscar - BUSCA por placa, marca, modelo ou proprietario


validacoes de erro 

-marca e modelo precisam ter pelo menos 2 caracteres
-ano precisa ser um numero entre 1950 e 2027
-nome do proprietario precisa ter pelo menos 2 caracteres
-placa precisa bater com o formato antigo (abc1234) ou mercosul (abc1d23)
-regra que consulta o banco: nao deixa cadastrar duas placas iguais, verifica no banco antes de gravar e mostra mensagem
-quando algum campo ta errado o formulario volta com a mensagem de erro, sem gravar nada no banco.


o que ficou faltando

-o cadastro de servico e feito so pelo dados_iniciais.py, nao tem rota propria pra cadastrar servico pelo navegador ainda. os servicos aparecem normal na pagina de detalhe do veiculo, so nao da pra adicionar um novo por ali.
