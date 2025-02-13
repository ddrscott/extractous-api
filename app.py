import click
import uuid
import os
import sys
import jwt
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException, Header, Depends
from extractous import Extractor


jwt_secret = os.getenv('JWT_SECRET', None)
if not jwt_secret:
    raise ValueError(f"Missing JWT_SECRET environment variable! Set it to a random string.")

# Set reasonable defaults for Extractor
extractor = Extractor()
extractor.set_extract_string_max_length(-1)
extractor.set_xml_output(True)

async def require_auth_token(authorization: str = Header(...)):
    try:
        logging.info(f'Authorization: {authorization}')
        token = authorization.split(' ')[1]
        payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])
        return payload
    except Exception as e:
        logging.exception("Invalid token", e)
        raise HTTPException(status_code=401, detail="Invalid token! Ask an admin to make one for you at https://jwt.io")

app = FastAPI(docs_url='/', dependencies=[Depends(require_auth_token)])

@click.command()
@click.option('--input', help='Input file path', required=True)
def main(input):
    result, metadata = extractor.extract_file_to_string(input)
    print(result)
    print(metadata, file=sys.stderr)

@app.post('/xml')
async def post_xml(upload: UploadFile = File(...)):
    # Create a unique name for the temporary file
    # Extractous can only read paths to files :(
    temp_file_name = f"temp_{uuid.uuid4().hex}.tmp"
    with open(temp_file_name, 'wb') as f:
        data = await upload.read()
        f.write(data)

    result, metadata = extractor.extract_file_to_string(temp_file_name)

    os.remove(temp_file_name)

    return {
        'data': {
            'xml': result,
            'metadata': metadata
        }
    }

if __name__ == "__main__":
    main()
