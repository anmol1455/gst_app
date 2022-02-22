from functools import wraps
from flask import request, redirect, url_for, render_template
from GST_API_BackEnd import GST_API, Database, GetDecryption
from GST_API_BackEnd.models import User, TaxPayer, Tax
from datetime import datetime


def login_required(function_to_protect):
    @wraps(function_to_protect)
    def wrapper(*args, **kwargs):
        Cookie = request.cookies.get('SiteCookie')
        if Cookie:
            user_id = GetDecryption(Cookie)
            user = User.query.filter_by(id=int(user_id)).first()
            if user:
                return function_to_protect(*args, **kwargs)
            else:
                return redirect(url_for('home'))
        else:
            return redirect(url_for('home'))

    return wrapper


@GST_API.route("/business-registration/<id>", methods=['POST', 'GET'])
@login_required
def put_business_details(id):
    gst_num = request.form.get('gst_num')
    pan_num = request.form.get('pan_num')
    business_name = request.form.get('business_name')
    constitution = request.form.get('constitution')
    address = request.form.get('address')

    business = TaxPayer(id=id, gst_num=gst_num, pan_num=pan_num, business_name=business_name, constitution=constitution,
                        address=address)

    Payer_Data = TaxPayer.query.filter_by(gst_num=gst_num).first()

    if Payer_Data:
        Payer_Data.gst_num = gst_num
        Payer_Data.pan_num = pan_num
        Payer_Data.business_name = business_name
        Payer_Data.constitution = constitution
        Payer_Data.address = address
        Database.session.commit()
        return "User Updated Close Tab now"

    else:
        Database.session.add(business)
        Database.session.commit()

        # redirect to page where his tax due details shows
        return redirect(url_for('tax_payer_home', id=id))


@GST_API.route("/payer-home/<id>", methods=['POST', 'GET'])
@login_required
def tax_payer_home(id):
    business = TaxPayer.query.filter_by(id=id).first()
    not_registred = True
    if business:
        not_registred = False
        tax_due = Tax.query.filter_by(associated_payer=id).all()
        BusinessDetails = TaxPayer.query.filter_by(id=id).first()

        return render_template("TaxPayerHome.html", not_registred=not_registred, Taxes=tax_due,
                               Name=BusinessDetails.business_name)

    else:
        return render_template("TaxPayerHome.html", not_registred=not_registred, id=id)


@GST_API.route("/accountant/<id>", methods=['POST', 'GET'])
@login_required
def accountant_home(id):
    Accountant = User.query.filter_by(id=id).first()
    tax_payers = TaxPayer.query.all()
    tax_due = Tax.query.all()

    """
    Add create Tax due form
    """
    return render_template("AccountantHome.html", tax_payers=tax_payers, PersonalData=Accountant, Taxes=tax_due)


@GST_API.route("/issue-tax", methods=['POST', 'GET'])
@login_required
def TaxMaker():
    gst_num = request.form.get('gst_num')
    Payer_Data = TaxPayer.query.filter_by(gst_num=gst_num).first()
    associated_payer = Payer_Data.id
    business_name = Payer_Data.business_name
    pan_num = Payer_Data.pan_num
    title = request.form.get('title')
    total_amount = request.form.get('total_amount')
    transaction_type = request.form.get('transaction_type')
    GST = request.form.get('GST')
    CGST = request.form.get('CGST')
    IGST = request.form.get('IGST')
    SGST = request.form.get('SGST')
    Penalty = request.form.get('Penalty')
    net_income = request.form.get('net_income')
    total_tax = request.form.get('total_tax')
    issued_by = request.form.get('issued_by')
    due_date = request.form.get('due_date')
    due_date = datetime.strptime(due_date, '%d-%m-%Y')

    NewTax = Tax(associated_payer=associated_payer, title=title, business_name=business_name, gst_num=gst_num,
                 pan_num=pan_num,
                 total_amount=total_amount, GST=GST, CGST=CGST, IGST=IGST, SGST=SGST, Penalty=Penalty,
                 net_income=net_income, transaction_type=transaction_type, total_tax=total_tax, issued_by=issued_by,
                 due_date=due_date)

    Database.session.add(NewTax)
    Database.session.commit()

    return "Made Tax Due close tab now"


@GST_API.route("/update-issued-tax/<id>", methods=['POST', 'GET'])
@login_required
def TaxUpdater(id):
    Tax_Data = Tax.query.filter_by(id=id).first()

    Tax_Data.title = request.form.get('title')
    Tax_Data.total_amount = request.form.get('total_amount')
    Tax_Data.transaction_type = request.form.get('transaction_type')
    Tax_Data.GST = request.form.get('GST')
    Tax_Data.CGST = request.form.get('CGST')
    Tax_Data.IGST = request.form.get('IGST')
    Tax_Data.SGST = request.form.get('SGST')
    Tax_Data.Penalty = request.form.get('Penalty')
    Tax_Data.net_income = request.form.get('net_income')
    Tax_Data.total_tax = request.form.get('total_tax')
    Tax_Data.issued_by = request.form.get('issued_by')
    due_date = request.form.get('due_date')
    due_date = datetime.strptime(due_date, '%d-%m-%Y')
    Tax_Data.due_date = due_date

    Database.session.commit()

    return "Tax Data Updated Close Tab now"
