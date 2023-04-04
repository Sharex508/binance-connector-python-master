def get_diff_of_db_api_values():
    start = time.time()
    db_resp = get_results()
    api_resp = get_data_from_wazirx()
    dicts_data = [obj['symbol'] for obj in db_resp]
    n = 25

    # using list comprehension
    final = [dicts_data[i * n:(i + 1) * n]
                               for i in range((len(dicts_data) + n - 1) // n)]
    # print (len(final))
    t1 = threading.Thread(target=task1, args=(db_resp, api_resp, final[0]))
    t2 = threading.Thread(target=task2, args=(db_resp, api_resp, final[1]))
    t3 = threading.Thread(target=task3, args=(db_resp, api_resp, final[2]))
    t4 = threading.Thread(target=task4, args=(db_resp, api_resp, final[3]))
    t5 = threading.Thread(target=task5, args=(db_resp, api_resp, final[4]))
    t6 = threading.Thread(target=task6, args=(db_resp, api_resp, final[5]))

    # starting threads
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()

    # wait until all threads finish
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    done = time.time()
    elapsed = done - start
    print(elapsed)


def task1(db_resp, api_resp, data):
    task(db_resp, api_resp, data)


def task2(db_resp, api_resp, data):
    task(db_resp, api_resp, data)


def task3(db_resp, api_resp, data):
    task(db_resp, api_resp, data)


def task4(db_resp, api_resp, data):
    task(db_resp, api_resp, data)


def task5(db_resp, api_resp, data):
    task(db_resp, api_resp, data)


def task6(db_resp, api_resp, data):
    task(db_resp, api_resp, data)


def task7(db_resp, api_resp, data):
    task(db_resp, api_resp, data)


def task8(db_resp, api_resp, data):
    task(db_resp, api_resp, data)


def task9(db_resp, api_resp, data):
    task(db_resp, api_resp, data)


def task10(db_resp, api_resp, data):
    task(db_resp, api_resp, data)


def task11(db_resp, api_resp, data):
    task(db_resp, api_resp, data)


def task12(db_resp, api_resp, data):
    task(db_resp, api_resp, data)


def task13(db_resp, api_resp, data):
    task(db_resp, api_resp, data)


def task14(db_resp, api_resp, data):
    task(db_resp, api_resp, data)






    def get_diff_of_db_api_values():
    start = time.time()
    db_resp = get_results()
    api_resp = get_data_from_wazirx()
    #print(api_resp);
    dicts_data = [obj['symbol'] for obj in db_resp]

    n = 1000
    chunks = [dicts_data[i:i+n] for i in range(0, len(dicts_data), n)]

    with ThreadPoolExecutor(max_workers=6) as executor:
        for chunk in chunks:
            executor.submit(task, db_resp, api_resp, chunk)

    done = time.time()
    elapsed = done - start
    print(elapsed)



    def task(db_resp, api_resp, data):
    api_last_price_ls= []
    db_margin_ls = []
    for ele in data:
        db_match_data = [item for item in db_resp if item["symbol"] == ele]
        api_match_data = [item for item in api_resp if item["symbol"] == ele]
        if(api_match_data[0]['symbol'] == db_match_data[0]['symbol']):
            api_last_price = float(api_match_data[0]['lastPrice'])
            db_margin = float(db_match_data[0]['margin'])
            api_last_price_ls.append(api_last_price)
            db_margin_ls.append(db_margin)        
            
        api_last_price_pd = pd.DataFrame(api_last_price_ls)
        db_margin_pd = pd.DataFrame(db_margin_ls)
        api_last_price_pd.rename(columns = {0:'api_last_price'}, inplace = True)
        db_margin_pd.rename(columns = {0:'db_margin'}, inplace = True)
        Price_full_compare=api_last_price_pd.join(db_margin_pd)
    #print(api_last_price_pd)
    #print(api_last_price_ls)
    print("i am in the loop")
    return [api_last_price_ls,db_margin_ls,Price_full_compare]  