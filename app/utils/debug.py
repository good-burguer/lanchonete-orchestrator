from fastapi import HTTPException
from pprint import pformat

def var_dump_die(data):
    formatted = pformat(data)
    
    raise HTTPException(status_code=400, detail=f"DEBUG: {formatted}")