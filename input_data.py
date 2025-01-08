import pandas as pd

username = []
bio = []
seguidores = []
while True:
    user = input("Digite a link do perfil: ")
    print("\n")
    this_bio = input("Digite a bio do perfil: ")
    print("\n")
    seguidores_this = input("Digite a quantidade de seguidores: ")
    print("\n")
    username.append(user)
    bio.append(this_bio)
    seguidores.append(seguidores_this)
    parar = int(input("Deseja parar? 0 - Sim | 1 - Não: "))
    if parar == 0:
        break

# Criação do DataFrame com as bios coletadas
data = {'Username': username, 'bio': bio}
df = pd.DataFrame(data)

print(df)