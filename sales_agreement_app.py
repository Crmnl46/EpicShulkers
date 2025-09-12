#!/usr/bin/env python3
"""
Sales Agreement Management Application (Verkaufsvereinbarungen)
A modern Python application for managing sales agreements with GUI.

Author: Crmnl46
License: MIT
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from datetime import datetime
import json
import csv
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import uuid
from PIL import Image as PILImage
from PIL import ImageTk
import tkinter.font as tkFont

class SalesAgreementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Verkaufsvereinbarungen - Sales Agreement Management")
        self.root.geometry("1200x800")
        self.root.configure(bg='white')
        
        # Color scheme as per requirements
        self.colors = {
            'bg': 'white',
            'text': '#4A90E2',  # Light blue
            'text_dark': 'black',
            'confirm': '#28A745',  # Green for yes/confirm
            'cancel': '#DC3545',   # Red for no/cancel
            'button_bg': '#F8F9FA'
        }
        
        # Data storage
        self.data_file = "sales_agreements.json"
        self.agreements = self.load_agreements()
        self.current_agreement = {}
        self.scanned_image_path = None
        
        # Create main interface
        self.create_styles()
        self.create_menu()
        self.create_main_interface()
        
    def create_styles(self):
        """Create custom styles for the application"""
        self.title_font = tkFont.Font(family="Arial", size=16, weight="bold")
        self.header_font = tkFont.Font(family="Arial", size=12, weight="bold")
        self.normal_font = tkFont.Font(family="Arial", size=10)
        
    def create_menu(self):
        """Create the menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Datei", menu=file_menu)
        file_menu.add_command(label="Neue Vereinbarung", command=self.new_agreement)
        file_menu.add_separator()
        file_menu.add_command(label="Monatsübersicht", command=self.monthly_overview)
        file_menu.add_command(label="Jahresübersicht", command=self.yearly_overview)
        file_menu.add_separator()
        file_menu.add_command(label="Als CSV exportieren", command=self.export_csv)
        file_menu.add_command(label="Als PDF speichern", command=self.save_pdf)
        file_menu.add_separator()
        file_menu.add_command(label="Beenden", command=self.root.quit)
        
        # Search menu
        search_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Suchen", menu=search_menu)
        search_menu.add_command(label="Nach KV-Nummer suchen", command=self.search_agreement)
        
    def create_main_interface(self):
        """Create the main interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, text="VERKAUFSVEREINBARUNG", 
                              font=self.title_font, fg=self.colors['text'], 
                              bg=self.colors['bg'])
        title_label.pack(pady=(0, 20))
        
        # Top section with KV number and date
        top_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        top_frame.pack(fill=tk.X, pady=(0, 20))
        
        # KV Number
        kv_frame = tk.Frame(top_frame, bg=self.colors['bg'])
        kv_frame.pack(side=tk.LEFT)
        
        tk.Label(kv_frame, text="KV-Nummer:", font=self.header_font, 
                fg=self.colors['text'], bg=self.colors['bg']).pack(anchor=tk.W)
        
        kv_input_frame = tk.Frame(kv_frame, bg=self.colors['bg'])
        kv_input_frame.pack(anchor=tk.W)
        
        tk.Label(kv_input_frame, text="KV", font=self.normal_font,
                fg=self.colors['text_dark'], bg=self.colors['bg']).pack(side=tk.LEFT)
        
        self.kv_number = tk.Entry(kv_input_frame, width=6, font=self.normal_font)
        self.kv_number.pack(side=tk.LEFT, padx=(2, 0))
        
        # Date
        date_frame = tk.Frame(top_frame, bg=self.colors['bg'])
        date_frame.pack(side=tk.RIGHT)
        
        tk.Label(date_frame, text="Datum:", font=self.header_font, 
                fg=self.colors['text'], bg=self.colors['bg']).pack(anchor=tk.E)
        
        self.date_entry = tk.Entry(date_frame, width=12, font=self.normal_font)
        self.date_entry.pack(anchor=tk.E)
        self.date_entry.insert(0, datetime.now().strftime("%d.%m.%Y"))
        
        # Image section
        image_frame = tk.Frame(top_frame, bg=self.colors['bg'])
        image_frame.pack(side=tk.RIGHT, padx=(20, 0))
        
        scan_button = tk.Button(image_frame, text="Ausweis scannen", 
                               command=self.scan_id_document,
                               bg=self.colors['button_bg'], fg=self.colors['text'],
                               font=self.normal_font)
        scan_button.pack()
        
        self.image_label = tk.Label(image_frame, text="Kein Bild", 
                                   width=15, height=8, relief=tk.SUNKEN,
                                   bg=self.colors['bg'])
        self.image_label.pack(pady=(5, 0))
        
        # Create notebook for tabbed interface
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Customer data tab
        self.create_customer_tab()
        
        # Electronics tab
        self.create_electronics_tab()
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        save_button = tk.Button(button_frame, text="Speichern", 
                               command=self.save_agreement,
                               bg=self.colors['confirm'], fg='white',
                               font=self.header_font, width=12)
        save_button.pack(side=tk.LEFT, padx=(0, 10))
        
        new_button = tk.Button(button_frame, text="Neue Vereinbarung", 
                              command=self.new_agreement,
                              bg=self.colors['button_bg'], fg=self.colors['text'],
                              font=self.normal_font, width=15)
        new_button.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_button = tk.Button(button_frame, text="Abbrechen", 
                                 command=self.cancel_agreement,
                                 bg=self.colors['cancel'], fg='white',
                                 font=self.normal_font, width=12)
        cancel_button.pack(side=tk.RIGHT)
        
    def create_customer_tab(self):
        """Create customer data tab"""
        customer_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(customer_frame, text="Kundendaten")
        
        # Create scrollable frame
        canvas = tk.Canvas(customer_frame, bg=self.colors['bg'])
        scrollbar = ttk.Scrollbar(customer_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Customer fields
        fields = [
            ("Vorname:", "first_name"),
            ("Nachname:", "last_name"),
            ("Adresse:", "address"),
            ("Geburtsdatum:", "birth_date"),
            ("Ausweisnummer:", "id_number")
        ]
        
        self.customer_entries = {}
        
        for i, (label, field) in enumerate(fields):
            row_frame = tk.Frame(scrollable_frame, bg=self.colors['bg'])
            row_frame.pack(fill=tk.X, pady=5, padx=20)
            
            tk.Label(row_frame, text=label, font=self.normal_font,
                    fg=self.colors['text'], bg=self.colors['bg'], width=15).pack(side=tk.LEFT, anchor=tk.W)
            
            if field == "address":
                entry = tk.Text(row_frame, height=3, width=50, font=self.normal_font)
            else:
                entry = tk.Entry(row_frame, width=50, font=self.normal_font)
            
            entry.pack(side=tk.LEFT, padx=(10, 0))
            self.customer_entries[field] = entry
        
        # ID Type dropdown
        id_frame = tk.Frame(scrollable_frame, bg=self.colors['bg'])
        id_frame.pack(fill=tk.X, pady=5, padx=20)
        
        tk.Label(id_frame, text="Ausweisart:", font=self.normal_font,
                fg=self.colors['text'], bg=self.colors['bg'], width=15).pack(side=tk.LEFT, anchor=tk.W)
        
        self.id_type = ttk.Combobox(id_frame, width=47, font=self.normal_font)
        self.id_type['values'] = ('Personalausweis', 'Reisepass', 'Führerschein', 'Aufenthaltstitel')
        self.id_type.pack(side=tk.LEFT, padx=(10, 0))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_electronics_tab(self):
        """Create electronics data tab"""
        electronics_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(electronics_frame, text="Elektronikgeräte")
        
        # Create scrollable frame
        canvas = tk.Canvas(electronics_frame, bg=self.colors['bg'])
        scrollbar = ttk.Scrollbar(electronics_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Electronics fields
        fields = [
            ("Marke:", "brand"),
            ("Typenbezeichnung:", "model"),
            ("Preis (€):", "price"),
            ("Seriennummer/IMEI:", "serial"),
            ("Sicherheitscode:", "security_code")
        ]
        
        self.electronics_entries = {}
        
        for i, (label, field) in enumerate(fields):
            row_frame = tk.Frame(scrollable_frame, bg=self.colors['bg'])
            row_frame.pack(fill=tk.X, pady=5, padx=20)
            
            tk.Label(row_frame, text=label, font=self.normal_font,
                    fg=self.colors['text'], bg=self.colors['bg'], width=20).pack(side=tk.LEFT, anchor=tk.W)
            
            entry = tk.Entry(row_frame, width=50, font=self.normal_font)
            entry.pack(side=tk.LEFT, padx=(10, 0))
            self.electronics_entries[field] = entry
        
        # Additional notes
        notes_frame = tk.Frame(scrollable_frame, bg=self.colors['bg'])
        notes_frame.pack(fill=tk.X, pady=5, padx=20)
        
        tk.Label(notes_frame, text="Sonstige Anmerkungen:", font=self.normal_font,
                fg=self.colors['text'], bg=self.colors['bg']).pack(anchor=tk.W)
        
        self.notes_entry = tk.Text(notes_frame, height=4, width=70, font=self.normal_font)
        self.notes_entry.pack(pady=(5, 0))
        
        # Standard annotation
        standard_frame = tk.Frame(scrollable_frame, bg=self.colors['bg'])
        standard_frame.pack(fill=tk.X, pady=20, padx=20)
        
        tk.Label(standard_frame, text="Standardanmerkung:", font=self.header_font,
                fg=self.colors['text'], bg=self.colors['bg']).pack(anchor=tk.W)
        
        standard_text = ("Der Verkäufer versichert dem Käufer, dass die oben bezeichneten "
                        "Geräte rechtmäßig erworben worden sind und nicht gestohlen wurden, "
                        "und dem Verkäufer die Herkunft der Geräte bekannt sind.")
        
        standard_label = tk.Label(standard_frame, text=standard_text, 
                                 font=self.normal_font, fg=self.colors['text_dark'], 
                                 bg=self.colors['bg'], wraplength=650, justify=tk.LEFT)
        standard_label.pack(anchor=tk.W, pady=(5, 0))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def scan_id_document(self):
        """Handle ID document scanning"""
        file_path = filedialog.askopenfilename(
            title="Ausweis-Bild auswählen",
            filetypes=[("Bilddateien", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        
        if file_path:
            try:
                # Load and resize image
                pil_image = PILImage.open(file_path)
                pil_image.thumbnail((150, 100), PILImage.Resampling.LANCZOS)
                
                # Convert for tkinter
                photo = ImageTk.PhotoImage(pil_image)
                self.image_label.configure(image=photo, text="")
                self.image_label.image = photo
                
                self.scanned_image_path = file_path
                messagebox.showinfo("Erfolg", "Ausweis-Bild erfolgreich geladen!")
                
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Laden des Bildes: {str(e)}")
    
    def new_agreement(self):
        """Create a new agreement"""
        self.clear_form()
        self.kv_number.focus()
        
    def clear_form(self):
        """Clear all form fields"""
        self.kv_number.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%d.%m.%Y"))
        
        for entry in self.customer_entries.values():
            if isinstance(entry, tk.Text):
                entry.delete(1.0, tk.END)
            else:
                entry.delete(0, tk.END)
        
        self.id_type.set("")
        
        for entry in self.electronics_entries.values():
            entry.delete(0, tk.END)
        
        self.notes_entry.delete(1.0, tk.END)
        
        self.image_label.configure(image="", text="Kein Bild")
        self.image_label.image = None
        self.scanned_image_path = None
        
    def save_agreement(self):
        """Save the current agreement"""
        # Validate required fields
        kv_num = self.kv_number.get().strip()
        if not kv_num:
            messagebox.showerror("Fehler", "Bitte geben Sie eine KV-Nummer ein!")
            return
        
        if not kv_num.isdigit() or len(kv_num) != 4:
            messagebox.showerror("Fehler", "KV-Nummer muss genau 4 Ziffern enthalten!")
            return
        
        full_kv = f"KV{kv_num}"
        
        # Check if KV number already exists
        if any(agreement['kv_number'] == full_kv for agreement in self.agreements):
            messagebox.showerror("Fehler", f"KV-Nummer {full_kv} existiert bereits!")
            return
        
        # Collect data
        agreement = {
            'id': str(uuid.uuid4()),
            'kv_number': full_kv,
            'date': self.date_entry.get(),
            'customer': {
                'first_name': self.customer_entries['first_name'].get(),
                'last_name': self.customer_entries['last_name'].get(),
                'address': self.customer_entries['address'].get(1.0, tk.END).strip(),
                'birth_date': self.customer_entries['birth_date'].get(),
                'id_type': self.id_type.get(),
                'id_number': self.customer_entries['id_number'].get()
            },
            'electronics': {
                'brand': self.electronics_entries['brand'].get(),
                'model': self.electronics_entries['model'].get(),
                'price': self.electronics_entries['price'].get(),
                'serial': self.electronics_entries['serial'].get(),
                'security_code': self.electronics_entries['security_code'].get(),
                'notes': self.notes_entry.get(1.0, tk.END).strip()
            },
            'image_path': self.scanned_image_path,
            'created_at': datetime.now().isoformat()
        }
        
        self.agreements.append(agreement)
        self.save_agreements()
        
        messagebox.showinfo("Erfolg", f"Verkaufsvereinbarung {full_kv} erfolgreich gespeichert!")
        self.clear_form()
        
    def cancel_agreement(self):
        """Cancel current agreement"""
        if messagebox.askquestion("Abbrechen", "Möchten Sie die aktuelle Vereinbarung wirklich abbrechen?",
                                 icon='warning') == 'yes':
            self.clear_form()
    
    def load_agreements(self):
        """Load agreements from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_agreements(self):
        """Save agreements to JSON file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.agreements, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern: {str(e)}")
    
    def search_agreement(self):
        """Search for agreement by KV number"""
        kv_num = simpledialog.askstring("Suchen", "KV-Nummer eingeben (z.B. KV1234):")
        if kv_num:
            if not kv_num.startswith("KV"):
                kv_num = f"KV{kv_num}"
            
            agreement = next((a for a in self.agreements if a['kv_number'] == kv_num), None)
            if agreement:
                self.load_agreement(agreement)
                messagebox.showinfo("Gefunden", f"Vereinbarung {kv_num} geladen!")
            else:
                messagebox.showwarning("Nicht gefunden", f"Vereinbarung {kv_num} nicht gefunden!")
    
    def load_agreement(self, agreement):
        """Load agreement data into form"""
        self.clear_form()
        
        # Set KV number (remove KV prefix)
        self.kv_number.insert(0, agreement['kv_number'][2:])
        
        # Set date
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, agreement['date'])
        
        # Set customer data
        customer = agreement['customer']
        self.customer_entries['first_name'].insert(0, customer.get('first_name', ''))
        self.customer_entries['last_name'].insert(0, customer.get('last_name', ''))
        self.customer_entries['address'].insert(1.0, customer.get('address', ''))
        self.customer_entries['birth_date'].insert(0, customer.get('birth_date', ''))
        self.customer_entries['id_number'].insert(0, customer.get('id_number', ''))
        self.id_type.set(customer.get('id_type', ''))
        
        # Set electronics data
        electronics = agreement['electronics']
        self.electronics_entries['brand'].insert(0, electronics.get('brand', ''))
        self.electronics_entries['model'].insert(0, electronics.get('model', ''))
        self.electronics_entries['price'].insert(0, electronics.get('price', ''))
        self.electronics_entries['serial'].insert(0, electronics.get('serial', ''))
        self.electronics_entries['security_code'].insert(0, electronics.get('security_code', ''))
        self.notes_entry.insert(1.0, electronics.get('notes', ''))
        
        # Load image if exists
        if agreement.get('image_path') and os.path.exists(agreement['image_path']):
            try:
                pil_image = PILImage.open(agreement['image_path'])
                pil_image.thumbnail((150, 100), PILImage.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(pil_image)
                self.image_label.configure(image=photo, text="")
                self.image_label.image = photo
                self.scanned_image_path = agreement['image_path']
            except:
                pass
    
    def monthly_overview(self):
        """Show monthly overview"""
        # Create window for month/year selection
        dialog = tk.Toplevel(self.root)
        dialog.title("Monatsübersicht")
        dialog.geometry("300x150")
        dialog.configure(bg=self.colors['bg'])
        
        tk.Label(dialog, text="Monat/Jahr auswählen:", font=self.header_font,
                fg=self.colors['text'], bg=self.colors['bg']).pack(pady=10)
        
        month_var = tk.StringVar(value=str(datetime.now().month))
        year_var = tk.StringVar(value=str(datetime.now().year))
        
        frame = tk.Frame(dialog, bg=self.colors['bg'])
        frame.pack(pady=10)
        
        tk.Label(frame, text="Monat:", fg=self.colors['text'], bg=self.colors['bg']).grid(row=0, column=0, padx=5)
        month_combo = ttk.Combobox(frame, textvariable=month_var, width=3)
        month_combo['values'] = [str(i) for i in range(1, 13)]
        month_combo.grid(row=0, column=1, padx=5)
        
        tk.Label(frame, text="Jahr:", fg=self.colors['text'], bg=self.colors['bg']).grid(row=0, column=2, padx=5)
        year_entry = tk.Entry(frame, textvariable=year_var, width=6)
        year_entry.grid(row=0, column=3, padx=5)
        
        def show_overview():
            month = int(month_var.get())
            year = int(year_var.get())
            self.show_period_overview(month, year)
            dialog.destroy()
        
        tk.Button(dialog, text="Anzeigen", command=show_overview,
                 bg=self.colors['confirm'], fg='white').pack(pady=10)
    
    def yearly_overview(self):
        """Show yearly overview"""
        year = simpledialog.askinteger("Jahresübersicht", "Jahr eingeben:", 
                                      initialvalue=datetime.now().year)
        if year:
            self.show_period_overview(None, year)
    
    def show_period_overview(self, month=None, year=None):
        """Show overview for specified period"""
        filtered_agreements = []
        
        for agreement in self.agreements:
            try:
                date_parts = agreement['date'].split('.')
                agreement_day = int(date_parts[0])
                agreement_month = int(date_parts[1])
                agreement_year = int(date_parts[2])
                
                if month:
                    if agreement_month == month and agreement_year == year:
                        filtered_agreements.append(agreement)
                else:
                    if agreement_year == year:
                        filtered_agreements.append(agreement)
            except:
                continue
        
        # Create overview window
        overview_window = tk.Toplevel(self.root)
        title = f"Monatsübersicht {month}/{year}" if month else f"Jahresübersicht {year}"
        overview_window.title(title)
        overview_window.geometry("800x600")
        overview_window.configure(bg=self.colors['bg'])
        
        # Create treeview
        columns = ('KV-Nummer', 'Datum', 'Kunde', 'Gerät', 'Preis')
        tree = ttk.Treeview(overview_window, columns=columns, show='headings', height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        # Populate data
        for agreement in filtered_agreements:
            customer_name = f"{agreement['customer'].get('first_name', '')} {agreement['customer'].get('last_name', '')}"
            device = f"{agreement['electronics'].get('brand', '')} {agreement['electronics'].get('model', '')}"
            price = agreement['electronics'].get('price', '')
            
            tree.insert('', tk.END, values=(
                agreement['kv_number'],
                agreement['date'],
                customer_name.strip(),
                device.strip(),
                f"{price} €" if price else ""
            ))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Export button
        export_btn = tk.Button(overview_window, text="Als CSV exportieren",
                              command=lambda: self.export_period_csv(filtered_agreements, title),
                              bg=self.colors['button_bg'], fg=self.colors['text'])
        export_btn.pack(pady=10)
    
    def export_csv(self):
        """Export all agreements to CSV"""
        filename = filedialog.asksaveasfilename(
            title="CSV-Datei speichern",
            defaultextension=".csv",
            filetypes=[("CSV-Dateien", "*.csv")]
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=';')
                    
                    # Header
                    writer.writerow(['KV-Nummer', 'Datum', 'Vorname', 'Nachname', 'Adresse', 
                                   'Geburtsdatum', 'Ausweisart', 'Ausweisnummer', 'Marke', 
                                   'Modell', 'Preis', 'Seriennummer', 'Sicherheitscode', 'Anmerkungen'])
                    
                    # Data
                    for agreement in self.agreements:
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
                
                messagebox.showinfo("Erfolg", f"CSV-Datei erfolgreich gespeichert: {filename}")
                
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Exportieren: {str(e)}")
    
    def export_period_csv(self, agreements, title):
        """Export period-specific agreements to CSV"""
        filename = filedialog.asksaveasfilename(
            title=f"{title} als CSV speichern",
            defaultextension=".csv",
            filetypes=[("CSV-Dateien", "*.csv")]
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=';')
                    
                    # Header
                    writer.writerow(['KV-Nummer', 'Datum', 'Kunde', 'Gerät', 'Preis'])
                    
                    # Data
                    for agreement in agreements:
                        customer = agreement['customer']
                        electronics = agreement['electronics']
                        customer_name = f"{customer.get('first_name', '')} {customer.get('last_name', '')}"
                        device = f"{electronics.get('brand', '')} {electronics.get('model', '')}"
                        
                        writer.writerow([
                            agreement['kv_number'],
                            agreement['date'],
                            customer_name.strip(),
                            device.strip(),
                            electronics.get('price', '')
                        ])
                
                messagebox.showinfo("Erfolg", f"CSV-Datei erfolgreich gespeichert: {filename}")
                
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Exportieren: {str(e)}")
    
    def save_pdf(self):
        """Save current agreement as PDF"""
        # Validate that we have data to save
        kv_num = self.kv_number.get().strip()
        if not kv_num:
            messagebox.showerror("Fehler", "Bitte geben Sie eine KV-Nummer ein!")
            return
        
        filename = filedialog.asksaveasfilename(
            title="PDF-Datei speichern",
            defaultextension=".pdf",
            filetypes=[("PDF-Dateien", "*.pdf")]
        )
        
        if filename:
            try:
                self.generate_pdf(filename)
                messagebox.showinfo("Erfolg", f"PDF erfolgreich gespeichert: {filename}")
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim PDF-Export: {str(e)}")
    
    def generate_pdf(self, filename):
        """Generate PDF for current agreement"""
        doc = SimpleDocTemplate(filename, pagesize=A4, topMargin=2*cm)
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
            [f"KV-Nummer: KV{self.kv_number.get()}", f"Datum: {self.date_entry.get()}"]
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
        
        customer_data = [
            ["Vorname:", self.customer_entries['first_name'].get()],
            ["Nachname:", self.customer_entries['last_name'].get()],
            ["Adresse:", self.customer_entries['address'].get(1.0, tk.END).strip()],
            ["Geburtsdatum:", self.customer_entries['birth_date'].get()],
            ["Ausweisart:", self.id_type.get()],
            ["Ausweisnummer:", self.customer_entries['id_number'].get()]
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
        
        electronics_data = [
            ["Marke:", self.electronics_entries['brand'].get()],
            ["Typenbezeichnung:", self.electronics_entries['model'].get()],
            ["Preis:", f"{self.electronics_entries['price'].get()} €"],
            ["Seriennummer/IMEI:", self.electronics_entries['serial'].get()],
            ["Sicherheitscode:", self.electronics_entries['security_code'].get()],
            ["Sonstige Anmerkungen:", self.notes_entry.get(1.0, tk.END).strip()]
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

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = SalesAgreementApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()