from django.utils import timezone

__author__ = 'Vishwash Gupta'

from django.db import transaction
from bs4 import BeautifulSoup
import requests
from blog.models import Opportunity, KeywordOpportunity, CodeOpportunity, Code, UserRequestOpportunity
from selenium import webdriver
from pyvirtualdisplay import Display
import time

PHANTOM_JS_PATH = "/usr/bin/phantomjs"
# PHANTOM_JS_PATH = "F:/vishwash/google_archive/phantomjs.exe"

def update_opportunities_for_keyword(keyword, rows):
    for row in rows:
        link = row.find("a", {"class": "lst-lnk-notice"})
        url = link['href']
        title = link.find("div", {"class": "solt"}).text
        date = row.find("td", {"headers": "lh_current_posted_date"}).text
        print keyword.name, " ---> ", title, date
        opportunity = Opportunity.objects.get_or_create(url=url, title=title)[0]
        opportunity.posted_on = date
        opportunity.save()
        KeywordOpportunity.objects.get_or_create(opportunity=opportunity, keyword=keyword)
        # br = mechanize.Browser()
        # br.open(url)
        # br.select_form('vendor_procurement_notice_search')
        # br.form['dnf_class_values[procurement_notice][keywords]'] = "award"
        # # br.form['name'] = "award"
        #
        # response = br.submit()
        # print response


def update_opportunities_for_code(code, rows):
    for row in rows:
        link = row.find("a", {"class": "lst-lnk-notice"})
        url = link['href']
        title = link.find("div", {"class": "solt"}).text
        date = row.find("td", {"headers": "lh_current_posted_date"}).text
        print code.code, " ---> ", title, date
        opportunity = Opportunity.objects.get_or_create(url=url, title=title)[0]
        opportunity.posted_on = date
        opportunity.save()
        CodeOpportunity.objects.get_or_create(opportunity=opportunity, code=code)


def update_opportunities_for_user_request(user_request, rows, keyword_to_be_matched):
    updated_count = 0
    for row in rows:
        link = row.find("a", {"class": "lst-lnk-notice"})
        url = link['href']
        title = link.find("div", {"class": "solt"}).text
        description = link.find("div", {"class": "solcc"})
        print "title, ---> ", title
        print "description --->",
        if description is not None:
            print description.text
            print keyword_to_be_matched
            print keyword_to_be_matched.lower() in description.text.lower()
            print keyword_to_be_matched.lower() not in title.lower()
        else:
            print "not available"
        if keyword_to_be_matched is not None:
            if keyword_to_be_matched.lower() not in title.lower() and (
                        description is not None and keyword_to_be_matched.lower() in description.text.lower()):
                continue
        date = row.find("td", {"headers": "lh_current_posted_date"}).text
        print user_request.id, " ---> ", title, date

        opportunity = Opportunity.objects.get_or_create(url=url, title=title)[0]
        opportunity.posted_on = date
        opportunity.save()
        updated_count += 1
        UserRequestOpportunity.objects.get_or_create(opportunity=opportunity, user_request=user_request)
        for keyword in user_request.keywords.all():
            KeywordOpportunity.objects.get_or_create(opportunity=opportunity, keyword=keyword)
        for code in user_request.codes.all():
            CodeOpportunity.objects.get_or_create(opportunity=opportunity, code=code)
    print "total updated opportunities %s" %updated_count
