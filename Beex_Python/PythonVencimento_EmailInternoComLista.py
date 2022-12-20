# This Python file uses the following encoding: ISO-8859-1
from datetime import datetime
from datetime import timedelta
import pymongo

import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Variaveis globais - pesquise sobre Global variables
host=""
port=0;
user=""
password=""
emailFrom=""
importantFlag=False

# Array - pesquise sobre array in Python
#emailToArray=["magnobrasil2013@gmail.com"]
emailToArray=["jvvleite@gmail.com", "magnobrasil2013@gmail.com", "contato@beextrading.com"]
#emailToArray=["magnobrasil2013@gmail.com", "contato@beextrading.com"]

numberDaysToValidate = 7

# data e hora de hoje
today = datetime.now()  
# data e hora do dia atual mais o numero de dias em numberDaysToValidate
dueDate = datetime.now() + timedelta(days=numberDaysToValidate)

# Funcao - Preenche variaveis para configuracao do email.
def preencheConfiguracoesEmail():
    # Configuração
    global host
    global port
    global user
    global password
    global emailFrom
    #USAR UM SERVIDOR DE UM EMAIL SEU, PEGUE ISSO NA CONFIGURACAO DO SEU PROVEDOR DE EMAIL
    host = "mail.beextrading.com"  # Eh algo mais ou menos neste formato: mail.beextrading.com
    #USAR UM SERVIDOR DE UM EMAIL SEU, PEGUE ISSO NA CONFIGURACAO DO SEU PROVEDOR DE EMAIL    
    port = 587
    #USAR AQUI O EMAIL        
    user = "contato@beextrading.com"
    password = "BeeX2021@"
    emailFrom= "contato@beextrading.com"

# Funcao - Cria conexao com o banco de dados, especifico para o Mongo
def criaConexaoMongoDB():
    # i have updated and included the complete code 
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["development"] # your database name
    clients = db['pedidos']
    try:
        db.validate_collection("pedidos")  # Try to validate a collection
    except pymongo.errors.OperationFailure:  # If the collection doesn't exist
        print("Esta colecao clients nao existe")    
        raise SystemExit(0);
    
    return clients

# Funcao - Pesquisa os cliente no banco da dados que estao com vencimentos proximos
def pesquisaClientesParaVencer(clients):
    #Primeira parte em json do comando find eh usada para o filtro, e a segunda parte depois da virgula eh usada para os campos que serao apresentados, 0 ocultar, 1 apresentar
    #resultQuery = clients.find({'cliente.ativoAte':{'$gte': today, '$lt': dueDate}}, {"_id": 1, "nome": 1, "cliente.dadosPessoais.email": 1, "cliente.ativoAte": 1, "plano": 1}).sort("cliente.ativoAte")    resultQuery = clients.find({'cliente.ativoAte':{'$gte': today, '$lt': dueDate}}, {"_id": 1, "nome": 1, "cliente.dadosPessoais.email": 1, "cliente.ativoAte": 1, "plano": 1}).sort("cliente.ativoAte")
    #resultQuery = clients.find({'cliente.ativoAte':{'$gte': today, '$lt': dueDate}}, {"_id": 1, "nome": 1, "cliente.dadosPessoais.email": 1, "cliente.ativoAte": 1, "plano": 1}).sort("cliente.ativoAte")
    
    
    #resultQuery = clients.find({'dataTermino':{'$gte': str(today), '$lt': str(dueDate)}})
    pipeline = [
        {
            '$match': {
                'dataTermino': {
                    '$gte': str(today), 
                    '$lt': str(dueDate)
                }
            }
        }, {
            '$lookup': {
                'from': 'planoperiodos', 
                'let': {
                    'duracao_plano_': '$duracaoPlano', 
                    'plano_': '$plano'
                }, 
                'pipeline': [
                    {
                        '$match': {
                            '$expr': {
                                '$and': [
                                    {
                                        '$eq': [
                                            '$plano', '$$plano_'
                                        ]
                                    }, {
                                        '$eq': [
                                            '$periodicidade', '$$duracao_plano_'
                                        ]
                                    }
                                ]
                            }
                        }
                    }
                ], 
                'as': 'planoPeriodos_'
            }
        }, {
            '$lookup': {
                'from': 'planos', 
                'localField': 'plano', 
                'foreignField': '_id', 
                'as': 'plano_'
            }
        }, {
            '$lookup': {
                'from': 'clientes', 
                'localField': 'cliente', 
                'foreignField': '_id', 
                'as': 'cliente_'
            }
        }
    ]

    resultQuery = clients.aggregate(pipeline)

    #working = resultQuery = clients.find({'duracaoPlano':'anual'},{"_id": 1}).sort('dataTermino')        
    resultList = list(resultQuery)
    return resultList

# Funcao - Envia Emails
def enviaEmail():
    importantText=''

    # preenche informacoes para envio do email
    preencheConfiguracoesEmail()

    # Criando objeto
    print('')    
    print('  Criando objeto servidor...')
    server = smtplib.SMTP(host, port)

    # Login com servidor
    print('  Login...')
    server.ehlo()
    server.starttls()
    server.login(user, password)

    for i in emailToArray:
        # Criando mensagem
       
        print('')        
        print('    Criando mensagem para ' + i)
        email_msg = MIMEMultipart()
        email_msg['From'] = user
        email_msg['To'] = i
        if importantFlag:
            importantText="IMPORTANT"
        
        email_msg['Subject'] = importantText + ' Beex - Clientes com vencimento de plano até ' + f"{str(dueDate.day):>02}" + "/" + f"{str(dueDate.month):>02}" + "/" + str(dueDate.year)
            
        #print('Adicionando texto...')
        email_msg.attach(MIMEText(msgBody, 'plain'))


