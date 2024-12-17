import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

def validate_supplier_data(name, tier):
    """Make sure tier number is an accepted value."""
    if tier not in [1, 2, 3, 4]:
        raise ValueError("Tier must be 1, 2, 3, or 4")
    try:
        # Try to load existing data to check for duplicates.
        existing_df = pd.read_csv(('f35_suppliers.csv'))
        if name in existing_df['Company_Name'].values:
            raise ValueError(f"Supplier {name} already exists in database")
    except FileNotFoundError:
        pass

def upload_supplier(name, ticker, tier, location, component, customer, source,
        note=None):
    """Upload suppliers into DataFrame."""
    try:
        # Call the validation function first.
        validate_supplier_data(name, tier)

        # Try to load existing data
        try:
            suppliers = pd.read_csv('f35_suppliers.csv')
        except FileNotFoundError:
            suppliers = pd. DataFrame(columns=['Company_Name', 'Ticker_Symbol',
                        'Location', 'Component_Type', 'Primary_Customer',
                        'Source', 'Additional_Notes'])

        # Add new row to DataFrame
        new_row = {
            'Company_Name': name,
            'Ticker_Symbol': ticker,
            'Tier_Level': tier,
            'Location': location,
            'Component_Type': component,
            'Primary_Customer': customer,
            'Source': source,
            'Additional_Notes': note
        }

        suppliers = pd.concat([suppliers, pd.DataFrame([new_row])], 
                           ignore_index=True)

        # Save updated DataFrame
        suppliers.to_csv('f35_suppliers.csv', index=False)

        # Print current state
        print("\nCurrent Supplier List:")
        print(suppliers)
    
    except Exception as e:
        print(f"Error adding supplier {name}: {str(e)}")

def delete_supplier(name):
    """Delete a supplier from the DataFrame."""
    try:
        # Load existing data.
        suppliers = pd.read_csv('f35_suppliers.csv')

        # Check if supplier exists.
        if name not in suppliers['Company_Name'].values:
            print(f"Error: Supplier {name} not found in database")

        # Remove the supplier
        suppliers = suppliers[suppliers['Company_Name'] != name]

        # Save updated DataFrame.
        suppliers.to_csv('f35_suppliers.csv', index=False)

        print(f"\nSupplier {name} deleted.")
        print(f"\nCurrent Supplier List:")
        print(suppliers)

    except FileNotFoundError:
        print("Error: No supplier database found")
    except Exception as e:
        print(f"Error deleting supplier {name}: {str(e)}")

def update_supplier(name, **updates):
    """Update information for an existing supplier."""
    try:
        # Load existing data.
        suppliers = pd.read_csv('f35_suppliers.csv')

        # Check if supplier exists.
        if name not in suppliers['Company_Name'].values:
            print(f"Error: {name} not found in database")
            return
        
        # Update the specified fields.
        for field, new_value in updates.items():
            if field in suppliers.columns:
                suppliers.loc[suppliers['Company_Name'] == name, 
                              field] = new_value
            else: 
                print(f"Warning: Field '{field}' not found in database")
                return
            
        # Save updated DataFrame
        suppliers.to_csv('f35_suppliers.csv', index=False)

        print(f"Supplier {name} updated.")
        print("\nCurrent Supplier List:")
        print(suppliers)

    except FileNotFoundError:
        print("Error: No supplier database found")
    except Exception as e:
        print(f"Error updating supplier {name}: {str(e)}")

def find_tier(tier):
    """Return suppliers for a certain tier."""
    suppliers = pd.read_csv('f35_suppliers.csv')
    
    public_companies = suppliers[
        (suppliers['Ticker_Symbol'].notna()) &
        (suppliers['Tier_Level'] == tier)
    ]

    if len(public_companies) == [0]:
        print(f"There are no public companies in tier {tier}")

    print(f"Public companies in tier {tier}:")
    print(public_companies[['Company_Name', 'Ticker_Symbol', 'Additional_Notes']])