@transaction.atomic
def scrape_from_advance_search_keyword(keyword):
    keyword_name = keyword.name
    data = '------WebKitFormBoundaryEY5KmOxkY2tN5Bbk \
Content-Disposition: form-data; name="_____dummy" \
        \
dnf_ \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk \
Content-Disposition: form-data; name="so_form_prefix" \
        \
dnf_\
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_opt_action"\
        \
search\
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_opt_template"\
        \
nS/WBg971GE/+gN9MRh/oTXxVYcDLoQW1MDkvvEnorEEQQXqMlNO+qihNxtVFxhn\
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_opt_template_dir"\
        \
/ZfXN0oc+rnouW8kca/WzbG6WrxuiBuGRpBBjyvqt1KAkN/anUTlMWIUZ8ga9kY+\
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_opt_subform_template"\
        \
GOhUNkCXr/mTC+3SmmWxD2F719zd85B9\
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_opt_finalize"\
        \
1\
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_opt_mode"\
        \
update\
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_opt_target"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_opt_validate"\
        \
1\
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][dnf_class_name]"\
        \
procurement_notice\
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][notice_id]"\
        \
dfa76543e5981005881ebb330d05f1f7\
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][_so_agent_save_agent]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][custom_response_date]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][custom_posted_date]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][zipstate][]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][zipstate][]"\
        \
AZ\
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][zipcode]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][searchtype]"\
        \
active\
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][set_aside][]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][procurement_type][]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][all_agencies]"\
        \
all\
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][agency][dnf_class_name]"\
        \
agency\
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="_status_43b364da3bd91e392aab74a5af5fd803"\
        \
0\
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][agency][dnf_multiplerelation_picks][]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="autocomplete_input_dnf_class_values[procurement_notice][agency][dnf_multiplerelation_picks][]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="autocomplete_hidden_dnf_class_values[procurement_notice][agency][dnf_multiplerelation_picks][]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][recovery_act]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][keywords]"\
        \
'
    if keyword_name is not None:
        data += keyword_name + "\n"
    data += '------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][naics_code][]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][classification_code][]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][ja_statutory][]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][fair_opp_ja][]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][posted_date][_start]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][posted_date][_start]_real"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][posted_date][_end]"\
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][posted_date][_end]_real"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][response_deadline][_start]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][response_deadline][_start]_real"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][response_deadline][_end]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][response_deadline][_end]_real"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][modified][_start]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][modified][_start]_real"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][modified][_end]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][modified][_end]_real"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][contract_award_date][_start]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][contract_award_date][_start]_real"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][contract_award_date][_end]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][contract_award_date][_end]_real"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_opt_submit"\
        \
Search\
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk--'

    headers = {
        'Content-Type': u'multipart/form-data; boundary=----WebKitFormBoundaryEY5KmOxkY2tN5Bbk',

    }
    url = "https://www.fbo.gov/index?s=opportunity&mode=list&tab=list&tabmode=list&pp=100"

    r = requests.post(url, data=data, headers=headers)
    html_content = r.text
    soup = BeautifulSoup(html_content)
    even_rows = soup.findAll("tr", {"class": "lst-rw lst-rw-even"})
    update_opportunities_for_keyword(keyword, even_rows)
    odd_rows = soup.findAll("tr", {"class": "lst-rw lst-rw-odd"})
    update_opportunities_for_keyword(keyword, odd_rows)
    keyword.last_scraped = timezone.now()
    keyword.save()
    print "successfully scraped for keyword %s" % keyword.name



