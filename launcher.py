#!/usr/bin/env python3
"""
Simple CLI launcher for the Sales Agreement Management Application
This provides a command-line interface when GUI is not available.
"""

import os
import sys
import json
from datetime import datetime

def check_gui_available():
    """Check if GUI is available"""
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Hide the window
        root.destroy()
        return True
    except:
        return False

def create_sample_agreement():
    """Create a sample agreement for demonstration"""
    print("Creating sample agreement...")
    
    agreement = {
        'id': 'sample-001',
        'kv_number': 'KV0001',
        'date': datetime.now().strftime("%d.%m.%Y"),
        'customer': {
            'first_name': 'Max',
            'last_name': 'Mustermann',
            'address': 'Musterstraße 1\n12345 Musterstadt',
            'birth_date': '01.01.1990',
            'id_type': 'Personalausweis',
            'id_number': 'DE123456789'
        },
        'electronics': {
            'brand': 'Apple',
            'model': 'iPhone 15 Pro',
            'price': '1200',
            'serial': 'ABC123456789DEF',
            'security_code': '1234',
            'notes': 'Gerät in sehr gutem Zustand, ohne Kratzer'
        },
        'image_path': None,
        'created_at': datetime.now().isoformat()
    }
    
    # Save to file
    data_file = "sales_agreements.json"
    agreements = []
    
    if os.path.exists(data_file):
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                agreements = json.load(f)
        except:
            agreements = []
    
    agreements.append(agreement)
    
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(agreements, f, ensure_ascii=False, indent=2)
    
    print(f"Sample agreement {agreement['kv_number']} created and saved!")
    return agreement

def export_sample_csv():
    """Export agreements to CSV for demonstration"""
    import csv
    
    data_file = "sales_agreements.json"
    if not os.path.exists(data_file):
        print("No agreements found. Creating sample agreement first...")
        create_sample_agreement()
    
    with open(data_file, 'r', encoding='utf-8') as f:
        agreements = json.load(f)
    
    csv_file = f"agreements_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        
        # Header
        writer.writerow(['KV-Nummer', 'Datum', 'Vorname', 'Nachname', 'Adresse', 
                        'Geburtsdatum', 'Ausweisart', 'Ausweisnummer', 'Marke', 
                        'Modell', 'Preis', 'Seriennummer', 'Sicherheitscode', 'Anmerkungen'])
        
        # Data
        for agreement in agreements:
            customer = agreement['customer']
            electronics = agreement['electronics']
            
            writer.writerow([
                agreement['kv_number'],
                agreement['date'],
                customer.get('first_name', ''),
                customer.get('last_name', ''),
                customer.get('address', '').replace('\n', ' '),
                customer.get('birth_date', ''),
                customer.get('id_type', ''),
                customer.get('id_number', ''),
                electronics.get('brand', ''),
                electronics.get('model', ''),
                electronics.get('price', ''),
                electronics.get('serial', ''),
                electronics.get('security_code', ''),
                electronics.get('notes', '').replace('\n', ' ')
            ])
    
    print(f"CSV exported to: {csv_file}")

