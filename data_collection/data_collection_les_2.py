from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import pandas as pd
from typing import List


def getSuperJobVacanciesDescription():
    superjob_url = 'https://www.superjob.ru'
    name = input('Введите название вакансии латинскими буквами: ')

    path = f'/vakansii/{name}.html?geo%5Bt%5D%5B0%5D=4'
    request_url = f'{superjob_url}{path}'
    page = 0
    pages_max = 2
    vacancies = []

    while page < 2:

        response = requests.get(request_url).text
        soup = bs(response, 'lxml')
        vacancies_list = soup.find_all('div', {'class': 'Fo44F QiY08 LvoDO'})
        pprint(len(vacancies_list))

        for vacancy in vacancies_list:
            vacancy_data = {
                'name': vacancy.find('a').getText(),
            }

            # salary
            salary_text = vacancy.find('span', {'class': '_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'})\
                .getText()\
                .replace('\xa0', '')
            salary_list = getSalaryFromText(salary_text, '—')
            vacancy_data['salary_min'] = salary_list[0]
            vacancy_data['salary_max'] = salary_list[1]
            vacancy_data['salary_currency'] = salary_list[2]
            vacancy_data['salary_text'] = salary_text

            # links
            links = vacancy.find_all('a')
            vacancy_data['link'] = superjob_url + links[0]['href']
            vacancy_data['source_link'] = superjob_url + links[1]['href']

            company = vacancy.find('div', {'class': '_3_eyK _3P0J7 _9_FPy'})
            vacancy_data['company_name'] = company.find('span').getText()

            address = vacancy.find('span', {'class': '_3mfro f-test-text-company-item-location _9fXTd _2JVkc _2VHxz'})
            vacancy_data['address'] = address.find_all('span')[2].getText().replace('\xa0', '')

            vacancies.append(vacancy_data)

        next_page_tag = soup.find('a', {'class': 'f-test-button-dalshe'})
        if next_page_tag is None:
            page = pages_max
        else:
            path = next_page_tag['href']
            page += 1

    v = pd.DataFrame(vacancies)
    print(v.to_string())


def getSalaryFromText(text, separator) -> List[str]:
    currency = 'руб.'
    salary_list = [None, None, currency]
    if text[-4:] == currency:
        text = text.replace(currency, '')

        if separator in text:
            text_list = text.split(separator)
            salary_list[0] = text_list[0]
            salary_list[1] = text_list[1]
        elif 'от' in text:
            salary_list[0] = text.replace('от', '')
        elif 'до' in text:
            salary_list[1] = text.replace('до', '')

    else:
        salary_list[2] = None

    return salary_list


def get_hh_vacancies_description():
    hh_url = 'https://www.hh.ru'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
        'Accept': '*/*'}
    name = input('Введите название вакансии: ')

    path = f'/search/vacancy?area=1&st=searchVacancy&text={name}&fromSearch=true'
    request_url = f'{hh_url}{path}'
    page = 0
    pages_max = 2
    vacancies = []

    while page < 2:

        response = requests.get(request_url, headers=header).text

        soup = bs(response, 'lxml')
        vacancies_list = soup.find_all('div', {'class': 'vacancy-serp-item'})
        pprint(len(vacancies_list))

        for vacancy in vacancies_list:
            vacancy_data = {'name': vacancy.find('div', {'class': 'vacancy-serp-item__info'}).getText(),
                            'link': vacancy.find('a', {'class': 'bloko-link HH-LinkModifier'})['href']}

            # salary
            salary_text = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'})\
                .getText()\
                .replace('\xa0', '')\
                .replace(' ', '')
            salary_list = getSalaryFromText(salary_text, '-')
            vacancy_data['salary_min'] = salary_list[0]
            vacancy_data['salary_max'] = salary_list[1]
            vacancy_data['salary_currency'] = salary_list[2]
            vacancy_data['salary_text'] = salary_text

            # company
            employer_info = vacancy.find('div', {'class': 'vacancy-serp-item__meta-info'})
            vacancy_data['employer_link'] = hh_url + employer_info.find('a')['href']
            vacancy_data['company_name'] = employer_info.getText()
            vacancy_data['address'] = vacancy.find('span', {'class': 'vacancy-serp-item__meta-info'}).getText()

            vacancies.append(vacancy_data)

        next_page_tag = soup.find('a', {'data-qa': 'pager-next'})
        if next_page_tag is None:
            page = pages_max
        else:
            path = next_page_tag['href']
            page += 1

    v = pd.DataFrame(vacancies)
    print(v.to_string())


getSuperJobVacanciesDescription()
get_hh_vacancies_description()
