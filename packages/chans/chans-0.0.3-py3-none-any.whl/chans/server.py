from fastapi import FastAPI
from fastapi import Request
from fastapi import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from pathlib import Path
import subprocess

from chans import chans
from chans import util


static_folder = Path(__file__).parent / 'static'
templates = Jinja2Templates(directory=static_folder / 'templates')
templates.env.filters['format_time'] = util.format_time

app = FastAPI()
app.mount('/static/', StaticFiles(directory=static_folder), name='static')


@app.get('/favicon.ico', response_class=HTMLResponse)
async def favicon():
    return FileResponse(static_folder / 'favicon.ico')


@app.get('/', response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(
        'root.j2', {
            'request': request,
        },
    )


@app.get('/{chan}', response_class=HTMLResponse)
def get_chan(
    chan: str, 
    request: Request,
    sortby: str = 'posts_count',
):
    supported_chans = {
        '2ch': chans.Ch2,
        '4ch': chans.Ch4,
    }
    if chan not in supported_chans:
        raise HTTPException(status_code=404, detail='Chan not found')
    cls = supported_chans[chan]
    return templates.TemplateResponse(
        'chan.j2', {
            'request': request,
            'chan': chan,
            'threads': cls.boards_threads(sortby=sortby),
        },
    )


def main():
    cmd = ["uvicorn", "chans.server:app", "--host", "0.0.0.0", "--port", "8004"]
    subprocess.run(cmd)

if __name__ == '__main__':
    main()
