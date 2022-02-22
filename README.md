<h1>Introduction</h1>
A secure GST Tax management system where different business owners can view and pay their pending taxes and Accountants can issue taxes to different businesses.
There are 3 roles.<br><br>
<l>1- Admin</l><br>
<l>2- Accountant</l><br>
<l>3- Tax Payer (Business Owner)</l><br>
<br>
<l>A Tax Payer can view and pay their own taxes only if due date is not passed.</l><br><br>
<l>An Accountatn can view all businesses and issue a tax receipt to them.</l><br><br>
<l>Admin can view all the information and control users.</l><br>

<h1>How to Run</h1>

<l>1- Clone the repo</l><br>
<l>2- Open terminal inside gst-flask-app folder</l><br>
<l>3- Run Following commands</l><br>

```
docker image build -t gst-flask-app .

docker run -p 2000:5000 -d gst-flask-app
```

<h1>Testing</h1>

```
Test cases are in How-to-USE PDF inside gst-flask-app
```

