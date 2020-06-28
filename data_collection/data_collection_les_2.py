from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import pandas as pd


def getSuperJobVacanciesDescription():
    superjob_url = 'https://www.superjob.ru'
    name = input('Введите название вакансии латинскими буквами: ')
    # интерсно почему,
    # возвращает правильное количество вакансий только с прараметром geo%5Bt%5D%5B0%5D=4 (Москва например)
    # хотя сам сайт возвращает все вакансии и без этого парметра
    request_url = f'{superjob_url}/vakansii/{name}.html?geo%5Bt%5D%5B0%5D=4'

    response = requests.get(request_url).text
    soup = bs(response, 'lxml')
    vacancies_list = soup.find_all('div', {'class': 'Fo44F QiY08 LvoDO'})
    pprint(len(vacancies_list))

    vacancies = []
    for vacancy in vacancies_list:
        vacancy_data = {
            'name': vacancy.find('a').getText(),
            'salary': vacancy.find('span', {'class': '_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'})
                .getText()
                .replace('\xa0', '')
        }

        links = vacancy.find_all('a')
        vacancy_data['link'] = superjob_url + links[0]['href']
        vacancy_data['source_link'] = superjob_url + links[1]['href']

        company = vacancy.find('div', {'class': '_3_eyK _3P0J7 _9_FPy'})
        vacancy_data['company_name'] = company.find('span').getText()

        address = vacancy.find('span', {'class': '_3mfro f-test-text-company-item-location _9fXTd _2JVkc _2VHxz'})
        vacancy_data['address'] = address.find_all('span')[2].getText().replace('\xa0', '')

        vacancies.append(vacancy_data)

    v = pd.DataFrame(vacancies)
    print(v.to_string())


def get_hh_vacancies_description():
    hh_url = 'https://www.hh.ru'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
        'Accept': '*/*'}
    name = input('Введите название вакансии: ')

    request_url = f'{hh_url}/search/vacancy?area=1&st=searchVacancy&text={name}&fromSearch=true'
    response = requests.get(request_url, headers=header).text

    soup = bs(response, 'lxml')
    vacancies_list = soup.find_all('div', {'class': 'vacancy-serp-item'})
    pprint(len(vacancies_list))

    vacancies = []
    for vacancy in vacancies_list:
        vacancy_data = {'name': vacancy.find('div', {'class': 'vacancy-serp-item__info'}).getText(),
                        'salary': vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}).getText(),
                        'link': vacancy.find('a', {'class': 'bloko-link HH-LinkModifier'})['href']}

        employer_info = vacancy.find('div', {'class': 'vacancy-serp-item__meta-info'})
        vacancy_data['employer_link'] = hh_url + employer_info.find('a')['href']
        vacancy_data['company_name'] = employer_info.getText()
        vacancy_data['address'] = vacancy.find('span', {'class': 'vacancy-serp-item__meta-info'}).getText()

        vacancies.append(vacancy_data)

    v = pd.DataFrame(vacancies)
    print(v.to_string())


getSuperJobVacanciesDescription()
get_hh_vacancies_description()
