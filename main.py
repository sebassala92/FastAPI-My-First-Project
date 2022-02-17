#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

#Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city: str
    state: str
    country: str


class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    age: int = Field(
        ...,
        gt=0,
        le=115
        )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default = None)



@app.get("/")
def home():
    return {"Hello": "World"}


#Request and Response Body

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

#validaciones: Query parameters

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=1,
        max_length=50,
        title="Person Name",
        description="This is the person name"
        ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age."
        )
):
    return {name: age}

#validaciones: path parameters

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,
        title="Person id",
        description="This is the person id"
        )
):
    return {person_id: "It exist!"}

@app.get("/person/calculo/{num_1}/{num_2}")
def calculo(
    num_1: int = Path(
        ..., 
        ge=0,
        title="numero 1",
        description="ingrese un numero natural"
        ),

    num_2: int = Path(
        ..., 
        ge=0,
        title="numero 2",
        description="ingrese un numero natural"
        )
):  
    list_fibonacci = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418, 317811, 514229, 832040, 1346269, 2178309, 3524578, 5702887, 9227465, 14930352, 24157817, 39088169, 63245986, 102334155, 165580141, 267914296, 43349443, 701408733, 1134903170, 1836311903, 2971215073, 4807526976, 7778742049, 12586269025, 20365011074, 32951280099, 53316291173, 86267571272, 139583862445, 225851433717, 365435296162, 591286729879, 956722026041, 1548008755920, 2504730781961, 4052739537881, 6557470319842, 10610209857723, 17167680177565, 27777890035288, 44945570212853, 72723460248141, 117669030460994, 190392490709135, 308061521170129, 498454011879264, 806515533049393, 1304969544928657, 2111485077978050, 3416454622906707, 5527939700884757, 8944394323791464, 14472334024676221, 23416728348467685, 37889062373143906, 61305790721611591, 99194853094755497, 160500643816367088, 259695496911122585, 420196140727489673, 679891637638612258, 1100087778366101931, 1779979416004714189, 2880067194370816120, 4660046610375530309, 7540113804746346429, 12200160415121876738, 19740274219868223167, 1940434634990099905, 51680708854858323072, 83621143489848422977, 135301852344706746049, 218922995834555169026]
    sum = num_1+num_2

    if sum in list_fibonacci:
        pertenece = True
    else:
        pertenece = False

    return {
        "mensaje": "se esta realizando el calculo",
        "numero 1": num_1,
        "numero 2": num_2,
        "suma de numeros": sum,
        "pertenece a la lista?": pertenece
    }

#Validaciones: Request Body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title= "person ID",
        description= "this is the person id",
        gt=0
    ),
    person: Person = Body(...),
    Location: Location = Body(...)

):
    results = person.dict()
    results.update(Location.dict())
    return results