@transaction.atomic
def scrape_from_advance_search_code(code):
    code_name = code.code
    data = '------WebKitFormBoundaryEY5KmOxkY2tN5Bbk \
Content-Disposition: form-data; name="_____dummy" \
        \
dnf_ \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk \
Content-Disposition: form-data; name="so_form_prefix" \
        \
dnf_\
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_opt_action"\
        \
search\
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_opt_template"\
        \
nS/WBg971GE/+gN9MRh/oTXxVYcDLoQW1MDkvvEnorEEQQXqMlNO+qihNxtVFxhn\
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_opt_template_dir"\
        \
/ZfXN0oc+rnouW8kca/WzbG6WrxuiBuGRpBBjyvqt1KAkN/anUTlMWIUZ8ga9kY+\
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_opt_subform_template"\
        \
GOhUNkCXr/mTC+3SmmWxD2F719zd85B9\
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_opt_finalize"\
        \
1\
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_opt_mode"\
        \
update\
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_opt_target"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_opt_validate"\
        \
1\
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][dnf_class_name]"\
        \
procurement_notice\
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][notice_id]"\
        \
dfa76543e5981005881ebb330d05f1f7\
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][_so_agent_save_agent]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][custom_response_date]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][custom_posted_date]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][zipstate][]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][zipstate][]"\
        \
AZ\
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][zipcode]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][searchtype]"\
        \
active\
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][set_aside][]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][procurement_type][]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][all_agencies]"\
        \
all\
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][agency][dnf_class_name]"\
        \
agency\
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="_status_43b364da3bd91e392aab74a5af5fd803"\
        \
0\
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][agency][dnf_multiplerelation_picks][]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="autocomplete_input_dnf_class_values[procurement_notice][agency][dnf_multiplerelation_picks][]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="autocomplete_hidden_dnf_class_values[procurement_notice][agency][dnf_multiplerelation_picks][]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][recovery_act]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][keywords]"\
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][naics_code][]"\
        \
'
    if code_name is not None:
        data += code_name + "\n"
    data += '------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][classification_code][]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][ja_statutory][]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][fair_opp_ja][]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][posted_date][_start]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][posted_date][_start]_real"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][posted_date][_end]"\
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][posted_date][_end]_real"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][response_deadline][_start]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][response_deadline][_start]_real"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][response_deadline][_end]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][response_deadline][_end]_real"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][modified][_start]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][modified][_start]_real"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][modified][_end]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][modified][_end]_real"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][contract_award_date][_start]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][contract_award_date][_start]_real"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][contract_award_date][_end]"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_class_values[procurement_notice][contract_award_date][_end]_real"\
        \
        \
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk\
Content-Disposition: form-data; name="dnf_opt_submit"\
        \
Search\
------WebKitFormBoundaryEY5KmOxkY2tN5Bbk--'

    headers = {
        'Content-Type': u'multipart/form-data; boundary=----WebKitFormBoundaryEY5KmOxkY2tN5Bbk',

    }
    url = "https://www.fbo.gov/index?s=opportunity&mode=list&tab=list&tabmode=list&pp=100"

    r = requests.post(url, data=data, headers=headers)
    html_content = r.text
    soup = BeautifulSoup(html_content)
    even_rows = soup.findAll("tr", {"class": "lst-rw lst-rw-even"})
    update_opportunities_for_code(code, even_rows)
    odd_rows = soup.findAll("tr", {"class": "lst-rw lst-rw-odd"})
    update_opportunities_for_code(code, odd_rows)
    code.last_scraped = timezone.now()
    code.save()
    print "successfully scraped for code %s" % code.code


def scrape_codes():
    url = "https://www.fbo.gov/index?s=opportunity&mode=list&tab=search&tabmode=list&="
    r = requests.get(url)
    html_content = r.text
    soup = BeautifulSoup(html_content)
    code_section = soup.find("div", {"id": "scrollable_checkbox_dnf_class_values_procurement_notice__naics_code___"})
    code_section_divs = code_section.findAll("div")
    for code_section_div in code_section_divs:
        input_tag = code_section_div.find("input")
        label_tag = code_section_div.find("label")
        print input_tag['value'], label_tag.text
        Code.objects.get_or_create(code=label_tag.text, code_id=input_tag['value'])


def scrape_keyword_in_selenium(keyword):
    selenium = webdriver.PhantomJS(executable_path=PHANTOM_JS_PATH)
    selenium.get('https://www.fbo.gov/index?s=opportunity&mode=list&tab=search&tabmode=list')
    keyword_input = selenium.find_element_by_name('dnf_class_values[procurement_notice][keywords]')
    submit = selenium.find_element_by_name('dnf_opt_submit')
    keyword_input.send_keys(keyword.name)
    submit.click()
    html_content = selenium.page_source
    soup = BeautifulSoup(html_content, "html5lib")
    even_rows = soup.findAll("tr", {"class": "lst-rw lst-rw-even"})
    update_opportunities_for_keyword(keyword, even_rows)
    odd_rows = soup.findAll("tr", {"class": "lst-rw lst-rw-odd"})
    update_opportunities_for_keyword(keyword, odd_rows)
    keyword.last_scraped = timezone.now()
    keyword.save()
    print "successfully scraped for keyword %s" % keyword.name


