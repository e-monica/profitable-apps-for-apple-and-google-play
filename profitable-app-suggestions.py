#Goal: analyze data to help developers see what types of apps attract more users relative to others

from csv import reader 

###Google play data
opened_file = open('googleplaystore.csv')
read_file = reader(opened_file)
android = list(read_file)
android_header = android[0]
android = android[1:]

###Apple store data
opened_file = open('AppleStore.csv')
read_file = reader(opened_file)
ios = list(read_file)
ios_header = ios[0]
ios = ios[1:]

def explore_data(dataset, start, end, row_and_columns=False):
    dataset_slice = dataset[start:end]
    for row in dataset_slice:
        print(row)
        print('\n') #paragraph (or row) break
    
    if row_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))

#To understand the explore_data function, we must recognize the two-sided nature of the last parameter.
#What this last parameter seeks is to account whether any rows or columns are recognized in the dataset
#and per the function, to count them in total if TRUE. In this binomial scenario we also recognize the 
#print statement as a sort of return statement requiring the process of verifying if row_and_columns are
#found, then to print a string concatenated with the said length of the corresponding dataset's sum of 
#rows and respective columns. 

#The parameter dataset should take in the name of the dataset being analyzed. The start should typically indicate 0 
#for the corresponding index unless the file of the data in question must be adjusted to accomodate other data, titles,
#and other miscellaneous information interfering with the run of the function. The separate dataset_slice variable identifies
#this characteristic need to differentiate in the computer program. 


###Data cleaning is done to detect inaccurate data and correct or remove it. It also is utilized in 
###detecting duplicate data and removing said duplicates. 
#Here, we are indentifying the headings corresponding to existing row and column names within the Google Play store and
#Apple store dataset csv files. Then, we insert a line break for clear reading and call our function for the first FOUR entries
#one of such entries including the organized heading names.

print(android_header)
print('\n')
explore_data(android, 0, 3, True)

print(ios_header)
print('\n')
explore_data(ios, 0, 3, True)

##Overview of further proceedings##
#############################################################################
##Parts of Data Cleaning in this csv: Deleting data that throws off the other rows/columns, Removing duplicates of the same entry, 
##and for the purposes of this analysis removing non-English apps for ease of understanding to American-based businesses. 

##Parts of Data Analysis: organizing free apps and paid apps separately, sorting apps by genre.

##DATA CLEANING CODE##
#####################
#We use the discussions section of those who have referenced this data before for issues as well as reading through
#the csv with our own eyes for spotting issues we have with the file.
#First we find a problem where a row has been thrown off from its line of reference to the header as 'Category' heading is found to correspond to 1.9 and not a genre.
print(android[10472])  # row location of mixup
print(android_header)  # header for categorical reference 
print(android[0])      # how the row should correspond to header
print(len(android))
del android[10472]  # don't rerun - comment out in case of need to rerun code
print(len(android))

#Next we find the possibility of multiple duplicate entries due to the discussion of Instagram repeated one too many times.
#Opportunity for another function:

#think of this as saying for row in android csv (row named app)
#name is a new variable for the leading app (most likely header titles in the file) and then for following read rows
#if this row is already found in the one_of_a_kind list, push it into the copies list. 
#Thus the following line with the backspace tab indentation back underneath if -- here we show it's a row NOT found in one_of_a_kind
#seeing as it's not in the list already, we ask the function to push the newly discovered row into the one_of_a_kind list

copies = []
one_of_a_kind = []

for column in android:
    app_name = column[0]
    if app_name in one_of_a_kind:
        copies.append(app_name)
    one_of_a_kind.append(app_name)

print(len(copies))
print(copies[0:15])
#Why aren't we sidestepping this whole thing & using a counter function?
#The purpose of this function lies in counting out the apps that have copies so one_of_a_kind is a little misleading
#The reality is one_of_a_kind is a first time registry and copies keeps track of the additional rows found for first timers repeat read rows.

#From a tip on DQ framework, we see all the Instagram entries laid out side by side. The difference? Number of reviews.
#We will remove the entries without the highest number of reviews as our factor of differentiation. 

reviews_max = {} #defines an empty dictionary, an array of (key,value) pairs 
for column in android:
    app_name = column[0] #indicates the list of all the application names in Android's Google Play Store 
    review_num_entry = column[3] #heading is reviews detailing the number of reviews entered per entry for app name
    if app_name in reviews_max and reviews_max[app_name] < review_num_entry:
        reviews_max[app_name] = review_num_entry  #reassignment of entry which values the higher level of reviews taken
    elif app_name not in reviews_max: #akin to else if in JS
        reviews_max[app_name] = review_num_entry #note that this line reaffirms a check on the entry to be TRUE, holding max # of reviews
#here, app_name is the key, entrys_reviews for number of reviews per entry for the value
print('Expected length:', len(android) - 1181)  #android was reassigned in top without the header so the indexing began with the data
print('Actual length:', len(reviews_max)) #1181 length of duplicate apps above

#The understanding of this function utilizes float to attribute the appropriate decimal to the rating reviews. However listing does 
#reveal anything other than integers. It may be to instill uniformity among type of the numerical inputs. 
#For now, no need found for its use. It actually creates error if used in the follow up function. 

android_clean = []
already_added = []
for column in android:
    app_name = column[0] #function specific variable, doesn't get called outside of it
    review_num_entry = column[3]  #use float to adjust according to how the data presents itself in your computer
    
    if (reviews_max[app_name] == review_num_entry) and (app_name not in already_added): #see membership test operations 6.10.2 in python doc
        android_clean.append(column) #while the variable is correct in reference it is specifically here a column value, not appending the entire column
        already_added.append(app_name) #remains under the condition of the if statement, no tab back

