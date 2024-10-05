def sort_list():
    d = {
        'Hendrix': '1942',
        'Allman': '1946',
        'King': '1925',
        'Clapton': '1945',
        'Johnson': '1911',
        'Berry': '1926',
        'Vaughan': '1954',
        'Cooder': '1947',
        'Page': '1944',
        'Richards': '1943',
        'Hammett': '1962',
        'Cobain': '1967',
        'Garcia': '1942',
        'Beck': '1944',
        'Santana': '1947',
        'Ramone': '1948',
        'White': '1975',
        'Frusciante': '1970',
        'Thompson': '1949',
        'Burton': '1939',
    }

    # Get the unique years, set will remove duplicates
    years = sorted(set(d.values()))

    for year in years:
        names_for_year = []
        for name, y in d.items():
            if y == year:
                names_for_year.append(name)

        sorted_names = sorted(names_for_year)
        for name in sorted_names:
            print(name)


if __name__ == '__main__':
    sort_list()
