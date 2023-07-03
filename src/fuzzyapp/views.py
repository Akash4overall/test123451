from django.shortcuts import render
from  rest_framework.viewsets import GenericViewSet
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
import json
from fuzzywuzzy import fuzz


# Create your views here.
@csrf_exempt
def fuzzy_match(request):
    if request.method =='POST':
        payload = json.loads(request.body)
        first_name = payload.get('first_name')
        xml_data = payload.get('xml')
        bs_data = BeautifulSoup(xml_data, 'xml')
        data = {}
        data['first_name'] = first_name
        old_ratio = 0
        all_names = []
        for tag in bs_data.find_all('Entry'):
            xml_first_name = tag.ClaimantFirstName.text
            xml_last_name = tag.ClaimantLastName.text
            xml_miidle_name = tag.ClaimantMiddleName
            final_xml_name = xml_first_name + " " + xml_last_name
            if xml_miidle_name:
                xml_miidle_name = xml_miidle_name.text
                final_xml_name = xml_first_name + " " + xml_miidle_name + " " + xml_last_name
            comp_xml_name = xml_first_name +" "+ xml_last_name
            xml_claimant_number = tag.Claimant.text
            ratio = fuzz.token_set_ratio(first_name,comp_xml_name)
            all_names.append(final_xml_name)
            if ratio>90:
                if ratio > old_ratio:
                    old_ratio = ratio
                data['matched_name'] = final_xml_name
                data['matched_number'] = xml_claimant_number
                data['names'] = all_names
            else:
                data['matched_name'] = ""
                data['matched_number'] = 999
                data['names'] = all_names

        response_data = json.dumps(data)
    return HttpResponse(response_data)