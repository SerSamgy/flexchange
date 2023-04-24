import jinja2
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates", loader=jinja2.PackageLoader("flexchange"))