def scrape_code_in_selenium(code):
    selenium = webdriver.PhantomJS(executable_path=PHANTOM_JS_PATH)
    selenium.get('https://www.fbo.gov/index?s=opportunity&mode=list&tab=search&tabmode=list')
    keyword_input = selenium.find_element_by_name('dnf_class_values[procurement_notice][keywords]')
    submit = selenium.find_element_by_name('dnf_opt_submit')
    selenium.find_element_by_xpath(
        ".//*[contains(@title, 'NAICS Code: " + code.code + "')]"
    ).click()
    submit.click()
    html_content = selenium.page_source
    soup = BeautifulSoup(html_content, "html5lib")
    even_rows = soup.findAll("tr", {"class": "lst-rw lst-rw-even"})
    update_opportunities_for_code(code, even_rows)
    odd_rows = soup.findAll("tr", {"class": "lst-rw lst-rw-odd"})
    update_opportunities_for_code(code, odd_rows)
    code.last_scraped = timezone.now()
    code.save()
    print "successfully scraped for code %s" % code.code


def scrape_user_request_opportunities_in_selenium(user_request):
    print "scraping opportunities for user_request %s", user_request.id
    display = Display(visible=0, size=(800, 600))
    display.start()
    print "display start"
    # selenium = webdriver.PhantomJS(executable_path=PHANTOM_JS_PATH)
    selenium = webdriver.Firefox()
    print "selenium initialized"
    selenium.get('https://www.fbo.gov/index?s=opportunity&mode=list&tab=search&tabmode=list')
    print "URL opened"
    keyword_input = selenium.find_element_by_name('dnf_class_values[procurement_notice][keywords]')
    submit = selenium.find_element_by_name('dnf_opt_submit')
    keywords = user_request.keywords.all()
    codes = user_request.codes.all()
    print "codes - %s, keywords - %s" % (len(codes), len(keywords))
    if len(codes) == 0 and len(keywords) == 0:
        print "no codes and keywords found for the request. Finished"
        return
    keyword_to_be_matched = None
    if len(keywords) > 0:
        keyword_to_be_matched = keywords[0].name
        keyword_input.send_keys(keyword_to_be_matched)
    if len(codes) > 0:
        for code in codes:
            selenium.find_element_by_xpath(
                ".//*[contains(@title, 'NAICS Code: " + code.code + "')]"
            ).click()
    submit.click()
    html_content = selenium.page_source
    print "Found HTML Content from the FBO page"
    soup = BeautifulSoup(html_content, "html5lib")
    rows = soup.findAll("tr")
    final_rows = []
    for row in rows:
        if 'id' in row.attrs:
            element_id = row.attrs['id']
            if element_id is not None and "row" in element_id:
                final_rows.append(row)
    # even_rows = soup.findAll("tr", {"class": "lst-rw lst-rw-even"})
    # update_opportunities_for_user_request(user_request, even_rows)
    # odd_rows = soup.findAll("tr", {"class": "lst-rw lst-rw-odd"})
    # update_opportunities_for_user_request(user_request, odd_rows)
    print "No of Found Results - %s", len(final_rows)
    update_opportunities_for_user_request(user_request, final_rows, keyword_to_be_matched)
    print "Updated Opportunities"
    user_request.last_scraped = timezone.now()
    user_request.save()
    print "successfully scraped for user request %s" % user_request.id
    selenium.quit()
    #print "Browser Closed"
    display.stop()