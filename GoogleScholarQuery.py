import pandas as pd
valid_staff = 0
invalid_staff = 0


def indexing(file_name):
    df1 = pd.read_csv(file_name)
    df1 = df1.set_index(['university', 'staffName'])
    df1.to_csv(file_name)


def query(staff):
    """Perform Google Scholar query and return author object"""
    import scholarly
    try:
        search_query = scholarly.search_author(staff.rstrip())
    except ConnectionError:
        print('Connection aborted.When querying ' + staff)
        return None

    try:
        author = next(search_query).fill()
        return author
    except StopIteration:
        print('Generator cannot be iterated! When querying ' + staff.rstrip())
        return None


def staff_query(uni_name):
    import GoogleQuery as gq
    import dataProcess as dp
    global valid_staff
    global invalid_staff
    f = open('staffLists\\' + uni_name + '.txt', 'r', encoding='utf-8')
    df = pd.DataFrame()
    for line in f:
        cite = []
        titles = []
        staffs = []
        query_result = query(line)
        if query_result:
            if query_result.name != line.rstrip():
                continue
            if query_result.name not in staffs:
                staffs.append(query_result.name)
                sorted_cite = get_sorted_pub_info(query_result)
                for title, eachcite in sorted_cite.items():
                    titles.append(title)
                    cite.append(eachcite)
                hindex = dp.get_hindex(cite)
                try:
                    sub_series = gq.init_series(uni_name, query_result.name, cite, int(hindex))
                    df = df.append([sub_series])
                    print(query_result.name + " saved!")
                    valid_staff += 1
                except TypeError:
                    print("There is no hindex value for " + query_result.name + "!")
        else:
            invalid_staff += 1
            continue
    with open('uniData\\' + uni_name + '.csv', 'a', encoding='utf-8') as f:
        df.to_csv(f)
        print(uni_name.rstrip() + ' has been saved successfully!')
    indexing('uniData\\' + uni_name + '.csv')


def get_sorted_pub_info(author):
    temp_cite = {}
    sorted_cite = {}
    for pub in author.publications:
        if 'year' in pub.bib.keys():
            if pub.bib['year'] > 2014:
                if hasattr(pub, 'citedby'):
                    temp_cite[pub.bib['title']] = pub.citedby
    cite = sorted(temp_cite.items(), key=lambda x: x[1], reverse=True)
    for sortedPub in cite:
        sorted_cite[sortedPub[0]] = sortedPub[1]
    return sorted_cite


def run():

    f = open("list.txt", 'r', encoding='utf-8-sig')
    for line in f:
        line.encode("ascii", "ignore")
        staff_query(line.rstrip())
    f.close()
    print("Query done!\n" + str(valid_staff) + " of staffs is saved to file.\n" + str(invalid_staff) + " of staffs saved unsuccessfully!")


run()
