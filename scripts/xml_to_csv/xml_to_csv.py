import xml.etree.ElementTree as XmlET
import pandas as pd


def writing_to_csv(df):
    df.to_csv('output.csv')


def parsing_xml(fileName):
    cols = ["name", "phone", "email", "date", "country"]
    rows = []

    xmlparse = XmlET.parse(fileName)
    root = xmlparse.getroot()
    for i in root:
        name = i.find("name").text
        phone = i.find("phone").text
        email = i.find("email").text
        date = i.find("date").text
        country = i.find("country").text
    
        rows.append({"name": name,
            "phone": phone,
            "email": email,
            "date": date,
            "country": country})
  
    df = pd.DataFrame(rows, columns=cols)

    return df


def main():
    fileName = "x_data.xml"
    writing_to_csv(parsing_xml(fileName))




if __name__ == '__main__':
    main()
