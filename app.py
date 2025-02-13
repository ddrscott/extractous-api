import click
import uuid
import os
import sys
from fastapi import FastAPI, File, UploadFile
from extractous import Extractor

# Set reasonable defaults
extractor = Extractor()
extractor = extractor.set_extract_string_max_length(-1)
extractor = extractor.set_xml_output(True)

app = FastAPI(docs_url='/')

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
