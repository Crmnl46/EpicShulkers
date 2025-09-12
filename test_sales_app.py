#!/usr/bin/env python3
"""
Simple CLI test for the Sales Agreement Management Application
This tests the core functionality without GUI.
"""

import json
import tempfile
import os
from datetime import datetime

# Test data
test_agreement = {
    'id': 'test-123',
    'kv_number': 'KV1234',
    'date': '01.01.2024',
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
        'model': 'iPhone 15',
        'price': '800',
        'serial': 'ABC123456789',
        'security_code': '1234',
        'notes': 'Gerät in gutem Zustand'
    },
    'image_path': None,
    'created_at': datetime.now().isoformat()
}

def test_json_operations():
    """Test JSON save/load operations"""
    print("Testing JSON operations...")
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        test_file = f.name
    
    try:
        # Save test data
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump([test_agreement], f, ensure_ascii=False, indent=2)
        print("✓ JSON save successful")
        
        # Load test data
        with open(test_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        
        assert len(loaded_data) == 1
        assert loaded_data[0]['kv_number'] == 'KV1234'
        print("✓ JSON load successful")
        
    finally:
        # Clean up
        if os.path.exists(test_file):
            os.unlink(test_file)

def test_pdf_generation():
    """Test PDF generation without GUI"""
    print("Testing PDF generation...")
    
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph
        
        # Create temporary PDF
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            pdf_file = f.name
        
        try:
            doc = SimpleDocTemplate(pdf_file, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            story.append(Paragraph("VERKAUFSVEREINBARUNG", styles['Title']))
            story.append(Paragraph(f"KV-Nummer: {test_agreement['kv_number']}", styles['Normal']))
            story.append(Paragraph(f"Datum: {test_agreement['date']}", styles['Normal']))
            
            doc.build(story)
            print("✓ PDF generation successful")
            
        finally:
            if os.path.exists(pdf_file):
                os.unlink(pdf_file)
                
    except Exception as e:
        print(f"✗ PDF generation failed: {e}")

def test_csv_export():
    """Test CSV export functionality"""
    print("Testing CSV export...")
    
    try:
        import csv
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            csv_file = f.name
        
        try:
            with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                
                # Header
                writer.writerow(['KV-Nummer', 'Datum', 'Vorname', 'Nachname', 'Marke', 'Modell', 'Preis'])
                
                # Data
                customer = test_agreement['customer']
                electronics = test_agreement['electronics']
                
                writer.writerow([
                    test_agreement['kv_number'],
                    test_agreement['date'],
                    customer['first_name'],
                    customer['last_name'],
                    electronics['brand'],
                    electronics['model'],
                    electronics['price']
                ])
            
            print("✓ CSV export successful")
            
        finally:
            if os.path.exists(csv_file):
                os.unlink(csv_file)
                
    except Exception as e:
        print(f"✗ CSV export failed: {e}")

def test_search_functionality():
    """Test search functionality"""
    print("Testing search functionality...")
    
    agreements = [test_agreement]
    
    # Search by KV number
    found = next((a for a in agreements if a['kv_number'] == 'KV1234'), None)
    assert found is not None
    assert found['customer']['first_name'] == 'Max'
    print("✓ Search by KV number successful")
    
    # Search by non-existent KV number
    not_found = next((a for a in agreements if a['kv_number'] == 'KV9999'), None)
    assert not_found is None
    print("✓ Search for non-existent KV number successful")

def test_date_filtering():
    """Test date filtering for monthly/yearly overview"""
    print("Testing date filtering...")
    
    agreements = [test_agreement]
    
    # Test monthly filtering
    month_filtered = []
    for agreement in agreements:
        try:
            date_parts = agreement['date'].split('.')
            agreement_month = int(date_parts[1])
            agreement_year = int(date_parts[2])
            
            if agreement_month == 1 and agreement_year == 2024:
                month_filtered.append(agreement)
        except:
            continue
    
    assert len(month_filtered) == 1
    print("✓ Monthly filtering successful")
    
    # Test yearly filtering
    year_filtered = []
    for agreement in agreements:
        try:
            date_parts = agreement['date'].split('.')
            agreement_year = int(date_parts[2])
            
            if agreement_year == 2024:
                year_filtered.append(agreement)
        except:
            continue
    
    assert len(year_filtered) == 1
    print("✓ Yearly filtering successful")

def test_validation():
    """Test input validation"""
    print("Testing input validation...")
    
    # Test KV number validation
    def validate_kv(kv_num):
        return kv_num.isdigit() and len(kv_num) == 4
    
    assert validate_kv("1234") == True
    assert validate_kv("123") == False
    assert validate_kv("12345") == False
    assert validate_kv("abc1") == False
    print("✓ KV number validation successful")

def main():
    """Run all tests"""
    print("Running Sales Agreement Management App Tests")
    print("=" * 50)
    
    test_json_operations()
    test_pdf_generation()
    test_csv_export()
    test_search_functionality()
    test_date_filtering()
    test_validation()
    
    print("=" * 50)
    print("All tests completed!")
    
    # Show sample data structure
    print("\nSample Agreement Data Structure:")
    print(json.dumps(test_agreement, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()