def main():
    """Store previously uploaded suppliers."""
    upload_supplier('Northrop Grumman', 'NOC', 1, 'El Segundo, CA', 
        'Center Fuselage', 'Lockheed Martin', 'Company Website')

    upload_supplier('BAE Systems', 'BAESY', 1, 'UK', 'Aft Fuselage',
        'Lockheed Martin', 'Company Website')

    upload_supplier('Pratt & Whitney', 'RTX', 1, 'East Hartfort, CT', 
        'F135 Engine', 'Lockheed Martin', 'Company Website')

    upload_supplier('L3Harris', 'LHX', 1, 'Various US', 'Avionics Systems', 
        'Lockheed Martin', 'Company Website')

    upload_supplier('Applied Aerospace Structures', 'N/A', 2, 'Cookstown, NJ',
        'Aircraft Structures', 'Northrop Grumman', 'Supplier Awards')

    upload_supplier('CohesionForce Inc.', 'N/A', 2, 'Various',
        'Engineering Services', 'Northrop Grumman', 'Supplier Awards')
    
    upload_supplier('Jackson Aerospace', 'N/A', 2, 'Various', 'Aerospace Parts',
        'Northrop Grumman', 'Supplier Awards')
    
    upload_supplier('Plexsys Interface Products', 'N/A', 2, 'Camas, Washington',  
        'Interface Systems', 'Northrop Grumman', 'Supplier Awards')

    upload_supplier('Advanced Wire and Cable', 'N/A', 2, 'Dayton, Ohio', 
        'Wiring Systems', 'Northrop Grumman', 'Supplier Awards')

    upload_supplier('Integrated Polymer Industries', 'N/A', 2, 'Irvine, CA',
        'Polymer Products', 'Northrop Grumman', 'Supplier Awards')

    upload_supplier('Jacon Fasteners & Electronics', 'N/A', 2, 'LA, CA', 
        'Fasteners/Electronics', 'Northrop Grumman', 'Supplier Awards')

    upload_supplier('Leonardo DRS', 'N/A', 2, 'Arlington, VA', 
        'Defense Technology', 'BAE Systems', 'Supplier Awards')

    upload_supplier('QuickLogic Corporation', 'QUIK', 2, 'San Jose, Ca',
        'FPGA Electronics', 'BAE Systems', 'Supplier Awards')

    upload_supplier('RFMW', 'N/A', 2, 'San Jose, CA', 'RF/Microwave Component',
        'BAE Systems', 'Supplier Awards')

    upload_supplier('PGM Corporation', 'N/A', 2, 'Rochester, NY', 
        'Precision Manufacturing', 'BAE Systems', 'Supplier Awards')

    upload_supplier('FAG Aerospace (Schaeffler)', 'SHA.DE', 2, 
        'Schweinfurt, Germany','Engine Components', 'Pratt & Whitney', 
        'Supplier Awards')

    upload_supplier('American Cladding Technologies', 'N/A', 2, 
        'East Granby, CT', 'Surface Technologies', 'Pratt & Whitney', 
        'Supplier Awards')

    upload_supplier('Tube Processing', 'N/A', 2, 'Indianapolis, IN', 
        'Engine Components', 'Pratt & Whitney', 'Supplier Awards')

    upload_supplier('MDS Coating Technologies', 'N/A', 2, 'Quebec, Canada',
        'Specialized Coatings', 'Pratt & Whitney', 'Supplier Awards')

    upload_supplier('MB Aerospace', 'N/A', 2, 'United Kingsom', 
        'Engine Components', 'Pratt & Whitney', 'Supplier Awards')

    upload_supplier('Horiguchi Engineering', 'N/A', 2, 'West Java, Indonesia',
        'Engine Stands', 'Pratt & Whitney', 'Supplier Awards')
    
    upload_supplier('American Aircraft Products', 'N/A', 2, 'Gardena, CA',
        'Sheet Metal Components', 'Lockheed Martin', 'Supplier Awards')

    upload_supplier('AFM Industries', 'N/A', 3, 'Anaheim, CA', 
        'Fabrication and Tooling', 'Lockheed Martin', 'Supplier Awards')

    upload_supplier('Bron Tapes of Colorado', 'N/A', 3, 'Denver, Colorado',
        'Pressure-Sensitive Tape', 'Lockheed Martin', 'Supplier Awards')

    upload_supplier('Flame Enterprises', 'N/A', 3, 'Chatsworth, CA',
        'Electrical Protection, Switching, Thermal Management, Interconnection',
        'Lockheed Martin', 'Supplier Awards')

    upload_supplier('M-Tron Components', 'N/A', 3, 'Ronkonkoma, NY',
        'Semiconductors & Electrical/Computer Components', 'Lockheed Martin', 
        'Supplier Awards')

    upload_supplier('Master Research & Manufacturing', 'N/A', 3, 'Norwalk, CA',
        'Multi-Spindle Complex Machining', 'Lockheed Martin','Supplier Awards')

    upload_supplier('Nor-Ral', 'N/A', 3, 'Canton, GA', 
        'Complex Machining Parts', 'Lockheed Martin', 'Supplier Awards')

    upload_supplier('S3 International', 'N/A', 2, 'Milwaukee, WI', 
        'Aircraft Component Repair', 'Lockheed Martin', 'Supplier Awards')

    upload_supplier('Sharp Tooling Solutions', 'N/A', 3, 'Bruce Township, MI',
        'Specialized Tooling', 'Lockheed Martin', 'Supplier Awards')

    upload_supplier('Williams RDM', 'N/A', 2, 'Fort Worth, TX', 
        'Automated Test Equipment', 'Lockheed Martin', 'Supplier Awards')

    upload_supplier('Champion Aerospace', 'N/A', 2, 'Liberty, SC',
        'Turbine Engine Parts', 'Lockheed Martin', 'Supplier Awards')

    upload_supplier('Collins Aerospace', 'N/A', 2, 'Troy, OH',
        'Automation and Intelligence Technologies, Co-Produces HMDS System, Landing Gear System, Portions of Avionics Suite', 
        'Lockheed Martin', 'Supplier Awards')

    upload_supplier('Future Metals', 'N/A', 3, 'Arlington, TX',
        'Tubing, Bar, and Sheet Metal Products', 'Lockheed Martin', 
        'Supplier Awards')

    upload_supplier('Goodyear', 'GT', 2, 'Akron, OH', 'Aviation Tires', 
        'Lockheed Martin', 'Supplier Awards')

    upload_supplier('TW Metals', 'N/A', 3, 'Forrest Park, GA', 
        'Tubing, Bar, and Sheet Metal Products', 'Lockheed Martin', 
        'Supplier Awards')

    upload_supplier('Syensqo', 'SYENS', 4, 'Brussels, Belgium', 
        'FM 300 structural adhesive', 'Lockheed Martin',
        'Airframer', 
        note='ADR based in Euronext Brussels. Has several US locations')

    upload_supplier('Hardide plc', 'HDD', 3, 'Martinsville, VA', 
        'Hardide A Coating - Drag Chute Components',
        'Lockheed Martin', 'Airframer',
        note='UK based company with a US based location. Traded in LSE AIM market')

    upload_supplier('Dupont de Nemours', 'DD', 3, 'Richmond, VA', 
        'Kevlar Based Honeycombs in Secondary Structures', 'Lockheed Martin',
        'Airframer', 
        note='Dupont Aerospace is a brance of the much larger Dupont company. Quarterly reports should have info on just this subsidiary.')

    upload_supplier('Elbit Systems', 'ESLT', 2, 'Fort Worth, TX', 
        'Co-Produces HMDS system, Honeycomb Sandwich Panels, Center Fuselage Components, Display Systems, Electronic Warfare Components',
        'Lockheed Martin', 'Airframer')

    upload_supplier('GKN Aerospace', 'MRO', 3, 'United Kingdom', 
        'Advanced Composite Parts for F135 Engine, Wiring & Electrical Components, Thermoplastic Composite Skin Panels',
        'Lockheed Martin/Pratt & Whitney', 'Airframer', 
        note='Subsidiary of Melrose, which is traded in the LSE')

    upload_supplier('Hexcel', 'HXL', 2, 'Stamfort, CT', 
        'Engineered Core Materials, Carbon Fibers, Advanced Composite Materials, Involevent in Early Design Phase',
        'Lockheed Martin and Other Tier 1 Suppliers', 'Airframer',
        note='Maintains crucial relationship with top tier suppliers. Has multinational locations supplying various components')

    upload_supplier('Quickstep Holdings', 'QHL', 3, 'Sydney, Australia',
        'Develops the Precise Conditions and Methods Needed to Cure Composite Materials that can Withstand Extreme Temperatures',
        'Lockheed Martin', 'Airframer', 
        note='Traded in the Autralian Securities Exchange (ASX)')

    upload_supplier('Kongsberg Gruppen', 'KOG', 2, 'Oslo, Norway',
        'Advanced Composite Center Fuselage Parts and Subassemblies, Composite and Titanium Rudder Components',
        'Lockheed Martin', 'Airframer', 
        note='Traded on the Oslo Stock Exchange(OSE)')

    upload_supplier('Carpenter Technology Corporation', 'CRS', 3, 'Latobe, PA',
        'Vacuum Induction Melting/Vacuum Arc Remelting Alloys for Engine Bearings, AerMet 100 alloy for the landing gear',
        'Lockheed Martin', 'Airframer')

    upload_supplier('Woodward HRT', 'WWD', 2, 'Santa Clarita, CA',
        'Fuel Metering Units and Actuation Systems', 'Lockheed Martin',
        'Airframer')

    upload_supplier('Moog', 'MOG.A and MOG.B', 2, 'Fort Worth, TX',
        'Flight Control Actuation Systems', 'Lockheed Martin', 'Airframer')

    upload_supplier('Ducommun Labarge Technologies', 'DCO', 3, 'Huntsville, AR',
        'Electronic Assemblies, Wiring Harnesses, Printed Circuit Boards', 
        'Lockheed Martin', 'Airframer')

    upload_supplier('Kitron ASA', 'OSE: KIT', 3, 'Oslo, Norway', 
        'Subassembly Integrated Communications, Navigation and Identification Modules',
        'Northrop Grumman', 'Airframer')

    upload_supplier('Materion Corporation', 'MTRN', 3, 'Mayfield Heights, OH',
        'AlBeCast Aluminum-Beryllium Investment Cast Components for Electro-Optical Targeting System',
        'Lockheed Martin', 'Airframer')

    upload_supplier('Sonaca SA', 'SONA', 2, 'Gosselies, Belgium',
        'Final Assembly of the Horizontal Tail, Aircraft Structural Components',
        'Lockheed Martin', 'Airframer', note='Trades on the EuroNext Belgium')

    upload_supplier('Safran Aero Boosters', 'SAF', 2, 'Herstal, Belgium',
        'Structural Components Including Low-Temperature Compressors for the F135 Engine',
        'Pratt & WHitney', 'Airframer', note='Traded on EuroNext Paris')

    upload_supplier('Kale Aero', 'KIPA', 3, 'Istanbul, Turkey',
        'Specialized Engine Hardware and Precision-Machined Components for F135 Engine',
        'Pratt & Whitney', 'Airframer', note='Listed on Borsa Instanbul')

    upload_supplier('Lightpath Technologies', 'LPTH', 3, 'Orlando, FL',
        'Precision Molded Glass Aspheric Lenses, Advanced Optical Assemblies',
        'Lockheed Martin', 'Airframer')

    upload_supplier('Luna Innovations', 'LUNA', 3, 'Roanoke, VA',
        'High-Performance Fiber Optic-Based Measurement Technology',
        'Lockheed Martin', 'Airframer')
    
if __name__ == "__main__":
    response = input("Do you want to load initial suppliers? (yes/no): ")
    if response.lower() == 'yes':
        main()