def export_sample_pdf():
    """Export sample agreement to PDF"""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    
    data_file = "sales_agreements.json"
    if not os.path.exists(data_file):
        print("No agreements found. Creating sample agreement first...")
        create_sample_agreement()
    
    with open(data_file, 'r', encoding='utf-8') as f:
        agreements = json.load(f)
    
    if not agreements:
        print("No agreements to export.")
        return
    
    agreement = agreements[0]  # Use first agreement
    pdf_file = f"agreement_{agreement['kv_number']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    doc = SimpleDocTemplate(pdf_file, pagesize=A4, topMargin=2*cm)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=30
    )
    story.append(Paragraph("VERKAUFSVEREINBARUNG", title_style))
    
    # KV Number and Date
    header_data = [
        [f"KV-Nummer: {agreement['kv_number']}", f"Datum: {agreement['date']}"]
    ]
    header_table = Table(header_data, colWidths=[8*cm, 8*cm])
    header_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 20))
    
    # Customer Data
    story.append(Paragraph("Kundendaten", styles['Heading2']))
    
    customer = agreement['customer']
    customer_data = [
        ["Vorname:", customer.get('first_name', '')],
        ["Nachname:", customer.get('last_name', '')],
        ["Adresse:", customer.get('address', '')],
        ["Geburtsdatum:", customer.get('birth_date', '')],
        ["Ausweisart:", customer.get('id_type', '')],
        ["Ausweisnummer:", customer.get('id_number', '')]
    ]
    
    customer_table = Table(customer_data, colWidths=[4*cm, 12*cm])
    customer_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    story.append(customer_table)
    story.append(Spacer(1, 20))
    
    # Electronics Data
    story.append(Paragraph("Elektronikgeräte", styles['Heading2']))
    
    electronics = agreement['electronics']
    electronics_data = [
        ["Marke:", electronics.get('brand', '')],
        ["Typenbezeichnung:", electronics.get('model', '')],
        ["Preis:", f"{electronics.get('price', '')} €"],
        ["Seriennummer/IMEI:", electronics.get('serial', '')],
        ["Sicherheitscode:", electronics.get('security_code', '')],
        ["Sonstige Anmerkungen:", electronics.get('notes', '')]
    ]
    
    electronics_table = Table(electronics_data, colWidths=[4*cm, 12*cm])
    electronics_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    story.append(electronics_table)
    story.append(Spacer(1, 30))
    
    # Standard annotation
    story.append(Paragraph("Rechtliche Bestätigung", styles['Heading2']))
    standard_text = ("Der Verkäufer versichert dem Käufer, dass die oben bezeichneten "
                    "Geräte rechtmäßig erworben worden sind und nicht gestohlen wurden, "
                    "und dem Verkäufer die Herkunft der Geräte bekannt sind.")
    story.append(Paragraph(standard_text, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    print(f"PDF exported to: {pdf_file}")

def show_menu():
    """Show the CLI menu"""
    print("\n" + "="*60)
    print("    VERKAUFSVEREINBARUNGEN - Sales Agreement Management")
    print("="*60)
    print("1. Create sample agreement")
    print("2. Export agreements to CSV")
    print("3. Export sample agreement to PDF")
    print("4. Start GUI application (if available)")
    print("5. Run tests")
    print("6. Show current agreements")
    print("0. Exit")
    print("="*60)

def show_agreements():
    """Show current agreements"""
    data_file = "sales_agreements.json"
    if not os.path.exists(data_file):
        print("No agreements found.")
        return
    
    with open(data_file, 'r', encoding='utf-8') as f:
        agreements = json.load(f)
    
    if not agreements:
        print("No agreements found.")
        return
    
    print(f"\nFound {len(agreements)} agreement(s):")
    print("-" * 80)
    
    for agreement in agreements:
        customer = agreement['customer']
        electronics = agreement['electronics']
        
        print(f"KV-Nummer: {agreement['kv_number']}")
        print(f"Datum: {agreement['date']}")
        print(f"Kunde: {customer.get('first_name', '')} {customer.get('last_name', '')}")
        print(f"Gerät: {electronics.get('brand', '')} {electronics.get('model', '')}")
        print(f"Preis: {electronics.get('price', '')} €")
        print("-" * 80)

def main():
    """Main CLI interface"""
    print("Sales Agreement Management Application")
    print("Developed for Python 3.13 with modern GUI")
    
    # Check if GUI is available
    gui_available = check_gui_available()
    
    if not gui_available:
        print("\nNote: GUI is not available in this environment.")
        print("Using CLI interface instead.")
    
    while True:
        show_menu()
        
        try:
            choice = input("Choose an option (0-6): ").strip()
            
            if choice == "0":
                print("Goodbye!")
                break
            elif choice == "1":
                create_sample_agreement()
            elif choice == "2":
                export_sample_csv()
            elif choice == "3":
                export_sample_pdf()
            elif choice == "4":
                if gui_available:
                    print("Starting GUI application...")
                    # Import and run the GUI app
                    try:
                        from sales_agreement_app import SalesAgreementApp
                        import tkinter as tk
                        root = tk.Tk()
                        app = SalesAgreementApp(root)
                        root.mainloop()
                    except Exception as e:
                        print(f"Error starting GUI: {e}")
                else:
                    print("GUI is not available in this environment.")
            elif choice == "5":
                print("Running tests...")
                os.system("python3 test_sales_app.py")
            elif choice == "6":
                show_agreements()
            else:
                print("Invalid choice. Please try again.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()