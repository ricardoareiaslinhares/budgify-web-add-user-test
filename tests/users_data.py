from itertools import combinations
from typing import TypedDict


class User(TypedDict):
    name: str
    email: str
    password: str
    dateOfBirth: str
    genre: str
    wallet: bool


valid_user_data: list[User] = [
    {
        "name": "Budgify1",
        "email": "testePass3@teste.com",
        "password": "teste123",
        "dateOfBirth": "1980-12-01",
        "genre": "Male",
        "wallet": True,
    },
    {
        "name": "Budgify2",
        "email": "testePass4@teste.com",
        "password": "teste123",
        "dateOfBirth": "1980-12-01",
        "genre": "Female",
        "wallet": False,
    },
]


def generate_invalid_user_data():
    wallet_values = [True, False]
    invalid_users = []

    template_user = valid_user_data[0]
    field_names = [f for f in template_user.keys() if f != "wallet"]
    n_fields = len(field_names)

    for r in range(1, n_fields + 1):
        for failing_fields in combinations(field_names, r):
            for wallet in wallet_values:
                user = template_user.copy()  # start with all valid
                # set selected fields to invalid
                for f in failing_fields:
                    if f == "genre":
                        # can only select valid options. Male is the default
                        user[f] = "Male"
                    else:
                        user[f] = ""  # default invalid
                # set carteira
                user["wallet"] = wallet
                invalid_users.append(user)
    print(f"Generated {len(invalid_users)} invalid entries")
    return invalid_users


generate_invalid_user_data()
