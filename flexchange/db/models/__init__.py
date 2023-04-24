"""flexchange models."""
import pkgutil
from pathlib import Path

from flexchange.db.models.trade import Directions, Trade
from flexchange.db.models.trader import Trader
from flexchange.db.models.user import User

__all__ = ["Directions", "Trade", "Trader", "User"]


def load_all_models() -> None:
    """Load all models from this folder."""
    package_dir = Path(__file__).resolve().parent
    modules = pkgutil.walk_packages(
        path=[str(package_dir)],
        prefix="flexchange.db.models.",
    )
    for module in modules:
        __import__(module.name)  # noqa: WPS421
