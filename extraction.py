import pandas as pd
from google.cloud import documentai_v1 as documentai

def online_process(
    location: str,
    processor_id: str,
    file_path: str,
    mime_type: str,
) -> documentai.Document:

    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}

    documentai_client = documentai.DocumentProcessorServiceClient(client_options=opts)

    resource_name = documentai_client.processor_path(location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as file:
        file_content = file.read()

    raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=resource_name, raw_document=raw_document)
    result = documentai_client.process_document(request=request)

    return result.document

LOCATION = "us" 
PROCESSOR_ID = "65204e0f795aa332" 
FILE_PATH = "google_invoice.pdf"
MIME_TYPE = "application/pdf"

document = online_process(
    location=LOCATION,
    processor_id=PROCESSOR_ID,
    file_path=FILE_PATH,
    mime_type=MIME_TYPE,
)

types = []
raw_values = []
normalized_values = []
confidence = []

for entity in document.entities:
    types.append(entity.type_)
    raw_values.append(entity.mention_text)
    normalized_values.append(entity.normalized_value.text)
    confidence.append(f"{entity.confidence:.0%}")

    for prop in entity.properties:
        types.append(prop.type_)
        raw_values.append(prop.mention_text)
        normalized_values.append(prop.normalized_value.text)
        confidence.append(f"{prop.confidence:.0%}")

df = pd.DataFrame(
    {
        "Type": types,
        "Raw Value": raw_values,
        "Normalized Value": normalized_values,
        "Confidence": confidence,
    }
)

print(df)