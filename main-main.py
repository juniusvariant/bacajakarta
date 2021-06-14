from fastapi import FastAPI, File, Form, UploadFile, Depends
from utils.asForm import as_form
from pydantic import BaseModel

@as_form
class Inner(BaseModel):
    tes: str

    class Config():
        orm_mode = True

@as_form
class Nested(BaseModel):
    foo: int
    bar: str

@as_form
class Outer(BaseModel):
    inner: Inner
    baz: float

app = FastAPI()


@app.post("/files/")
async def create_file(token: str = Form(None), file: bytes = File(...), fileb: UploadFile = File(...)
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }

@app.post("/test")
async def test_form(form: Outer = Depends(Outer.as_form)):
    return {"foo": form.inner.foo, "bar": form.inner.bar, "baz": form.baz}
