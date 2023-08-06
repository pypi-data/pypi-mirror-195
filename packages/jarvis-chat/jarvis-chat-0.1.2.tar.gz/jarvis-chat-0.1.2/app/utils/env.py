def read_env_variables():
    try:
        file = open(".env", "r")
        keys = {}

        for line in file.readlines():
            split = line.split("=")

            if len(split) != 2:
                continue

            key, val = split

            keys[key] = val[:-1]

        file.close()

        return keys
    except:
        return {}


def write_env_variables(keys):
    file = open(".env", "w")

    for key, val in keys.items():
        file.write("{}={}\n".format(key, val))

    file.close()


def set_env_variable(key, value):
    keys = read_env_variables()
    keys[key] = value
    write_env_variables(keys)

def get_env_variable(key):
    keys = read_env_variables()
    return keys.get(key)