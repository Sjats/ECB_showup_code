@startuml
class Titol {
  id : int
  nom : str
  data_principi : date
  data_final : date
  territori : str
  foto_path : str
}

class Dinastia {
  id : int
  nom : str
  data_principi : date
  data_final : date
  foto_path : str
}


class Senyor {
  id : int
  nom : str
  data_neixement : date
  data_mort : date
  ordinal : str
  dinastia_id : int
  foto_path : str
}


class Govern {
  id : int
  senyor_id : int
  titol_id : int
  numero : text
  data_debut : date
  data_final : date
}


class Peça {
  id : int
  moneda_id : int
  estat : str
  descripcio : str
  serie_emissio : str
  valor_estimat : float
  lloc : str
  foto_path : str
}

class Moneda {
  id : int
  valor_nominal : float
  any : date
  govern_id : int
  devisa_id : int
  descripcio : str
  material : str
  foto_path : str
}

class Devisa {
  id : int
  nom : str
  data_creacio : date
  data_final : date
  foto_path : str
}

Devisa --> Moneda
Govern --> Moneda
Moneda --> Peça
Titol --> Govern 
Dinastia --> Senyor
Senyor --> Govern
@enduml