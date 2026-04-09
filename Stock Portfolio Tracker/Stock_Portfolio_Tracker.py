# stock_portfolio_tracker_ui.py
import flet as ft
from datetime import datetime
import csv

# Hardcoded stock prices
STOCK_PRICES = {
    "AAPL": 180.50,
    "TSLA": 250.75,
    "GOOGL": 140.30,
    "MSFT": 330.20,
    "AMZN": 145.80,
    "META": 310.45,
    "NFLX": 480.90,
    "NVDA": 890.60
}

def main(page: ft.Page):
    # Page configuration
    page.title = "Stock Portfolio Tracker"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1200
    page.window_height = 700
    page.window_min_width = 900
    page.window_min_height = 600
    page.padding = 20
    
    # App state
    portfolio = {}
    
    # UI Components
    stock_dropdown = ft.Dropdown(
        label="Select Stock",
        width=300,
        options=[ft.dropdown.Option(symbol) for symbol in STOCK_PRICES.keys()],
        value="AAPL"
    )
    
    quantity_field = ft.TextField(
        label="Quantity",
        width=200,
        keyboard_type=ft.KeyboardType.NUMBER,
        suffix=ft.Text("shares")
    )
    
    add_button = ft.ElevatedButton(
        "Add to Portfolio",
        icon=ft.Icons.ADD_SHOPPING_CART,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.GREEN_700,
        width=200
    )
    
    # Portfolio Data Table
    portfolio_table = ft.DataTable(
        width=float("inf"),
        columns=[
            ft.DataColumn(ft.Text("Stock", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Quantity", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Price", weight=ft.FontWeight.BOLD), numeric=True),
            ft.DataColumn(ft.Text("Total Value", weight=ft.FontWeight.BOLD), numeric=True),
            ft.DataColumn(ft.Text("Actions", weight=ft.FontWeight.BOLD)),
        ],
        rows=[],
    )
    
    total_value_text = ft.Text("Total Portfolio Value: $0.00", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_400)
    
    # Stats Cards
    stocks_count_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("Stocks Owned", size=14, color=ft.Colors.GREY_400),
                ft.Text("0", size=32, weight=ft.FontWeight.BOLD),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            width=200,
        )
    )
    
    total_value_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("Total Value", size=14, color=ft.Colors.GREY_400),
                ft.Text("$0.00", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_400),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            width=200,
        )
    )
    
    def update_portfolio_display():
        """Update the UI with current portfolio data"""
        portfolio_table.rows.clear()
        
        if not portfolio:
            # Show empty state
            portfolio_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("No stocks in portfolio", italic=True, color=ft.Colors.GREY_400)),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                ])
            )
            total_value_text.value = "Total Portfolio Value: $0.00"
            total_value_card.content.content.controls[1].value = "$0.00"
            stocks_count_card.content.content.controls[1].value = "0"
        else:
            total_value = 0
            
            for symbol, quantity in portfolio.items():
                price = STOCK_PRICES[symbol]
                total = price * quantity
                total_value += total
                
                # Add row to table
                portfolio_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(symbol, weight=ft.FontWeight.BOLD)),
                            ft.DataCell(ft.Text(f"{quantity:.2f}")),
                            ft.DataCell(ft.Text(f"${price:.2f}")),
                            ft.DataCell(ft.Text(f"${total:.2f}", color=ft.Colors.GREEN_400 if total > 0 else ft.Colors.RED_400)),
                            ft.DataCell(
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE,
                                    icon_color=ft.Colors.RED_400,
                                    tooltip=f"Remove {symbol}",
                                    on_click=lambda e, s=symbol: remove_stock(s)
                                )
                            ),
                        ]
                    )
                )
            
            total_value_text.value = f"Total Portfolio Value: ${total_value:.2f}"
            total_value_card.content.content.controls[1].value = f"${total_value:.2f}"
            stocks_count_card.content.content.controls[1].value = str(len(portfolio))
        
        page.update()
    
    def add_stock_to_portfolio(e):
        """Add stock to portfolio"""
        if not quantity_field.value:
            page.snack_bar = ft.SnackBar(content=ft.Text("Please enter quantity"), bgcolor=ft.Colors.RED_400)
            page.snack_bar.open = True
            page.update()
            return
        
        try:
            quantity = float(quantity_field.value)
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
            
            stock_symbol = stock_dropdown.value
            
            if stock_symbol in portfolio:
                portfolio[stock_symbol] += quantity
                message = f"Added {quantity} more shares of {stock_symbol}"
            else:
                portfolio[stock_symbol] = quantity
                message = f"Added {quantity} shares of {stock_symbol}"
            
            # Show success message
            page.snack_bar = ft.SnackBar(content=ft.Text(message), bgcolor=ft.Colors.GREEN_400)
            page.snack_bar.open = True
            
            # Clear quantity field
            quantity_field.value = ""
            
            # Update display
            update_portfolio_display()
            
        except ValueError:
            page.snack_bar = ft.SnackBar(content=ft.Text("Please enter a valid positive number"), bgcolor=ft.Colors.RED_400)
            page.snack_bar.open = True
            page.update()
    
    def remove_stock(symbol):
        """Remove stock from portfolio"""
        if symbol in portfolio:
            del portfolio[symbol]
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Removed {symbol} from portfolio"), bgcolor=ft.Colors.ORANGE_400)
            page.snack_bar.open = True
            update_portfolio_display()
    
    def clear_all_stocks(e):
        """Clear all stocks from portfolio"""
        if portfolio:
            portfolio.clear()
            page.snack_bar = ft.SnackBar(content=ft.Text("All stocks removed from portfolio"), bgcolor=ft.Colors.ORANGE_400)
            page.snack_bar.open = True
            update_portfolio_display()
    
    def save_to_text_file(e):
        """Save portfolio to text file"""
        if not portfolio:
            page.snack_bar = ft.SnackBar(content=ft.Text("No stocks to save"), bgcolor=ft.Colors.RED_400)
            page.snack_bar.open = True
            page.update()
            return
        
        try:
            filename = f"portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w') as file:
                file.write("="*60 + "\n")
                file.write("STOCK PORTFOLIO REPORT\n")
                file.write("="*60 + "\n\n")
                
                file.write(f"{'Stock':<10} {'Quantity':<12} {'Price':<10} {'Total':<12}\n")
                file.write("-"*60 + "\n")
                
                total_value = 0
                for symbol, quantity in portfolio.items():
                    price = STOCK_PRICES[symbol]
                    total = price * quantity
                    total_value += total
                    file.write(f"{symbol:<10} {quantity:<12.2f} ${price:<9.2f} ${total:<11.2f}\n")
                
                file.write("-"*60 + "\n")
                file.write(f"{'TOTAL PORTFOLIO VALUE':<44} ${total_value:.2f}\n")
                file.write("="*60 + "\n")
                file.write(f"\nReport generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Portfolio saved to {filename}"), bgcolor=ft.Colors.GREEN_400)
            page.snack_bar.open = True
            page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Error saving file: {ex}"), bgcolor=ft.Colors.RED_400)
            page.snack_bar.open = True
            page.update()
    
    def save_to_csv_file(e):
        """Save portfolio to CSV file"""
        if not portfolio:
            page.snack_bar = ft.SnackBar(content=ft.Text("No stocks to save"), bgcolor=ft.Colors.RED_400)
            page.snack_bar.open = True
            page.update()
            return
        
        try:
            filename = f"portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = ['Symbol', 'Quantity', 'Price', 'Total Value']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                total_value = 0
                for symbol, quantity in portfolio.items():
                    price = STOCK_PRICES[symbol]
                    total = price * quantity
                    total_value += total
                    writer.writerow({
                        'Symbol': symbol,
                        'Quantity': f"{quantity:.2f}",
                        'Price': f"${price:.2f}",
                        'Total Value': f"${total:.2f}"
                    })
                
                writer.writerow({
                    'Symbol': 'TOTAL',
                    'Quantity': '',
                    'Price': '',
                    'Total Value': f"${total_value:.2f}"
                })
            
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Portfolio saved to {filename}"), bgcolor=ft.Colors.GREEN_400)
            page.snack_bar.open = True
            page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Error saving CSV: {ex}"), bgcolor=ft.Colors.RED_400)
            page.snack_bar.open = True
            page.update()
    
    # Attach event handlers
    add_button.on_click = add_stock_to_portfolio
    
    # Create available stocks grid
    stocks_grid = ft.GridView(
        expand=1,
        runs_count=4,
        max_extent=150,
        child_aspect_ratio=1.5,
        spacing=10,
        run_spacing=10,
    )
    
    for symbol, price in STOCK_PRICES.items():
        stocks_grid.controls.append(
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(symbol, size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(f"${price:.2f}", size=14, color=ft.Colors.GREEN_400),
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=15,
                ),
                elevation=2,
            )
        )
    
    # Left Panel - Stock Selection
    left_panel = ft.Container(
        content=ft.Column([
            ft.Text("Available Stocks", size=20, weight=ft.FontWeight.BOLD),
            ft.Container(height=10),
            stocks_grid,
            ft.Divider(),
            ft.Text("Add Stock to Portfolio", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(height=10),
            stock_dropdown,
            quantity_field,
            ft.Container(height=10),
            add_button,
        ], scroll=ft.ScrollMode.AUTO),
        width=350,
        bgcolor=ft.Colors.BLUE_GREY_900,
        border_radius=10,
        padding=15,
    )
    
    # Right Panel - Portfolio Display
    right_panel = ft.Container(
        content=ft.Column([
            ft.Text("My Portfolio", size=24, weight=ft.FontWeight.BOLD),
            ft.Row([
                stocks_count_card,
                total_value_card,
                ft.Container(expand=True),
                ft.IconButton(
                    icon=ft.Icons.CLEAR_ALL,
                    tooltip="Clear All Stocks",
                    on_click=clear_all_stocks,
                    icon_color=ft.Colors.RED_400,
                ),
            ], alignment=ft.MainAxisAlignment.START),
            ft.Container(height=10),
            ft.Container(
                content=ft.Column([
                    ft.ListView(
                        controls=[portfolio_table],
                        expand=True,
                        spacing=10,
                    ),
                ]),
                expand=True,
                border=ft.border.all(1, ft.Colors.GREY_800),
                border_radius=10,
                padding=10,
            ),
            total_value_text,
            ft.Divider(),
            ft.Row([
                ft.ElevatedButton(
                    "Save as Text File",
                    icon=ft.Icons.DOCUMENT_SCANNER,
                    on_click=save_to_text_file,
                ),
                ft.ElevatedButton(
                    "Save as CSV",
                    icon=ft.Icons.TABLE_CHART,
                    on_click=save_to_csv_file,
                ),
            ], alignment=ft.MainAxisAlignment.END),
        ], expand=True),
        expand=True,
        padding=15,
    )
    
    # Main layout
    main_layout = ft.Row([
        left_panel,
        ft.VerticalDivider(width=1),
        right_panel,
    ], expand=True, spacing=20)
    
    page.add(main_layout)
    
    # Initialize display
    update_portfolio_display()

if __name__ == "__main__":
    ft.run(main, view=ft.AppView.WEB_BROWSER)
