def log(message: str, file: str = 'log.txt'):
    with open(file, 'w') as f:
        f.write(message)