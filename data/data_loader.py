from foil.foil_model import FoilImageClassifier
import json
import os
import shutil


class ClassificationDataManager:
    """Provide utility methods for data preprocessing in classification mode."""

    def get_data_from_db(self, url="mongodb://localhost:27017"):
        """
        Retrive data from MongoDB and parse data into X, X_unlabeled and y.

        @param url: url to db
        @return: X, X_unlabeled, y
        """
        from pymongo import MongoClient
        client = MongoClient(url)
        db = client['NSIL']
        images_collection = db['images']
        workspaces_collection = db['workspaces']

        # Get all images
        images: list[object] = images_collection.find({})
        # Get all imageMetaDatas
        ws = workspaces_collection.find_one({})
        image_meta_datas = ws['collections'][0]['images']

        # Get X, y
        X = []
        X_unlabeled = []
        y = []
        for img_md in image_meta_datas:
            img_id = img_md['imageId']
            target_img = next(x for x in images if str(x['_id']) == str(img_id))
            # process labeled images
            if img_md['labels'] and len(img_md['labels']) == 1 and img_md['labels'][0]['name'] and len(
                    img_md['labels'][0]['name']) == 1 and img_md['labels'][0]['confirmed']:
                x_single, y_single = FoilImageClassifier.parse_data(img_md, target_img['interpretation'])
                X.append(x_single)
                y.append(y_single)
            else:
                # process unlabeled images
                x_single, _ = FoilImageClassifier.parse_data(img_md, target_img['interpretation'], isManual=False)
                X_unlabeled.append(x_single)

        client.close()
        return X, X_unlabeled, y

    def save_data_to_file(self, X=[], X_unlabeled=[], y=[], filename='data', from_db=False, original_filename=None):
        """
        Save X, X_unlabeled and y to local file.

        @param X: data X
        @param X_unlabeled: data X_unlabeled
        @param y: data y
        @param filename: filename to save
        @param from_db: if True, data is retrived from db and no need to provide X, X_unlabeled and y
        @param original_filename: filename to load data
        """
        import os
        if (os.path.isfile(filename)):
            print("File already exists. Stop saving.")
            return
        import pickle
        if from_db:
            X, X_unlabeled, y = self.get_data_from_db()
        # save X, X_unlabeled, y as a list
        else:
            if original_filename:
                X, X_unlabeled, y = self.transform_data(original_filename)
        with open(filename, 'wb') as f:
            pickle.dump([X, X_unlabeled, y], f)

    def transform_data(self, filename):
        """
        Transform data from original format to X, X_unlabeled and y.

        @param filename: filename to load
        @return: X, X_unlabeled, y
        """
        X = []
        X_unlabeled = []
        y = []
        with open(filename, 'r') as f:
            json_data = json.load(f)
            for img in json_data:
                x_dict = {}
                x_dict['imageId'] = img['imageId']
                x_dict['object_detect'] = img['object_detect']
                if 'panoptic_segmentation' in img.keys():
                    x_dict['panoptic_segmentation'] = img['panoptic_segmentation']
                if img['type']:
                    X.append(x_dict)
                    y.append(img['type'])
                else:
                    X_unlabeled.append(x_dict)

        return X, X_unlabeled, y

    def get_data_from_file(self, filename='data'):
        """
        Load X, X_unlabeled and y from local file.

        @param filename: filename to load
        @return: X, X_unlabeled, y
        """
        import pickle
        with open(filename, 'rb') as f:
            return pickle.load(f)

    def split_data(self, data_file, config_file, save=False, task="bird"):
        """
        Split data into train, test and val according to config file and save to local file.

        @param data_file: filename to load data
        @param config_file: filename to load config for data
        @param save: if True, save data to local file
        @param task: the name of the task to creat folder
        """
        X, _, y = self.transform_data(data_file)
        with open(config_file, 'r') as f:
            config_data = json.load(f)
        X_train_id = [img['imageId'] for img in config_data if img['train']]
        X_test_id = [img['imageId'] for img in config_data if img['test']]
        X_val_id = [img['imageId'] for img in config_data if img['val']]

        X_train = [img for img in X if img['imageId'] in X_train_id]
        y_train = [y[i] for i in range(len(y)) if X[i]['imageId'] in X_train_id]
        X_test = [img for img in X if img['imageId'] in X_test_id]
        y_test = [y[i] for i in range(len(y)) if X[i]['imageId'] in X_test_id]
        X_val = [img for img in X if img['imageId'] in X_val_id]
        y_val = [y[i] for i in range(len(y)) if X[i]['imageId'] in X_val_id]
        if save:
            self.save_data_to_file(X_train, [], y_train, filename=f'./data_file/{task}/train')
            self.save_data_to_file(X_test, [], y_test, filename=f'./data_file/{task}/test')
            self.save_data_to_file(X_val, [], y_val, filename=f'./data_file/{task}/val')
        return X_train, X_test, X_val, y_train, y_test, y_val

    def split_images(self, data_file, config_file, image_dir, target_path):
        """
        According to the data config file, split the images folders into train, test, validation image folders.
        The original image folder should has the structure of each labels and the file name is the imageId.

        @param data_file: filename to load data
        @param config_file: filename to load config for data
        @param image_dir: the directory of the original images
        @param target_path: the directory to save the splited images
        """
        with open(data_file, 'r') as f:
            data = json.load(f)
        with open(config_file, 'r') as f:
            config_data = json.load(f)
        types = set([img['type'] for img in data])
        # Create path for train test val folder
        os.mkdir(target_path) if not os.path.exists(target_path) else None
        os.mkdir(f'{target_path}/train') if not os.path.exists(f'{target_path}/train') else None
        os.mkdir(f'{target_path}/test') if not os.path.exists(f'{target_path}/test') else None
        os.mkdir(f'{target_path}/val') if not os.path.exists(f'{target_path}/val') else None
        for label in types:
            os.mkdir(f'{target_path}/train/{label}') if not os.path.exists(f'{target_path}/train/{label}') else None
            os.mkdir(f'{target_path}/test/{label}') if not os.path.exists(f'{target_path}/test/{label}') else None
            os.mkdir(f'{target_path}/val/{label}') if not os.path.exists(f'{target_path}/val/{label}') else None
        # get train test val image id
        X_train_id = [img['imageId'] for img in config_data if img['train']]
        X_test_id = [img['imageId'] for img in config_data if img['test']]
        X_val_id = [img['imageId'] for img in config_data if img['val']]
        # copy images into train test val folders
        for img in data:
            if img['imageId'] in X_train_id:
                shutil.copy(f'{image_dir}/{img["type"]}/{img["imageId"]}.jpg',
                            f'{target_path}/train/{img["type"]}/{img["imageId"]}.jpg')
            elif img['imageId'] in X_test_id:
                shutil.copy(f'{image_dir}/{img["type"]}/{img["imageId"]}.jpg',
                            f'{target_path}/test/{img["type"]}/{img["imageId"]}.jpg')
            elif img['imageId'] in X_val_id:
                shutil.copy(f'{image_dir}/{img["type"]}/{img["imageId"]}.jpg',
                            f'{target_path}/val/{img["type"]}/{img["imageId"]}.jpg')
