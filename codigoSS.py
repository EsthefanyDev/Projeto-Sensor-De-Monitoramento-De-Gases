import machine
import time
from machine import Pin

# Configuração do pino do sensor de gás
sensor_gas = machine.ADC(0)  # Conecte o MQ-8 ao pino A0

# Configuração do buzzer (D5 - GPIO 14)
buzzer = machine.PWM(machine.Pin(14))  # D5 é GPIO 14 no ESP8266

# Configuração dos LEDs (D6 e D7)
led_verde = Pin(0, Pin.OUT)  # GPIO 12 (D6)
led_vermelho = Pin(2, Pin.OUT)  # GPIO 13 (D7)

# Função para ler o sensor de gás
def ler_sensor_gas():
    valor_bruto = sensor_gas.read()  # Lê o valor do sensor
    # Converter o valor bruto para uma escala mais significativa (percentual)
    valor_convertido = (valor_bruto / 1023) * 100  # Converte para percentual
    return valor_convertido

# Função para tocar o buzzer
def tocar_buzzer(frequencia=1000):  # Frequência padrão de 1000 Hz
    buzzer.freq(frequencia)  # Define a frequência do buzzer
    buzzer.duty(512)  # Define a intensidade (valor entre 0 e 1023)
    time.sleep(3)  # O buzzer tocará por 3 segundos
    buzzer.duty(0)  # Desliga o buzzer

# Função principal para monitorar o sensor de gás e controlar LEDs e buzzer
def monitorar_gas():
    while True:
        valor_gas = ler_sensor_gas()
        print('Nível de gás detectado: {:.2f}%'.format(valor_gas))

        # Limite ajustado para 10% de presença de gases inflamáveis ou fumaça
        if valor_gas > 10:  # Limite de alerta
            print('Alerta: Nível perigoso de gás detectado!')
            led_vermelho.value(1)  # Acende o LED vermelho
            led_verde.value(0)  # Apaga o LED verde
            tocar_buzzer()  # Ativa o buzzer
        else:
            print('Nível de gás seguro.')
            led_verde.value(1)  # Acende o LED verde
            led_vermelho.value(0)  # Apaga o LED vermelho

        time.sleep(1)  # Atraso de 1 segundo entre leituras

# Iniciar o monitoramento do sensor de gás
monitorar_gas()


#####################################################

import machine
import time
from machine import Pin

# Configuração do pino do sensor de gás
sensor_gas = machine.ADC(0)  # Conecte o MQ-8 ao pino A0

# Configuração do buzzer (D5 - GPIO 14)
buzzer = machine.PWM(machine.Pin(14))  # D5 é GPIO 14 no ESP8266

# Configuração dos LEDs (D6 e D7)
led_verde = Pin(0, Pin.OUT)  # GPIO 12 (D6)
led_vermelho = Pin(2, Pin.OUT)  # GPIO 13 (D7)

# Função para ler o sensor de gás
def ler_sensor_gas():
    valor_bruto = sensor_gas.read()  # Lê o valor do sensor
    # Converter o valor bruto para uma escala mais significativa (percentual)
    valor_convertido = (valor_bruto / 1023) * 100  # Converte para percentual
    return valor_convertido

# Função para tocar o buzzer
def tocar_buzzer(frequencia=1000):  # Frequência padrão de 1000 Hz
    buzzer.freq(frequencia)  # Define a frequência do buzzer
    buzzer.duty(512)  # Define a intensidade (valor entre 0 e 1023)
    time.sleep(3)  # O buzzer tocará por 3 segundos
    buzzer.duty(0)  # Desliga o buzzer

