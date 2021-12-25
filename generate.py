from flask import Flask, app, render_template, make_response,request
import pdfkit
from datetime import date
import os, sys, subprocess, platform

def _get_pdfkit_config():
     """wkhtmltopdf lives and functions differently depending on Windows or Linux. We
      need to support both since we develop on windows but deploy on Heroku.

     Returns:
         A pdfkit configuration
     """
     if platform.system() == 'Windows':
         return pdfkit.configuration(wkhtmltopdf=os.environ.get('WKHTMLTOPDF_BINARY', 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'))
     else:
         WKHTMLTOPDF_CMD = subprocess.Popen(['which', os.environ.get('WKHTMLTOPDF_BINARY', 'wkhtmltopdf')], stdout=subprocess.PIPE).communicate()[0].strip()
         return pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)

app = Flask(__name__,template_folder='templates')
@app.route("/")
def home():
    return render_template("form.html")

@app.route("/data",methods=["POST","GET"])
def login():
    print("*****************client 1 login*****************************************")
    if request.method == "POST":
        # client_course = request.form['Course']
        client_course = 'Science'
        client_name = request.form['Name']
        client_number = request.form['Number']
        client_address_1 = request.form['inputAddress']
        client_address_2 = request.form['inputAddress2']
        client_city = request.form['inputCity']
        client_state = request.form['inputState']
        total_amount = request.form['amount']
        advance = request.form['advance']
        paymethod = request.form['payMethod']
        due = str(int(total_amount) - int(advance))

        line_2 = "{},{},{}".format(client_address_2, client_city,client_state)
        

        date_today = date.today()
        output = {
            'client_name' : client_name,
            'client_number' : client_number,
            'client_address_1': client_address_1,
            'client_address_2' : line_2,
            'total_amount':total_amount,
            'advance':advance,
            'paymethod':paymethod,
            'due':due,
            'date':date_today,
            'client_course':client_course
        }

        rendered = render_template('index.html',payload=output)
        # config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
        config = _get_pdfkit_config()
        pdf = pdfkit.from_string(rendered, False, configuration=config)
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
        return response
# @app.route('/')
# def pdf_generate():
#     now = date.today()
#     rendered = render_template('index.html',date=now)
#     css = ['style.css']
#     config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
#     pdf = pdfkit.from_string(rendered, False, configuration=config)
#     response = make_response(pdf)
#     response.headers['Content-Type'] = 'application/pdf'
#     response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
    
    
    # print ("Current date and time : ")
    # print (now.strftime("%Y-%m-%d %H:%M:%S"))
    # return response

    
if __name__ == '__main__':
    app.run(debug=True)