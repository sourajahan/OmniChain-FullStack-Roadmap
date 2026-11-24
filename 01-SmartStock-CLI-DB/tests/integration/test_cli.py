import uuid
from typer.testing import CliRunner

from smartstock.cli import app
from smartstock.infra.db import SessionLocal
from smartstock.infra.models import Product

runner = CliRunner()


def test_cli_add_adjust_show_and_list() -> None:
    sku = f"CLI-{uuid.uuid4().hex[:8].upper()}"

    try:
        res_add = runner.invoke(
            app, ["add", "--sku", sku, "--name", "CLI Keyboard", "--qty", "10"]
        )
        assert res_add.exit_code == 0
        assert "Added:" in res_add.stdout

        res_adj = runner.invoke(
            app, ["adjust", "--sku", sku, "--delta", "-3", "--reason", "order"]
        )
        assert res_adj.exit_code == 0
        assert "new qty: 7" in res_adj.stdout

        res_show = runner.invoke(app, ["show", "--sku", sku])
        assert res_show.exit_code == 0
        assert "CLI Keyboard" in res_show.stdout
        assert "order" in res_show.stdout

        res_list = runner.invoke(app, ["list"])
        assert res_list.exit_code == 0
        assert sku in res_list.stdout
    finally:
        with SessionLocal() as session:
            product = session.query(Product).filter_by(sku=sku).first()
            if product is not None:
                session.delete(product)
                session.commit()
