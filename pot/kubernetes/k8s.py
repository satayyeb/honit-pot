import re

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from pot.llm import LLMApi
import json

from pot.models import Service

app = FastAPI()

k8s_service: Service
apis = {}


@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def catch_all(request: Request, full_path: str):
    method = request.method
    path = "/" + full_path
    try:
        payload = await request.json()
    except Exception:
        payload = None

    headers = dict(request.headers)
    kubectl_session = headers.get('kubectl-session', 'default-session')
    api = apis.get(kubectl_session)
    if not api:
        api = LLMApi(k8s_service, session_base=True)
        apis[kubectl_session] = api

    input_to_llm = {
        "method": method,
        "path": path,
        "headers": headers,
        "payload": payload
    }

    raw_response = api.chat(json.dumps(input_to_llm)).strip()

    # Strip ```json ... ``` if present
    if raw_response.startswith('```json'):
        raw_response = raw_response.removeprefix('```json').removesuffix('```').strip()
    elif raw_response.startswith('```'):
        raw_response = raw_response.removeprefix('```').removesuffix('```').strip()

    raw_response = re.sub(r"\n", "", raw_response)

    # Convert to dict
    try:
        response_data = json.loads(raw_response)

    except json.JSONDecodeError:
        response_data = {
            "kind": "Status",
            "apiVersion": "v1",
            "status": "Failure",
            "message": "LLM returned invalid JSON",
            "reason": "BadRequest",
            "code": 400
        }
    return JSONResponse(content=response_data)


def kubernetes_runner(service: Service):
    global k8s_service
    k8s_service = service
    uvicorn.run(app, host="127.0.0.1", port=service.port, ssl_certfile="pot/kubernetes/cert.pem",
                ssl_keyfile="pot/kubernetes/key.pem")
