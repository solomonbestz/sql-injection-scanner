import requests
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Function to get all forms
def get_forms(url) -> BeautifulSoup:
    soup = BeautifulSoup(s.get(url).content, "html.parser")
    return soup.find_all("form")

def form_details(form) -> dict:
    details_of_form = {}
    action = form.attrs.get("action")
    method = form.attrs.get("method", "get")
    inputs = []

    for input_tag in form.find_all("input"):
        input_type =  input_tag.attrs.get("type", "text")
        input_name =  input_tag.attrs.get("name")
        input_value =  input_tag.attrs.get("value", "")
        inputs.append({
            "type": input_type,
            "name": input_name,
            "value": input_value
        })
    details_of_form['action'] = action
    details_of_form['method'] = method
    details_of_form['inputs'] = inputs
    return details_of_form

def vulnerable(response) -> bool:
    errors = {"quoted string not properly terminated",
              "unclosed quotation mark after the character string",
              "you have an error in your SQL syntax"}

    for error in errors:
        if error in response.content.decode().lower():
            return True
    return False  

def injection_scanner(url):
    forms = get_forms(url)
    print(f"[+] Detected {len(forms)} forms on {url}.")

    for form in forms:
        details = form_details(form)
 
    for i in "\"'":
        data = {}
        for input_tag in details["inputs"]:
            if input_tag["type"] == "hidden" or input_tag["value"]:
                data[input_tag['name']] = input_tag["value"] + i
            elif input_tag["type"] != "submit":
                data[input_tag['name']] = f"test{i}"
        print(url)
        form_details(form)

        if details["method"] == "post":
            res = s.post(url, data=data)
        elif details["method"] == "get":
            res = s.get(url, params=data)
        if vulnerable(res):
            print("SQL Injection attack vulnerability in link: ", url)
        else:
            print("No SQL injection attack vulnerability detected")
            break




if __name__=='__main__':
    s = requests.Session()
    s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"

    urlToBeChecked = input("Enter Url: ")
    injection_scanner(urlToBeChecked)