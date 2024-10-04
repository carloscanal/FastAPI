
        
from fastapi import FastAPI, Response               # FastAPI
from fastapi.middleware.cors import CORSMiddleware  # CORS, permitir origenes como swagger.io
from typing import Union                            # typing, anotacionesiones de tipos
from pydantic import BaseModel                      # pydantic, comprobaciones de tipos en runtime; tipos complejos


class Item(BaseModel):
    nombre: str = "Anónimo"
    descripcion: Union[str, None] = None
    precio: int = 0


# ejecutar con    python -m uvicorn main:api --reload --port 8000


api = FastAPI()

origins = [
    "https://editor.swagger.io"                     # para probar con OpenAPI desde Swagger
]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

path = "/api/v1/"


# 1. GET a un path (sin variables)

@api.get(path + "hola")                             # endpoint: /api/v1/hola
async def hola():                                   # o simplemente con def
    return {"message": "Hola, mundo"}



# 2. GET con variables de path: nombre

@api.get(path + "hola/{nombre}")                    # endpoint: api/v1/hola/{nombre}    (Parámetro de Path)
async def hola(nombre : str):
    return {"message": "Hola, " + nombre}



# 3. GET con parámetros de query opcionales: nombre

path = "/api/v2/"                                   # evita colision de paths cuando no hay parámetro de query (/hola)

@api.get(path + "hola")                      
async def hola(nombre : Union[str, None] = None):   # endpoint: api/v2/hola?nombre=<nombre>
    if nombre == None :                             #     p.ej. api/v2/hola?nombre=Pepe
        nombre = "mundo"                              
    return {"message": "Hola, " + nombre}

# 3.1. Alternativa más sencilla

path = "/api/v3/"

@api.get(path + "hola")                      
async def hola(nombre : str = "mundo"):             # endpoint: api/v3/hola?nombre=<nombre>; "mundo" como valor por defecto                      
    return {"message": "Hola, " + nombre}

# 4. GET con variables de path y query: nombre, saludo

@api.get(path + "hola/{nombre}")                      
async def hola(nombre : str, saludo : Union[str, None] = None):

    if saludo != None :                            # endpoint: api/v3/hola/{nombre}?saludo=<saludo>
        saludo = ", " + saludo                     #     p.ej. api/v3/hola/Pepe?saludo=qué%20tal%20estás?
    else:
        saludo = ""

    return {"message": "Hola, " + nombre + saludo}


path = "/api/v4/"

# 5. POST con objeto nuevo en el body; código de estado por defecto

@api.post(path + "items", status_code=201)         # response status code por defecto 
async def create_item(item: Item):
    
    return item


# 6. PUT con objeto actualizado en el body

@api.put(path + "items/{id}")          
async def update_item(id: int, item: Item):

    item.precio += 10
    return item


# 7. DELETE, con código de estado condicionado

@api.delete(path + "items/{id}")          
async def remove_item(id: int, response : Response):

    response.status_code=404                        # cambio el status code dependiendo de alguna condicion
    return {"message": "Item no encontrado" }
    
    
    
    
    
    
    
    