#Parte abaixo aqui funciona perfeitamente colocando o attachment. FAzer a logica para mandar arquivo para cada cliente
        filename = "C:/Users/Administrator/Desktop/Beex_All_Plans_QrCode/Green_Mensal.jpeg"  # In same directory as script

        # Open PDF file in binary mode
        #with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
        #    part = MIMEBase("application", "octet-stream")
        #    part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
        #encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        #part.add_header(
        #    "Content-Disposition",
        #    f"attachment; filename= {filename}",
        #)

        # Add attachment to message and convert message to string
        #email_msg.attach(part)
#Parte acima aqui funciona perfeitamente colocando o attachment. FAzer a logica para mandar arquivo para cada cliente



        # Enviando mensagem
        # print('Enviando mensagem para ' + i)
        server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())
        print('    Mensagem enviada!')
        print('')        
    server.quit()

# Funcao - Cria o corpo da mensagem
def criaMensagemCorpoEmail(resultList):
    msgBody=""
    # se o tamanho de result list for igual a zero, significa que nao trouxe ninguem com a data para vencer em N dias
    if len(resultList)==0:
        msgBody="Nenhum cliente com vencimento dentro deste periodo."
        print("  Nenhum cliente com vencimento dentro deste periodo.")
    else:
        msgBody = "  CLIENTES COM VENCIMENTO entre HOJE " + f"{today.day:>02}" + "/" + f"{today.month:>02}" + "/" + str(today.year) + " e " + str(numberDaysToValidate) + " DIAS do dia de hoje " + f"{str(dueDate.day):>02}" + "/" + f"{str(dueDate.month):>02}" + "/" + str(dueDate.year) + "\r\n"
        # faz um looping em todos os resultados preenchendo a variavel msgBody com a mensagem final para o cliente
        for x in resultList:    
            # concatena todos os fields para montar mensagem para o cliente por email
            # Original- funcionando UM somente - msgBody = msgBody + "  " +str(x['_id']) + " - " + f"{str(x['nome']):<40}" + " - " + f"{str(x['cliente']['dadosPessoais']['email']):<40}" + " - Vencimento: " + f"{str(x['cliente']['ativoAte'].day):>02}" + "/" + f"{str(x['cliente']['ativoAte'].month):>02}" + "/" + str(x['cliente']['ativoAte'].year) + " - " + x['plano'] + "\r\n"
            #msgBody = msgBody + "  " +str(x['_id']) + " - " + f"{str(x['cliente_'][0]['nome']):<40}" + " - " + f"{str(x['cliente_'][0]['email']):<40}" + " - Vencimento: " + f"{str(x['dataTermino'].day):>02}" + "/" + f"{str(x['dataTermino'].month):>02}" + "/" + str(x['dataTermino'].year) + " - " + x['plano'][0]['nome'] +  "\r\n"
            msgBody = msgBody + "  " +str(x['_id']) + " - " + f"{str(x['cliente_'][0]['nome']):<40}" + " - " + f"{str(x['cliente_'][0]['email']):<40}" + " - Vencimento: " + str(x['dataTermino']) + " - " + x['plano_'][0]['nome'] +  "\r\n"
            global importantFlag
            importantFlag=True
    return msgBody

# Funcao - Apresenta simplesmente a mensagem do email para o console
def apresentaMensagemConsoleInicio():
    print("");
    print("********************************************************************************************************")    
    print("************************************************* LISTA ************************************************")
    #print("  CLIENTES COM VENCIMENTO entre HOJE",f"{today.day:>02}","/",f"{today.month:>02}","/",today.year,"e ",numberDaysToValidate," DIAS do dia de hoje",f"{str(dueDate.day):>02}","/",f"{str(dueDate.month):>02}","/",str(dueDate.year))

def apresentaMensagemEnviandoEmail():
    print("********************************************************************************************************")    
    print("  Enviando email de alerta:")
    print("********************************************************************************************************")

def apresentaMensagemConsole(msgBody):
    print("")
    print(str(msgBody))

def apresentaMensagemConsoleFim():
    print("********************************************************************************************************")
    print("*************************************************  FIM  ***************************************************")

if today.weekday() > 4:
    print('Hoje eh fim de semana, nao enviar mensagem!')
    raise SystemExit(0);  # Finalizar programa aqui

# chama funcao e recebe como retorno clients
clients = criaConexaoMongoDB()

# chama funcao passando clients e recebe o resultado em como List (nao como cursor, nao como dict)
resultList = pesquisaClientesParaVencer(clients)


print("Result List = " + str(resultList));



# chama funcao passando resultList e recebe o corpo da mensagem
msgBody = criaMensagemCorpoEmail(resultList)

# chama funcao para apresentar mensagem inicial na tela
apresentaMensagemConsoleInicio()

# chama funcao para apresentar mensagem na tela
apresentaMensagemConsole(msgBody)

# chama funcao para apresentar mensagem enviando email na tela
apresentaMensagemEnviandoEmail()

# chama funcao para enviar email, existe um array de email, quantos emails tiverem nesse array receberao a mensagem
enviaEmail()

# chama funcao para apresentar mensagem final na tela
apresentaMensagemConsoleFim()