explore_data(android_clean, 0, 3, True) 

#Removing the not English apps
#the following refer to locations of non-English apps
print(ios[813][1]) #813 is a list of lists of Chinese-character entries 
print(ios[6731][1]) #the 1 subset refers to the second column where the Chinese characters are speficially found, rest are numeric indicators
print(android_clean[4412][0]) #from beginning of row to end
print(android_clean[7940][0])

#We are told in DQ English follows ASCII coding.
#https://docs.python.org/3/howto/unicode.html reveals English is 128 and greater
def is_English(string):
    for character in string:
        if ord(character) > 127:    
            return False
    return True

print(is_English('Instagram'))
print(is_English('爱奇艺PPS -《欢乐颂2》电视剧热播'))
#We have to account for other characters not considered in ASCII unicoding
print(is_English('Docs To Go™ Free Office Suite'))
print(is_English('Instachat 😜'))
#prints False for both trademark & emoji
print(ord('™')) #8482
print(ord('😜')) #128540

#Removing only apps with more than 3 non-ASCII characters 
def is_English(string):
    non_ascii = 0
    for character in string:
        if ord(character) > 127:
            non_ascii += 1
    if non_ascii > 3:
        return False
    else:
        return True

#print(is_English('Docs To Go™ Free Office Suite')) #True
#print(is_English('Instachat 😜')) #True

#Further filtering non-English rows
android_english = []
ios_english = []

for app in android_clean:
    name = app[0]
    if is_English(name): #this is a true/false test 
        android_english.append(app) #if is_English(name) checks true through above function, it's added to english list
                                #if False, it will be discarded as non-English
for app in ios:
    name = app[1]
    if is_English(name):
        ios_english.append(app)
        
explore_data(android_english, 0, 3, True)
print('\n')
explore_data(ios_english, 0, 3, True)
#runs through explore_data function after direct above function is read
###########################################################################################################################################

#We are only interested in free apps for revenue received via in-app advertising
#so this code separates further the free from the paid #Part 8 of 14 on DQ
android_final = []
ios_final = []

for app in android_english:
    price = app[7]
    if price == '0':     ##to align with string value found in csv          
        android_final.append(app)
        
for app in ios_english:
    price = app[4]
    if price == '0.0':
        ios_final.append(app)


print(len(android_final))
print(len(ios_final))


##Developing a frequency table to measure the most common genres of apps downloaded
#This will utilize prime_genre off the App Store csv, alike to Genres and Category columns in Google Play dataset

def freq_table(dataset, index):
    table = {}
    total = 0
    
    for row in dataset:
        total += 1
        value = row[index]
        if value in table:
            table[value] += 1
        else:
            table[value] = 1
    
    table_percentages = {}
    for key in table:
        percentage = (table[key] / total) * 100
        table_percentages[key] = percentage 
    
    return table_percentages


def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)
        
    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])



#####################
#Analysis
display_table(ios_final, -5)
display_table(android_final, 1)
display_table(android_final, -4) 

#Average number of user ratings per genre in Apple App Store

genres_ios = freq_table(ios_final, -5)

for genre in genres_ios:
    total = 0
    len_genre = 0
    for app in ios_final:
        genre_app = app[-5]
        if genre_app == genre:            
            n_ratings = float(app[5])
            total += n_ratings
            len_genre += 1
    avg_n_ratings = total / len_genre
    print(genre, ':', avg_n_ratings)


for app in ios_final:
    if app[-5] == 'Navigation':
        print(app[1], ':', app[5]) # print name and number of ratings


for app in ios_final:
    if app[-5] == 'Reference':
        print(app[1], ':', app[5])


display_table(android_final, 5)



######################################
categories_android = freq_table(android_final, 1)

for category in categories_android:
    total = 0
    len_category = 0
    for app in android_final:
        category_app = app[1]
        if category_app == category:            
            n_installs = app[5]
            n_installs = n_installs.replace(',', '')
            n_installs = n_installs.replace('+', '')
            total += float(n_installs)
            len_category += 1
    avg_n_installs = total / len_category
    print(category, ':', avg_n_installs)




for app in android_final:
    if app[1] == 'COMMUNICATION' and (app[5] == '1,000,000,000+'
                                      or app[5] == '500,000,000+'
                                      or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])



under_100_m = []

for app in android_final:
    n_installs = app[5]
    n_installs = n_installs.replace(',', '')
    n_installs = n_installs.replace('+', '')
    if float(n_installs) < 100000000:
        under_100_m.append(float(n_installs))
        
sum(under_100_m) / len(under_100_m)



for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE':
        print(app[0], ':', app[5])



for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000,000+'
                                            or app[5] == '500,000,000+'
                                            or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])




for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000+'
                                            or app[5] == '5,000,000+'
                                            or app[5] == '10,000,000+'
                                            or app[5] == '50,000,000+'):
        print(app[0], ':', app[5])


##While books are widely downloaded, they may not be the apps most in use. We would argue a simplistic classic game with a twist
##enough to be unique would be profitable. etc. etc. 

###The list in github solutions suggests the Quran is a book like any other, just as the other top downloads are the Bible and Hindu books.
###The approach I would suggest would be any sort of genre of app that incorporated elements of exploring, questioning or re-enacting religious
###models would be useful to emulate for the purposes of drawing familiarity to the user of the content within the app. 
###A show like Lucifer on Netflix and the Chronicles of Sabrina Spellman are proof of this concept in building a wide user base for profitability. 