# This Python file uses the following encoding: ISO-8859-1
from datetime import datetime
from datetime import timedelta
from datetime import date
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
#prefixFilename = "C:/Users/MagnodaSilvaLeite(t2/AppData/Local/Temp/"
prefixFilename = "C:/Windows/Temp/"
                  


# Array - pesquise sobre array in Python
#emailToArray=["magnobrasil2013@gmail.com"]
emailToArray=["jvvleite@gmail.com","magnobrasil2013@gmail.com","contato@beextrading.com"]
#emailToArray=["jvvleite@gmail.com", "magnobrasil2013@gmail.com", "contato@beextrading.com"]
#emailToArray=["magnobrasil2013@gmail.com", "contato@beextrading.com"]

numberDaysToValidate = 7

# data e hora de hoje
today = datetime.now()  
# data e hora do dia atual mais o numero de dias em numberDaysToValidate
dueDate = datetime.now() + timedelta(days=numberDaysToValidate)

print("Today: ",today)
print("Termino: ", dueDate)


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
    
    # pipeline = [
        # {
            # '$project':
            # {
            
                # 'dataTermino1': {
                    # '$dateFromString': {
                        # 'dateString': '$dataTermino'
                    # }
                # },
                # 'dataEmailCobranca1': {
                    # '$dateFromString': {
                        # 'dateString': '$dataEmailCobranca'
                    # }
                # },
            # }
        # },
        # {
            # '$match': {
                # # 'fieldMath':{
                    # # "$gt": 0
                # # },   
                # 'dataTermino': {
                    # '$gte': str(today), 
                    # '$lt': str(dueDate)
                # },
                
                # 'dataEmailCobranca': {
                    # '$lt': '$dataTermino1'
                # },
                
                # #'$or': [
                # #    { 'dataEmailCobranca': {'$lt': str(today)} },  
                # #    { 'dataEmailCobranca': { '$exists': True } },
                # #    { 'dataEmailCobranca': { '$exists': False } }
                # #],
                # 'plataformaDePagamento':'PIX'
            # }
        # }, 
        # {
            # '$lookup': {
                # 'from': 'planoperiodos', 
                # 'let': {
                    # 'duracao_plano_': '$duracaoPlano', 
                    # 'plano_': '$plano'
                # }, 
                # 'pipeline': [
                    # {
                        # '$match': {
                            # '$expr': {
                                # '$and': [
                                    # {
                                        # '$eq': [
                                            # '$plano', '$$plano_'
                                        # ]
                                    # }, {
                                        # '$eq': [
                                            # '$periodicidade', '$$duracao_plano_'
                                        # ]
                                    # }
                                # ]
                            # }
                        # }
                    # }
                # ], 
                # 'as': 'planoPeriodos_'
            # }
        # }, {
            # '$lookup': {
                # 'from': 'planos', 
                # 'localField': 'plano', 
                # 'foreignField': '_id', 
                # 'as': 'plano_'
            # }
        # }, {
            # '$lookup': {
                # 'from': 'clientes', 
                # 'localField': 'cliente', 
                # 'foreignField': '_id', 
                # 'as': 'cliente_'
            # }
        # }        
    # ]
    

    # Primeira duas partes com dataTermino1 e dataEmailCobranca1 funcionam bem.. 'a' nao.
    # pipeline = [
        # {
            # '$project':
            # {
                # 'dataTermino1':{
                    # '$dateSubtract': {
                        # 'startDate': {
                            # '$dateFromString': {
                                # 'dateString': '$dataTermino'
                            # }
                        # },
                        # 'unit': 'day',
                        # 'amount': 1
                    # }
                # }
            # }
        # }
    # ]   





   
    # Primeira duas partes com dataTermino1 e dataEmailCobranca1 funcionam bem.. 'a' nao.
    # pipeline = [
        # {
            # '$project':
            # {
            
                # 'dataTermino1': { 
                  # '$toDate': '$dataTermino' 
                # },
                # 'dataEmailCobranca1': { 
                  # '$toDate': '$dataEmailCobranca' 
                # },
            
                # 'a':{
                    # '$dateDiff':
                    # {
                        # 'startDate': '$dataTermino1',
                        # 'endDate': '$dataEmailCobranca1',
                        # 'unit': 'day'
                    # }
                # }
            # }
        # }
    # ]
    
    
    
    
    
    # Primeira duas partes com dataTermino1 e dataEmailCobranca1 funcionam bem.. 'a' nao.
    # pipeline = [
        # {
            # '$project':
            # {
            
                # 'dataTermino1': {
                    # '$dateFromString': {
                        # 'dateString': '$dataTermino'
                    # }
                # },
                # 'dataEmailCobranca1': {
                    # '$dateFromString': {
                        # 'dateString': '$dataEmailCobranca'
                    # }
                # },
            
                # 'a':{
                    # '$dateDiff':
                    # {
                        # 'startDate': '$dataTermino1',
                        # 'endDate': '$dataEmailCobranca1',
                        # 'unit': 'day'
                    # }
                # }
            # }
        # }
    # ]
    
    
    # pipeline = [
        # {
            # '$project':
            # {
               # 'location': 1,
               
                # 'born': {
                    # '$dateFromString': {
                        # 'dateString': '$dataTermino'
                    # }
                # },
               
                # 'days':{
                    # '$dateToString':{
                        # 'format': '%Y-%m-%d',
                        # 'date':{
                            # '$dateSubtract':{
                               # 'startDate': '$born',
                               # 'unit': 'day',
                               # 'amount': 1,
                               # 'timezone': '$location'
                            # }
                        # }
                    # }
                # }
            # }
        # }
    # ]


    # pipeline = [
        # {
            # '$project': {
                # 'dataTerminoSubtracted1':{
                    # '$dateToString':{
                        # 'format': '%Y-%m-%d',
                        # 'date': {
                            # '$dateSubtract': {
                                # 'startDate': {
                                    # '$dateFromString': {
                                        # 'dateString': '$dataTermino'
                                    # }
                                # },
                                # 'unit': 'day',
                                # 'amount': 7
                            # }
                        # }
                    # }
                # }
                # ,
                # 'dataTermino': '$dataTermino',
                # 'dataEmailCobranca': '$dataEmailCobranca',
                # 'plataformaDePagamento': '$plataformaDePagamento',
                # 'duracaoPlano': '$duracaoPlano',
                # 'cliente':'$cliente',
                # 'plano': '$plano'
                
            # }
        # },
        # {
            # '$match': {  
                
                # # 'dataTermino': {
                    # # '$gte': str(today), 
                    # # '$lt': str(dueDate)
                # # }, 
                
                # 'dataTerminoSubtracted1':'$dataTerminoSubtracted1',
                
                # # 'dataEmailCobranca1':{
                    # # '$lt': '$dataTerminoSubtracted'
                # # },
                
                # # 'dataEmailCobranca': {
                    # # '$lt': str(today)
                # # },
                

            # }
        # }        
    # ]




    # Funcionando perfeitamento aqui
    # pipeline = [
        # {
            # '$project': {
                # 'dataTerminoSubtracted': {
                    # '$dateSubtract': {
                        # 'startDate': {
                            # '$dateFromString': {
                                # 'dateString': '$dataTermino'
                            # }
                        # },
                        # 'unit': 'day',
                        # 'amount': 1
                    # }
                # },
                # 'dataTermino': '$dataTermino',
                # 'dataEmailCobranca': '$dataEmailCobranca',
                # 'plataformaDePagamento': '$plataformaDePagamento',
                # 'duracaoPlano': '$duracaoPlano',
                # 'cliente':'$cliente',
                # 'plano': '$plano'
            # }
        # }
    # ]
    
    #Funciona perfeitamente usar este, data em string como deve ser
    # pipeline = [
        
        # {
            # '$project': {
                # 'dataTerminoSubtracted7':{
                    # '$dateToString':{
                        # 'format': '%Y-%m-%d',
                        # 'date': {
                            # '$dateSubtract': {
                                # 'startDate': {
                                    # '$dateFromString': {
                                        # 'dateString': '$dataTermino'
                                    # }
                                # },
                                # 'unit': 'day',
                                # 'amount': 7
                            # }
                        # }
                    # }
                # }
                # ,
                # 'dataTermino': '$dataTermino',
                # 'dataEmailCobranca': '$dataEmailCobranca',
                # 'plataformaDePagamento': '$plataformaDePagamento',
                # 'duracaoPlano': '$duracaoPlano',
                # 'cliente':'$cliente',
                # 'plano': '$plano'
                
            # }
        # }
    # ]    
    
    
    #resultQuery = clients.find({'dataTermino':{'$gte': str(today), '$lt': str(dueDate)}})
    pipeline = [
        {
            '$project': {
                'dataTerminoSubtracted': {
                    '$dateSubtract': {
                        'startDate': {
                            '$dateFromString': {
                                'dateString': '$dataTermino'
                            }
                        },
                        'unit': 'day',
                        'amount': 1
                    }
                },            
                'dataTerminoSubtracted7':{
                    '$dateToString':{
                        'format': '%Y-%m-%d',
                        'date': {
                            '$dateSubtract': {
                                'startDate': {
                                    '$dateFromString': {
                                        'dateString': '$dataTermino'
                                    }
                                },
                                'unit': 'day',
                                'amount': 7
                            }
                        }
                    }
                }
                ,
                'valorPago': '$valorPago',
                'dataTermino': '$dataTermino',
                'dataEmailCobranca': '$dataEmailCobranca',
                'plataformaDePagamento': '$plataformaDePagamento',
                'duracaoPlano': '$duracaoPlano',
                'cliente':'$cliente',
                'plano': '$plano'
                
            }
        },        
        {
            '$match': {   
                'dataTermino': {
                    '$gte': str(today), 
                    '$lt': str(dueDate)
                }, 
                'plataformaDePagamento': { 
                    '$in': ['PIX','Transferencia'] 
                }
                
                #'plataformaDePagamento':'PIX'
                # 'dataEmailCobranca':{
                    # '$lt': str('dataTerminoSubtracted')
                # },
                
                # 'dataEmailCobranca': {
                    # '$lt': str(today)
                # },
                
                #'$or': [
                #    { 'dataEmailCobranca': {'$lt': str(today)} },  
                #    { 'dataEmailCobranca': { '$exists': True } },
                #    { 'dataEmailCobranca': { '$exists': False } }
                #],
                
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


# Format date in this from this format (yyyy-mm-dd to dd de mes de yyyy)
def formatMesPorExtenso(mes):
    mes_ext = {1: 'janeiro', 2 : 'fevereiro', 3: 'março', 4: 'abril', 5: 'maio', 6: 'junho', 7: 'julho', 8: 'agosto', 9: 'setembro', 10: 'outubro', 11: 'novembro', 12:'dezembro'}
    return mes_ext[int(mes)]

# Funcao - Envia Emails
def enviaEmail(email, msgBody, urlQrCode, dataTerminoPorExtenso):
    importantText=''

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
        # Criando mensagem para todos os emails INTERNOS da Beex ou privado dos empregados contando no array emailToArray.
       
        print('')        
        print('    Criando mensagem para ' + i)
        email_msg = MIMEMultipart()
        email_msg['From'] = user
        email_msg['To'] = i
        if importantFlag:
            importantText="IMPORTANT"
        
        #email_msg['Subject'] = importantText + ' Beex - Vencimento de plano dia ' + f"{str(dueDate.day):>02}" + "/" + f"{str(dueDate.month):>02}" + "/" + str(dueDate.year)

        email_msg['Subject'] = importantText + ' Beex - Vencimento de plano dia ' + dataTerminoPorExtenso

        #print('Adicionando texto...')
        #email_msg.attach(MIMEText(msgBody, 'plain'))
        email_msg.attach(MIMEText(msgBody, 'html'))

#Parte abaixo aqui funciona perfeitamente colocando o attachment. FAzer a logica para mandar arquivo para cada cliente
        #filename = "C:/Users/Administrator/Desktop/Beex_All_Plans_QrCode/Green_Mensal.jpeg"  # In same directory as script
        filename = urlQrCode
        filename = prefixFilename + urlQrCode

        print("File name = " + filename)

        # Open PDF file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        # Add attachment to message and convert message to string
        email_msg.attach(part)
        #Parte acima aqui funciona perfeitamente colocando o attachment. FAzer a logica para mandar arquivo para cada cliente

        # Enviando mensagem
        # print('Enviando mensagem para ' + i)
        server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())
        print('    Mensagem enviada!')
        print('')     

    #Daqui para baixo mensagem para o cliente
    print('')        
    print('    Criando mensagem para ' + email)
    email_msg = MIMEMultipart()
    email_msg['From'] = user
    email_msg['To'] = email
    if importantFlag:
        importantText="IMPORTANTE"
    
    #email_msg['Subject'] = importantText + ' Beex - Vencimento de plano ' + f"{str(dueDate.day):>02}" + "/" + f"{str(dueDate.month):>02}" + "/" + str(dueDate.year)
    email_msg['Subject'] = importantText + ' Beex - Vencimento de plano ' + dataTerminoPorExtenso
      
        
    html = "<b>test_body</b>"    
        
    #print('Adicionando texto...')
    #email_msg.attach(MIMEText(msgBody, 'plain'))
    email_msg.attach(MIMEText(msgBody, 'html'))


#Parte abaixo aqui funciona perfeitamente colocando o attachment. FAzer a logica para mandar arquivo para cada cliente
    #filename = "C:/Users/Administrator/Desktop/Beex_All_Plans_QrCode/Green_Mensal.jpeg"  # In same directory as script
    filename = urlQrCode
    filename = prefixFilename + urlQrCode

    print("File name = " + filename)

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("image", "jpeg")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    email_msg.attach(part)
    #Parte acima aqui funciona perfeitamente colocando o attachment. FAzer a logica para mandar arquivo para cada cliente

    # Enviando mensagem
    # print('Enviando mensagem para ' + i)
    server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())
    print('    Mensagem enviada!')
    print('')        


        
    server.quit()

# Funcao - Cria o corpo da mensagem
#def criaMensagemCorpoEmail(resultList):
#    msgBody=""
#    # se o tamanho de result list for igual a zero, significa que nao trouxe ninguem com a data para vencer em N dias
#    if len(resultList)==0:
#        msgBody="Nenhum cliente com vencimento dentro deste periodo."
#        print("  Nenhum cliente com vencimento dentro deste periodo.")
#    else:
#        msgBody = "  CLIENTES COM VENCIMENTO entre HOJE " + f"{today.day:>02}" + "/" + f"{today.month:>02}" + "/" + str(today.year) + " e " + str(numberDaysToValidate) + " DIAS do dia de hoje " + f"{str(dueDate.day):>02}" + "/" + f"{str(dueDate.month):>02}" + "/" + str(dueDate.year) + "\r\n"
#        # faz um looping em todos os resultados preenchendo a variavel msgBody com a mensagem final para o cliente
#        for x in resultList:    
#            # concatena todos os fields para montar mensagem para o cliente por email
#            # Original- funcionando UM somente - msgBody = msgBody + "  " +str(x['_id']) + " - " + f"{str(x['nome']):<40}" + " - " + f"{str(x['cliente']['dadosPessoais']['email']):<40}" + " - Vencimento: " + f"{str(x['cliente']['ativoAte'].day):>02}" + "/" + f"{str(x['cliente']['ativoAte'].month):>02}" + "/" + str(x['cliente']['ativoAte'].year) + " - " + x['plano'] + "\r\n"
#            #msgBody = msgBody + "  " +str(x['_id']) + " - " + f"{str(x['cliente_'][0]['nome']):<40}" + " - " + f"{str(x['cliente_'][0]['email']):<40}" + " - Vencimento: " + f"{str(x['dataTermino'].day):>02}" + "/" + f"{str(x['dataTermino'].month):>02}" + "/" + str(x['dataTermino'].year) + " - " + x['plano'][0]['nome'] +  "\r\n"
#            msgBody = msgBody + "  " +str(x['_id']) + " - " + f"{str(x['cliente_'][0]['nome']):<40}" + " - " + f"{str(x['cliente_'][0]['email']):<40}" + " - Vencimento: " + str(x['dataTermino']) + " - " + x['plano_'][0]['nome'] +  "\r\n"
#            global importantFlag
#            importantFlag=True
#    return msgBody

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

def atualizaDataDeCobranca(clients, idPedido):
    dateToday = datetime.today().strftime("%Y-%m-%d")

    clients.update_one(
        { "_id": idPedido },
        {
            "$set": {
                "dataEmailCobranca": dateToday
            }
        }
    )    

#if today.weekday() > 4:
#    print('Hoje eh fim de semana, nao enviar mensagem!')
#    raise SystemExit(0);  # Finalizar programa aqui

def executaLogicaVencimentoEnviaEmail(clients, resultList):
    msgBody=""
    # se o tamanho de result list for igual a zero, significa que nao trouxe ninguem com a data para vencer em N dias
    if len(resultList)==0:
        msgBody="Nenhum cliente com vencimento dentro deste periodo."
        print("  Nenhum cliente com vencimento dentro deste periodo.")
    else:
        #print(resultList)
    
        # msgBody = "  CLIENTES COM VENCIMENTO entre HOJE " + f"{today.day:>02}" + "/" + f"{today.month:>02}" + "/" + str(today.year) + " e " + str(numberDaysToValidate) + " DIAS do dia de hoje " + f"{str(dueDate.day):>02}" + "/" + f"{str(dueDate.month):>02}" + "/" + str(dueDate.year) + "\r\n"
        # faz um looping em todos os resultados preenchendo a variavel msgBody com a mensagem final para o cliente
        for x in resultList:    
            #print("x[plano_][0][nome] ===>", x['plano_'][0]['nome'])
            #print("x[planoPeriodos_][0][periodicidade ===>", x['planoPeriodos_'][0]['periodicidade'])

            if x['dataEmailCobranca'] is None or x['dataEmailCobranca']  <  x['dataTerminoSubtracted7']:
                date_time_obj = datetime. strptime(x['dataTermino'], '%Y-%m-%d')
                dataTerminoPorExtenso = f"{str(date_time_obj.day):>02}" + " de " + formatMesPorExtenso(f"{str(date_time_obj.month):>02}") + " de " + str(date_time_obj.year)

                # concatena todos os fields para montar mensagem para o cliente por email
                # Original- funcionando UM somente - msgBody = msgBody + "  " +str(x['_id']) + " - " + f"{str(x['nome']):<40}" + " - " + f"{str(x['cliente']['dadosPessoais']['email']):<40}" + " - Vencimento: " + f"{str(x['cliente']['ativoAte'].day):>02}" + "/" + f"{str(x['cliente']['ativoAte'].month):>02}" + "/" + str(x['cliente']['ativoAte'].year) + " - " + x['plano'] + "\r\n"
                #msgBody = msgBody + "  " +str(x['_id']) + " - " + f"{str(x['cliente_'][0]['nome']):<40}" + " - " + f"{str(x['cliente_'][0]['email']):<40}" + " - Vencimento: " + f"{str(x['dataTermino'].day):>02}" + "/" + f"{str(x['dataTermino'].month):>02}" + "/" + str(x['dataTermino'].year) + " - " + x['plano'][0]['nome'] +  "\r\n"
                #msgBody = msgBody + "  " +str(x['_id']) + " - " + f"{str(x['cliente_'][0]['nome']):<40}" + " - " + f"{str(x['cliente_'][0]['email']):<40}" + " - Vencimento: " + str(x['dataTermino']) + " - " + x['plano_'][0]['nome'] +  "\r\n"
                msgBody = ""
                #msgBody = msgBody + "Olá Beexers," + "\r\n"
                #msgBody = msgBody + "Esperamos que a sua experiência com a nossa abelhinha querida seja sempre um sucesso." + "\r\n"
                #msgBody = msgBody + "O vencimento do seu plano " + x['plano_'][0]['nome'] + " - " + x['planoPeriodos_'][0]['periodicidade'] + " ocorrerá no dia " + str(x['dataTermino']) + ", a partir deste dia o robô não estará mais operacional. \r\n"
                #msgBody = msgBody + "Para o seu planejamento e sua conveniência estamos enviando com antecedência o PIX (código de barras) em anexo." + "\r\n"
                #msgBody = msgBody + "Após o pagamento, pedimos que por gentileza o comprovante seja enviado para o seguinte email: " + emailFrom + ", assim conseguiremos ajustar para que o robô fique operacional no novo período.\r\n"
                #msgBody = msgBody + "Se o valor a ser pago diverge do esperado favor entrar em contato com o nosso suporte comercial." + "\r\n"
                #msgBody = msgBody + "Agradecemos a sua confiança!" + "\r\n"
                
                msgBody = msgBody + "<table align=\"center\" border=\"0\" cellpadding=\"0\" cellspacing=\"0\" width=\"600\">"
                msgBody = msgBody + "<tr>"
                msgBody = msgBody + "<td align=\"center\" bgcolor=\"#FFFFFF\" style=\"padding: 40px 0 30px 0;\">"
                msgBody = msgBody + "<IMG class=\"displayed\" src=\"https://beextrading.com/EmailPics/BeexGoldLogo241x155.PNG\" alt=\"Beex Trading Logo\"/>"
                msgBody = msgBody + "</td>"
                msgBody = msgBody + "</tr>"
                #msgBody = msgBody + "</table>"
                msgBody = msgBody + "<tr>"
                msgBody = msgBody + "	<td bgcolor=\"#ffffff\" style=\"padding: 40px 30px 40px 30px;\">"
                msgBody = msgBody + "		<table border=\"0\" cellpadding=\"0\" cellspacing=\"0\" width=\"100%\">"
                msgBody = msgBody + "			<tr>"
                msgBody = msgBody + "		        <td>"
                msgBody = msgBody + "					<h1 align=\"center\">Olá Querido " + x['cliente_'][0]['nome'] + ",</h1>"
                msgBody = msgBody + "				</td>"
                msgBody = msgBody + "			</tr>"
                msgBody = msgBody + "			<tr>"
                msgBody = msgBody + "				<td style='font-size:16px;line-height: 1.5'>"
                          
                msgBody = msgBody + "					Viemos lembrá-lo(a) o vencimento de seu Plano Beex " + x['plano_'][0]['nome'] + " " + x['duracaoPlano'] + ", no dia " +  dataTerminoPorExtenso + "."
                
                # + f"{str(dataTermino.day):>02}" + "/" + f"{str(dataTermino.month):>02}" + "/" + str(dataTermino.year)
                    
                msgBody = msgBody + "					<p style='font-size:16px;line-height: 1.5'>Identificamos o seu último pagamento como sendo através de um PIX."
                          
                msgBody = msgBody + "					<p style='font-size:16px;line-height: 1.5'>Para o seu planejamento e conveniência estamos enviando este email automático com antecedência com o PIX (QR code) no valor de R$  " + str(x['planoPeriodos_'][0]['valor']) + " em anexo, para facilitar o processo de pagamento. Você também pode optar por pagar via Chave PIX 42959993000173."
                          
                msgBody = msgBody + "					<p style='font-size:16px;line-height: 1.5'><b>IMPORTANTE:</b> Após o pagamento, por gentileza enviar o comprovante para o seguinte email: " + emailFrom + ", assim conseguiremos ajustar para que o robô fique operacional para o novo período."
                          
                msgBody = msgBody + "					<p style='font-size:16px;line-height: 1.5'>Qualquer dúvida ou problema, entre em contato conosco pelo whatsapp (11)91259-5500 ou responda este e-mail."

                msgBody = msgBody + "					<p style='font-size:16px;line-height: 1.5'>Caso o pagamento já tenha sido efetuado, por favor, desconsidere este aviso."
                          
                msgBody = msgBody + "					<p style='font-size:16px;line-height: 1.5'>Agradecemos a sua confiança!"
                    
                msgBody = msgBody + "				</td>"
                msgBody = msgBody + "			</tr>"
                msgBody = msgBody + "			<tr>"
                msgBody = msgBody + "				<td>"
                msgBody = msgBody + "				</td>"
                msgBody = msgBody + "			</tr>"
                msgBody = msgBody + "		</table>"
                msgBody = msgBody + "	</td>"
                msgBody = msgBody + "</tr>"
                msgBody = msgBody + "<tr>"
                msgBody = msgBody + "	<td bgcolor=\"#FFFFFF\" align=\"center\">"
                msgBody = msgBody + "		<table border=\"0\">"
                msgBody = msgBody + "			<tr>"
                msgBody = msgBody + "				<td colspan=\"4\">"
                msgBody = msgBody + "					<table>"
                msgBody = msgBody + "						<tr>"
                msgBody = msgBody + "							<td>"
                msgBody = msgBody + "								<img src=\"https://beextrading.com/EmailPics/AssinaturaCompleta500x177.jpg\" width=\"500\" height=\"177\" />"
                msgBody = msgBody + "							</td>"				
                msgBody = msgBody + "						</tr>"
                msgBody = msgBody + "					</table>"
                msgBody = msgBody + "				</td>"
                msgBody = msgBody + "			</tr>"
                        
                msgBody = msgBody + "			<tr>"
                msgBody = msgBody + "				<td>"
                msgBody = msgBody + "					<table>"
                msgBody = msgBody + "						<tr>"
                msgBody = msgBody + "							<td>"
                msgBody = msgBody + "								<a title=\"Beextrading Web Site\" href=\"https://beextrading.com/\">"
                msgBody = msgBody + "									<img src=\"https://beextrading.com/EmailPics/www15x15.jpg\" />"
                msgBody = msgBody + "								</a>"
                msgBody = msgBody + "							</td>"
                msgBody = msgBody + "							<td>"
                msgBody = msgBody + "								<a title=\"Beex Website\" href=\"https://beextrading.com/\">"
                msgBody = msgBody + "									<span style=\"font-size: 8pt;\">Website</span>"
                msgBody = msgBody + "								</a>"
                msgBody = msgBody + "							</td>"			
                msgBody = msgBody + "						</tr>"
                msgBody = msgBody + "					</table>"		
                msgBody = msgBody + "				</td>"
                                
                msgBody = msgBody + "				<td>"
                msgBody = msgBody + "					<table>"
                msgBody = msgBody + "						<tr>"
                msgBody = msgBody + "							<td>"
                msgBody = msgBody + "								<a title=\"Beex Trading Whatsapp\" href=\"https://api.whatsapp.com/send/?phone=5511912595500&amp;text=Ola+vim+do+email+beex&amp;app_absent=0\">"
                msgBody = msgBody + "									<img src=\"https://beextrading.com/EmailPics/whatsapp15x15.png\" />"
                msgBody = msgBody + "								</a>"
                msgBody = msgBody + "							</td>"
                msgBody = msgBody + "							<td>"
                msgBody = msgBody + "								<span style=\"font-size: 8pt;\">"
                msgBody = msgBody + "									<a title=\"Beex Whatsapp\" href=\"https://api.whatsapp.com/send/?phone=5511912595500&amp;text=Ola+vim+do+email+beex&amp;app_absent=0\">Whatsapp</a>"
                msgBody = msgBody + "								</span>"
                msgBody = msgBody + "							</td>"		
                msgBody = msgBody + "						</tr>"
                msgBody = msgBody + "					</table>"
                msgBody = msgBody + "				</td>"
                                
                                
                msgBody = msgBody + "				<td>"
                msgBody = msgBody + "					<table>"
                msgBody = msgBody + "						<tr>"
                msgBody = msgBody + "							<td>"
                msgBody = msgBody + "								<a title=\"Beex Trading Canal Youtube\" href=\"https://www.youtube.com/channel/UCdBLFlxGhQGXUH7K6xctZxA\">"
                msgBody = msgBody + "									<img src=\"https://beextrading.com/EmailPics/youtube15x15.png\" />"
                msgBody = msgBody + "								</a>"
                msgBody = msgBody + "							</td>"
                msgBody = msgBody + "							<td>"
                msgBody = msgBody + "								<a title=\"Beex Canal Youtube\" href=\"https://www.youtube.com/channel/UCdBLFlxGhQGXUH7K6xctZxA\">"
                msgBody = msgBody + "									<span style=\"font-size: 8pt;\">Canal Youtube</span>"
                msgBody = msgBody + "								</a>"
                msgBody = msgBody + "							</td>"				
                msgBody = msgBody + "						</tr>"
                msgBody = msgBody + "					</table>"		
                msgBody = msgBody + "				</td>"
                        
                msgBody = msgBody + "				<td>"
                msgBody = msgBody + "					<table>"
                msgBody = msgBody + "						<tr>"
                msgBody = msgBody + "							<td>"
                msgBody = msgBody + "								<a title=\"Beex Trading Instagram\" href=\"https://www.instagram.com/beex.trading/?utm_medium=copy_link\">"
                msgBody = msgBody + "									<img src=\"https://beextrading.com/EmailPics/instagram15x15.jfif\" />"
                msgBody = msgBody + "								</a>"
                msgBody = msgBody + "							</td>"
                msgBody = msgBody + "							<td>"
                msgBody = msgBody + "								<a title=\"Beex Instagram\" href=\"https://www.instagram.com/beex.trading/?utm_medium=copy_link\">"
                msgBody = msgBody + "									<span style=\"font-size: 8pt;\">Instagram</span>"
                msgBody = msgBody + "								</a>"
                msgBody = msgBody + "							</td>"				
                msgBody = msgBody + "						</tr>"
                msgBody = msgBody + "					</table>"		
                msgBody = msgBody + "				</td>"
                msgBody = msgBody + "			</tr>"
                msgBody = msgBody + "		</table>"
                msgBody = msgBody + "	</td>"
                msgBody = msgBody + "</tr>"
                msgBody = msgBody + "</table>"            

                privateUrl = x['planoPeriodos_'][0]['qrCode'][0]['privateUrl']
                email = x['cliente_'][0]['email']
                
                #msgBody = msgBody + " URL= " + downloadURL
                
                #global importantFlag
                #importantFlag=True
                # chama funcao para apresentar mensagem inicial na tela
                apresentaMensagemConsoleInicio()   
                # chama funcao para apresentar mensagem na tela
                #apresentaMensagemConsole(msgBody)            
                # chama funcao para apresentar mensagem enviando email na tela
                apresentaMensagemEnviandoEmail()
                # chama funcao para enviar email, existe um array de email, quantos emails tiverem nesse array receberao a mensagem
                enviaEmail(email, msgBody, privateUrl, dataTerminoPorExtenso)
                
                #atualiza tabela de pedidos colocando a data de envio do email
                atualizaDataDeCobranca(clients, x['_id'])
                
                # chama funcao para apresentar mensagem final na tela
                apresentaMensagemConsoleFim()
                
            else:
                print("Nao enviar email para ", x['cliente_'][0]['nome'])
            


# chama funcao e recebe como retorno clients
clients = criaConexaoMongoDB()

# chama funcao passando clients e recebe o resultado em como List (nao como cursor, nao como dict)
resultList = pesquisaClientesParaVencer(clients)

#print("Result List = " + str(resultList));

# preenche informacoes para envio do email
preencheConfiguracoesEmail()

# chama funcao passando resultList e recebe o corpo da mensagem
# msgBody = criaMensagemCorpoEmail(resultList)
executaLogicaVencimentoEnviaEmail(clients, resultList)
