
def yes_or_no(question:str, answer:bool)->str:
    """
    This silly seemingly useless function, makes debugging suprisingly easy.
    
    usage:
    log.debug(f'''
            This can be a detailed debug, that explain what code is doing,
            and why these question might asked. So for example, a server is 
            needed to be accessable by the program. So you could write a test
            fot that and use it as your yes or no indicator. The reason I 
            made this is sometimes True is the valid and sometimes False, but asking
            question it's clear which state is valid and which is not
            {yes_or_no('Is the server up',server_return_200(ip_address))}
               ''')

    Args:
        question (str): This the question you want answer when debuging.
        example: "Is the server up"
        answer (bool): This a boolean function that answers the question
        example: server_return_200(ip_address)        
    Returns:
        str: A string that ask and answers the question
        example: Is the server up: yes if server returns 200 status else no
    """    
    return f"{question}:  {(' yes' if answer else ' no')}"
    