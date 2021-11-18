# Solution Engineering Home Assignment

## Part 1 (UI and preparation):
We follow this instructions:
1. Create a demo account on the Dataloop platform - https://console.dataloop.ai/
2. Create a project
    <img width="700" alt="screenshot" src="Part 1 images\create project.jpg">
3. Create a dataset
    <img width="700" alt="screenshot" src="Part 1 images\dataset.jpg">
4. Upload up to 10 images of your choice into the dataset (you can use Google Images or
any free data source you may find)
    <img width="700" alt="screenshot" src="Part 1 images\dataset2.jpg">
5. Create a basic Recipe for this dataset. Make sure to use Labels and Attributes that have
relevance to the data presented.
6. Annotate the images with tools of your choice. Try and use at least 2 types of annotation
tools.
    <img width="700" alt="screenshot" src="Part 1 images\lable.jpg">

## Part 2 (SDK):
* We use [Dataloop documentation](https://dataloop.ai/docs/) for technical tips and guidance.
* Python version 3.5.4 til 3.8 needs to be installed on your system using this [official website](https://www.python.org/downloads/).
### Running Locally
```
pip install - r requirements.txt
python -u script.py
```
#### Login
I created a bot user with a unique name,with developer permissions to be used for every M2M login.
```
import dtlpy as dl
dl.login() # use browser login to create the bot
project = dl.projects.get(project_name='myProject') # get your project
myBot = project.bots.create(name='my-unique-name', return_credentials=True)
print("the bot email is "+myBot.email)
print("the bot password is "+myBot.password)
```
Then I saved the email and the password in the config file and we can log in to the SDK with your new bot
```
import dtlpy as dl
# Login to Dataloop platform
dl.login_m2m(email=config.email, password=config.password)
```
I follow this instructions to make the project:
1. Install [dataloop SDK](https://dataloop.ai/docs/sdk-register)
2. Create a script that does the following:
    * Create new dataset
    ```
        dataset = project.datasets.create(dataset_name='new_dataset') 
    ```
    * Add 2 labels to the dataset recipe (class1 and class2 and key)
    ```
        dataset.add_labels(label_list=labels)
    ```
    * upload directory with 5 images
    ```
        dataset.items.upload(local_path=r'5_images/*') 
    ```
    * Add a UTM metadata to an item user metadata - collection time
    {collected:<the current time in UTM timestamp>}
    ```
        item.metadata['user'] = dict()
        item.metadata['user']['UTM'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    ```
    * Add a classification of class1 to the first two of the images you uploaded
    * Add a classification of class2 to the rest of the images you uploaded
    ```
        builder = item.annotations.builder()
        builder.add(annotation_definition=dl.Classification(label=label))
        # Upload classification to the item
        item.annotations.upload(builder)
    ```
    * Add 5 random key points with the label “key” to one item
    ```
        # random point 
        x = random.randint(0, item.metadata['system']['width'])
        y = random.randint(0, item.metadata['system']['height'])
        # Create a builder instance
        builder = item.annotations.builder()
        # Create point annotation with label and attribute
        builder.add(annotation_definition=dl.Point(x= x, y= y, label= 'key'))
        # Upload point to the item
        item.annotations.upload(builder)  
    ```
3. Create a query that selects only image items that have been labeled as “class1”
    ```
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
    ```
4. Create a query that retrieves all point annotations from the datase
    ```
    filters = dl.Filters()
    # Create filters instance
    filters.add_join(field='type', values='point')
    # Filter only annotated items with point
    pages = dataset.items.list(filters=filters)
    # Get filtered items list in a page object
    print('Number of items in dataset: {}'.format(pages.items_count))
    points = []
    for page in pages:
        for item in page:
            points = item.annotations.list()
            item.print()
    points = pd.DataFrame(points)
    return points
    ```


