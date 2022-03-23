'''
Who Done It? 
 
A crime has taken place and the lead detective needs your help. The detective gave you the crime scene report, but you somehow lost it.

You vaguely remember that the crime was a murder that occurred sometime on Jan.15, 2018.

All the clues to this mystery are buried in a various databases, and you need to use  Pandas to navigate through this vast network of information.

Your first step to solving the mystery is to retrieve the corresponding crime scene report from the police department's database.

From there, you can use your Python/Pandas skills to find the murderer.
'''

import pandas as pd

crime_scene = pd.read_csv('crime_scene_report.csv')
license = pd.read_csv('drivers_license.csv')
fb = pd.read_csv('facebook_event_check_in.csv')
gym = pd.read_csv('get_fit_now_check_in.csv')
gym_members = pd.read_csv('get_fit_now_members.csv')
income = pd.read_csv('income.csv')
interview = pd.read_csv('interview.csv')
person = pd.read_csv('person.csv')


'''
Q1
You vaguely remember that the crime was a murder that occurred sometime on Jan.15, 2018.

Use the `crime scene` data to determine who the witnesses are.
'''

crime_scene['description'][
    (crime_scene['date'] == 20180115) &
    (crime_scene['type'] == 'murder') &
    (crime_scene['city'] == 'SQL City')].values[0]

'''
Q2
Security footage shows that there were 2 witnesses. The first witness lives at the last house on "Northwestern Dr". The second witness, named Annabel, lives somewhere on "Franklin Ave".

Use the `person` data to determine the names of the witnesses and the `interview` data to get the witnesses' statements.
'''

witness1 = person[(person['address_street_name'].str.contains('Northwestern Dr')) & (
    person['address_number'] == person['address_number'].max())]

witness2 = person[((person['name'].str.contains('Annabel')) & (
    person['address_street_name'].str.contains('Franklin')))]

interview['transcript'][interview['person_id'].isin(
    (witness1['id'].iloc[0], witness2['id'].iloc[0]))].values

'''
'I heard a gunshot and then saw a man run out. He had a "Get Fit Now Gym" bag. The membership number on the bag started with "48Z". Only gold members have those bags. The man got into a car with a plate that included "H42W".'

I saw the murder happen, and I recognized the killer from my gym when I was working out last week on January the 9th.


'''

suspects = gym_members[(gym_members['id'].str.contains('48Z')) & (
    gym_members['membership_status'] == 'gold')]

suspects = person[person['id'].isin(suspects['person_id'])]

licenseid = license['id'][(license['plate_number'].str.contains(
    'H42W')) & (license['id'].isin(suspects['license_id']))]

suspects = suspects[suspects['license_id'] == licenseid.values[0]]

interview['transcript'][interview['person_id']
                        == suspects['id'].values[0]].values[0]

'''
I was hired by a woman with a lot of money. I don't know her name but I know she's around 5'5" (65") or 5'7" (67"). She has red hair and she drives a Tesla Model S. I know that she attended the SQL Symphony Concert 3 times in December 2017.
'''

red_haired_female_drives_tesla_license_id = license[(license['hair_color'] == 'red') & (
    license['gender'] == 'female') & (license['car_make'] == 'Tesla') & (license['height'].isin(range(65, 68)))]['id']

attended_concert_person_id = fb[(fb['event_name'].str.contains('SQL')) & (fb['date'] >= 20171201) & (
    fb['date'] <= 20180101)].groupby('person_id').filter(lambda x: len(x) == 3)['person_id'].unique()

master_mind = person[(person['license_id'].isin(red_haired_female_drives_tesla_license_id)) & (
    person['id'].isin(attended_concert_person_id))]


statement = f'''
{master_mind['name'].values[0]} hired {suspects['name'].values[0]} to kill
the deceased.
'''

print(statement)
