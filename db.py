from main import SQLiteModel

class MyModel(SQLiteModel):
    table_name = 'my_models'

if __name__ == "__main__":
    MyModel.create_table()
    
    MyModel.create(name='Test Model')

    all_models = MyModel.all()
    print(all_models)

    filtered_models = MyModel.filter(name='Test Model')
    print(filtered_models)

    MyModel.update(1, name='Updated Model')

    MyModel.delete(1)