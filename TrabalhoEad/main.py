
from fastapi import FastAPI, Query,HTTPException
from pydantic import BaseModel
from typing import Optional
import datetime

app = FastAPI()

class Cliente(BaseModel):
    id: Optional[int] = 0
    nome: str
    tipoAtendimento: str
    posicaoFila: int
    dataEntrada: datetime.datetime
    atendido: bool

db_clientes=[]

contador = 0

@app.get("/fila")
def clientes_pendentes():
    return {"Cliente": [cliente for cliente in db_clientes if cliente.atendido == False]}

@app.get("/fila/{id}")
def busca_clientes(id:int):
    clientes = [cliente for cliente in db_clientes if cliente.id == id]
    if clientes == []:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return {"Cliente": clientes }

@app.post("/fila")
def adcionar_fila(TipoAtendimento:str = Query(max_length=1), Nome: str = Query(max_length=20)):
    global contador
    novoCliente = Cliente(id = contador, tipoAtendimento= TipoAtendimento,nome = Nome, posicaoFila= contador+1, dataEntrada=datetime.datetime.now(), atendido=False)
    db_clientes.append(novoCliente)
    contador += 1
    return {"Cliente": novoCliente}

@app.put("/fila")
def atendido():
    for cliente in db_clientes:
        if cliente.posicaoFila == 1:
            cliente.atendido = True
            cliente.posicaoFila = 0
        else:
            cliente.posicaoFila = cliente.posicaoFila -1       
    return {"Cliente": db_clientes }


@app.delete("/fila/{id}")
def remover_fila(id: int):
    cliente_deletado = [cliente for cliente in db_clientes if cliente.id == id]
    db_clientes.remove(cliente_deletado[0])
    for cliente in db_clientes:
        if  cliente.id > cliente_deletado[0].id:
            cliente.posicaoFila = cliente.posicaoFila -1 
    return {"Cliente": db_clientes }
        
