import dtlpy as dl
import config
from datetime import datetime
import random
import sys
import pandas as pd

'''
project = dl.projects.get(project_name='Dataloop Task') # get your project
myBot = project.bots.create(name='Ahmad', return_credentials=True)

print("the bot email is "+myBot.email)
print("the bot password is "+myBot.password)
'''

def login(email,password):
    if dl.token_expired():
        dl.login_m2m(email=email, password=password)

def createDataset(project_name,dataset_name):
    projects = dl.projects.list()
    # check if the project is exist.
    project_exist = False
    for project in projects:
        if project.name == project_name:
            project = dl.projects.get(project_name='Dataloop Task') # get your project
            project_exist = True
            break
    if project_exist == False:
        print("please create project")
        sys.exit()
    datasets = project.datasets.list()
    # check if the dataset is exist.
    for dataset in datasets: 
        if dataset.name == dataset_name:
            dataset = project.datasets.get(dataset_name=dataset_name)
            return dataset
    dataset = project.datasets.create(dataset_name=dataset_name)
    return dataset

def add_metadata(dataset,items):
    # get the list of the items
    for img in items:
        # get the id of the image 
        id=img.id
        # get item by id
        item = dataset.items.get(item_id=id)
        item.metadata['user'] = dict()
        item.metadata['user']['UTM'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        # update and reclaim item
        item = item.update()

def addClassification(dataset, label, items):
    for img in items:
        id=img.id
        item = dataset.items.get(item_id=id)
        # Create a builder instance
        builder = item.annotations.builder()
        builder.add(annotation_definition=dl.Classification(label=label))
        # Upload classification to the item
        item.annotations.upload(builder)

def addRandPointKey(dataset, items):
    # get random item
    item_rand_num = random.randint(0, len(items)-1)
    item = dataset.items.get(item_id=items[item_rand_num].id)
    for i in range(5):
        # random point 
        x = random.randint(0, item.metadata['system']['width'])
        y = random.randint(0, item.metadata['system']['height'])
        # Create a builder instance
        builder = item.annotations.builder()
        # Create point annotation with label and attribute
        builder.add(annotation_definition=dl.Point(x= x, y= y, label= 'key'))
        # Upload point to the item
        item.annotations.upload(builder)  

def filterByLable(dataset, lable):
    # Create filters instance
    filters = dl.Filters()
    filters.add_join(field='label', values=lable, operator=dl.FILTERS_OPERATIONS_EQUAL)
    pages = dataset.items.list(filters=filters)
    # Count the items
    print('Number of filtered items in dataset: {}'.format(pages.items_count))
    # Go over all item and print the properties
    for page in pages:
            for item in page:
                    item.print()

def retrievesPoints(dataset):
    filters = dl.Filters()  # Create filters instance
    filters.add_join(field='type', values='point')  # Filter only annotated items with point
    pages = dataset.items.list(filters=filters)  # Get filtered items list in a page object
    print('Number of items in dataset: {}'.format(pages.items_count))
    points = []
    for page in pages:
        for item in page:
            points = item.annotations.list()
            item.print()
    points = pd.DataFrame(points)
    return points

def main():
    login(config.email,config.password)
    dataset = createDataset('Dataloop Task','new_dataset') # parameters is : project name , data set name
    # Add multiple labels
    labels = [
        dl.Label(tag='class1', color=(1, 1, 1)),
        dl.Label(tag='class2', color=(34, 56, 7)),
        dl.Label(tag='key', color=(100, 14, 150))
    ]
    # Add the labels to the Recipe
    dataset.add_labels(label_list=labels)    
    # upload directory with 5 images
    dataset.items.upload(local_path=r'5_images/*') 
    # list of items
    items = dataset.items.list()[0]
    # Add a UTM metadata to an item user metadata
    add_metadata(dataset,items) 
    # classification of class1 to the first two of the images
    addClassification(dataset, 'calss1', items[0:2])
    # classification of class1 to the rest of the images
    addClassification(dataset, 'calss2', items[2:])
    # Add 5 random key points with the label “key” to one item
    addRandPointKey(dataset, items)
    # query that selects only image items that have been labeled as “class1”
    filterByLable(dataset,'class1')
    # query that retrieves all point annotations from the dataset
    retrievesPoints(dataset)
    dl.logout()

    
if __name__ == "__main__":
    main()