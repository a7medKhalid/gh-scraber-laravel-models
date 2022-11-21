
# import the necessary packages
from time import time
from github import Github
import requests
import pandas as pd
import math
from bs4 import BeautifulSoup


# First create a Github instance:
g = Github('******', '*****')

# list of all laravel repos query 

# search for repos from date 2022-10 to 2015-01

dates = pd.date_range(start='2015-01', end='2016-11', freq='M').tolist()

# strip day and time from dates
dates = [date.strftime('%Y-%m') for date in dates]

# reverse dates list
dates.reverse()


for date in dates:

    startTime = time()

    print(date)



    laravelRepos = g.search_repositories(query='language:php created:' + date + ' laravel', order='desc')


    print(laravelRepos.totalCount)
    

    # create csv file
    df = pd.DataFrame(columns=['Repo Name','Repo URL', 'Repo Models' ] )



    # 



    counter = 0
    # get project model names
    for repo in laravelRepos:

        counter += 1

        # print if percntage ends with 0
        percntage = (counter / laravelRepos.totalCount) * 100
       
        print(counter)
        print(percntage , '%')


        # if repo name is laravel skip it
        # if repo.name == 'laravel':
        #     continue

        repoRow = []
        repoRow.append(repo.name)

        # get the defualt branch name of the repo
        branch = repo.default_branch 

        modelURL = 'https://github.com/' + repo.full_name + '/tree/' + branch + '/database/migrations'

        repoRow.append(modelURL)

        # get the response from the URL
        response = requests.get(modelURL)

        # parse the response using beautiful soup
        soup = BeautifulSoup(response.text, 'html.parser')

        # get js-details-container Details div
        detailsDiv = soup.find('div', {'class': 'js-details-container Details'})


        # check if the div is not empty
        if detailsDiv is not None:
            # get the list of files names
            filesList = detailsDiv.find_all('a', {'class': 'js-navigation-open Link--primary'})


            models = ''
            for file in filesList:

                # check if file has text
                if file.text is not None:

                    # check if the file is a table migration file
                    
                    if file.text.find('create_') != -1:
                        
                        # strip table name from file name after create_ and before _table or .php
                        tableName = file.text.split('create_')[1].split('_table')[0]

                        # if trailing .php is found remove it
                        if tableName.find('.php') != -1:
                            tableName = tableName.split('.php')[0]

                        # add table name to models string
                        models += tableName + ', '


                        

            # add model names to the repo row
            repoRow.append(models)

            # if models number 4 or less skip
            if models.count(',') <= 4:
                continue

        
        # add repo row to the dataframe if columns are not null

        if len(repoRow) == 3:
            # handle all exceptions
            try:
                df.loc[len(df)] = repoRow
                df.to_csv('laravelRepos' + date + '.csv', index=False)

                print('yes', repoRow)
            except:
                print('error', repoRow)
                # save the dataframe to csv file
                df.to_csv('laravelRepos' + date + '.csv', index=False)
                pass

        else:
            print('no', repoRow, len(repoRow))

    finishTime = time()

    print('time', finishTime - startTime)

    # print art
    print('''
    ██████╗░░█████╗░███╗░░██╗███████╗██████╗░░█████╗░██╗░░░██╗
    ██╔══██╗██╔══██╗████╗░██║██╔════╝██╔══██╗██╔══██╗╚██╗░██╔╝
    ██████╔╝██║░░██║██╔██╗██║█████╗░░██████╔╝██║░░██║░╚████╔╝░
    ██╔══██╗██║░░██║██║╚████║██╔══╝░░██╔══██╗██║░░██║░░╚██╔╝░░
    ██║░░██║╚█████╔╝██║░╚███║███████╗██║░░██║╚█████╔╝░░░██║░░░
    ╚═╝░░╚═╝░╚════╝░╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝░╚════╝░░░░╚═╝░░░
    ''')
    print('--------------------------------------------')

    # predicted finish time
    print('predicted finish time', (finishTime - startTime) * (laravelRepos.totalCount - counter) / 60, 'minutes')


        
    


