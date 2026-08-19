#holds the UserRecord Pydantic model and validate_users(), 
#which checks that fetched data actually matches the expected shape.

from pydantic import BaseModel, ValidationError
# we create a shape from BaseModel - what the data should look like
# UserRecord is the "template" of our data. It defines the fields and their types.

class UserRecord(BaseModel):
    id: int         # id number nai huнu parcha
    name: str        # name text huनu parcha
    email: str        # email text huनu parcha
    phone: str        # phone text huनu parcha

def validate_users(raw_users: list) -> list:
    valid = []                      # keeping correct records in list
    for u in raw_users:              # checking each user in the list
        try:
            # checks if it matches the UserRecord template
            record = UserRecord(id=u["id"], name=u["name"], email=u["email"], phone=u["phone"])
            valid.append(record.model_dump())   # if valid, add to the list
        except ValidationError as e:
            # if invalid, print error and skip the record
            print(f"Skipping invalid record: {e}")
    return valid