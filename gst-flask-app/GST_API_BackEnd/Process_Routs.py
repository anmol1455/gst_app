from functools import wraps
from flask import request, render_template, flash, redirect, url_for
from GST_API_BackEnd import GST_API, Database, GetDecryption
from GST_API_BackEnd.models import TaxPayer, Tax, User
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


@GST_API.route("/Update-TaxPayer-data/<id>", methods=['POST', 'GET'])
@login_required
def UpdateTaxPayer(id):
    Payer_Data = TaxPayer.query.filter_by(id=id).first()
    return render_template("EditFrom.html", id=id, data=Payer_Data)


@GST_API.route("/Update-Tax-data/<id>", methods=['POST', 'GET'])
@login_required
def UpdateTaxDetails(id):
    Tax_Data = Tax.query.filter_by(id=id).first()

    # check for time details

    if Tax_Data.due_date < datetime.now().date():
        return "Can't Edit Tax Data as Due Date is Passed"

    return render_template("EditTax.html", id=id, data=Tax_Data)


@GST_API.route("/Create-new-tax", methods=['POST'])
@login_required
def Create_Tax():
    cur_gst_num = request.form.get('gst_num')
    Payer_Data = TaxPayer.query.filter_by(gst_num=cur_gst_num).first()

    if Payer_Data:
        return render_template("TaxDue.html", gst=cur_gst_num)

    flash('No such GST number exists in Database')
    return ('', 204)


@GST_API.route("/Pay-tax/<id>", methods=['POST'])
@login_required
def Pay_Tax(id):
    Taxobj = Tax.query.filter_by(id=id).first()

    if Taxobj.due_date > datetime.now().date():
        Tax.query.filter_by(id=id).delete()
        Database.session.commit()

        return "Paid"

    return "Due Date Passed Can not Pay Now"
