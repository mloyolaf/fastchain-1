from fastapi import APIRouter

router = APIRouter()

def metadata_func(record: dict, metadata: dict) -> dict:

    print(record)
    metadata["description"] = record.get("description")
    metadata["attrib_name"] = record.get("name")

    return metadata

@router.get("/{context_id}")
async def read(context_id):
    return { 'context': context_id }

@router.put("/{context_id}")
async def read(context_id):
    return { 'context': context_id }

@router.patch("/{context_id}")
async def read(context_id):
    return { 'context': context_id }

@router.delete("/{context_id}")
async def read(context_id):
    return { 'context': context_id }
