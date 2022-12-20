#!/usr/bin/env python
#Execute commond on windows machine to install psutil>>>>python -m pip install psutil
import psutil
import smtplib
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
#emailToArray=["jvvleite@gmail.com", "magnobrasil2013@gmail.com", "contato@beextrading.com"]
emailToArray=["magnobrasil2013@gmail.com"]

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

# Funcao - Envia Emails
def enviaEmail(msgBody):
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
        email_msg['Subject'] = " BEEX ALERTA URGENTE - MEMORIA COM ALTO CONSUMO - LOCAWEB"
            
        #print('Adicionando texto...')
        email_msg.attach(MIMEText(msgBody, 'plain'))

        # Enviando mensagem
        # print('Enviando mensagem para ' + i)
        server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())
        print('    Mensagem enviada!')
        print('')        
    server.quit()

# Funcao - Cria o corpo da mensagem
def criaMensagemCorpoEmail(percentageResult):
    msgBody=""
    msgBody="ALERT: URGENCIA: Memoria servidor Beex LOCAWEB em " + str(percentageResult) + " %  AGIR para corrigir problema."
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

#if today.weekday() > 4:
#    print('Hoje eh fim de semana, nao enviar mensagem!')
#    raise SystemExit(0);  # Finalizar programa aqui


print ('                                                                   ')
print ('----------------------CPU Information summary----------------------')
print ('                                                                   ')

# gives a single float value
vcc=psutil.cpu_count()
print ('Total number of CPUs :',vcc)

vcpu=psutil.cpu_percent()
print ('Total CPUs utilized percentage :',vcpu,'%')

print ('                                                                   ')
print ('----------------------RAM Information summary----------------------')
print ('                                                                   ')
# you can convert that object to a dictionary 
#print(dict(psutil.virtual_memory()._asdict()))
# gives an object with many fields
vvm=psutil.virtual_memory()

x=dict(psutil.virtual_memory()._asdict())

def forloop():
    for i in x:
        print (i,"--",x[i]/1024/1024/1024)#Output will be printed in GBs

forloop()
print ('                                                                   ')
print ('----------------------RAM Utilization summary----------------------')
print ('                                                                   ')
# you can have the percentage of used RAM
print('Percentage of used RAM :',psutil.virtual_memory().percent,'%')
#79.2
# you can calculate percentage of available memory
print('Percentage of available RAM :',psutil.virtual_memory().available * 100 / psutil.virtual_memory().total,'%')
#20.8

if psutil.virtual_memory().percent > 70:
    # chama funcao passando resultList e recebe o corpo da mensagem
    msgBody = criaMensagemCorpoEmail(psutil.virtual_memory().percent)

    # chama funcao para apresentar mensagem inicial na tela
    apresentaMensagemConsoleInicio()

    # chama funcao para apresentar mensagem na tela
    apresentaMensagemConsole(msgBody)

    # chama funcao para apresentar mensagem enviando email na tela
    apresentaMensagemEnviandoEmail()

    # chama funcao para enviar email, existe um array de email, quantos emails tiverem nesse array receberao a mensagem
    enviaEmail(msgBody)

    # chama funcao para apresentar mensagem final na tela
    apresentaMensagemConsoleFim()