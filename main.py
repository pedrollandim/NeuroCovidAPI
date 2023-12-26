import mysql.connector

# Configurações do banco de dados
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'neuro_covid'
}

def realizar_login(email, senha):
    # Conectar ao banco de dados
    try:
        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor()

        # Consultar o banco de dados para verificar as credenciais
        query = "SELECT * FROM usuarios WHERE email = %s AND senha = %s"
        cursor.execute(query, (email, senha))

        # Recuperar o resultado da consulta
        usuario = cursor.fetchone()

        # Fechar a conexão
        cursor.close()
        conexao.close()

        return usuario is not None

    except mysql.connector.Error as err:
        print(f"Erro de banco de dados: {err}")
        return False

# Exemplo de uso
email_digitado = input("Digite o email: ")
senha_digitada = input("Digite a senha: ")

if realizar_login(email_digitado, senha_digitada):
    print("Login bem-sucedido!")
else:
    print("Credenciais inválidas.")