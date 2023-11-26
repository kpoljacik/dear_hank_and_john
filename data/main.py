import json
import csv

def get_data(): #from the raw text data, feed rows into splitting function
    with open('data/episodes.json', 'r') as input_file:
        data = input_file.read()
        json_data = (json.loads(data))
        return json_data['data']
    #returns list of epsiodes, each episode is a dictionary
    
#episode number, title, and description(text)
def parse_episodes(episode_list):
    episode_items_list = []
    for episode in episode_list:
        attributes = episode['attributes']
        if attributes['kind'] == 'trailer':
            continue
        description = attributes['description']['standard']
        number = attributes['episodeNumber']
        title = attributes['itunesTitle']
        episode_items_list.append({
            'number': number, 
            'title': title, 
            'questions': extract_questions(description)
        })
    return episode_items_list

def extract_questions(description):
    new_description = description.split(' And more!')[0]
    questions = new_description.split('?')[:-1]
    cleaned_questions = []
    for question in questions:
        cleaned_questions.append(question.strip() + '?')
    return cleaned_questions

def sort_eps(episode):
    return episode['number']

def create_full_csv(episode_list):
    with open('output.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Episode Number', 'Episode Title', 'Question'])
        for episode in episode_list:
            questions = episode['questions']
            for question in questions:
                csvwriter.writerow([episode['number'], episode['title'], question])

def description_text(episode_list):
    episode_descriptions = []
    for episode in episode_list:
        description = ' '.join(episode['questions'])
        episode_descriptions.append(description)
    print(' '.join(episode_descriptions))


def main():
    episode_items_list = parse_episodes(get_data())
    episode_items_list.sort(key=sort_eps)
    #create_full_csv(episode_items_list)
    description_text(episode_items_list)

main()