# Função principal para monitorar o sensor de gás e controlar LEDs e buzzer
def monitorar_gas():
    tempo_inicial = time.time()  # Armazena o tempo de início
    periodo_aquecimento = 60 * 5  # 5 minutos de aquecimento (ajustável)

    while True:
        valor_gas = ler_sensor_gas()
        tempo_atual = time.time()

        # Ignorar as leituras durante o período de aquecimento
        if tempo_atual - tempo_inicial < periodo_aquecimento:
            print("Aquecendo o sensor... (Ignorando leituras por enquanto)")
        else:
            print('Nível de gás detectado: {:.2f}%'.format(valor_gas))

            # Limite ajustado para 10% de presença de gases inflamáveis ou fumaça
            if valor_gas > 10:  # Limite de alerta
                print('Alerta: Nível perigoso de gás detectado!')
                led_vermelho.value(1)  # Acende o LED vermelho
                led_verde.value(0)  # Apaga o LED verde
                tocar_buzzer()  # Ativa o buzzer
            else:
                print('Nível de gás seguro.')
                led_verde.value(1)  # Acende o LED verde
                led_vermelho.value(0)  # Apaga o LED vermelho

            time.sleep(1)  # Atraso de 1 segundo entre leituras

    # Iniciar o monitoramento do sensor de gás
    monitorar_gas()
#################################



import time
import machine
import urequests
from machine import Pin

# Configuração do Wi-Fi
import network

ssid = 'Online.Rodrigo'
password = 'Rodrigo21'

def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando ao WiFi...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('Conexão estabelecida:', wlan.ifconfig())

# Configuração do pino do sensor de gás
sensor_gas = machine.ADC(0)  # Conecte o MQ-8 ao pino A0

# Configuração do buzzer (D5 - GPIO 14)
buzzer = machine.PWM(machine.Pin(14))  # D5 é GPIO 14 no ESP8266

# Configuração dos LEDs (D6 e D7)
led_verde = Pin(0, Pin.OUT)  # GPIO 0 (D4)
led_vermelho = Pin(2, Pin.OUT)  # GPIO 2  (D3)

# Configuração do ThingSpeak
THINGSPEAK_URL = "http://api.thingspeak.com/update"
CHANNEL_KEY = "TRY5MM6Z4GJSHFP8"

# Função para enviar dados ao ThingSpeak
def enviar_dados_thingspeak(valor_gas):
    try:
        resposta = urequests.get(THINGSPEAK_URL + "?api_key=" + CHANNEL_KEY + "&field1=" + str(valor_gas))
        print('Dados enviados ao ThingSpeak:', resposta.text)
        resposta.close()
    except Exception as e:
        print('Falha ao enviar dados:', e)

# Função para ler o sensor de gás
def ler_sensor_gas():
    valor_bruto = sensor_gas.read()  # Lê o valor do sensor
    # Converter o valor bruto para uma escala mais significativa (percentual)
    valor_convertido = (valor_bruto / 1023) * 100  # Converte para percentual
    return valor_convertido

# Função para tocar o buzzer
def tocar_buzzer(frequencia=1000):  # Frequência padrão de 1000 Hz
    buzzer.freq(frequencia)  # Define a frequência do buzzer
    buzzer.duty(512)  # Define a intensidade (valor entre 0 e 1023)
    time.sleep(3)  # O buzzer tocará por 3 segundos
    buzzer.duty(0)  # Desliga o buzzer

# Função principal para monitorar o sensor de gás e controlar LEDs e buzzer
def monitorar_gas():
    ultimo_envio = time.time()  # Marca o tempo do último envio
    while True:
        valor_gas = ler_sensor_gas()
        print('Nível de gás detectado: {:.2f}%'.format(valor_gas))

        # Verifica se é hora de enviar os dados para o ThingSpeak (a cada 15 segundos)
        if time.time() - ultimo_envio >= 15:
            enviar_dados_thingspeak(valor_gas)
            ultimo_envio = time.time()  # Atualiza o tempo do último envio

        # Limite ajustado para 10% de presença de gases inflamáveis ou fumaça
        if valor_gas > 10:  # Limite de alerta
            print('Alerta: Nível perigoso de gás detectado!')
            led_vermelho.value(1)  # Acende o LED vermelho
            time.sleep(0.5)
            led_vermelho.value(0)  # Apaga o LED vermelho
            led_verde.value(0)  # Apaga o LED verde
            tocar_buzzer()  # Ativa o buzzer por 3 segundos
        else:
            print('Nível de gás seguro.')
            led_verde.value(1)  # Acende o LED verde
            led_vermelho.value(0)  # Apaga o LED vermelho

        time.sleep(3)  # Atraso de 1 segundo entre leituras do sensor

# Conectar ao Wi-Fi
conectar_wifi()

# Iniciar o monitoramento do sensor de gás
monitorar_gas()