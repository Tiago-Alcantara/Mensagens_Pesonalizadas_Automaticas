from senha import API_KEY,EMAIL
import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time




#parte de configuração do Chat Gpt
def IA(descricao):
        headers = {"Authorization": f"Bearer {API_KEY}","content-type":"Application/json"}
        link = "https://api.openai.com/v1/chat/completions"
        id_modelo = "gpt-3.5-turbo"
        
        body_mensagem = {

                "model": id_modelo,

                "messages": [{"role": "user", "content": f"escreva um e-mail a recrutadora dessa vaga {descricao} dizendo os beneficios de me contrarar com base nisso Sou um profissional adaptável, focado em constante aprendizado técnico e prático. Valorizo a comunicação e o trabalho em equipe, assumindo a responsabilidade pelo meu crescimento e sucesso. Minha experiência inclui criação de macros no Excel com VBA, Web Scraping com Python e análise de dados usando Pandas, Pandas Datareader, Matplotlib e Power Bi, permitindo-me abordar indicadores de desempenho comercial e tendências de forma eficaz e estou me formando em Analise e desenvolvimento de sistemas e ja sou Tecnico em informatica"}]

        }

        body_mensagem = json.dumps(body_mensagem)
        requisicao = requests.post(link, headers=headers, data=body_mensagem)
        resposta = requisicao.json()
        mensagem = resposta["choices"][0]["message"]["content"]
        mensagem_sem_colchetes = mensagem.replace("[", "").replace("]", "")
        mensagem_final = mensagem_sem_colchetes.replace("[Seu nome]", "")
        
        return mensagem_final


#configuração do web Scraping
drive = webdriver.Chrome(service= Service(ChromeDriverManager().install()))

url = "https://br.indeed.com"

drive.get(url)


login = drive.find_element("xpath",'''/html/body/div[1]/header/nav/div/div/div[2]/div[2]/div[2]/a''').click()

email = drive.find_element("xpath",'''/html/body/div[1]/div[2]/main/div/div/div[2]/div/form/div/span/input''')
email.send_keys(EMAIL)


input("fazer login para dar certo, assim que terminar dar enter")

a = 1
#Configuraçao de Pegar as informações do Indeed
# entrar nas notificações para sempre pegar tanto a conversa quanto a descrição 
notificacao = drive.find_element("xpath",'''/html/body/div[1]/header/nav/div/div/div[2]/div[1]/div[2]/a''').click()
while a>=2:
    #entrar na vaga para pegar as descrições e resposnabilidades 
    try:
        vaga_descricao = drive.find_element("xpath",'''/html/body/div[1]/main/div[2]/div/div/div/div/div[2]/div[2]/div[1]/div[3]/div[2]/div/div[1]/a''').click()
    except  NoSuchElementException: #para caso nao exista o elemento que pedi
        a += 1 
        break
    else:
        
        texto_descricao_vaga = drive.find_element("id","jobDescriptionText").text

        drive.back()

        time.sleep(2)
        #entrar na conversa
        entrar_conversa = drive.find_element("xpath",'''/html/body/div[1]/main/div[2]/div/div/div/div/div[2]/div[2]/div[2]/a''').click()

        time.sleep(2)

        try:
            botão_cookies = drive.find_element("xpath",'''/html/body/div[2]/div[2]/div/div[1]/div/div[2]/div/button[3]''').click()
        except  NoSuchElementException:
            print("SemCooke")
        finally:
            caixa_de_mensagem = drive.find_element("xpath",'''/html/body/div[1]/div/main/div[2]/div[2]/div/div[3]/div/div[1]/textarea''',)
            mensagem = caixa_de_mensagem.send_keys(IA(texto_descricao_vaga))
            botao_enviar = drive.find_element("xpath","/html/body/div[1]/div/main/div[2]/div[2]/div/div[3]/div/div[2]/div[2]/button").click()

            time.sleep(2)

            #mensagem final pré editada
            mensagem_final = "Quero compartilhar um segredo com você, recrutador(a). O texto que compartilhei anteriormente foi gerado de forma totalmente automatizada por uma inteligência artificial que eu mesmo programei. Essa IA utiliza minhas experiências, características profissionais e competências, juntamente com a descrição da vaga, para tentar conciliar tanto as especificações da vaga quanto as minhas próprias qualificações, demonstrando assim a compatibilidade com a posição em questão. Agradeço pelo seu tempo e estou à disposição para uma conversa, basta me chamar no chat."
            caixa_de_mensagem = drive.find_element("xpath",'''/html/body/div[1]/div/main/div[2]/div[2]/div/div[3]/div/div[1]/textarea''',)
            caixa_de_mensagem.send_keys(mensagem_final)
            botao_enviar = drive.find_element("xpath","/html/body/div[1]/div/main/div[2]/div[2]/div/div[3]/div/div[2]/div[2]/button").click()

            time.sleep(2)

            #voltar para a pagina anterior e pagar essa notificação
            drive.back()
            botao_deletar = drive.find_element("xpath","/html/body/div[1]/main/div[2]/div/div/div/div/div[2]/div[2]/div[1]/div[1]/button").click()


            time.sleep(5)




