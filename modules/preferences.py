import json


def save_preferences(data={
    "steamPath": r"C:\Program Files (x86)\Steam"
}):
    with open("users_prefs.json", "w") as f:
        f.write(json.dumps(data, indent=True))
        f.close()


def load_preferences():
    with open("users_prefs.json", "r") as f:
        return json.load(f)


if __name__ == "__main__":
    # save_preferences({'is_claimed': True, 'rating': 3.5})
    print(load_preferences())
