from pony import orm
from datetime import datetime
from pony.orm import select

DB = orm.Database()

class Transakcija(DB.Entity):
    id = orm.PrimaryKey(int, auto=True)
    opis = orm.Required(str)
    iznos = orm.Required(int)
    datum = orm.Optional(datetime)
    tip = orm.Required(str)

    def to_dict(self):
        return {
            "id": self.id,
            "opis": self.opis,
            "iznos": self.iznos,
            "datum": self.datum,
            "tip": self.tip
        }


def formatiraj_datum(datum):
    return datum.strftime("%d-%m-%Y") if datum else None



DB.bind(provider="sqlite", filename="db.sqlite", create_db=True)
DB.generate_mapping(create_tables=True)


def get_transakcije():
    try:
        with orm.db_session:           
            db_upit = Transakcija.select()
            db_upit = list(db_upit)
            results_list = []
            for r in db_upit:
                results_list.append(r.to_dict())
            response = {"response": "Success", "data": results_list}
            return response
    except Exception as e:
        return {"response": "Fail", "error": str(e)}


def get_transakcija_by_id(transakcija_id):
    try:
        with orm.db_session:
            result = Transakcija[transakcija_id].to_dict()
            result["datum"] = formatiraj_datum(result["datum"])
            response = {"response": "Success", "data": result}
            return response
    except Exception as e:
        return {"response": "Fail", "error": str(e)}


def add_transakcija(json_request):
    try:
        opis = json_request["opis"]
        iznos = json_request["iznos"]
        tip = json_request["tip"]
        
        try:
            datum = datetime.strptime(json_request["datum"], "%d-%m-%Y")
        except ValueError:
            datum = None

        with orm.db_session:
            Transakcija(opis=opis, iznos=iznos, datum=datum, tip=tip)
            response = {"response": "Success"}
            return response

    except Exception as e:
        return {"response": "Fail", "error": str(e)}
    

def delete_transakcija(transakcija_id):
    try:
        with orm.db_session:
            stara = Transakcija[transakcija_id]
            stara.delete()
            response = {"response": "Success"}
            return response
    except Exception as e:
        return {"response": "Fail", "error": str(e)}

def patch_transakcija(transakcija_id, json_request):
    try:
        with orm.db_session:
            stara = Transakcija[transakcija_id]

            if "opis" in json_request:
                stara.opis = json_request["opis"]
            if "iznos" in json_request:
                stara.iznos = json_request["iznos"]
            if "datum" in json_request:
                datum = datetime.strptime(json_request["datum"], "%d-%m-%Y")
                stara.datum = datum
            if "tip" in json_request:
                stara.tip = json_request["tip"]
            
            response = {"response": "Success"}
            return response
        
    except Exception as e:
        return {"response": "Fail", "error": str(e)}
