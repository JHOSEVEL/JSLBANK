import random
from datetime import datetime, timedelta


def gerar_cartao_ficticio(nome_usuario, sobrenome_usuario):
    # creat e a fictitious card number
    numero_cartao = "".join([str(random.randint(0, 9)) for _ in range(16)])
    
    # format a card number in groups of 4 digits
    numero_formatado = " ".join([numero_cartao[i:i+4] for i in range(0,16, 4)])

    # create a security code (CVV) with 3 digits
    cvv = "".join([str(random.randint(0, 9)) for _ in range(3)])


    # create an expiration date 5 years from now
    data_validade = datetime.now() + timedelta(days=5*365)
    validade = data_validade.strftime("%m/%y")

    # create a fictitious cardholder name
    nome_cartao = f"{nome_usuario} {sobrenome_usuario.upper()}"

    return {
        "numero": numero_formatado,
        "nome_titular": nome_cartao,
        "validade": validade,
        "cvv": cvv,
        "bandeira": random.choice(["Visa", "Mastercard", "American Express", "Discover"]),
        "limite": random.randint(1000, 10000)
    }