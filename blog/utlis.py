from django.utils import timezone

__author__ = 'Vishwash Gupta'

from django.db import transaction
from bs4 import BeautifulSoup
import requests
from blog.models import Opportunity, KeywordOpportunity, CodeOpportunity, Code


def update_opportunities_for_keyword(keyword, rows):
    for row in rows:
        link = row.find("a", {"class": "lst-lnk-notice"})
        url = link['href']
        print url, keyword.name
        title = link.find("div", {"class": "solt"}).text
        opportunity = Opportunity.objects.get_or_create(url=url, title=title)[0]
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
        print url, code.code
        title = link.find("div", {"class": "solt"}).text
        opportunity = Opportunity.objects.get_or_create(url=url, title=title)[0]
        CodeOpportunity.objects.get_or_create(opportunity=opportunity, code=code)


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
