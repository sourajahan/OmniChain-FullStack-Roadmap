import typer
from rich.console import Console
from rich.table import Table

from smartstock.domain.exceptions import SmartStockError
from smartstock.infra.db import SessionLocal
from smartstock.service.inventory_service import InventoryService

app = typer.Typer(help="SmartStock Inventory Management CLI")
console = Console()


@app.command()
def add(
    sku: str = typer.Option(..., "--sku", "-s", help="Unique product SKU"),
    name: str = typer.Option(..., "--name", "-n", help="Product name"),
    quantity: int = typer.Option(0, "--qty", "-q", help="Initial quantity"),
) -> None:
    """Add a new product to inventory."""
    try:
        with SessionLocal() as session:
            service = InventoryService(session)
            product = service.create_product(
                sku=sku, name=name, initial_quantity=quantity
            )
            session.commit()
            console.print(
                f"[green]Added:[/green] {product.sku} - {product.name} (qty: {product.quantity})"
            )
    except SmartStockError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(code=1)


@app.command()
def adjust(
    sku: str = typer.Option(..., "--sku", "-s", help="Product SKU"),
    delta: int = typer.Option(..., "--delta", "-d", help="Quantity change (+/-)"),
    reason: str = typer.Option(..., "--reason", "-r", help="Reason for adjustment"),
) -> None:
    """Adjust stock quantity for an existing product."""
    try:
        with SessionLocal() as session:
            service = InventoryService(session)
            product = service.adjust_stock(sku=sku, delta=delta, reason=reason)
            session.commit()
            console.print(
                f"[green]Updated:[/green] {product.sku} new qty: {product.quantity} ({reason})"
            )
    except SmartStockError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(code=1)


@app.command(name="list")
def list_products() -> None:
    """List all products in inventory."""
    with SessionLocal() as session:
        service = InventoryService(session)
        products = service.list_products()

    if not products:
        console.print("[yellow]No products found.[/yellow]")
        return

    table = Table(title="SmartStock Inventory")
    table.add_column("SKU", style="cyan", no_wrap=True)
    table.add_column("Name", style="white")
    table.add_column("Quantity", justify="right", style="green")

    for p in products:
        table.add_row(p.sku, p.name, str(p.quantity))

    console.print(table)


@app.command()
def show(
    sku: str = typer.Option(..., "--sku", "-s", help="Product SKU"),
) -> None:
    """Show product details and stock movement history."""
    try:
        with SessionLocal() as session:
            service = InventoryService(session)
            product = service.get_product(sku)
            console.print(
                f"[bold cyan]{product.sku}[/bold cyan] - {product.name} | Qty: [green]{product.quantity}[/green]"
            )
            if not product.movements:
                console.print("[yellow]No stock movements yet.[/yellow]")
                return

            table = Table(title="Stock Movements")
            table.add_column("ID", justify="right")
            table.add_column("Delta", justify="right")
            table.add_column("Reason")
            for m in product.movements:
                color = "green" if m.delta > 0 else "red"
                table.add_row(str(m.id), f"[{color}]{m.delta:+d}[/{color}]", m.reason)
            console.print(table)
    except SmartStockError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
