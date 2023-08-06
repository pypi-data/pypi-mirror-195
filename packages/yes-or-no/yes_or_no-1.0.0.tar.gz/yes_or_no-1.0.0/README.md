# yes_or_no
    
This silly seemingly useless function, makes debugging suprisingly easy.


## Install

Requres Python 3.8 or above, and can be installed with pip or poetry. 
To install with pip, simply run:

```shell
pip install yes-or-no
```
To install with poetry, run:

```shell
poetry add yes-or-no
```

## Useage

When debugging code, it is often helpful to know whether a particular condition is
True or False. 
However sometimes the True state is fail state, this allows to ask the question
in the form:
Are you sure this condition is False: yes if false no if True
This function allows you to frame a test as a question with a yes or no answer, 
which can make it easier to understand the results.

For example, if you are testing whether a server is accessible, you can use this function to ask the question "Is the server up?" and get a clear answer based on the server's status code.

How I like to use it, is in multi line f strings, which I will pass to a log.debug.
The fact that it's a mutli line f sting allows for documentation around what is
happening in code.

```python
#sever_return_200(ip_address) -> bool: True if status is 200 else False
log.debug(f'''
            This can be a detailed debug, that explain what code is doing,
            and why these question might asked. So for example, a server is 
            needed to be accessable by the program. So you could write a test
            fot that and use it as your yes or no indicator. The reason I 
            made this is sometimes True is the valid and sometimes False, but asking
            question it's clear which state is valid and which is not
            {yes_or_no('Is the server up',server_return_200(ip_address))}
               ''')
```

## Args

```
question (str): This the question you want answer when debuging.
example: "Is the server up"
answer (bool): This a boolean function that answers the question
example: server_return_200(ip_address)        
```

## Returns

```
str: A string that ask and answers the question
example: Is the server up: yes if server returns 200 status else no        
```        
        