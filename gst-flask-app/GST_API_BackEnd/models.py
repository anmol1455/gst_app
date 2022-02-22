from _datetime import datetime
from GST_API_BackEnd import Database


class User(Database.Model):
    id = Database.Column(Database.Integer, primary_key=True)
    email = Database.Column(Database.String(100), unique=True, nullable=False)
    password = Database.Column(Database.String(100), nullable=False)
    date_of_registration = Database.Column(Database.DateTime, default=datetime.utcnow)
    role = Database.Column(Database.Enum("Tax_Payer", "Accountant"), default="Tax_Payer")

    def __repr__(self):
        return f"User('{self.id}','{self.email}', '{self.date_of_registration}','{self.role}')"


class TaxPayer(Database.Model):
    id = Database.Column(Database.ForeignKey(User.id), primary_key=True)
    gst_num = Database.Column(Database.String(15), unique=True)
    pan_num = Database.Column(Database.String(10), unique=True)
    business_name = Database.Column(Database.String(500), nullable=False)
    date_of_registration = Database.Column(Database.DateTime, default=datetime.utcnow)
    constitution = Database.Column(Database.Enum("Individual", "Partnership", "Company", "HUF"))
    address = Database.Column(Database.String(500))

    def __repr__(self):
        return f"Tax-Payer('{self.id}','{self.gst_num}', '{self.pan_num}', '{self.business_name}', '{self.date_of_registration}', '{self.constitution}', '{self.address}')"


class Tax(Database.Model):
    id = Database.Column(Database.Integer, primary_key=True)
    associated_payer = Database.Column(Database.ForeignKey(TaxPayer.id))
    business_name = Database.Column(Database.ForeignKey(TaxPayer.business_name))
    gst_num = Database.Column(Database.ForeignKey(TaxPayer.gst_num))
    pan_num = Database.Column(Database.ForeignKey(TaxPayer.pan_num))
    title = Database.Column(Database.String(100))
    total_amount = Database.Column(Database.String(15))
    transaction_type = Database.Column(Database.Enum("Interstate", "Intrastate"))
    GST = Database.Column(Database.String(15))
    CGST = Database.Column(Database.String(15))
    IGST = Database.Column(Database.String(15))
    SGST = Database.Column(Database.String(15))
    Penalty = Database.Column(Database.String(15))
    net_income = Database.Column(Database.String(15))
    total_tax = Database.Column(Database.String(15))
    issued_by = Database.Column(Database.String(100))
    due_date = Database.Column(Database.Date)

    def __repr__(self):
        return f"Tax('{self.gst_num}', '{self.total_tax}', '{self.due_date}')"
