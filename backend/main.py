from general_controller import runAplication

def main(ano, csvFileName, modal, modo, client):
    anoToInt = int(ano)
    runAplication(anoToInt, csvFileName, modal, modo, client)



