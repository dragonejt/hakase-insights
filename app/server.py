from os import getenv
from typing import Annotated

import sentry_sdk
from fastapi import Depends, FastAPI, Header, HTTPException
from httpx import AsyncClient, HTTPStatusError
from langserve import add_routes

from app.chains import date_time_runnable

DEBUG = getenv("ENV") != "production"
if DEBUG is False:
    sentry_sdk.init(
        dsn="https://b4cecd13d2182474676b78a7cc6c61f7@o4507124907638784.ingest.us.sentry.io/4509120901939200",
        send_default_pii=True,
        enable_tracing=True,
        traces_sample_rate=1,
        profiles_sample_rate=1,
        environment=getenv("ENV"),
    )


async def auth(
    authorization: Annotated[str, Header(alias="authorization")],
    course: Annotated[str, Header(alias="x-hakase-course")],
):
    backend_url = getenv("BACKEND_URL")
    async with AsyncClient() as client:
        try:
            (
                await client.get(
                    f"{backend_url}/courses?course_id={course}",
                    headers={"authorization": authorization},
                )
            ).raise_for_status()
        except HTTPStatusError as err:
            raise HTTPException(status_code=err.response.status_code, detail=err.response.text)


app = FastAPI(
    title="hakase-insights",
    summary="Class Academic Insights from hakase, powered by AI",
    debug=DEBUG,
    redoc_url="/",
)

add_routes(app, date_time_runnable(), path="/datetime", dependencies=[Depends(auth)])
