# Stock Portfolio Tracker
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

def calculate_investment(stock_name, quantity):
    """Calculate total investment for a single stock"""
    if stock_name in STOCK_PRICES:
        return STOCK_PRICES[stock_name] * quantity
    else:
        return None

def display_available_stocks():
    """Show user which stocks are available"""
    print("\n📊 Available Stocks:")
    print("-" * 40)
    for symbol, price in STOCK_PRICES.items():
        print(f"  {symbol}: ${price:.2f}")
    print("-" * 40)

def get_user_portfolio():
    """Get stock holdings from user"""
    portfolio = {}
    
    print("\n" + "="*50)
    print("💰 STOCK PORTFOLIO TRACKER 💰")
    print("="*50)
    
    display_available_stocks()
    
    while True:
        print("\n📝 Enter stock details (or 'done' to finish):")
        stock_symbol = input("Stock Symbol: ").upper()
        
        if stock_symbol == 'DONE':
            break
        
        if stock_symbol not in STOCK_PRICES:
            print(f"❌ '{stock_symbol}' not found in available stocks!")
            print("Please choose from the list above.")
            continue
        
        try:
            quantity = float(input(f"Quantity of {stock_symbol}: "))
            if quantity <= 0:
                print("❌ Quantity must be positive!")
                continue
            
            if stock_symbol in portfolio:
                portfolio[stock_symbol] += quantity
                print(f"✅ Added {quantity} more shares of {stock_symbol}")
            else:
                portfolio[stock_symbol] = quantity
                print(f"✅ Added {quantity} shares of {stock_symbol}")
                
        except ValueError:
            print("❌ Invalid quantity! Please enter a number.")
    
    return portfolio

def calculate_total_portfolio(portfolio):
    """Calculate total investment value"""
    total_value = 0
    stock_details = []
    
    print("\n" + "="*50)
    print("📈 PORTFOLIO SUMMARY")
    print("="*50)
    print(f"{'Stock':<10} {'Quantity':<10} {'Price':<10} {'Total':<12}")
    print("-"*50)
    
    for symbol, quantity in portfolio.items():
        price = STOCK_PRICES[symbol]
        total = price * quantity
        total_value += total
        
        print(f"{symbol:<10} {quantity:<10.2f} ${price:<9.2f} ${total:<11.2f}")
        stock_details.append({
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'total': total
        })
    
    print("-"*50)
    print(f"{'TOTAL INVESTMENT':<42} ${total_value:.2f}")
    print("="*50)
    
    return total_value, stock_details

def save_to_file(portfolio, total_value, stock_details, filename="portfolio.txt"):
    """Save portfolio data to a text file"""
    try:
        with open(filename, 'w') as file:
            file.write("="*60 + "\n")
            file.write("STOCK PORTFOLIO REPORT\n")
            file.write("="*60 + "\n\n")
            
            file.write(f"{'Stock':<10} {'Quantity':<12} {'Price':<10} {'Total':<12}\n")
            file.write("-"*60 + "\n")
            
            for item in stock_details:
                file.write(f"{item['symbol']:<10} {item['quantity']:<12.2f} ${item['price']:<9.2f} ${item['total']:<11.2f}\n")
            
            file.write("-"*60 + "\n")
            file.write(f"{'TOTAL PORTFOLIO VALUE':<44} ${total_value:.2f}\n")
            file.write("="*60 + "\n")
            
            # Add timestamp
            from datetime import datetime
            file.write(f"\nReport generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        print(f"\n💾 Portfolio saved to '{filename}' successfully!")
        return True
    except Exception as e:
        print(f"\n❌ Error saving file: {e}")
        return False

def save_to_csv(portfolio, total_value, stock_details, filename="portfolio.csv"):
    """Save portfolio data to a CSV file"""
    try:
        import csv
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['Symbol', 'Quantity', 'Price', 'Total Value']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for item in stock_details:
                writer.writerow({
                    'Symbol': item['symbol'],
                    'Quantity': f"{item['quantity']:.2f}",
                    'Price': f"${item['price']:.2f}",
                    'Total Value': f"${item['total']:.2f}"
                })
            
            # Add total row
            writer.writerow({
                'Symbol': 'TOTAL',
                'Quantity': '',
                'Price': '',
                'Total Value': f"${total_value:.2f}"
            })
        
        print(f"\n💾 Portfolio saved to '{filename}' (CSV format) successfully!")
        return True
    except Exception as e:
        print(f"\n❌ Error saving CSV file: {e}")
        return False

def main():
    # Get user's portfolio
    portfolio = get_user_portfolio()
    
    if not portfolio:
        print("\n❌ No stocks entered. Exiting...")
        return
    
    # Calculate and display total
    total_value, stock_details = calculate_total_portfolio(portfolio)
    
    # Ask if user wants to save results
    while True:
        save_option = input("\n💾 Save results to file? (yes/no): ").lower()
        if save_option in ['yes', 'y']:
            print("\nSave options:")
            print("1. Text file (.txt)")
            print("2. CSV file (.csv)")
            print("3. Both")
            
            choice = input("Choose option (1/2/3): ")
            
            if choice == '1':
                save_to_file(portfolio, total_value, stock_details)
            elif choice == '2':
                save_to_csv(portfolio, total_value, stock_details)
            elif choice == '3':
                save_to_file(portfolio, total_value, stock_details)
                save_to_csv(portfolio, total_value, stock_details)
            else:
                print("❌ Invalid choice. Files not saved.")
            break
        elif save_option in ['no', 'n']:
            print("\n✅ Portfolio not saved.")
            break
        else:
            print("❌ Please enter 'yes' or 'no'")
    
    print("\n🎉 Thank you for using Stock Portfolio Tracker! 🎉")

if __name__ == "__main__":
    main()
    