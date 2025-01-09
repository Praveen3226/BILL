from flask import Flask, render_template, request, jsonify
from decimal import Decimal
from datetime import datetime

app = Flask(__name__)

# Sample categories and courses data
categories = {

    "CIVIL": [
        ("AutoCAD",11682),
        ("3dsMax",19942),
        ("RevitMEP",25783),
        ( "Lumion", 15222),
        ("BIM360", 40000),
        ("Revit Architecture", 21122),
        ("Sketchup(V-ray)", 24780),
        ( "Revit Structure", 19942),
        ( "StadPro", 18762),
        ( "Photoshop", 10856),
        ("Quantity Take Off", 15222),
        ( "Primavera", 18762),
        ("MS Project",  14042),
        ( "ETABS",18762),
        ("Registration", 1000)
    ],

    "ELECTRICAL": [
        ( "AutoCAD",  11682),
        ("Revit MEP",  25783),
        ( "PLC Scada",  12000)
    ],

    "IT": [
        ( "C Programming", 8000),
        ("C++ Programming",  8000),
        ("Python with Django", 15000),
        ( "Core Java", 12000),
        ( "Java Script",  15000),
        ( "Advance Java",  15000),
        ("ReactJS",  12000),
        ("MySQL Database", 15000),
        ( "MongoDB Database",15000),
        ( "Front End Development",  20000),
        ( "Java Full Stack Web Development", 35000),
        ( "Python Full Stack Web Development",35000),
        ( "DevOps", 25000),
        ("Basic Computer Course", 12000)
    ],

    "MECHANICAL": [
        ("AutoCAD", 11682),
        ("Catia", 21122),
        ( "Solidworks", 18762),
        ("Creo",  23482),
        ( "NX-CAD",  23482),
        ("Revit MEP", 25783),
        ( "NX-CAM", 23482),
        ( "Hypermesh",  17582),
        ( "AnsysWB",  18762),
        ("Solid Edge",  8820),
        ("Nastran", 18762),
        ( "Registration", 1000)
    ]
}


invoice_counter = 1

@app.route('/')
def index():
    return render_template('index.html', categories=categories)

@app.route('/invoice', methods=['POST'])
def generate_invoice():
    global invoice_counter
    name = request.form['name']
    mobile = request.form['mobile']
    address = request.form['address']
    category = request.form['category']
    selected_courses = request.form.getlist('selected_courses')
    discount = Decimal(request.form['discount'])
    installments = int(request.form['installments'])
    
    courses = categories.get(category, [])
    total_amount = 0
    selected_course_names = []
    for course_name, course_price in courses:
        if course_name in selected_courses:
            total_amount += course_price
            selected_course_names.append((course_name, course_price))

    discounted_amount = total_amount - (total_amount * discount / 100)
    final_amount = discounted_amount
    installment_amount = final_amount / installments

    # Generate invoice number and date
    invoice_number = invoice_counter
    invoice_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    invoice_counter += 1

    return render_template('invoice.html', 
                           name=name,
                           mobile=mobile,
                           address=address,
                           category=category,
                           selected_courses=selected_course_names,
                           total_amount=total_amount,
                           discount=discount,
                           final_amount=final_amount,
                           installments=installments,
                           installment_amount=installment_amount,
                           invoice_number=invoice_number,
                           invoice_date=invoice_date)

if __name__ == '__main__':
    # Use PORT from environment variable for Render compatibility
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
