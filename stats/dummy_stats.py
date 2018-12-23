from jobs import views
from DB_mysql import DB

data_struct = {"Date":	"",
"PayTo":	"",
"Amount":	"",
"Words":	"",
"For/Memo":	"",
"Signature":	"",
"Rtn#":	"",
"Acc#":	"",
"Check#":	"",
 "Fraud": None,
 "Comments": "",
}
def get_stats_db(image_name):
    db = DB('root', 'root', 'srlogs')
    imageurl = 'images/{}'.format(image_name)
    result = db.query("select * from srlogs where imageurl='images/{}' order by sno desc limit 1;".format(image_name))
    if result==[]:
        return [[None for i in range(10)]]#raise ValueError("No such image file")
    return result

def return_formatted_data(image_name):
    """
    Returns stats from db
    """
    result = get_stats_db(image_name)
    data_struct["Acc#"] = result[0][4]
    data_struct["Rtn#"] = result[0][5]
    data_struct["Date"] = result[0][6]
    data_struct["PayTo"] = result[0][7]
    data_struct["Amount"] = result[0][8]
    data_struct["Fraud"] = result[0][9]
    
    return data_struct

def data(image_name):
    data = {"img-thumb-1.jpg":
    {"Date":	"1/21/16",
    "PayTo":	"Jane lee",
    "Amount":	"180.25",
    "Words":	"one hundred and eight and twenty five cents",
    "For/Memo":	"",
    "Signature":	"",
    "Rtn#":	"123456780",
    "Acc#":	"004523456",
    "Check#":	"4501",
     "Fraud": get_stats_db("img-thumb-1.jpg")[0][9],
     "Comments": "",
    },
    "img-thumb-2.jpg":
            {
    "Date":	"06/06/17",
    "PayTo":	"Sarannah grace",
    "Amount":	"422",
    "Words":	"four hundred twenty two",
    "For/Memo":	"",
    "Signature":	"",
    "Rtn#":	"134412780",
    "Acc#":	"342123456",
    "Check#":	"1034",
     "Fraud": get_stats_db("img-thumb-2.jpg")[0][9],
     "Comments": "",
    },
    "img-thumb-3.jpg":
            {
               "Date":	"09/05/17",
    "PayTo":	"Timo ball",
    "Amount":	"12400.25",
    "Words":	"twelve thousand four hundred 25 cents",
    "For/Memo":	"",
    "Signature":	"",
    "Rtn#":	"123456120",
    "Acc#":	"120123456",
    "Check#":	"1012", 
    "Fraud": True,
    "Comments": "Signature Mismatch and High amount",

     },
    "20171202_132418.jpg":
            {
               "Date":	"3/19/16",
    "PayTo":	"Maik Fostu",
    "Amount":	"102.75",
    "Words":	"",
    "For/Memo":	"",
    "Signature":	"",
    "Rtn#":	"401042",
    "Acc#":	"323354781",
    "Check#":	"222291231231", 
    "Fraud": get_stats_db("20171202_132418.jpg")[0][9],
    "Comments": "",

     },
     "20171202_132420.jpg":
            {
               "Date":	"2/19/12",
    "PayTo":	"Mark Foster",
    "Amount":	"300",
    "Words":	"",
    "For/Memo":	"",
    "Signature":	"",
    "Rtn#":	"401042",
    "Acc#":	"323354781",
    "Check#":	"222291231231", 
    "Fraud": get_stats_db("20171202_132420.jpg")[0][9],
    "Comments": "",

            }
    }
    return data[image_name]