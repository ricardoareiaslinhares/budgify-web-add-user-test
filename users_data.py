from itertools import combinations, product

valid_user_data = [
    {
        "name": "Budgify1",
        "email": "testePass3@teste.com",
        "password": "teste123",
        "birthdate": "1980-12-01",
        "gender": "Male",
        "wallet": True,
    },
    {
        "name": "Budgify2",
        "email": "testePass4@teste.com",
        "password": "teste123",
        "birthdate": "1980-12-01",
        "gender": "Female",
        "wallet": False,
    },
]


def generate_invalid_user_data():
    wallet_values = [True, False]
    invalid_value = ""  # empty counts as invalid
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
                    user[f] = invalid_value
                # set carteira
                user["wallet"] = wallet
                invalid_users.append(user)
    print(f"Generated {len(invalid_users)} invalid entries")
    return invalid_users


generate_invalid_user_data()
