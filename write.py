import ast

def writeCFG(HSV_UP, HSV_LOW):
    with open("save.cfg", "w") as file:
            file.write(f"HSV_upper={HSV_UP}\n")
            file.write(f"HSV_lower={HSV_LOW}")

def loadCFG():
    cfg = []
    try:
        with open("save.cfg", "r") as file:
            for line in file:
                cfg.append(ast.literal_eval(line.replace("\n", "").split("=")[1]))
            return cfg
    except:
        cfg.append([0,0,0])
        cfg.append([0,0,0])
        print("file is not found, trying to write....")
        writeCFG([0,0,0], [0,0,0])
        print("file write succed")
        return cfg
print(loadCFG())