from fastapi.requests import Request

def log(tag="", message="no message", request: Request = None):
    with open("log.txt", "a+") as log:
        log.write(f"{tag}: {message} \n")
        log.write(f'\t{request.url} \n')