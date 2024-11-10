       
class BaseException(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        

class AskNameEqualityArgsException(BaseException):
    def __init__(self, message):
        message = '''Wrong parameters\nExpected structuse of params:
            "args":{
                "contractName":"<text>" // not null
            }
        '''
        super().__init__(message)
        
class AskContractGuaranteeArgsException(BaseException):
    def __init__(self, message):
        self.message = '''Wrong parameters\nExpected structuse of params:
            "args":{
                "isContractGuaranteeRequired":true // required
            }4
            
        ''' + message

        super().__init__(self.message)
        
class AskCertificationArgsException(BaseException):
    def __init__(self, message):
        self.message = '''Wrong parameters\nExpected structuse of params:
            "args":{
                "licenseFiles":[
                "text" // nullable
                ...
                ]
            }
            
        ''' + message
        super().__init__(self.message)
    
class AskSupplySheduleAndStageArgsException(BaseException):
    def __init__(self, message):
        self.message = '''Wrong parameters\nExpected structuse of params:
            "args":{
                "periodDaysFrom":"<text>", // required
                "periodDaysTo":"<text>",    // required
                "deliveryStage":"smth text"// required
            }
            
        ''' + message
        super().__init__(self.message)
    
class AskContractPrizeArgsException(BaseException):
    def __init__(self, message):
        self.message = '''Wrong parameters\nExpected structuse of params:
            "args":{
                "startCost":"<text>",
                "maxContractCost":"<text>"
            }
            
        ''' + message
        super().__init__(self.message)
    
class AskaskTechnicalSpecificationsArgsException(BaseException):
    def __init__(self, message):
        self.message = '''Wrong parameters\nExpected structuse of params:
            "args":{
                "items":[
                    {
                        "name":"<text>",
                        "properties":[
                            {
                                "name":"<text>",
                                "value":"<text>", // згачение + ед. измерения
                            }
                        ],
                        "quantity":"<text>",
                        "costPerUnit":"<text>" // цена за единицу товара
                    }
                ]
            }
        }
        '''+message
        super().__init__(self.message)
    
