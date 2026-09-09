from app.ingestion.ingestion_manager import process_file


result = process_file("ppt content.pdf")

print(result["metadata"])

for paragraph in result["data"]:
    print(paragraph)
