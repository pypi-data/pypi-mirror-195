from ._internal import Launch

class dynamic:
    @staticmethod
    def step(name: str):
        caller = Launch.get_caller_name()
        item_id = Launch.create_report_item(
                    name=name,
                    parent_item=caller,
                    type='test',
                    description='')
        
        Launch.items[caller] = item_id
    
    @staticmethod
    def title(test_title: str):
        caller = Launch.get_caller_name()
        item_id = Launch.create_report_item(
                    name=test_title,
                    parent_item=caller,
                    type='test',
                    description='')
        
        Launch.items[caller] = item_id

