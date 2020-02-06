from queue import LifoQueue as Stack


def check_balance(word):
    stack_validator = Stack()
    for i in word:
        if i == '(' or i == '[' or i == '{':
            stack_validator.put(i)
        else:
            if i == ')':
                if stack_validator.get() != '(':
                    return False
            elif i == ']':
                if stack_validator.get() != '[':
                    return False
            elif i == '}':
                if stack_validator.get() != '{':
                    return False
    if stack_validator.empty():
        return True
    else:
        return False


if __name__ == "__main__":
    word = '[(){}]'
    if check_balance(word):
        print("{} is valid".format(word))
    else:
        print("{} is not valid".format(word))
    
    word = '{([)]}'
    if check_balance(word):
        print("{} is valid".format(word))
    else:
        print("{} is not valid".format(word))

