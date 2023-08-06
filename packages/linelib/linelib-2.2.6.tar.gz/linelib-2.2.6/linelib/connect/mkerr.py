# make error description
from ..exceptions import ClientException


def mk(resJson: dict):
    if "message" in resJson: # some errors in there
        errs = ""
        if not 'details' in resJson:
          raise ClientException(f"""Error while making a request:\n ~ {resJson['message']}""")
        for e in resJson['details']:
            errs += f"• {e['message']}\n~~~~AT `{e['property']}`\n\n"

        raise ClientException(
             f"""\n\nError while making a request:\n ~ {resJson['message']}\n\n{errs}"""
        )
