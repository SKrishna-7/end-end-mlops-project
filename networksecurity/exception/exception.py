import sys
from networksecurity.logging import logger

class NetworkSecurityException(Exception):
    def __init__(self,err_msg,err_details:sys):
        
        self.err_msg=err_msg
        _,_,exc_tb=err_details.exc_info()

        self.lineno=exc_tb.tb_lineno
        self.file_name=exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return "Error occured in [{0}] line number [{1}] error message [{2}]".format(self.file_name,self.lineno,str(self.err_msg))
    

if __name__ =='__main__':
    try:
        logger.logging.info("Entered the try block..")
        a=1/0
        print(a)
    except Exception as e:
        logger.logging.info(NetworkSecurityException(e,sys))

        raise NetworkSecurityException(e,sys)